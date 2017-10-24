import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def bland_altman_plot(data1, data2, *args, **kwargs):
    in_mask_indices = np.logical_not(np.logical_or(
    np.logical_or(np.isnan(data1), np.absolute(data1) == 0),
    np.logical_or(np.isnan(data2), np.absolute(data2) == 0)))

    data1 = data1[in_mask_indices]
    data2 = data2[in_mask_indices]

    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference
    
    return mean, diff, md, sd

def bland_altman(Title, afni_stat_file, spm_stat_file,
                 afni_reslice_spm, afni_spm_reslice,
                 fsl_stat_file=None, fsl_reslice_spm=None,
                 afni_fsl_reslice=None, afni_reslice_fsl=None, fsl_spm_reslice=None):
    plt.style.use('seaborn-colorblind')
    
    # Get data from stat images
    afni_dat = nib.load(afni_stat_file).get_data()
    spm_dat = nib.load(spm_stat_file).get_data()
    if fsl_stat_file is not None:
        fsl_dat = nib.load(fsl_stat_file).get_data()

    # Get data from resliced images   
    afni_res_spm_dat = nib.load(afni_reslice_spm).get_data()
    afni_spm_res_dat = nib.load(afni_spm_reslice).get_data()
    if fsl_stat_file is not None:
        afni_res_fsl_dat = nib.load(afni_reslice_fsl).get_data()
        fsl_res_spm_dat = nib.load(fsl_reslice_spm).get_data()
        afni_fsl_res_dat = nib.load(afni_fsl_reslice).get_data()
        fsl_spm_res_dat = nib.load(fsl_spm_reslice).get_data()
    
    # Reshape to 1-dimension
    afni_1d = np.reshape(afni_dat, -1)
    spm_1d = np.reshape(spm_dat, -1)
    afni_res_spm_1d = np.reshape(afni_res_spm_dat, -1)
    afni_spm_res_1d = np.reshape(afni_spm_res_dat, -1)
    if fsl_stat_file is not None:
        fsl_1d = np.reshape(fsl_dat, -1)
        afni_res_fsl_1d = np.reshape(afni_res_fsl_dat, -1)
        afni_fsl_res_1d = np.reshape(afni_fsl_res_dat, -1)
        fsl_res_spm_1d = np.reshape(fsl_res_spm_dat, -1)
        fsl_spm_res_1d = np.reshape(fsl_spm_res_dat, -1)
    
    # Create Bland-Altman plots
    # AFNI/FSL B-A plots
    if fsl_stat_file is not None:
        fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
        fig.suptitle(Title, fontsize=20, x=0.47, y=1.06)
        fig.subplots_adjust(hspace=1.0, wspace=0.4, left=0.07, right=0.93)
        
        ax = axs[0]
        mean, diff, md, sd = bland_altman_plot(afni_res_fsl_1d, fsl_1d)
        hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
        ax.axhline(linewidth=1, color='r')
        ax.set_title('AFNI reslice on FSL Bland-Altman')
        ax.set_xlabel('Average of T-statistics')
        ax.set_ylabel('Difference of T-statistics (AFNI - FSL)')
        cb = fig.colorbar(hb, ax=ax)
        cb.set_label('log10(N)')
        
        ax = axs[1]
        mean, diff, md, sd = bland_altman_plot(afni_1d, afni_fsl_res_1d)
        hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
        ax.axhline(linewidth=1, color='r')
        ax.set_title('FSL reslice on AFNI Bland-Altman')
        ax.set_xlabel('Average of T-statistics')
        ax.set_ylabel('Difference of T-statistics (AFNI - FSL)')
        cb = fig.colorbar(hb, ax=ax)
        cb.set_label('log10(N)')
        
        plt.show()

    # AFNI/SPM B-A plots
    fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
    if fsl_stat_file is None:
        fig.suptitle(Title, fontsize=20, x=0.47, y=1.06)
    fig.subplots_adjust(hspace=1.0, wspace=0.4, left=0.07, right=0.93)
    
    ax = axs[0]
    mean, diff, md, sd = bland_altman_plot(afni_res_spm_1d, spm_1d)    
    hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
    ax.axhline(linewidth=1, color='r')
    ax.set_title('AFNI reslice on SPM Bland-Altman')
    ax.set_xlabel('Average of T-statistics')
    ax.set_ylabel('Difference of T-statistics (AFNI - SPM)')
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('log10(N)')

    ax = axs[1]
    mean, diff, md, sd = bland_altman_plot(afni_1d, afni_spm_res_1d)
    hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
    ax.axhline(linewidth=1, color='r')
    ax.set_title('SPM reslice on AFNI Bland-Altman')
    ax.set_xlabel('Average of T-statistics')
    ax.set_ylabel('Difference of T-statistics (AFNI - SPM)')
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('log10(N)')

    plt.show()
    
    # FSL/SPM B-A plots
    if fsl_stat_file is not None:
        fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
        fig.subplots_adjust(hspace=1.0, wspace=0.4, left=0.07, right=0.93)
        
        ax = axs[0]
        mean, diff, md, sd = bland_altman_plot(fsl_res_spm_1d, spm_1d)
        hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
        ax.axhline(linewidth=1, color='r')
        ax.set_title('FSL reslice on SPM Bland-Altman')
        ax.set_xlabel('Average of T-statistics')
        ax.set_ylabel('Difference of T-statistics (FSL - SPM)')
        cb = fig.colorbar(hb, ax=ax)
        cb.set_label('log10(N)')
        
        ax = axs[1]
        mean, diff, md, sd = bland_altman_plot(fsl_1d, fsl_spm_res_1d)
        hb = ax.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
        ax.axhline(linewidth=1, color='r')
        ax.set_title('SPM reslice on FSL Bland-Altman')
        ax.set_xlabel('Average of T-statistics')
        ax.set_ylabel('Difference of T-statistics (FSL - SPM)')
        cb = fig.colorbar(hb, ax=ax)
        cb.set_label('log10(N)')

        plt.show()

def bland_altman_intra(Title, afni_stat_file, afni_perm_file,
                 fsl_stat_file, fsl_perm_file,
                 spm_stat_file, spm_perm_file):
    plt.style.use('seaborn-colorblind')
    
    # Get data from stat images
    afni_stat_dat = nib.load(afni_stat_file).get_data()
    afni_perm_dat = nib.load(afni_perm_file).get_data()
    fsl_stat_dat = nib.load(fsl_stat_file).get_data()
    fsl_perm_dat = nib.load(fsl_perm_file).get_data()
    spm_stat_dat = nib.load(spm_stat_file).get_data()
    spm_perm_dat = nib.load(spm_perm_file).get_data()
    
    # Reshape to 1-dimension
    afni_stat_1d = np.reshape(afni_stat_dat, -1)
    afni_perm_1d = np.reshape(afni_perm_dat, -1)
    fsl_stat_1d = np.reshape(fsl_stat_dat, -1)
    fsl_perm_1d = np.reshape(fsl_perm_dat, -1)
    spm_stat_1d = np.reshape(spm_stat_dat, -1)
    spm_perm_1d = np.reshape(spm_perm_dat, -1)
      
    # AFNI Parametric/AFNI Permutation Bland-Altman
    fig = plt.figure()
    fig.suptitle(Title, fontsize=20, x=0.40, y=3.70)
    fig.subplots_adjust(hspace=0.3, top=3.58, bottom=1.0, left=0.1, right=0.8)
    ax1 = fig.add_subplot(311)      
    mean, diff, md, sd = bland_altman_plot(afni_stat_1d, afni_perm_1d)
    hb = ax1.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
    ax1.axhline(linewidth=1, color='r')
    ax1.set_title('AFNI Parametric/Permutation')
    ax1.set_xlabel('Average of T-statistics')
    ax1.set_ylabel('Difference of T-statistics (Para - Perm)')
    cb = fig.colorbar(hb, ax=ax1)
    cb.set_label('log10(N)')
    
    # FSL Parametric/FSL Permutation Bland-Altman
    ax2 = fig.add_subplot(312)
    mean, diff, md, sd = bland_altman_plot(fsl_stat_1d, fsl_perm_1d)
    hb = ax2.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
    ax2.axhline(linewidth=1, color='r')
    ax2.set_title('FSL Parametric/Permutation')
    ax2.set_xlabel('Average of T-statistics')
    ax2.set_ylabel('Difference of T-statistics (Para - Perm)')
    cb = fig.colorbar(hb, ax=ax2)
    cb.set_label('log10(N)')

    # SPM Parametric/SPM Permutation Bland-Altman
    ax3 = fig.add_subplot(313)
    mean, diff, md, sd = bland_altman_plot(spm_stat_1d, spm_perm_1d)
    hb = ax3.hexbin(mean, diff, bins='log', cmap='viridis', gridsize=50)
    ax3.axhline(linewidth=1, color='r')
    ax3.set_title('SPM Parametric/Permutation')
    ax3.set_xlabel('Average of T-statistics')
    ax3.set_ylabel('Difference of T-statistics (Para - Perm)')
    cb = fig.colorbar(hb, ax=ax3)
    cb.set_label('log10(N)')

    plt.show()