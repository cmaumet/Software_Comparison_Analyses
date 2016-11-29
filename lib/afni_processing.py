import os
import time
import sys
from subprocess import check_call
import glob
import re
import string
import shutil
from lib.fsl_processing import create_fsl_onset_files


def copy_raw(raw_dir, preproc_dir):
    """
    Copy to raw data (anatomical and functional) from 'raw_dir' (organised
    according to BIDS) to 'preproc_dir' and run BET on the anatomical images.
    """
    # All subject directories
    sub_dirs = glob.glob(os.path.join(raw_dir, 'sub-*'))

    if not os.path.isdir(preproc_dir):
        os.mkdir(preproc_dir)

    # For each subject
    for sub_folder in sub_dirs:
        anat_regexp = '*_T1w.nii.gz'
        fun_regexp = '*_bold.nii.gz'

        # Find the anatomical MRI
        amri = glob.glob(
            os.path.join(sub_folder, 'anat', anat_regexp))[0]

        # Find the fMRI
        fmris = glob.glob(
            os.path.join(sub_folder, 'func', fun_regexp))

        # Copy the anatomical image
        anat_preproc_dir = os.path.join(preproc_dir, 'ANATOMICAL')
        if not os.path.isdir(anat_preproc_dir):
            os.mkdir(anat_preproc_dir)
        shutil.copy(amri, anat_preproc_dir)

        # For each run, copy the fMRI image
        func_preproc_dir = os.path.join(preproc_dir, 'FUNCTIONAL')
        if not os.path.isdir(func_preproc_dir):
            os.mkdir(func_preproc_dir)

        for fmri in fmris:
            shutil.copy(fmri, func_preproc_dir)


def create_afni_onset_files(study_dir, onset_dir, conditions):
    """
    Create AFNI onset files based on BIDS tsv files. Input data in
    'study_dir' is organised according to BIDS, the 'conditions' variable
    specifies the conditions of interest with respect to the regressors defined
    in BIDS. After completion, the onset files are saved in 'onset_dir'.
    """
    # Create FSL onset files from BIDS
    create_fsl_onset_files(study_dir, onset_dir, conditions)

    # Convert FSL onset files to AFNI onset files
    cmd = '3coltoAFNI.sh ' + onset_dir
    print(cmd)
    check_call(cmd, shell=True)

    # Delete FSL onset files
    filelist = glob.glob(os.path.join(onset_dir, "*.txt"))
    for f in filelist:
        os.remove(f)

    sub_dirs = glob.glob(os.path.join(study_dir, 'sub-*'))
    subs = [os.path.basename(w) for w in sub_dirs]

    # Get the condition names
    condition_names = list()
    for cond_names, cond_info in conditions:
        if isinstance(cond_names, tuple):
            for cond_name in cond_names:
                condition_names.append(cond_name)
        else:
            condition_names.append(cond_names)

    # Combine all runs into one .1d combined onset for each condition/subject
    for sub in subs:
        for cond in condition_names:
            # All onset files for this subject and condition
            onset_files = glob.glob(
                os.path.join(onset_dir, sub + '_run-[0-9][0-9]_' + cond + '*.1d'))
            combined_onset_file = os.path.join(
                onset_dir, sub + '_combined_' + cond + '_afni.1d')
            if not onset_files:
                raise Exception('No onset files for ' + sub + ' ' + cond)

            with open(combined_onset_file, 'w') as outfile:
                for fname in onset_files:
                    with open(fname) as infile:
                        outfile.write(infile.read())
                    os.remove(fname)


def run_subject_level_analyses(preproc_dir, onset_dir, level1_dir,
    sub_level_template, level2_dir):

    scripts_dir = os.path.join(preproc_dir, os.pardir, 'SCRIPTS')

    if not os.path.isdir(scripts_dir):
        os.mkdir(scripts_dir)

    # Pre-processing directories storing the fMRIs and aMRIs for all subjects
    func_dir = os.path.join(preproc_dir, 'FUNCTIONAL')
    anat_dir = os.path.join(preproc_dir, 'ANATOMICAL')

    # All aMRI files (for all subjects)
    amri_files = glob.glob(os.path.join(anat_dir, 'sub-*_T1w.nii.gz'))

    # For each subject
    for amri in amri_files:
        # New dict for each subject
        values = dict()
        values["anat_dir"] = anat_dir
        values["func_dir"] = func_dir
        values["stim_dir"] = onset_dir

        subreg = re.search('sub-\d+', amri)
        sub = subreg.group(0)
        values["sub"] = sub
        values["subj"] = sub.replace("-", "")

        # Fill-in the subject-level template
        with open(sub_level_template) as f:
            tpm = f.read()
            t = string.Template(tpm)
            sub_script = t.substitute(values)

        sub_script_file = os.path.join(scripts_dir, sub + '_level1.sh')

        with open(sub_script_file, "w") as f:
            f.write(sub_script)

        # # Run feat
        # cmd = "feat " + sub_fsf_file
        # print(cmd)
        # check_call(cmd, shell=True)