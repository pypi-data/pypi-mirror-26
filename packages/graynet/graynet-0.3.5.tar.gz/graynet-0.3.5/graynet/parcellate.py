__all__ = ['read_atlas', 'freesurfer_roi_labels', 'null_roi_name', 'atlas_list']

import os
from os.path import join as pjoin, exists as pexists, dirname, isdir, realpath
import numpy as np
import nibabel as nib
from .run_workflow import roi_info

atlas_list = ['FSAVERAGE', 'GLASSER2016']

# roi labelled ?? in Glasser parcellation has label 16777215
# fsaverage: label unknown --> 1639705, corpuscallosum --> 3294840
ignore_roi_labels = {'GLASSER2016': [16777215, ], 'FSAVERAGE': [1639705, 3294840]}
ignore_roi_names = {'GLASSER2016': ['??', '???', 'lh_???', 'rh_???', 'lh_???', 'rh_???'],
                    'FSAVERAGE'  : ['unknown', 'corpuscallosum',
                                    'lh_unknown', 'lh_corpuscallosum',
                                    'rh_unknown', 'rh_corpuscallosum']}

null_roi_index = 0
null_roi_name = 'null_roi_ignore'


def check_atlas_name(atlas_name=None):
    "Validates the atlas name and returs its location"

    if atlas_name in [None, 'None']:
        atlas_name = 'FSAVERAGE'

    atlas_name = atlas_name.upper()

    if atlas_name in ['GLASSER2016']:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        atlas_path = os.path.realpath(pjoin(this_dir, 'atlases', 'glasser2016', 'fsaverage_annot_figshare3498446'))
    elif atlas_name in ['FSAVERAGE']:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        atlas_path = os.path.realpath(pjoin(this_dir, 'atlases', 'fsaverage'))
    else:
        raise NotImplementedError('Requested atlas is not implemented or unreadable.')

    return atlas_path, atlas_name


def get_atlas_annot(atlas_name=None):
    "High level wrapper to get all the info just by using a name."

    atlas_path, atlas_name = check_atlas_name(atlas_name)
    annot = read_atlas_annot(atlas_path)

    return annot, atlas_path


def freesurfer_roi_labels(atlas_name='GLASSER2016'):
    "Returns just the vertex-wise indices for grouping the vertices into ROIs. Order:  left followed by right."

    annot, _ = get_atlas_annot(atlas_name)
    roi_labels = __combine_annotations(annot, atlas_name)

    return roi_labels, annot


def __combine_annotations(annot, atlas_name):
    "Combines named labels from two hemisphers, ignoring non-cortex"

    ignore_list = list()
    max_len = 1 + max(max(map(len, annot['lh']['names'] + annot['rh']['names'])), len(null_roi_name))
    str_dtype = np.dtype('U{}'.format(max_len))

    named_labels = dict()
    for hemi in ['lh', 'rh']:
        named_labels[hemi] = np.empty(annot[hemi]['labels'].shape, str_dtype)
        uniq_labels = np.unique(annot[hemi]['labels'])
        for label in uniq_labels:
            if not (label == null_roi_index or label in ignore_roi_labels[atlas_name]):  # to be ignored
                idx_roi = np.nonzero(annot[hemi]['ctab'][:, 4] == label)[0][0]
                mask_label = annot[hemi]['labels'] == label
                named_labels[hemi][mask_label] = '{}_{}'.format(hemi, annot[hemi]['names'][idx_roi])

        # setting the non-accessed vertices (part of non-cortex) to specific label to ignore later
        null_mask = named_labels[hemi] == ''
        named_labels[hemi][null_mask] = null_roi_name

    wholebrain_named_labels = np.hstack((named_labels['lh'], named_labels['rh']))

    for ignore_label in ignore_roi_names[atlas_name]:
        wholebrain_named_labels[wholebrain_named_labels == ignore_label] = null_roi_name

    # # original implementation for glasser2016, with labels in different hemi coded differently
    # roi_labels = np.hstack((annot['lh']['labels'], annot['rh']['labels']))

    return wholebrain_named_labels


def check_atlas_annot_exist(atlas_dir, hemi_list=None):
    " Checks for the presence of atlas annotations "

    if hemi_list is None:
        hemi_list = ['lh', 'rh']

    for hemi in hemi_list:
        annot_path = pjoin(atlas_dir, 'label', '{}.aparc.annot'.format(hemi))
        if not pexists(annot_path) or os.path.getsize(annot_path) == 0:
            return False

    return True


def read_atlas_annot(atlas_dir, hemi_list=None):
    " Returns atlas annotations "

    if hemi_list is None:
        hemi_list = ['lh', 'rh']

    annot = dict()
    for hemi in hemi_list:
        annot[hemi] = dict()
        annot_path = pjoin(atlas_dir, 'label', '{}.aparc.annot'.format(hemi))
        annot[hemi]['labels'], annot[hemi]['ctab'], annot[hemi]['names'] = nib.freesurfer.io.read_annot(annot_path,
                                                                                                        orig_ids=True)

        # ensuring names are plainstring
        if isinstance(annot[hemi]['names'][0], np.bytes_):
            annot[hemi]['names'] = [bytestr.decode('UTF-8') for bytestr in annot[hemi]['names']]

    return annot


def read_atlas(atlas_spec, hemi_list=None):
    " Script to read the pre-computed parcellations for fsaverage and HCP-MMP-1.0 "

    if hemi_list is None:
        hemi_list = ['lh', 'rh']

    if isdir(atlas_spec):
        atlas_dir = realpath(atlas_spec)
    else:
        atlas_dir, atlas_name = check_atlas_name(atlas_spec)

    coords, faces, info = dict(), dict(), dict()

    for hemi in hemi_list:
        hemi_path = os.path.join(atlas_dir, 'surf', '{}.orig'.format(hemi))
        coords[hemi], faces[hemi], info[hemi] = nib.freesurfer.io.read_geometry(hemi_path, read_metadata=True)

    num_vertices_left_hemi = coords['lh'].shape[0]

    coords['whole'] = np.vstack((coords['lh'], coords['rh']))
    faces['whole'] = np.vstack((faces['lh'], faces['rh'] + num_vertices_left_hemi))

    # labels, ctab, names = nib.freesurfer.io.read_annot(pjoin(mmp_fs,'lh.HCP-MMP1.annot'))

    annot = read_atlas_annot(atlas_dir, hemi_list)

    return coords, faces, annot


def roi_labels_centroids(atlas_name):
    "Returns a list of ROI centroids, for use in visualizations (nodes on a network)"

    atlas_dir, atlas_name = check_atlas_name(atlas_name)
    coords, faces, annot = read_atlas(atlas_dir)
    roi_labels, ctx_annot = freesurfer_roi_labels(atlas_name)
    uniq_rois, roi_size, num_nodes = roi_info(roi_labels)

    centroids = dict()
    for roi in uniq_rois:
        this_roi_vertices = coords['whole'][roi_labels == roi, :]
        centroids[roi] = np.median(this_roi_vertices, axis=0)

    return uniq_rois, centroids, roi_labels


def subdivide_cortex(atlas_dir, hemi_list=None):
    "Subdivides the given cortical parcellation (each label into smaller patches)"

    raise NotImplementedError('This function has not been implemented yet.')

    # noinspection PyUnreachableCode
    if hemi_list is None:
        hemi_list = ['lh', 'rh']

    coords, faces, annot = read_atlas(atlas_dir)

    labels_to_remove = ['corpuscallosum', 'unknown']
    null_label = 0


    def ismember(A, B):
        B_unique_sorted, B_idx = np.unique(B, return_index=True)
        B_in_A_bool = np.in1d(B_unique_sorted, A, assume_unique=True)


    cortex_label = dict()
    for hemi in hemi_list:
        cortex_label_path = pjoin(atlas_dir, 'label', '{}.cortex.label'.format(hemi))
        cortex_label[hemi] = nib.freesurfer.io.read_label(cortex_label_path)

        # # cortex_label[hemi] is an index into annot[hemi]['labels']

        mask_for_cortex = np.in1d(annot[hemi]['labels'], cortex_label, assume_unique=True)
