#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
BOLD fMRI -processing workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: init_func_preproc_wf
.. autofunction:: init_bold_reference_wf
.. autofunction:: init_bold_stc_wf
.. autofunction:: init_bold_hmc_wf
.. autofunction:: init_bold_reg_wf

Registration workflows
++++++++++++++++++++++

.. autofunction:: fmriprep.workflows.util.init_bbreg_wf
.. autofunction:: fmriprep.workflows.util.init_fsl_bbr_wf

Resampling workflows
++++++++++++++++++++

.. autofunction:: init_bold_surf_wf
.. autofunction:: init_bold_mni_trans_wf

"""

# Originally coded by Craig Moodie. Refactored by the CRN Developers.

import os
import os.path as op

import pkg_resources as pkgr

from niworkflows.nipype import logging
from niworkflows.nipype.utils.filemanip import split_filename
from niworkflows.nipype.pipeline import engine as pe
from niworkflows.nipype.interfaces import afni, fsl, utility as niu, freesurfer as fs

import niworkflows.data as nid
from niworkflows.interfaces.registration import EstimateReferenceImage
from niworkflows.interfaces.fixes import (FixHeaderApplyTransforms as ApplyTransforms,
                                          FixHeaderRegistration as Registration)
from niworkflows.interfaces.utils import GenerateSamplingReference
from niworkflows.interfaces import SimpleBeforeAfter, NormalizeMotionParams


from ..interfaces import (
    DerivativesDataSink, InvertT1w, ValidateImage,
    GiftiNameSource, GiftiSetAnatomicalStructure,
    MCFLIRT2ITK, MultiApplyTransforms
)

# See https://github.com/poldracklab/fmriprep/issues/768
from ..interfaces.freesurfer import PatchedConcatenateLTA as ConcatenateLTA

from ..interfaces.images import extract_wm
from ..interfaces.nilearn import Merge
from ..interfaces.reports import FunctionalSummary
from ..workflows import confounds
from ..workflows.fieldmap.unwarp import init_pepolar_unwarp_wf
from ..workflows.util import (
    init_enhance_and_skullstrip_bold_wf, init_skullstrip_bold_wf,
    init_bbreg_wf, init_fsl_bbr_wf)


DEFAULT_MEMORY_MIN_GB = 0.01
LOGGER = logging.getLogger('workflow')


def init_func_preproc_wf(bold_file, ignore, freesurfer,
                         use_bbr, bold2t1w_dof, reportlets_dir,
                         output_spaces, template, output_dir, omp_nthreads,
                         fmap_bspline, fmap_demean, use_syn, force_syn,
                         use_aroma, ignore_aroma_err, medial_surface_nan,
                         debug, low_mem, output_grid_ref, layout=None):
    """
    This workflow controls the functional preprocessing stages of FMRIPREP.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_func_preproc_wf
        wf = init_func_preproc_wf('/completely/made/up/path/sub-01_task-nback_bold.nii.gz',
                                  omp_nthreads=1,
                                  ignore=[],
                                  freesurfer=True,
                                  reportlets_dir='.',
                                  output_dir='.',
                                  template='MNI152NLin2009cAsym',
                                  output_spaces=['T1w', 'fsnative',
                                                 'template', 'fsaverage5'],
                                  debug=False,
                                  use_bbr=True,
                                  bold2t1w_dof=9,
                                  fmap_bspline=True,
                                  fmap_demean=True,
                                  use_syn=True,
                                  force_syn=True,
                                  low_mem=False,
                                  output_grid_ref=None,
                                  medial_surface_nan=False,
                                  use_aroma=False,
                                  ignore_aroma_err=False)

    **Parameters**

        bold_file : str
            BOLD series NIfTI file
        ignore : list
            Preprocessing steps to skip (may include "slicetiming", "fieldmaps")
        freesurfer : bool
            Enable FreeSurfer functional registration (bbregister) and resampling
            BOLD series to FreeSurfer surface meshes.
        use_bbr : bool or None
            Enable/disable boundary-based registration refinement.
            If ``None``, test BBR result for distortion before accepting.
        bold2t1w_dof : 6, 9 or 12
            Degrees-of-freedom for BOLD-T1w registration
        reportlets_dir : str
            Directory in which to save reportlets
        output_spaces : list
            List of output spaces functional images are to be resampled to.
            Some parts of pipeline will only be instantiated for some output spaces.

            Valid spaces:

                - T1w
                - template
                - fsnative
                - fsaverage (or other pre-existing FreeSurfer templates)
        template : str
            Name of template targeted by `'template'` output space
        output_dir : str
            Directory in which to save derivatives
        omp_nthreads : int
            Maximum number of threads an individual process may use
        fmap_bspline : bool
            **Experimental**: Fit B-Spline field using least-squares
        fmap_demean : bool
            Demean voxel-shift map during unwarp
        use_syn : bool
            **Experimental**: Enable ANTs SyN-based susceptibility distortion correction (SDC).
            If fieldmaps are present and enabled, this is not run, by default.
        force_syn : bool
            **Temporary**: Always run SyN-based SDC
        use_aroma : bool
            Perform ICA-AROMA on MNI-resampled functional series
        ignore_aroma_err : bool
            Do not fail on ICA-AROMA errors
        medial_surface_nan : bool
            Replace medial wall values with NaNs on functional GIFTI files
        debug : bool
            Enable debugging outputs
        low_mem : bool
            Write uncompressed .nii files in some cases to reduce memory usage
        output_grid_ref : str or None
            Path of custom reference image for normalization
        layout : BIDSLayout
            BIDSLayout structure to enable metadata retrieval

    **Inputs**

        bold_file
            BOLD series NIfTI file
        t1_preproc
            Bias-corrected structural template image
        t1_brain
            Skull-stripped ``t1_preproc``
        t1_mask
            Mask of the skull-stripped template image
        t1_seg
            Segmentation of preprocessed structural image, including
            gray-matter (GM), white-matter (WM) and cerebrospinal fluid (CSF)
        t1_tpms
            List of tissue probability maps in T1w space
        t1_2_mni_forward_transform
            ANTs-compatible affine-and-warp transform file
        t1_2_mni_reverse_transform
            ANTs-compatible affine-and-warp transform file (inverse)
        subjects_dir
            FreeSurfer SUBJECTS_DIR
        subject_id
            FreeSurfer subject ID
        t1_2_fsnative_forward_transform
            LTA-style affine matrix translating from T1w to FreeSurfer-conformed subject space
        t1_2_fsnative_reverse_transform
            LTA-style affine matrix translating from FreeSurfer-conformed subject space to T1w


    **Outputs**

        bold_t1
            BOLD series, resampled to T1w space
        bold_mask_t1
            BOLD series mask in T1w space
        bold_mni
            BOLD series, resampled to template space
        bold_mask_mni
            BOLD series mask in template space
        confounds
            TSV of confounds
        surfaces
            BOLD series, resampled to FreeSurfer surfaces
        aroma_noise_ics
            Noise components identified by ICA-AROMA
        melodic_mix
            FSL MELODIC mixing matrix


    **Subworkflows**

        * :py:func:`~fmriprep.workflows.bold.init_bold_reference_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_stc_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_hmc_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_reg_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_confounds_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.unwarp.init_pepolar_unwarp_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.init_fmap_estimator_wf`
        * :py:func:`~fmriprep.workflows.fieldmap.init_sdc_unwarp_wf`
        * :py:func:`~fmriprep.workflows.bold.init_nonlinear_sdc_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_mni_trans_wf`
        * :py:func:`~fmriprep.workflows.bold.init_bold_surf_wf`

    """

    if bold_file == '/completely/made/up/path/sub-01_task-nback_bold.nii.gz':
        bold_file_size_gb = 1
    else:
        bold_file_size_gb = os.path.getsize(bold_file) / (1024**3)

    LOGGER.info('Creating bold processing workflow for "%s".', bold_file)
    fname = split_filename(bold_file)[1]
    fname_nosub = '_'.join(fname.split("_")[1:])
    name = "func_preproc_" + fname_nosub.replace(
        ".", "_").replace(" ", "").replace("-", "_").replace("_bold", "_wf")

    # For doc building purposes
    if layout is None or bold_file == 'bold_preprocesing':

        LOGGER.info('No valid layout: building empty workflow.')
        metadata = {"RepetitionTime": 2.0,
                    "SliceTiming": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}
        fmaps = [{
            'type': 'phasediff',
            'phasediff': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_phasediff.nii.gz',
            'magnitude1': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_magnitude1.nii.gz',
            'magnitude2': 'sub-03/ses-2/fmap/sub-03_ses-2_run-1_magnitude2.nii.gz'
        }]
        run_stc = True
        bold_pe = 'j'
    else:
        metadata = layout.get_metadata(bold_file)
        # Find fieldmaps. Options: (phase1|phase2|phasediff|epi|fieldmap)
        fmaps = layout.get_fieldmap(bold_file, return_list=True) \
            if 'fieldmaps' not in ignore else []

        # Short circuits: (True and True and (False or 'TooShort')) == 'TooShort'
        run_stc = ("SliceTiming" in metadata and
                   'slicetiming' not in ignore and
                   (_get_series_len(bold_file) > 4 or "TooShort"))
        bold_pe = metadata.get("PhaseEncodingDirection")

    # TODO: To be removed (supported fieldmaps):
    if not set([fmap['type'] for fmap in fmaps]).intersection(['phasediff', 'fieldmap', 'epi']):
        fmaps = None

    # Run SyN if forced or in the absence of fieldmap correction
    use_syn = force_syn or (use_syn and not fmaps)

    # Build workflow
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(niu.IdentityInterface(
        fields=['bold_file', 't1_preproc', 't1_brain', 't1_mask', 't1_seg', 't1_tpms',
                't1_2_mni_forward_transform', 't1_2_mni_reverse_transform',
                'subjects_dir', 'subject_id', 't1_2_fsnative_forward_transform',
                't1_2_fsnative_reverse_transform']),
        name='inputnode')
    inputnode.inputs.bold_file = bold_file

    outputnode = pe.Node(niu.IdentityInterface(
        fields=['bold_t1', 'bold_mask_t1', 'bold_mni', 'bold_mask_mni', 'confounds', 'surfaces',
                'aroma_noise_ics', 'melodic_mix', 'nonaggr_denoised_file']),
        name='outputnode')

    summary = pe.Node(
        FunctionalSummary(output_spaces=output_spaces,
                          slice_timing=run_stc,
                          registration='FreeSurfer' if freesurfer else 'FSL',
                          registration_dof=bold2t1w_dof,
                          pe_direction=bold_pe),
        name='summary', mem_gb=DEFAULT_MEMORY_MIN_GB, run_without_submitting=True)

    func_reports_wf = init_func_reports_wf(reportlets_dir=reportlets_dir,
                                           freesurfer=freesurfer,
                                           use_aroma=use_aroma,
                                           use_syn=use_syn)

    func_derivatives_wf = init_func_derivatives_wf(output_dir=output_dir,
                                                   output_spaces=output_spaces,
                                                   template=template,
                                                   freesurfer=freesurfer,
                                                   use_aroma=use_aroma)

    workflow.connect([
        (inputnode, func_reports_wf, [('bold_file', 'inputnode.source_file')]),
        (inputnode, func_derivatives_wf, [('bold_file', 'inputnode.source_file')]),
        (outputnode, func_derivatives_wf, [
            ('bold_t1', 'inputnode.bold_t1'),
            ('bold_mask_t1', 'inputnode.bold_mask_t1'),
            ('bold_mni', 'inputnode.bold_mni'),
            ('bold_mask_mni', 'inputnode.bold_mask_mni'),
            ('confounds', 'inputnode.confounds'),
            ('surfaces', 'inputnode.surfaces'),
            ('aroma_noise_ics', 'inputnode.aroma_noise_ics'),
            ('melodic_mix', 'inputnode.melodic_mix'),
            ('nonaggr_denoised_file', 'inputnode.nonaggr_denoised_file'),
        ]),
    ])

    bold_reference_wf = init_bold_reference_wf(omp_nthreads=omp_nthreads)

    # STC on the BOLD
    # bool('TooShort') == True, so check True explicitly
    if run_stc is True:
        bold_stc_wf = init_bold_stc_wf(name='bold_stc_wf', metadata=metadata)

    # HMC on the BOLD
    bold_hmc_wf = init_bold_hmc_wf(name='bold_hmc_wf',
                                   bold_file_size_gb=bold_file_size_gb,
                                   omp_nthreads=omp_nthreads)

    # mean BOLD registration to T1w
    bold_reg_wf = init_bold_reg_wf(name='bold_reg_wf',
                                   freesurfer=freesurfer,
                                   use_bbr=use_bbr,
                                   bold2t1w_dof=bold2t1w_dof,
                                   bold_file_size_gb=bold_file_size_gb,
                                   omp_nthreads=omp_nthreads,
                                   use_compression=not low_mem,
                                   use_fieldwarp=(fmaps is not None or use_syn))

    # get confounds
    bold_confounds_wf = confounds.init_bold_confs_wf(
        bold_file_size_gb=bold_file_size_gb,
        use_aroma=use_aroma,
        ignore_aroma_err=ignore_aroma_err,
        metadata=metadata,
        name='bold_confounds_wf')
    bold_confounds_wf.get_node('inputnode').inputs.t1_transform_flags = [False]

    workflow.connect([
        (inputnode, bold_reference_wf, [('bold_file', 'inputnode.bold_file')]),
        (bold_reference_wf, bold_hmc_wf, [
            ('outputnode.raw_ref_image', 'inputnode.raw_ref_image')]),
        (inputnode, bold_reg_wf, [
            ('bold_file', 'inputnode.name_source'),
            ('t1_preproc', 'inputnode.t1_preproc'),
            ('t1_brain', 'inputnode.t1_brain'),
            ('t1_mask', 'inputnode.t1_mask'),
            ('t1_seg', 'inputnode.t1_seg'),
            # Undefined if --no-freesurfer, but this is safe
            ('subjects_dir', 'inputnode.subjects_dir'),
            ('subject_id', 'inputnode.subject_id'),
            ('t1_2_fsnative_reverse_transform', 'inputnode.t1_2_fsnative_reverse_transform')
        ]),
        (inputnode, bold_confounds_wf, [('t1_tpms', 'inputnode.t1_tpms'),
                                        ('t1_mask', 'inputnode.t1_mask')]),
        (bold_hmc_wf, bold_reg_wf, [('outputnode.bold_split', 'inputnode.bold_split'),
                                    ('outputnode.xforms', 'inputnode.hmc_xforms')]),
        (bold_hmc_wf, bold_confounds_wf, [('outputnode.movpar_file', 'inputnode.movpar_file')]),
        (bold_reg_wf, bold_confounds_wf, [
            ('outputnode.bold_t1', 'inputnode.bold_t1'),
            ('outputnode.bold_mask_t1', 'inputnode.bold_mask_t1')]),
        (bold_reference_wf, func_reports_wf, [
            ('outputnode.validation_report', 'inputnode.validation_report')]),
        (bold_reg_wf, func_reports_wf, [
            ('outputnode.out_report', 'inputnode.bold_reg_report'),
            ('outputnode.fallback', 'inputnode.bold_reg_fallback'),
        ]),
        (bold_confounds_wf, outputnode, [
            ('outputnode.confounds_file', 'confounds'),
            ('outputnode.aroma_noise_ics', 'aroma_noise_ics'),
            ('outputnode.melodic_mix', 'melodic_mix'),
            ('outputnode.nonaggr_denoised_file', 'nonaggr_denoised_file'),
        ]),
        (bold_reg_wf, outputnode, [('outputnode.bold_t1', 'bold_t1'),
                                   ('outputnode.bold_mask_t1', 'bold_mask_t1')]),
        (bold_confounds_wf, func_reports_wf, [
            ('outputnode.acompcor_report', 'inputnode.acompcor_report'),
            ('outputnode.tcompcor_report', 'inputnode.tcompcor_report'),
            ('outputnode.ica_aroma_report', 'inputnode.ica_aroma_report')]),
        (bold_confounds_wf, summary, [('outputnode.confounds_list', 'confounds')]),
        (bold_reg_wf, summary, [('outputnode.fallback', 'fallback')]),
        (summary, func_reports_wf, [('out_report', 'inputnode.summary_report')]),
    ])

    # bool('TooShort') == True, so check True explicitly
    if run_stc is True:
        workflow.connect([
            (bold_reference_wf, bold_stc_wf, [('outputnode.bold_file', 'inputnode.bold_file'),
                                              ('outputnode.skip_vols', 'inputnode.skip_vols')]),
            (bold_stc_wf, bold_hmc_wf, [('outputnode.stc_file', 'inputnode.bold_file')])])
    else:
        workflow.connect([
            (bold_reference_wf, bold_hmc_wf, [('outputnode.bold_file', 'inputnode.bold_file')])])

    # Cases:
    # fmaps | use_syn | force_syn  |  ACTION
    # ----------------------------------------------
    #   T   |    *    |     T      | Fieldmaps + SyN
    #   T   |    *    |     F      | Fieldmaps
    #   F   |    *    |     T      | SyN
    #   F   |    T    |     F      | SyN
    #   F   |    F    |     F      | HMC only

    # Predefine to pacify the lintian checks about
    # "could be used before defined" - logic was tested to be sound
    nonlinear_sdc_wf = sdc_unwarp_wf = None

    if fmaps:
        # In case there are multiple fieldmaps prefer EPI
        fmaps.sort(key=lambda fmap: {'epi': 0, 'fieldmap': 1, 'phasediff': 2}[fmap['type']])
        fmap = fmaps[0]

        LOGGER.info('Fieldmap estimation: type "%s" found', fmap['type'])
        summary.inputs.distortion_correction = fmap['type']

        if fmap['type'] == 'epi':
            epi_fmaps = [fmap_['epi'] for fmap_ in fmaps if fmap_['type'] == 'epi']
            sdc_unwarp_wf = init_pepolar_unwarp_wf(fmaps=epi_fmaps,
                                                   layout=layout,
                                                   bold_file=bold_file,
                                                   omp_nthreads=omp_nthreads,
                                                   name='pepolar_unwarp_wf')
        else:
            # Import specific workflows here, so we don't brake everything with one
            # unused workflow.
            from .fieldmap import init_fmap_estimator_wf, init_sdc_unwarp_wf
            fmap_estimator_wf = init_fmap_estimator_wf(fmap_bids=fmap,
                                                       reportlets_dir=reportlets_dir,
                                                       omp_nthreads=omp_nthreads,
                                                       fmap_bspline=fmap_bspline)
            sdc_unwarp_wf = init_sdc_unwarp_wf(reportlets_dir=reportlets_dir,
                                               omp_nthreads=omp_nthreads,
                                               fmap_bspline=fmap_bspline,
                                               fmap_demean=fmap_demean,
                                               debug=debug,
                                               name='sdc_unwarp_wf')
            workflow.connect([
                (fmap_estimator_wf, sdc_unwarp_wf, [
                    ('outputnode.fmap', 'inputnode.fmap'),
                    ('outputnode.fmap_ref', 'inputnode.fmap_ref'),
                    ('outputnode.fmap_mask', 'inputnode.fmap_mask')]),
            ])

        # Connections and workflows common for all types of fieldmaps
        workflow.connect([
            (inputnode, sdc_unwarp_wf, [('bold_file', 'inputnode.name_source')]),
            (bold_reference_wf, sdc_unwarp_wf, [
                ('outputnode.ref_image', 'inputnode.in_reference'),
                ('outputnode.ref_image_brain', 'inputnode.in_reference_brain'),
                ('outputnode.bold_mask', 'inputnode.in_mask')]),
            (sdc_unwarp_wf, bold_reg_wf, [
                ('outputnode.out_warp', 'inputnode.fieldwarp'),
                ('outputnode.out_reference_brain', 'inputnode.ref_bold_brain'),
                ('outputnode.out_mask', 'inputnode.ref_bold_mask')]),
            (sdc_unwarp_wf, func_reports_wf, [
                ('outputnode.out_mask_report', 'inputnode.bold_mask_report')])
        ])

        # Report on BOLD correction
        fmap_unwarp_report_wf = init_fmap_unwarp_report_wf(reportlets_dir=reportlets_dir,
                                                           name='fmap_unwarp_report_wf')
        workflow.connect([
            (inputnode, fmap_unwarp_report_wf, [
                ('t1_seg', 'inputnode.in_seg'),
                ('bold_file', 'inputnode.name_source')]),
            (bold_reference_wf, fmap_unwarp_report_wf, [
                ('outputnode.ref_image', 'inputnode.in_pre')]),
            (sdc_unwarp_wf, fmap_unwarp_report_wf, [
                ('outputnode.out_reference', 'inputnode.in_post')]),
            (bold_reg_wf, fmap_unwarp_report_wf, [
                ('outputnode.itk_t1_to_bold', 'inputnode.in_xfm')]),
        ])
    elif not use_syn:
        LOGGER.warn('No fieldmaps found or they were ignored, building base workflow '
                    'for dataset %s.', bold_file)
        summary.inputs.distortion_correction = 'None'
        workflow.connect([
            (bold_reference_wf, func_reports_wf, [
                ('outputnode.bold_mask_report', 'inputnode.bold_mask_report')]),
            (bold_reference_wf, bold_reg_wf, [
                ('outputnode.ref_image_brain', 'inputnode.ref_bold_brain'),
                ('outputnode.bold_mask', 'inputnode.ref_bold_mask')]),
        ])

    if use_syn:
        nonlinear_sdc_wf = init_nonlinear_sdc_wf(
            bold_file=bold_file, bold_pe=bold_pe, freesurfer=freesurfer, bold2t1w_dof=bold2t1w_dof,
            template=template, omp_nthreads=omp_nthreads)

        workflow.connect([
            (inputnode, nonlinear_sdc_wf, [
                ('t1_brain', 'inputnode.t1_brain'),
                ('t1_seg', 'inputnode.t1_seg'),
                ('t1_2_mni_reverse_transform', 'inputnode.t1_2_mni_reverse_transform')]),
            (bold_reference_wf, nonlinear_sdc_wf, [
                ('outputnode.ref_image_brain', 'inputnode.bold_ref')]),
            (nonlinear_sdc_wf, func_reports_wf, [
                ('outputnode.out_warp_report', 'inputnode.syn_sdc_report')]),
        ])

        # XXX Eliminate branch when forcing isn't an option
        if not fmaps:
            LOGGER.warn('No fieldmaps found or they were ignored. Using EXPERIMENTAL '
                        'nonlinear susceptibility correction for dataset %s.', bold_file)
            summary.inputs.distortion_correction = 'SyN'
            workflow.connect([
                (nonlinear_sdc_wf, func_reports_wf, [
                    ('outputnode.out_mask_report', 'inputnode.bold_mask_report')]),
                (nonlinear_sdc_wf, bold_reg_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp'),
                    ('outputnode.out_reference_brain', 'inputnode.ref_bold_brain'),
                    ('outputnode.out_mask', 'inputnode.ref_bold_mask')]),
            ])

    if 'template' in output_spaces:
        # Apply transforms in 1 shot
        # Only use uncompressed output if AROMA is to be run
        bold_mni_trans_wf = init_bold_mni_trans_wf(
            template=template,
            bold_file_size_gb=bold_file_size_gb,
            omp_nthreads=omp_nthreads,
            output_grid_ref=output_grid_ref,
            use_compression=not (low_mem and use_aroma),
            use_fieldwarp=(fmaps is not None or use_syn),
            name='bold_mni_trans_wf'
        )

        workflow.connect([
            (inputnode, bold_mni_trans_wf, [
                ('bold_file', 'inputnode.name_source'),
                ('t1_2_mni_forward_transform', 'inputnode.t1_2_mni_forward_transform')]),
            (bold_hmc_wf, bold_mni_trans_wf, [
                ('outputnode.bold_split', 'inputnode.bold_split'),
                ('outputnode.xforms', 'inputnode.hmc_xforms')]),
            (bold_reg_wf, bold_mni_trans_wf, [
                ('outputnode.itk_bold_to_t1', 'inputnode.itk_bold_to_t1')]),
            (bold_mni_trans_wf, outputnode, [('outputnode.bold_mni', 'bold_mni'),
                                             ('outputnode.bold_mask_mni', 'bold_mask_mni')]),
            (bold_mni_trans_wf, bold_confounds_wf, [
                ('outputnode.bold_mask_mni', 'inputnode.bold_mask_mni'),
                ('outputnode.bold_mni', 'inputnode.bold_mni')])
        ])

        if fmaps:
            workflow.connect([
                (sdc_unwarp_wf, bold_mni_trans_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp'),
                    ('outputnode.out_mask', 'inputnode.bold_mask')]),
            ])
        elif use_syn:
            workflow.connect([
                (nonlinear_sdc_wf, bold_mni_trans_wf, [
                    ('outputnode.out_warp', 'inputnode.fieldwarp'),
                    ('outputnode.out_mask', 'inputnode.bold_mask')]),
            ])
        else:
            workflow.connect([
                (bold_reference_wf, bold_mni_trans_wf, [
                    ('outputnode.bold_mask', 'inputnode.bold_mask')]),
            ])

    if freesurfer and any(space.startswith('fs') for space in output_spaces):
        LOGGER.info('Creating BOLD surface-sampling workflow.')
        bold_surf_wf = init_bold_surf_wf(output_spaces=output_spaces,
                                         medial_surface_nan=medial_surface_nan,
                                         name='bold_surf_wf')
        workflow.connect([
            (inputnode, bold_surf_wf, [
                ('t1_preproc', 'inputnode.t1_preproc'),
                ('subjects_dir', 'inputnode.subjects_dir'),
                ('subject_id', 'inputnode.subject_id'),
                ('t1_2_fsnative_forward_transform', 'inputnode.t1_2_fsnative_forward_transform')]),
            (bold_reg_wf, bold_surf_wf, [('outputnode.bold_t1', 'inputnode.source_file')]),
            (bold_surf_wf, outputnode, [('outputnode.surfaces', 'surfaces')]),
        ])

    return workflow


def init_bold_reference_wf(omp_nthreads, bold_file=None, name='bold_reference_wf'):
    """
    This workflow generates reference BOLD images for a series

    The raw reference image is the target of :abbr:`HMC (head motion correction)`, and a
    contrast-enhanced reference is the subject of distortion correction, as well as
    boundary-based registration to T1w and template spaces.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_reference_wf
        wf = init_bold_reference_wf(omp_nthreads=1)

    **Parameters**

        bold_file : str
            BOLD series NIfTI file
        omp_nthreads : int
            Maximum number of threads an individual process may use
        name : str
            Name of workflow (default: ``bold_reference_wf``)

    **Inputs**

        bold_file
            BOLD series NIfTI file

    **Outputs**

        bold_file
            Validated BOLD series NIfTI file
        raw_ref_image
            Reference image to which BOLD series is motion corrected
        skip_vols
            Number of non-steady-state volumes detected at beginning of ``bold_file``
        ref_image
            Contrast-enhanced reference image
        ref_image_brain
            Skull-stripped reference image
        bold_mask
            Skull-stripping mask of reference image
        bold_mask_report
            Reportlet showing quality of masking
        validation_report
            HTML reportlet indicating whether ``bold_file`` had a valid affine


    **Subworkflows**

        * :py:func:`~fmriprep.workflows.util.init_enhance_and_skullstrip_wf`

    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(niu.IdentityInterface(fields=['bold_file']), name='inputnode')
    outputnode = pe.Node(
        niu.IdentityInterface(fields=['bold_file', 'raw_ref_image', 'skip_vols', 'ref_image',
                                      'ref_image_brain', 'bold_mask', 'bold_mask_report',
                                      'validation_report']),
        name='outputnode')

    # Simplify manually setting input image
    if bold_file is not None:
        inputnode.inputs.bold_file = bold_file

    validate = pe.Node(ValidateImage(), name='validate', mem_gb=DEFAULT_MEMORY_MIN_GB,
                       run_without_submitting=True)

    gen_ref = pe.Node(EstimateReferenceImage(), name="gen_ref",
                      mem_gb=1)  # OE: 128x128x128x50 * 64 / 8 ~ 900MB.
    enhance_and_skullstrip_bold_wf = init_enhance_and_skullstrip_bold_wf(omp_nthreads=omp_nthreads)

    workflow.connect([
        (inputnode, validate, [('bold_file', 'in_file')]),
        (validate, gen_ref, [('out_file', 'in_file')]),
        (gen_ref, enhance_and_skullstrip_bold_wf, [('ref_image', 'inputnode.in_file')]),
        (validate, outputnode, [('out_file', 'bold_file'),
                                ('out_report', 'validation_report')]),
        (gen_ref, outputnode, [('ref_image', 'raw_ref_image'),
                               ('n_volumes_to_discard', 'skip_vols')]),
        (enhance_and_skullstrip_bold_wf, outputnode, [
            ('outputnode.bias_corrected_file', 'ref_image'),
            ('outputnode.mask_file', 'bold_mask'),
            ('outputnode.out_report', 'bold_mask_report'),
            ('outputnode.skull_stripped_file', 'ref_image_brain')]),
    ])

    return workflow


# pylint: disable=R0914
def init_bold_stc_wf(metadata, name='bold_stc_wf'):
    """
    This workflow performs :abbr:`STC (slice-timing correction)` over the input
    :abbr:`BOLD (blood-oxygen-level dependent)` image.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_stc_wf
        wf = init_bold_stc_wf(
            metadata={"RepetitionTime": 2.0,
                      "SliceTiming": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]},
            )

    **Parameters**

        metadata : dict
            BIDS metadata for BOLD file
        name : str
            Name of workflow (default: ``bold_stc_wf``)

    **Inputs**

        bold_file
            BOLD series NIfTI file
        skip_vols
            Number of non-steady-state volumes detected at beginning of ``bold_file``

    **Outputs**

        stc_file
            Slice-timing corrected BOLD series NIfTI file

    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(niu.IdentityInterface(fields=['bold_file', 'skip_vols']), name='inputnode')
    outputnode = pe.Node(niu.IdentityInterface(fields=['stc_file']), name='outputnode')

    LOGGER.info('Slice-timing correction will be included.')

    def create_custom_slice_timing_file_func(metadata):
        import os
        slice_timings = metadata["SliceTiming"]
        slice_timings_ms = [str(t) for t in slice_timings]
        out_file = "timings.1D"
        with open("timings.1D", "w") as fp:
            fp.write("\t".join(slice_timings_ms))

        return os.path.abspath(out_file)

    create_custom_slice_timing_file = pe.Node(
        niu.Function(function=create_custom_slice_timing_file_func),
        name="create_custom_slice_timing_file",
        mem_gb=DEFAULT_MEMORY_MIN_GB)
    create_custom_slice_timing_file.inputs.metadata = metadata

    # It would be good to fingerprint memory use of afni.TShift
    slice_timing_correction = pe.Node(
        afni.TShift(outputtype='NIFTI_GZ', tr='{}s'.format(metadata["RepetitionTime"])),
        name='slice_timing_correction')

    def _prefix_at(x):
        return "@" + x

    workflow.connect([
        (inputnode, slice_timing_correction, [('bold_file', 'in_file'),
                                              ('skip_vols', 'ignore')]),
        (create_custom_slice_timing_file, slice_timing_correction, [
            (('out', _prefix_at), 'tpattern')]),
        (slice_timing_correction, outputnode, [('out_file', 'stc_file')]),
    ])

    return workflow


# pylint: disable=R0914
def init_bold_hmc_wf(bold_file_size_gb, omp_nthreads, name='bold_hmc_wf'):
    """
    This workflow performs :abbr:`HMC (head motion correction)` over the input
    :abbr:`BOLD (blood-oxygen-level dependent)` image.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_hmc_wf
        wf = init_bold_hmc_wf(bold_file_size_gb=3, omp_nthreads=1)

    **Parameters**

        bold_file_size_gb : float
            Size of BOLD file in GB
        omp_nthreads : int
            Maximum number of threads an individual process may use
        name : str
            Name of workflow (default: ``bold_hmc_wf``)

    **Inputs**

        bold_file
            BOLD series NIfTI file
        raw_ref_image
            Reference image to which BOLD series is motion corrected

    **Outputs**

        bold_split
            Individual 3D volumes, not motion corrected
        xforms
            ITKTransform file aligning each volume to ``ref_image``
        movpar_file
            MCFLIRT motion parameters, normalized to SPM format (X, Y, Z, Rx, Ry, Rz)

    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(niu.IdentityInterface(fields=['bold_file', 'raw_ref_image']),
                        name='inputnode')
    outputnode = pe.Node(
        niu.IdentityInterface(fields=['bold_split', 'xforms', 'movpar_file']),
        name='outputnode')

    # Head motion correction (hmc)
    mcflirt = pe.Node(fsl.MCFLIRT(save_mats=True, save_plots=True),
                      name='mcflirt', mem_gb=bold_file_size_gb * 3)

    fsl2itk = pe.Node(MCFLIRT2ITK(), name='fsl2itk',
                      mem_gb=0.05, n_procs=omp_nthreads)

    normalize_motion = pe.Node(NormalizeMotionParams(format='FSL'),
                               name="normalize_motion",
                               mem_gb=DEFAULT_MEMORY_MIN_GB)

    split = pe.Node(fsl.Split(dimension='t'), name='split',
                    mem_gb=bold_file_size_gb * 3)

    workflow.connect([
        (inputnode, split, [('bold_file', 'in_file')]),
        (inputnode, mcflirt, [('raw_ref_image', 'ref_file'),
                              ('bold_file', 'in_file')]),
        (inputnode, fsl2itk, [('raw_ref_image', 'in_source'),
                              ('raw_ref_image', 'in_reference')]),
        (mcflirt, fsl2itk, [('mat_file', 'in_files')]),
        (mcflirt, normalize_motion, [('par_file', 'in_file')]),
        (fsl2itk, outputnode, [('out_file', 'xforms')]),
        (normalize_motion, outputnode, [('out_file', 'movpar_file')]),
        (split, outputnode, [('out_files', 'bold_split')]),
    ])

    return workflow


def init_bold_reg_wf(freesurfer, use_bbr, bold2t1w_dof, bold_file_size_gb, omp_nthreads,
                     name='bold_reg_wf', use_compression=True,
                     use_fieldwarp=False):
    """
    This workflow registers the reference BOLD image to T1-space, using a
    boundary-based registration (BBR) cost function.

    If FreeSurfer-based preprocessing is enabled, the ``bbregister`` utility
    is used to align the BOLD images to the reconstructed subject, and the
    resulting transform is adjusted to target the T1 space.
    If FreeSurfer-based preprocessing is disabled, FSL FLIRT is used with the
    BBR cost function to directly target the T1 space.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_reg_wf
        wf = init_bold_reg_wf(freesurfer=True,
                              bold_file_size_gb=3,
                              omp_nthreads=1,
                              use_bbr=True,
                              bold2t1w_dof=9)

    **Parameters**

        freesurfer : bool
            Enable FreeSurfer functional registration (bbregister)
        use_bbr : bool or None
            Enable/disable boundary-based registration refinement.
            If ``None``, test BBR result for distortion before accepting.
        bold2t1w_dof : 6, 9 or 12
            Degrees-of-freedom for BOLD-T1w registration
        bold_file_size_gb : float
            Size of BOLD file in GB
        omp_nthreads : int
            Maximum number of threads an individual process may use
        name : str
            Name of workflow (default: ``bold_reg_wf``)
        use_compression : bool
            Save registered BOLD series as ``.nii.gz``
        use_fieldwarp : bool
            Include SDC warp in single-shot transform from BOLD to T1

    **Inputs**

        name_source
            BOLD series NIfTI file
            Used to recover original information lost during processing
        ref_bold_brain
            Reference image to which BOLD series is aligned
            If ``fieldwarp == True``, ``ref_bold_brain`` should be unwarped
        ref_bold_mask
            Skull-stripping mask of reference image
        t1_preproc
            Bias-corrected structural template image
        t1_brain
            Skull-stripped ``t1_preproc``
        t1_mask
            Mask of the skull-stripped template image
        t1_seg
            Segmentation of preprocessed structural image, including
            gray-matter (GM), white-matter (WM) and cerebrospinal fluid (CSF)
        bold_split
            Individual 3D BOLD volumes, not motion corrected
        hmc_xforms
            List of affine transforms aligning each volume to ``ref_image`` in ITK format
        subjects_dir
            FreeSurfer SUBJECTS_DIR
        subject_id
            FreeSurfer subject ID
        t1_2_fsnative_reverse_transform
            LTA-style affine matrix translating from FreeSurfer-conformed subject space to T1w
        fieldwarp
            a :abbr:`DFM (displacements field map)` in ITK format

    **Outputs**

        itk_bold_to_t1
            Affine transform from ``ref_bold_brain`` to T1 space (ITK format)
        itk_t1_to_bold
            Affine transform from T1 space to BOLD space (ITK format)
        bold_t1
            Motion-corrected BOLD series in T1 space
        bold_mask_t1
            BOLD mask in T1 space
        out_report
            Reportlet visualizing quality of registration
        fallback
            Boolean indicating whether BBR was rejected (mri_coreg registration returned)


    **Subworkflows**

        * :py:func:`~fmriprep.workflows.util.init_bbreg_wf`
        * :py:func:`~fmriprep.workflows.util.init_fsl_bbr_wf`

    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=['name_source', 'ref_bold_brain', 'ref_bold_mask',
                    't1_preproc', 't1_brain', 't1_mask',
                    't1_seg', 'bold_split', 'hmc_xforms',
                    'subjects_dir', 'subject_id', 't1_2_fsnative_reverse_transform', 'fieldwarp']),
        name='inputnode'
    )
    outputnode = pe.Node(
        niu.IdentityInterface(fields=['itk_bold_to_t1', 'itk_t1_to_bold',
                                      'bold_t1', 'bold_mask_t1',
                                      'out_report', 'fallback']),
        name='outputnode'
    )

    if freesurfer:
        bbr_wf = init_bbreg_wf(use_bbr=use_bbr, bold2t1w_dof=bold2t1w_dof,
                               omp_nthreads=omp_nthreads)
    else:
        bbr_wf = init_fsl_bbr_wf(use_bbr=use_bbr, bold2t1w_dof=bold2t1w_dof)

    workflow.connect([
        (inputnode, bbr_wf, [
            ('ref_bold_brain', 'inputnode.in_file'),
            ('t1_2_fsnative_reverse_transform', 'inputnode.t1_2_fsnative_reverse_transform'),
            ('subjects_dir', 'inputnode.subjects_dir'),
            ('subject_id', 'inputnode.subject_id'),
            ('t1_seg', 'inputnode.t1_seg'),
            ('t1_brain', 'inputnode.t1_brain')]),
        (bbr_wf, outputnode, [('outputnode.itk_bold_to_t1', 'itk_bold_to_t1'),
                              ('outputnode.itk_t1_to_bold', 'itk_t1_to_bold'),
                              ('outputnode.out_report', 'out_report'),
                              ('outputnode.fallback', 'fallback')]),
    ])

    gen_ref = pe.Node(GenerateSamplingReference(), name='gen_ref',
                      mem_gb=0.3)  # 256x256x256 * 64 / 8 ~ 150MB

    mask_t1w_tfm = pe.Node(
        ApplyTransforms(interpolation='NearestNeighbor', float=True),
        name='mask_t1w_tfm', mem_gb=0.1
    )

    workflow.connect([
        (inputnode, gen_ref, [('ref_bold_brain', 'moving_image'),
                              ('t1_brain', 'fixed_image'),
                              ('t1_mask', 'fov_mask')]),
        (gen_ref, mask_t1w_tfm, [('out_file', 'reference_image')]),
        (bbr_wf, mask_t1w_tfm, [('outputnode.itk_bold_to_t1', 'transforms')]),
        (inputnode, mask_t1w_tfm, [('ref_bold_mask', 'input_image')]),
        (mask_t1w_tfm, outputnode, [('output_image', 'bold_mask_t1')])
    ])

    # Merge transforms placing the head motion correction last
    nforms = 3 if use_fieldwarp else 2
    merge_xforms = pe.Node(niu.Merge(nforms), name='merge_xforms',
                           run_without_submitting=True, mem_gb=DEFAULT_MEMORY_MIN_GB)
    workflow.connect([
        (inputnode, merge_xforms, [('hmc_xforms', 'in%d' % nforms)])
    ])

    if use_fieldwarp:
        workflow.connect([
            (inputnode, merge_xforms, [('fieldwarp', 'in2')])
        ])

    bold_to_t1w_transform = pe.Node(
        MultiApplyTransforms(interpolation="LanczosWindowedSinc", float=True, copy_dtype=True),
        name='bold_to_t1w_transform', mem_gb=bold_file_size_gb * 3, n_procs=omp_nthreads)

    merge = pe.Node(Merge(compress=use_compression), name='merge', mem_gb=bold_file_size_gb * 3)

    workflow.connect([
        (bbr_wf, merge_xforms, [('outputnode.itk_bold_to_t1', 'in1')]),
        (merge_xforms, bold_to_t1w_transform, [('out', 'transforms')]),
        (inputnode, merge, [('name_source', 'header_source')]),
        (merge, outputnode, [('out_file', 'bold_t1')]),
        (inputnode, bold_to_t1w_transform, [('bold_split', 'input_image')]),
        (gen_ref, bold_to_t1w_transform, [('out_file', 'reference_image')]),
        (bold_to_t1w_transform, merge, [('out_files', 'in_files')]),
    ])

    return workflow


def init_bold_surf_wf(output_spaces, medial_surface_nan, name='bold_surf_wf'):
    """
    This workflow samples functional images to FreeSurfer surfaces

    For each vertex, the cortical ribbon is sampled at six points (spaced 20% of thickness apart)
    and averaged.

    Outputs are in GIFTI format.

    .. workflow::
        :graph2use: colored
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_surf_wf
        wf = init_bold_surf_wf(output_spaces=['T1w', 'fsnative',
                                             'template', 'fsaverage5'],
                               medial_surface_nan=False)

    **Parameters**

        output_spaces : list
            List of output spaces functional images are to be resampled to
            Target spaces beginning with ``fs`` will be selected for resampling,
            such as ``fsaverage`` or related template spaces
            If the list contains ``fsnative``, images will be resampled to the
            individual subject's native surface
        medial_surface_nan : bool
            Replace medial wall values with NaNs on functional GIFTI files

    **Inputs**

        source_file
            Motion-corrected BOLD series in T1 space
        t1_preproc
            Bias-corrected structural template image
        subjects_dir
            FreeSurfer SUBJECTS_DIR
        subject_id
            FreeSurfer subject ID
        t1_2_fsnative_forward_transform
            LTA-style affine matrix translating from T1w to FreeSurfer-conformed subject space

    **Outputs**

        surfaces
            BOLD series, resampled to FreeSurfer surfaces

    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(
        niu.IdentityInterface(fields=['source_file', 't1_preproc', 'subject_id', 'subjects_dir',
                                      't1_2_fsnative_forward_transform']),
        name='inputnode')

    outputnode = pe.Node(niu.IdentityInterface(fields=['surfaces']), name='outputnode')

    spaces = [space for space in output_spaces if space.startswith('fs')]

    def select_target(subject_id, space):
        """ Given a source subject ID and a target space, get the target subject ID """
        return subject_id if space == 'fsnative' else space

    targets = pe.MapNode(niu.Function(function=select_target),
                         iterfield=['space'], name='targets',
                         mem_gb=DEFAULT_MEMORY_MIN_GB)
    targets.inputs.space = spaces

    # Rename the source file to the output space to simplify naming later
    rename_src = pe.MapNode(niu.Rename(format_string='%(subject)s', keep_ext=True),
                            iterfield='subject', name='rename_src', run_without_submitting=True,
                            mem_gb=DEFAULT_MEMORY_MIN_GB)
    rename_src.inputs.subject = spaces

    resampling_xfm = pe.Node(fs.utils.LTAConvert(in_lta='identity.nofile', out_lta=True),
                             name='resampling_xfm')
    set_xfm_source = pe.Node(ConcatenateLTA(out_type='RAS2RAS'), name='set_xfm_source')

    sampler = pe.MapNode(
        fs.SampleToSurface(sampling_method='average', sampling_range=(0, 1, 0.2),
                           sampling_units='frac', interp_method='trilinear', cortex_mask=True,
                           override_reg_subj=True, out_type='gii'),
        iterfield=['source_file', 'target_subject'],
        iterables=('hemi', ['lh', 'rh']),
        name='sampler', mem_gb=3)

    def medial_wall_to_nan(in_file, subjects_dir, target_subject):
        """ Convert values on medial wall to NaNs
        """
        import nibabel as nb
        import numpy as np
        import os

        fn = os.path.basename(in_file)
        if not target_subject.startswith('fs'):
            return in_file

        cortex = nb.freesurfer.read_label(os.path.join(
            subjects_dir, target_subject, 'label', '{}.cortex.label'.format(fn[:2])))
        func = nb.load(in_file)
        medial = np.delete(np.arange(len(func.darrays[0].data)), cortex)
        for darray in func.darrays:
            darray.data[medial] = np.nan

        out_file = os.path.join(os.getcwd(), fn)
        func.to_filename(out_file)
        return out_file

    medial_nans = pe.MapNode(niu.Function(function=medial_wall_to_nan),
                             iterfield=['in_file', 'target_subject'], name='medial_nans',
                             mem_gb=DEFAULT_MEMORY_MIN_GB)

    merger = pe.JoinNode(niu.Merge(1, ravel_inputs=True), name='merger',
                         joinsource='sampler', joinfield=['in1'], run_without_submitting=True,
                         mem_gb=DEFAULT_MEMORY_MIN_GB)

    update_metadata = pe.MapNode(GiftiSetAnatomicalStructure(), iterfield='in_file',
                                 name='update_metadata', mem_gb=DEFAULT_MEMORY_MIN_GB)

    workflow.connect([
        (inputnode, targets, [('subject_id', 'subject_id')]),
        (inputnode, rename_src, [('source_file', 'in_file')]),
        (inputnode, resampling_xfm, [('source_file', 'source_file'),
                                     ('t1_preproc', 'target_file')]),
        (inputnode, set_xfm_source, [('t1_2_fsnative_forward_transform', 'in_lta2')]),
        (resampling_xfm, set_xfm_source, [('out_lta', 'in_lta1')]),
        (inputnode, sampler, [('subjects_dir', 'subjects_dir'),
                              ('subject_id', 'subject_id')]),
        (set_xfm_source, sampler, [('out_file', 'reg_file')]),
        (targets, sampler, [('out', 'target_subject')]),
        (rename_src, sampler, [('out_file', 'source_file')]),
        (merger, update_metadata, [('out', 'in_file')]),
        (update_metadata, outputnode, [('out_file', 'surfaces')]),
    ])

    if medial_surface_nan:
        workflow.connect([
            (inputnode, medial_nans, [('subjects_dir', 'subjects_dir')]),
            (sampler, medial_nans, [('out_file', 'in_file')]),
            (targets, medial_nans, [('out', 'target_subject')]),
            (medial_nans, merger, [('out', 'in1')]),
        ])
    else:
        workflow.connect(sampler, 'out_file', merger, 'in1')

    return workflow


def init_bold_mni_trans_wf(template, bold_file_size_gb, omp_nthreads,
                           name='bold_mni_trans_wf',
                           output_grid_ref=None, use_compression=True,
                           use_fieldwarp=False):
    """
    This workflow samples functional images to the MNI template in a "single shot"
    from the original BOLD series.

    .. workflow::
        :graph2use: colored
        :simple_form: yes

        from fmriprep.workflows.bold import init_bold_mni_trans_wf
        wf = init_bold_mni_trans_wf(template='MNI152NLin2009cAsym',
                                    bold_file_size_gb=3,
                                    omp_nthreads=1,
                                    output_grid_ref=None)

    **Parameters**

        template : str
            Name of template targeted by `'template'` output space
        bold_file_size_gb : float
            Size of BOLD file in GB
        omp_nthreads : int
            Maximum number of threads an individual process may use
        name : str
            Name of workflow (default: ``bold_mni_trans_wf``)
        output_grid_ref : str or None
            Path of custom reference image for normalization
        use_compression : bool
            Save registered BOLD series as ``.nii.gz``
        use_fieldwarp : bool
            Include SDC warp in single-shot transform from BOLD to MNI

    **Inputs**

        itk_bold_to_t1
            Affine transform from ``ref_bold_brain`` to T1 space (ITK format)
        t1_2_mni_forward_transform
            ANTs-compatible affine-and-warp transform file
        bold_split
            Individual 3D volumes, not motion corrected
        bold_mask
            Skull-stripping mask of reference image
        name_source
            BOLD series NIfTI file
            Used to recover original information lost during processing
        hmc_xforms
            List of affine transforms aligning each volume to ``ref_image`` in ITK format
        fieldwarp
            a :abbr:`DFM (displacements field map)` in ITK format

    **Outputs**

        bold_mni
            BOLD series, resampled to template space
        bold_mask_mni
            BOLD series mask in template space

    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(
        niu.IdentityInterface(fields=[
            'itk_bold_to_t1',
            't1_2_mni_forward_transform',
            'name_source',
            'bold_split',
            'bold_mask',
            'hmc_xforms',
            'fieldwarp'
        ]),
        name='inputnode'
    )

    outputnode = pe.Node(
        niu.IdentityInterface(fields=['bold_mni', 'bold_mask_mni']),
        name='outputnode')

    def _aslist(in_value):
        if isinstance(in_value, list):
            return in_value
        return [in_value]

    gen_ref = pe.Node(GenerateSamplingReference(), name='gen_ref',
                      mem_gb=0.3)  # 256x256x256 * 64 / 8 ~ 150MB)
    template_str = nid.TEMPLATE_MAP[template]
    gen_ref.inputs.fixed_image = op.join(nid.get_dataset(template_str), '1mm_T1.nii.gz')

    mask_mni_tfm = pe.Node(
        ApplyTransforms(interpolation='NearestNeighbor', float=True),
        name='mask_mni_tfm',
        mem_gb=3
    )

    # Write corrected file in the designated output dir
    mask_merge_tfms = pe.Node(niu.Merge(2), name='mask_merge_tfms', run_without_submitting=True,
                              mem_gb=DEFAULT_MEMORY_MIN_GB)

    nxforms = 4 if use_fieldwarp else 3
    merge_xforms = pe.Node(niu.Merge(nxforms), name='merge_xforms',
                           run_without_submitting=True, mem_gb=DEFAULT_MEMORY_MIN_GB)
    workflow.connect([(inputnode, merge_xforms, [('hmc_xforms', 'in%d' % nxforms)])])

    if use_fieldwarp:
        workflow.connect([(inputnode, merge_xforms, [('fieldwarp', 'in3')])])

    workflow.connect([
        (inputnode, gen_ref, [('bold_mask', 'moving_image')]),
        (inputnode, mask_merge_tfms, [('t1_2_mni_forward_transform', 'in1'),
                                      (('itk_bold_to_t1', _aslist), 'in2')]),
        (mask_merge_tfms, mask_mni_tfm, [('out', 'transforms')]),
        (mask_mni_tfm, outputnode, [('output_image', 'bold_mask_mni')]),
        (inputnode, mask_mni_tfm, [('bold_mask', 'input_image')])
    ])

    bold_to_mni_transform = pe.Node(
        MultiApplyTransforms(interpolation="LanczosWindowedSinc", float=True, copy_dtype=True),
        name='bold_to_mni_transform', mem_gb=bold_file_size_gb * 3, n_procs=omp_nthreads)

    merge = pe.Node(Merge(compress=use_compression), name='merge',
                    mem_gb=bold_file_size_gb * 3)

    workflow.connect([
        (inputnode, merge_xforms, [('t1_2_mni_forward_transform', 'in1'),
                                   (('itk_bold_to_t1', _aslist), 'in2')]),
        (merge_xforms, bold_to_mni_transform, [('out', 'transforms')]),
        (inputnode, merge, [('name_source', 'header_source')]),
        (inputnode, bold_to_mni_transform, [('bold_split', 'input_image')]),
        (bold_to_mni_transform, merge, [('out_files', 'in_files')]),
        (merge, outputnode, [('out_file', 'bold_mni')]),
    ])

    if output_grid_ref is None:
        workflow.connect([
            (gen_ref, mask_mni_tfm, [('out_file', 'reference_image')]),
            (gen_ref, bold_to_mni_transform, [('out_file', 'reference_image')]),
        ])
    else:
        mask_mni_tfm.inputs.reference_image = output_grid_ref
        bold_to_mni_transform.inputs.reference_image = output_grid_ref
    return workflow


def init_nonlinear_sdc_wf(bold_file, freesurfer, bold2t1w_dof,
                          template, omp_nthreads, bold_pe='j',
                          atlas_threshold=3, name='nonlinear_sdc_wf'):
    """
    This workflow takes a skull-stripped T1w image and reference BOLD image and
    estimates a susceptibility distortion correction warp, using ANTs symmetric
    normalization (SyN) and the average fieldmap atlas described in
    [Treiber2016]_.

    SyN deformation is restricted to the phase-encoding (PE) direction.
    If no PE direction is specified, anterior-posterior PE is assumed.

    SyN deformation is also restricted to regions that are expected to have a
    >3mm (approximately 1 voxel) warp, based on the fieldmap atlas.

    This technique is a variation on those developed in [Huntenburg2014]_ and
    [Wang2017]_.

    .. workflow ::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.bold import init_nonlinear_sdc_wf
        wf = init_nonlinear_sdc_wf(
            bold_file='/dataset/sub-01/func/sub-01_task-rest_bold.nii.gz',
            bold_pe='j',
            freesurfer=True,
            bold2t1w_dof=9,
            template='MNI152NLin2009cAsym',
            omp_nthreads=8)

    **Inputs**

        t1_brain
            skull-stripped, bias-corrected structural image
        bold_ref
            skull-stripped reference image
        t1_seg
            FAST segmentation white and gray matter, in native T1w space
        t1_2_mni_reverse_transform
            inverse registration transform of T1w image to MNI template

    **Outputs**

        out_reference_brain
            the ``bold_ref`` image after unwarping
        out_warp
            the corresponding :abbr:`DFM (displacements field map)` compatible with
            ANTs
        out_mask
            mask of the unwarped input file
        out_mask_report
            reportlet for the skullstripping

    .. [Huntenburg2014] Huntenburg, J. M. (2014) Evaluating Nonlinear
                        Coregistration of BOLD EPI and T1w Images. Berlin: Master
                        Thesis, Freie Universität. `PDF
                        <http://pubman.mpdl.mpg.de/pubman/item/escidoc:2327525:5/component/escidoc:2327523/master_thesis_huntenburg_4686947.pdf>`_.
    .. [Treiber2016] Treiber, J. M. et al. (2016) Characterization and Correction
                     of Geometric Distortions in 814 Diffusion Weighted Images,
                     PLoS ONE 11(3): e0152472. doi:`10.1371/journal.pone.0152472
                     <https://doi.org/10.1371/journal.pone.0152472>`_.
    .. [Wang2017] Wang S, et al. (2017) Evaluation of Field Map and Nonlinear
                  Registration Methods for Correction of Susceptibility Artifacts
                  in Diffusion MRI. Front. Neuroinform. 11:17.
                  doi:`10.3389/fninf.2017.00017
                  <https://doi.org/10.3389/fninf.2017.00017>`_.
    """
    workflow = pe.Workflow(name=name)
    inputnode = pe.Node(
        niu.IdentityInterface(['t1_brain', 'bold_ref', 't1_2_mni_reverse_transform',
                               't1_seg']),
        name='inputnode')
    outputnode = pe.Node(
        niu.IdentityInterface(['out_reference_brain', 'out_mask', 'out_warp',
                               'out_warp_report', 'out_mask_report']),
        name='outputnode')

    if bold_pe is None or bold_pe[0] not in ['i', 'j']:
        LOGGER.warning('Incorrect phase-encoding direction, assuming PA (posterior-to-anterior')
        bold_pe = 'j'

    # Collect predefined data
    # Atlas image and registration affine
    atlas_img = pkgr.resource_filename('fmriprep', 'data/fmap_atlas.nii.gz')
    atlas_2_template_affine = pkgr.resource_filename(
        'fmriprep', 'data/fmap_atlas_2_{}_affine.mat'.format(template))
    # Registration specifications
    affine_transform = pkgr.resource_filename('fmriprep', 'data/affine.json')
    syn_transform = pkgr.resource_filename('fmriprep', 'data/susceptibility_syn.json')

    invert_t1w = pe.Node(InvertT1w(), name='invert_t1w',
                         mem_gb=0.3)

    ref_2_t1 = pe.Node(Registration(from_file=affine_transform),
                       name='ref_2_t1', n_procs=omp_nthreads)
    t1_2_ref = pe.Node(ApplyTransforms(invert_transform_flags=[True]),
                       name='t1_2_ref', n_procs=omp_nthreads)

    # 1) BOLD -> T1; 2) MNI -> T1; 3) ATLAS -> MNI
    transform_list = pe.Node(niu.Merge(3), name='transform_list',
                             mem_gb=DEFAULT_MEMORY_MIN_GB)
    transform_list.inputs.in3 = atlas_2_template_affine

    # Inverting (1), then applying in reverse order:
    #
    # ATLAS -> MNI -> T1 -> BOLD
    atlas_2_ref = pe.Node(
        ApplyTransforms(invert_transform_flags=[True, False, False]),
        name='atlas_2_ref', n_procs=omp_nthreads,
        mem_gb=0.3)
    atlas_2_ref.inputs.input_image = atlas_img

    threshold_atlas = pe.Node(
        fsl.maths.MathsCommand(args='-thr {:.8g} -bin'.format(atlas_threshold),
                               output_datatype='char'),
        name='threshold_atlas', mem_gb=0.3)

    fixed_image_masks = pe.Node(niu.Merge(2), name='fixed_image_masks',
                                mem_gb=DEFAULT_MEMORY_MIN_GB)
    fixed_image_masks.inputs.in1 = 'NULL'

    restrict = [[int(bold_pe[0] == 'i'), int(bold_pe[0] == 'j'), 0]] * 2
    syn = pe.Node(
        Registration(from_file=syn_transform, restrict_deformation=restrict),
        name='syn', n_procs=omp_nthreads)

    seg_2_ref = pe.Node(
        ApplyTransforms(interpolation='NearestNeighbor', float=True,
                        invert_transform_flags=[True]),
        name='seg_2_ref', n_procs=omp_nthreads, mem_gb=0.3)
    sel_wm = pe.Node(niu.Function(function=extract_wm), name='sel_wm',
                     mem_gb=DEFAULT_MEMORY_MIN_GB)
    syn_rpt = pe.Node(SimpleBeforeAfter(), name='syn_rpt',
                      mem_gb=0.1)

    skullstrip_bold_wf = init_skullstrip_bold_wf()

    workflow.connect([
        (inputnode, invert_t1w, [('t1_brain', 'in_file'),
                                 ('bold_ref', 'ref_file')]),
        (inputnode, ref_2_t1, [('bold_ref', 'moving_image')]),
        (invert_t1w, ref_2_t1, [('out_file', 'fixed_image')]),
        (inputnode, t1_2_ref, [('bold_ref', 'reference_image')]),
        (invert_t1w, t1_2_ref, [('out_file', 'input_image')]),
        (ref_2_t1, t1_2_ref, [('forward_transforms', 'transforms')]),
        (ref_2_t1, transform_list, [('forward_transforms', 'in1')]),
        (inputnode, transform_list, [('t1_2_mni_reverse_transform', 'in2')]),
        (inputnode, atlas_2_ref, [('bold_ref', 'reference_image')]),
        (transform_list, atlas_2_ref, [('out', 'transforms')]),
        (atlas_2_ref, threshold_atlas, [('output_image', 'in_file')]),
        (threshold_atlas, fixed_image_masks, [('out_file', 'in2')]),
        (inputnode, syn, [('bold_ref', 'moving_image')]),
        (t1_2_ref, syn, [('output_image', 'fixed_image')]),
        (fixed_image_masks, syn, [('out', 'fixed_image_masks')]),
        (inputnode, seg_2_ref, [('t1_seg', 'input_image')]),
        (ref_2_t1, seg_2_ref, [('forward_transforms', 'transforms')]),
        (syn, seg_2_ref, [('warped_image', 'reference_image')]),
        (seg_2_ref, sel_wm, [('output_image', 'in_seg')]),
        (inputnode, syn_rpt, [('bold_ref', 'before')]),
        (syn, syn_rpt, [('warped_image', 'after')]),
        (sel_wm, syn_rpt, [('out', 'wm_seg')]),
        (syn, skullstrip_bold_wf, [('warped_image', 'inputnode.in_file')]),
        (syn, outputnode, [('forward_transforms', 'out_warp')]),
        (skullstrip_bold_wf, outputnode, [
            ('outputnode.skull_stripped_file', 'out_reference_brain'),
            ('outputnode.mask_file', 'out_mask'),
            ('outputnode.out_report', 'out_mask_report')]),
        (syn_rpt, outputnode, [('out_report', 'out_warp_report')])])

    return workflow


def init_fmap_unwarp_report_wf(reportlets_dir, name='fmap_unwarp_report_wf'):
    """
    This workflow generates and saves a reportlet showing the effect of fieldmap
    unwarping a BOLD image.

    .. workflow::
        :graph2use: orig
        :simple_form: yes

        from fmriprep.workflows.anatomical import init_fmap_unwarp_report_wf
        wf = init_fmap_unwarp_report_wf(reportlets_dir='.')

    **Parameters**

        reportlets_dir : str
            Directory in which to save reportlets
        name : str, optional
            Workflow name (default: fmap_unwarp_report_wf)

    **Inputs**

        in_pre
            Reference image, before unwarping
        in_post
            Reference image, after unwarping
        in_seg
            Segmentation of preprocessed structural image, including
            gray-matter (GM), white-matter (WM) and cerebrospinal fluid (CSF)
        in_xfm
            Affine transform from T1 space to BOLD space (ITK format)

    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(niu.IdentityInterface(
        fields=['in_pre', 'in_post', 'in_seg', 'in_xfm',
                'name_source']), name='inputnode')

    map_seg = pe.Node(ApplyTransforms(
        dimension=3, float=True, interpolation='NearestNeighbor'),
        name='map_seg', mem_gb=0.3)

    sel_wm = pe.Node(niu.Function(function=extract_wm), name='sel_wm',
                     mem_gb=DEFAULT_MEMORY_MIN_GB)

    bold_rpt = pe.Node(SimpleBeforeAfter(), name='bold_rpt',
                       mem_gb=0.1)
    bold_rpt_ds = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='variant-hmcsdc_preproc'), name='bold_rpt_ds',
        mem_gb=DEFAULT_MEMORY_MIN_GB,
        run_without_submitting=True
    )
    workflow.connect([
        (inputnode, bold_rpt, [('in_post', 'after'),
                               ('in_pre', 'before')]),
        (inputnode, bold_rpt_ds, [('name_source', 'source_file')]),
        (bold_rpt, bold_rpt_ds, [('out_report', 'in_file')]),
        (inputnode, map_seg, [('in_post', 'reference_image'),
                              ('in_seg', 'input_image'),
                              ('in_xfm', 'transforms')]),
        (map_seg, sel_wm, [('output_image', 'in_seg')]),
        (sel_wm, bold_rpt, [('out', 'wm_seg')]),
    ])

    return workflow


def init_func_reports_wf(reportlets_dir, freesurfer, use_aroma, use_syn, name='func_reports_wf'):
    """
    Set up a battery of datasinks to store reports in the right location
    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=['source_file', 'summary_report', 'validation_report', 'bold_mask_report',
                    'bold_reg_report', 'bold_reg_fallback', 'acompcor_report', 'tcompcor_report',
                    'syn_sdc_report', 'ica_aroma_report']),
        name='inputnode')

    ds_summary_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='summary'),
        name='ds_summary_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_validation_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='validation'),
        name='ds_validation_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_bold_mask_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='bold_mask'),
        name='ds_bold_mask_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_syn_sdc_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='syn_sdc'),
        name='ds_syn_sdc_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    def _bold_reg_suffix(fallback, freesurfer):
        if fallback:
            return 'coreg' if freesurfer else 'flirt'
        else:
            return 'bbr' if freesurfer else 'flt_bbr'

    ds_bold_reg_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir),
        name='ds_bold_reg_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_acompcor_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='acompcor'),
        name='ds_acompcor_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_tcompcor_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='tcompcor'),
        name='ds_tcompcor_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_ica_aroma_report = pe.Node(
        DerivativesDataSink(base_directory=reportlets_dir,
                            suffix='ica_aroma'),
        name='ds_ica_aroma_report', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    workflow.connect([
        (inputnode, ds_summary_report, [('source_file', 'source_file'),
                                        ('summary_report', 'in_file')]),
        (inputnode, ds_validation_report, [('source_file', 'source_file'),
                                           ('validation_report', 'in_file')]),
        (inputnode, ds_bold_mask_report, [('source_file', 'source_file'),
                                          ('bold_mask_report', 'in_file')]),
        (inputnode, ds_bold_reg_report, [
            ('source_file', 'source_file'),
            ('bold_reg_report', 'in_file'),
            (('bold_reg_fallback', _bold_reg_suffix, freesurfer), 'suffix')]),
        (inputnode, ds_acompcor_report, [('source_file', 'source_file'),
                                         ('acompcor_report', 'in_file')]),
        (inputnode, ds_tcompcor_report, [('source_file', 'source_file'),
                                         ('tcompcor_report', 'in_file')]),
    ])

    if use_aroma:
        workflow.connect([
            (inputnode, ds_ica_aroma_report, [('source_file', 'source_file'),
                                              ('ica_aroma_report', 'in_file')]),
        ])

    if use_syn:
        workflow.connect([
            (inputnode, ds_syn_sdc_report, [('source_file', 'source_file'),
                                            ('syn_sdc_report', 'in_file')]),
        ])

    return workflow


def init_func_derivatives_wf(output_dir, output_spaces, template, freesurfer,
                             use_aroma, name='func_derivatives_wf'):
    """
    Set up a battery of datasinks to store derivatives in the right location
    """
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=['source_file', 'bold_t1', 'bold_mask_t1', 'bold_mni', 'bold_mask_mni',
                    'confounds', 'surfaces', 'aroma_noise_ics', 'melodic_mix',
                    'nonaggr_denoised_file']),
        name='inputnode')

    ds_bold_t1 = pe.Node(DerivativesDataSink(
        base_directory=output_dir, suffix='space-T1w_preproc'),
        name='ds_bold_t1', run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_bold_mask_t1 = pe.Node(DerivativesDataSink(base_directory=output_dir,
                                                  suffix='space-T1w_brainmask'),
                              name='ds_bold_mask_t1', run_without_submitting=True,
                              mem_gb=DEFAULT_MEMORY_MIN_GB)

    suffix_fmt = 'space-{}_{}'.format
    ds_bold_mni = pe.Node(DerivativesDataSink(base_directory=output_dir,
                                              suffix=suffix_fmt(template, 'preproc')),
                          name='ds_bold_mni', run_without_submitting=True,
                          mem_gb=DEFAULT_MEMORY_MIN_GB)

    variant_suffix_fmt = 'space-{}_variant-{}_{}'.format
    ds_aroma_mni = pe.Node(DerivativesDataSink(base_directory=output_dir,
                                               suffix=variant_suffix_fmt(template,
                                                                         'smoothAROMAnonaggr',
                                                                         'preproc')),
                           name='ds_aroma_mni', run_without_submitting=True,
                           mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_bold_mask_mni = pe.Node(DerivativesDataSink(base_directory=output_dir,
                                                   suffix=suffix_fmt(template, 'brainmask')),
                               name='ds_bold_mask_mni', run_without_submitting=True,
                               mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_confounds = pe.Node(DerivativesDataSink(base_directory=output_dir, suffix='confounds'),
                           name="ds_confounds", run_without_submitting=True,
                           mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_aroma_noise_ics = pe.Node(DerivativesDataSink(base_directory=output_dir,
                                                     suffix='AROMAnoiseICs'),
                                 name="ds_aroma_noise_ics", run_without_submitting=True,
                                 mem_gb=DEFAULT_MEMORY_MIN_GB)

    ds_melodic_mix = pe.Node(DerivativesDataSink(base_directory=output_dir, suffix='MELODICmix'),
                             name="ds_melodic_mix", run_without_submitting=True,
                             mem_gb=DEFAULT_MEMORY_MIN_GB)

    if use_aroma:
        workflow.connect([
            (inputnode, ds_aroma_noise_ics, [('source_file', 'source_file'),
                                             ('aroma_noise_ics', 'in_file')]),
            (inputnode, ds_melodic_mix, [('source_file', 'source_file'),
                                         ('melodic_mix', 'in_file')]),
            (inputnode, ds_aroma_mni, [('source_file', 'source_file'),
                                       ('nonaggr_denoised_file', 'in_file')]),
        ])

    name_surfs = pe.MapNode(GiftiNameSource(pattern=r'(?P<LR>[lr])h.(?P<space>\w+).gii',
                                            template='space-{space}.{LR}.func'),
                            iterfield='in_file',
                            name='name_surfs',
                            mem_gb=DEFAULT_MEMORY_MIN_GB,
                            run_without_submitting=True)
    ds_bold_surfs = pe.MapNode(DerivativesDataSink(base_directory=output_dir),
                               iterfield=['in_file', 'suffix'], name='ds_bold_surfs',
                               run_without_submitting=True,
                               mem_gb=DEFAULT_MEMORY_MIN_GB)

    workflow.connect([
        (inputnode, ds_confounds, [('source_file', 'source_file'),
                                   ('confounds', 'in_file')]),
    ])

    if 'T1w' in output_spaces:
        workflow.connect([
            (inputnode, ds_bold_t1, [('source_file', 'source_file'),
                                     ('bold_t1', 'in_file')]),
            (inputnode, ds_bold_mask_t1, [('source_file', 'source_file'),
                                          ('bold_mask_t1', 'in_file')]),
        ])
    if 'template' in output_spaces:
        workflow.connect([
            (inputnode, ds_bold_mni, [('source_file', 'source_file'),
                                      ('bold_mni', 'in_file')]),
            (inputnode, ds_bold_mask_mni, [('source_file', 'source_file'),
                                           ('bold_mask_mni', 'in_file')]),
        ])
    if freesurfer and any(space.startswith('fs') for space in output_spaces):
        workflow.connect([
            (inputnode, name_surfs, [('surfaces', 'in_file')]),
            (inputnode, ds_bold_surfs, [('source_file', 'source_file'),
                                        ('surfaces', 'in_file')]),
            (name_surfs, ds_bold_surfs, [('out_name', 'suffix')]),
        ])

    return workflow


def _get_series_len(bold_fname):
    import nibabel as nb
    from niworkflows.interfaces.registration import _get_vols_to_discard
    img = nb.load(bold_fname)
    if len(img.shape) < 4:
        return 1

    skip_vols = _get_vols_to_discard(img)

    return img.shape[3] - skip_vols
