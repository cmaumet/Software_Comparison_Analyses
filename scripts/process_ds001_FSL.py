import os

from lib.fsl_processing import copy_and_BET, create_fsl_onset_files
from lib.fsl_processing import run_run_level_analyses
from lib.fsl_processing import run_subject_level_analyses
from lib.fsl_processing import run_group_level_analysis

raw_dir = '/storage/essicd/data/NIDM-Ex/BIDS_Data/DATA/BIDS/ds001_R2.0.4'
results_dir = '/storage/essicd/data/NIDM-Ex/BIDS_Data/RESULTS/SOFTWARE_COMPARISON/ds001'

fsl_dir = os.path.join(results_dir, 'FSL')
if not os.path.isdir(fsl_dir):
    os.mkdir(fsl_dir)

preproc_dir = os.path.join(fsl_dir, 'PREPROCESSING')
level1_dir = os.path.join(fsl_dir, 'LEVEL1')
level2_dir = os.path.join(fsl_dir, 'LEVEL1')
level3_dir = os.path.join(fsl_dir, 'LEVEL2', 'group')

cwd = os.path.dirname(os.path.realpath(__file__))

# Copy raw anatomical and functional data to the preprocessing directory and
# run BET on the anatomical images
copy_and_BET(raw_dir, preproc_dir)

# Directory to store the onset files
onsetDir = os.path.join(fsl_dir, 'ONSETS')

# Define conditions and parametric modulations (if any)
conditions = (
    (('pumps_fixed', 'pumps_demean'), ('pumps_demean',)),
    ('pumps_RT', ('pumps_demean', 'response_time')),
    (('cash_fixed', 'cash_demean'), ('cash_demean',)),
    ('cash_RT', ('cash_demean', 'response_time')),
    (('explode_fixed', 'explode_demean'), ('explode_demean',)),
    (('control_pumps_fixed', 'control_pumps_demean'),
     ('control_pumps_demean',)),
    ('control_pumps_RT', ('control_pumps_demean', 'response_time')))

# Create 3-columns onset files based on BIDS tsv files
cond_files = create_fsl_onset_files(raw_dir, onsetDir, conditions)

run_level_fsf = os.path.join(cwd, 'lib', 'template_ds001_FSL_level1.fsf')
sub_level_fsf = os.path.join(cwd, 'lib', 'template_ds001_FSL_level2.fsf')
grp_level_fsf = os.path.join(cwd, 'lib', 'template_ds001_FSL_level3.fsf')

# Run a GLM for each fMRI run of each subject
run_run_level_analyses(preproc_dir, run_level_fsf, level1_dir, cond_files)

# Run a GLM combining all the fMRI runs of each subject
run_subject_level_analyses(level1_dir, sub_level_fsf, level2_dir)

# Run the group-level GLM
run_group_level_analysis(level2_dir, grp_level_fsf, level3_dir, '1')