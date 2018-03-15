import nibabel as nib
from nibabel.processing import resample_from_to
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm as cm
import scipy
import os

def sorrenson_dice(data1_file, data2_file, reslice=True):
    # Load nifti images
    data1_img = nib.load(data1_file)
    data2_img = nib.load(data2_file)

    # Load data from images
    data2 = data2_img.get_data()
    data1 = data1_img.get_data()

    # Get asbolute values (positive and negative blobs are of interest)
    data2 = np.absolute(data2)
    data1 = np.absolute(data1)

    if reslice:
        # Resample data1 on data2 using nearest nneighbours
        data1_resl_img = resample_from_to(data1_img, data2_img, order=0)
        # Load data from images
        data1_res = data1_resl_img.get_data()
            
        # Resample data2 on data1 using nearest nneighbours
        data2_resl_img = resample_from_to(data2_img, data1_img, order=0)        
        data2_res = data2_resl_img.get_data()

    # Mask using zeros
    data1 = np.nan_to_num(data1)
    data2 = np.nan_to_num(data2)
    if reslice:
        data1_res = np.nan_to_num(data1_res)
        data2_res = np.nan_to_num(data2_res)

    # Vectorize
    data1 = np.reshape(data1, -1)
    data2 = np.reshape(data2, -1)
    if reslice:
        data1_res = np.reshape(data1_res, -1)
        data2_res = np.reshape(data2_res, -1)

    if reslice:
        dices = (1-scipy.spatial.distance.dice(data1_res>0, data2>0), 
                 1-scipy.spatial.distance.dice(data1>0, data2_res>0))
    else:
        dices = 1-scipy.spatial.distance.dice(data1>0, data2>0)
    
    return dices

def ds001_dice_matrix(df, filename=None):
    mask = np.tri(df.shape[0], k=0)
    mask = 1-mask
    df = np.ma.array(df, mask=mask)
    fig = plt.figure(figsize=(7,7))
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Reds')
    cmap.set_bad('w')
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
        
    for (i, j), z in np.ndenumerate(df):
        if j < i:
            ax1.text(j, i, '{:0.3f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    
    plt.title('Positive Activation Dice Coefficients', fontsize=15)
    labels=['','AFNI','FSL','SPM','AFNI perm', 'SPM perm']
    ax1.set_xticklabels(labels,fontsize=12)
    ax1.set_yticklabels(labels,fontsize=12)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[0,0.2,0.4,0.6,0.8,1], fraction=0.046, pad=0.04)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')

    if filename is not None:
        plt.savefig(os.path.join('img', filename))

    plt.show()


def ds109_dice_matrix(df, filename=None):
    mask = np.tri(df.shape[0], k=0)
    mask = 1-mask
    df = np.ma.array(df, mask=mask)
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Reds')
    cmap.set_bad('w')
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
    
    for (i, j), z in np.ndenumerate(df):
        if j < i:
            ax1.text(j, i, '{:0.3f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    
    plt.title('Positive Activation Dice Coefficients', fontsize=15)
    labels=['','AFNI','FSL','SPM','AFNI perm','FSL perm','SPM perm']
    ax1.set_xticklabels(labels,fontsize=12)
    ax1.set_yticklabels(labels,fontsize=12)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[0,0.2,0.4,0.6,0.8,1], fraction=0.046, pad=0.04)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_ticks_position('none')

    if filename is not None:
        plt.savefig(os.path.join('img', filename))

    plt.show()
    
def negative_dice_matrix(df, filename=None):
    mask = np.tri(df.shape[0], k=0)
    mask = 1-mask
    df = np.ma.array(df, mask=mask)
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Blues')
    cmap.set_bad('w')
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
    
    for (i, j), z in np.ndenumerate(df):
        if j < i:
            ax1.text(j, i, '{:0.3f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    
    plt.title('Negative Activation Dice Coefficients', fontsize=15)
    labels=['','AFNI','FSL','SPM','AFNI perm','FSL perm','SPM perm']
    ax1.set_xticklabels(labels,fontsize=12)
    ax1.set_yticklabels(labels,fontsize=12)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[0,0.2,0.4,0.6,0.8,1], fraction=0.046, pad=0.04)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_ticks_position('none')

    if filename is not None:
        plt.savefig(os.path.join('img', filename))

    plt.show()
    
def ds120_dice_matrix(df, filename=None):
    mask = np.tri(df.shape[0], k=0)
    mask = 1-mask
    df = np.ma.array(df, mask=mask)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Reds')
    cmap.set_bad('w')
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
    
    for (i, j), z in np.ndenumerate(df):
        if j < i:
            ax1.text(j, i, '{:0.3f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    
    plt.title('Positive Activation Dice Coefficients', fontsize=15)
    xlabels=['','AFNI', '', 'SPM']
    ylabels=['','','AFNI','','','','SPM','','']
    ax1.set_xticklabels(xlabels,fontsize=12)
    ax1.set_yticklabels(ylabels,fontsize=12)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[0,0.2,0.4,0.6,0.8,1])
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_ticks_position('none')

    if filename is not None:
        plt.savefig(os.path.join('img', filename))

    plt.show()

def dice(afni_exc_set_file, spm_exc_set_file,
         afni_perm_pos_exc=None, spm_perm_pos_exc=None,
         afni_exc_set_file_neg=None, spm_exc_set_file_neg=None,
         fsl_exc_set_file=None, fsl_exc_set_file_neg=None, 
         fsl_perm_pos_exc=None, 
         afni_perm_neg_exc=None, fsl_perm_neg_exc=None, spm_perm_neg_exc=None,
         study=None
         ):

   
    # *** Obtain Dice coefficient for each combination of images
    # Comparison of replication analyses
    if fsl_exc_set_file is not None:
        afni_res_fsl_pos_dice, afni_fsl_res_pos_dice = sorrenson_dice(afni_exc_set_file, fsl_exc_set_file)
        afni_res_fsl_neg_dice, afni_fsl_res_neg_dice = sorrenson_dice(afni_exc_set_file_neg, fsl_exc_set_file_neg)

    afni_res_spm_pos_dice, afni_spm_res_pos_dice = sorrenson_dice(afni_exc_set_file, spm_exc_set_file)
    if afni_exc_set_file_neg is not None:
        afni_res_spm_neg_dice, afni_spm_res_neg_dice = sorrenson_dice(afni_exc_set_file_neg, spm_exc_set_file_neg)
    
    if fsl_exc_set_file is not None:
        fsl_res_spm_pos_dice, fsl_spm_res_pos_dice = sorrenson_dice(fsl_exc_set_file, spm_exc_set_file)
        fsl_res_spm_neg_dice, fsl_spm_res_neg_dice = sorrenson_dice(fsl_exc_set_file_neg, spm_exc_set_file_neg)
    
    # Comparison of permutation tests
    if fsl_perm_pos_exc is not None:
        afni_res_fsl_pos_dice_perm, afni_fsl_res_pos_dice_perm = sorrenson_dice(afni_perm_pos_exc, fsl_perm_pos_exc)
    if fsl_perm_neg_exc is not None:
        afni_res_fsl_neg_dice_perm, afni_fsl_res_neg_dice_perm = sorrenson_dice(afni_perm_neg_exc, fsl_perm_neg_exc)
    
    if afni_perm_pos_exc is not None:
        afni_res_spm_pos_dice_perm, afni_spm_res_pos_dice_perm = sorrenson_dice(afni_perm_pos_exc, spm_perm_pos_exc)
    if afni_perm_neg_exc is not None:
        afni_res_spm_neg_dice_perm, afni_spm_res_neg_dice_perm = sorrenson_dice(afni_perm_neg_exc, spm_perm_neg_exc)
    
    if fsl_perm_pos_exc is not None:
        fsl_res_spm_pos_dice_perm, fsl_spm_res_pos_dice_perm = sorrenson_dice(fsl_perm_pos_exc, spm_perm_pos_exc)
    if fsl_perm_neg_exc is not None:
        fsl_res_spm_neg_dice_perm, fsl_spm_res_neg_dice_perm = sorrenson_dice(fsl_perm_neg_exc, spm_perm_neg_exc)
    
    # Intra-software comparison of replications against permutations
    if afni_perm_pos_exc is not None:
        afni_rep_perm_pos_dice = sorrenson_dice(afni_exc_set_file, afni_perm_pos_exc, False)
        fsl_rep_perm_pos_dice = sorrenson_dice(fsl_exc_set_file, fsl_perm_pos_exc, False)
        spm_rep_perm_pos_dice = sorrenson_dice(spm_exc_set_file, spm_perm_pos_exc, False)
    if afni_perm_neg_exc is not None:
        afni_rep_perm_neg_dice = sorrenson_dice(afni_exc_set_file_neg, afni_perm_neg_exc, False)
        fsl_rep_perm_neg_dice = sorrenson_dice(fsl_exc_set_file_neg, fsl_perm_neg_exc, False)
        spm_rep_perm_neg_dice = sorrenson_dice(spm_exc_set_file_neg, spm_perm_neg_exc, False)
    
    # Comparison of permutations with parametric tests
    if afni_perm_pos_exc is not None:
        afni_fsl_perm_res_pos_dice, afni_res_fsl_perm_pos_dice = sorrenson_dice(fsl_perm_pos_exc, afni_exc_set_file)
        afni_spm_perm_res_pos_dice, afni_res_spm_perm_pos_dice = sorrenson_dice(spm_perm_pos_exc, afni_exc_set_file)
        afni_perm_res_fsl_pos_dice, afni_perm_fsl_res_pos_dice = sorrenson_dice(afni_perm_pos_exc, fsl_exc_set_file)
        fsl_spm_perm_res_pos_dice, fsl_res_spm_perm_pos_dice = sorrenson_dice(spm_perm_pos_exc, fsl_exc_set_file)
        afni_perm_res_spm_pos_dice, afni_perm_spm_res_pos_dice = sorrenson_dice(afni_perm_pos_exc, spm_exc_set_file)
        fsl_perm_res_spm_pos_dice, fsl_perm_spm_res_pos_dice = sorrenson_dice(fsl_perm_pos_exc, spm_exc_set_file)
    
    if afni_perm_neg_exc is not None:
        afni_fsl_perm_res_neg_dice, afni_res_fsl_perm_neg_dice = sorrenson_dice(fsl_perm_neg_exc, afni_exc_set_file_neg)
        afni_spm_perm_res_neg_dice, afni_res_spm_perm_neg_dice = sorrenson_dice(spm_perm_neg_exc, afni_exc_set_file_neg)
        afni_perm_res_fsl_neg_dice, afni_perm_fsl_res_neg_dice = sorrenson_dice(afni_perm_neg_exc, fsl_exc_set_file_neg)
        fsl_spm_perm_res_neg_dice, fsl_res_spm_perm_neg_dice = sorrenson_dice(spm_perm_neg_exc, fsl_exc_set_file_neg)
        afni_perm_res_spm_neg_dice, afni_perm_spm_res_neg_dice = sorrenson_dice(afni_perm_neg_exc, spm_exc_set_file_neg)
        fsl_perm_res_spm_neg_dice, fsl_perm_spm_res_neg_dice = sorrenson_dice(fsl_perm_neg_exc, spm_exc_set_file_neg)
    
    else:
        [afni_fsl_perm_res_neg_dice, afni_res_fsl_perm_neg_dice,
         afni_spm_perm_res_neg_dice, afni_res_spm_perm_neg_dice,
         afni_perm_res_fsl_neg_dice, afni_perm_fsl_res_neg_dice,
         fsl_spm_perm_res_neg_dice, fsl_res_spm_perm_neg_dice,
         afni_perm_res_spm_neg_dice, afni_perm_spm_res_neg_dice,
         fsl_perm_res_spm_neg_dice, fsl_perm_spm_res_neg_dice] = np.zeros(12)
        
    # *** Printing results
    if fsl_exc_set_file is not None:
        print "AFNI/FSL positive activation dice coefficient = %.6f" % afni_res_fsl_pos_dice
        print "FSL/AFNI positive activation dice coefficient = %.6f" % afni_fsl_res_pos_dice
    print "AFNI/SPM positive activation dice coefficient = %.6f" % afni_res_spm_pos_dice
    print "SPM/AFNI positive activation dice coefficient = %.6f" % afni_spm_res_pos_dice
    if fsl_exc_set_file is not None:
        print "FSL/SPM positive activation dice coefficient = %.6f" % fsl_res_spm_pos_dice
        print "SPM/FSL positive activation dice coefficient = %.6f" % fsl_spm_res_pos_dice
        print "Permutation test AFNI/SPM positive activation dice coefficient = %.6f" % afni_res_spm_pos_dice_perm
        print "Permutation test SPM/AFNI positive activation dice coefficient = %.6f" % afni_spm_res_pos_dice_perm
        print "Permutation test AFNI/FSL positive activation dice coefficient = %.6f" % afni_res_fsl_pos_dice_perm
        print "Permutation test FSL/AFNI positive activation dice coefficient = %.6f" % afni_fsl_res_pos_dice_perm
        print "Permutation test FSL/SPM positive activation dice coefficient = %.6f" % fsl_res_spm_pos_dice_perm
        print "Permutation test SPM/FSL positive activation dice coefficient = %.6f" % fsl_spm_res_pos_dice_perm
        print "AFNI classical inference/permutation test positive activation dice coefficient = %.6f" % afni_rep_perm_pos_dice
        print "FSL classical inference/permutation test positive activation dice coefficient = %.6f" % fsl_rep_perm_pos_dice
        print "SPM classical inference/permutation test positive activation dice coefficient = %.6f" % spm_rep_perm_pos_dice
        print "AFNI parametric/FSL permutation positive activivation dice coefficient = %.6f" % afni_res_fsl_perm_pos_dice
        print "FSL permutation/AFNI parametric positive activivation dice coefficient = %.6f" % afni_fsl_perm_res_pos_dice
        print "AFNI parametric/SPM permutation positive activivation dice coefficient = %.6f" % afni_res_spm_perm_pos_dice
        print "SPM permutation/AFNI parametric positive activivation dice coefficient = %.6f" % afni_spm_perm_res_pos_dice
        print "FSL parametric/AFNI permutation positive activivation dice coefficient = %.6f" % afni_perm_fsl_res_pos_dice
        print "AFNI permutation/FSL parametric positive activivation dice coefficient = %.6f" % afni_perm_res_fsl_pos_dice
        print "FSL parametric/SPM permutation positive activivation dice coefficient = %.6f" % fsl_res_spm_perm_pos_dice
        print "SPM permutation/FSL parametric positive activivation dice coefficient = %.6f" % fsl_spm_perm_res_pos_dice
        print "SPM parametric/AFNI permutation positive activivation dice coefficient = %.6f" % afni_perm_spm_res_pos_dice
        print "AFNI permutation/SPM parametric positive activivation dice coefficient = %.6f" % afni_perm_res_spm_pos_dice
        print "SPM parametric/FSL permutation positive activivation dice coefficient = %.6f" % fsl_perm_spm_res_pos_dice
        print "FSL permutation/SPM parametric positive activivation dice coefficient = %.6f\n" % fsl_perm_res_spm_pos_dice

    if spm_perm_neg_exc is not None:
        print "AFNI/FSL negative activation dice coefficient = %.6f" % afni_res_fsl_neg_dice
        print "FSL/AFNI negative activation dice coefficient = %.6f" % afni_fsl_res_neg_dice
        print "AFNI/SPM negative activation dice coefficient = %.6f" % afni_res_spm_neg_dice
        print "SPM/AFNI negative activation dice coefficient = %.6f" % afni_spm_res_neg_dice
        print "FSL/SPM negative activation dice coefficient = %.6f" % fsl_res_spm_neg_dice
        print "SPM/FSL negative activation dice coefficient = %.6f" % fsl_spm_res_neg_dice
        print "Permutation test AFNI/SPM negative activation dice coefficient = %.6f" % afni_res_spm_neg_dice_perm
        print "Permutation test SPM/AFNI negative activation dice coefficient = %.6f" % afni_spm_res_neg_dice_perm
        print "Permutation test AFNI/FSL negative activation dice coefficient = %.6f" % afni_res_fsl_neg_dice_perm
        print "Permutation test FSL/AFNI negative activation dice coefficient = %.6f" % afni_fsl_res_neg_dice_perm
        print "Permutation test FSL/SPM negative activation dice coefficient = %.6f" % fsl_res_spm_neg_dice_perm
        print "Permutation test SPM/FSL negative activation dice coefficient = %.6f" % fsl_spm_res_neg_dice_perm
        print "AFNI classical inference/permutation test negative activation dice coefficient = %.6f" % afni_rep_perm_neg_dice
        print "FSL classical inference/permutation test negative activation dice coefficient = %.6f" % fsl_rep_perm_neg_dice
        print "SPM classical inference/permutation test negative activation dice coefficient = %.6f" % spm_rep_perm_neg_dice    
        print "AFNI parametric/FSL permutation negative activivation dice coefficient = %.6f" % afni_res_fsl_perm_neg_dice
        print "FSL permutation/AFNI parametric negative activivation dice coefficient = %.6f" % afni_fsl_perm_res_neg_dice    
        print "AFNI parametric/SPM permutation negative activivation dice coefficient = %.6f" % afni_res_spm_perm_neg_dice
        print "SPM permutation/AFNI parametric negative activivation dice coefficient = %.6f" % afni_spm_perm_res_neg_dice    
        print "FSL parametric/AFNI permutation negative activivation dice coefficient = %.6f" % afni_perm_fsl_res_neg_dice
        print "AFNI permutation/FSL parametric negative activivation dice coefficient = %.6f" % afni_perm_res_fsl_neg_dice    
        print "FSL parametric/SPM permutation negative activivation dice coefficient = %.6f" % fsl_res_spm_perm_neg_dice
        print "SPM permutation/FSL parametric negative activivation dice coefficient = %.6f" % fsl_spm_perm_res_neg_dice    
        print "SPM parametric/AFNI permutation negative activivation dice coefficient = %.6f" % afni_perm_spm_res_neg_dice
        print "AFNI permutation/SPM parametric negative activivation dice coefficient = %.6f" % afni_perm_res_spm_neg_dice    
        print "SPM parametric/FSL permutation negative activivation dice coefficient = %.6f" % fsl_perm_spm_res_neg_dice
        print "FSL permutation/SPM parametric negative activivation dice coefficient = %.6f\n" % fsl_perm_res_spm_neg_dice
    
    # Creating a table of the Dice coefficients
    if fsl_exc_set_file is not None:
        dice_coefficients = dict()
        dice_coefficients["1"] = [1, 
                                  np.mean([afni_res_fsl_pos_dice, afni_fsl_res_pos_dice]),
                                  np.mean([afni_res_spm_pos_dice, afni_spm_res_pos_dice]),
                                  afni_rep_perm_pos_dice,
                                  np.mean([afni_res_fsl_perm_pos_dice, afni_fsl_perm_res_pos_dice]),
                                  np.mean([afni_res_spm_perm_pos_dice, afni_spm_perm_res_pos_dice])
                                 ]
        dice_coefficients["2"] = [np.mean([afni_res_fsl_pos_dice, afni_fsl_res_pos_dice]), 
                                  1,
                                  np.mean([fsl_res_spm_pos_dice, fsl_spm_res_pos_dice]),
                                  np.mean([afni_perm_res_fsl_pos_dice, afni_perm_fsl_res_pos_dice]), 
                                  fsl_rep_perm_pos_dice, 
                                  np.mean([fsl_res_spm_perm_pos_dice, fsl_spm_perm_res_pos_dice])
                                 ]
        dice_coefficients["3"] = [np.mean([afni_res_spm_pos_dice, afni_spm_res_pos_dice]),
                                  np.mean([fsl_res_spm_pos_dice, fsl_spm_res_pos_dice]),
                                  1,
                                  np.mean([afni_perm_res_spm_pos_dice, afni_perm_spm_res_pos_dice]),
                                  np.mean([fsl_perm_res_spm_pos_dice, fsl_perm_spm_res_pos_dice]),
                                  spm_rep_perm_pos_dice
                                 ]
        dice_coefficients["4"] = [afni_rep_perm_pos_dice, 
                                  np.mean([afni_perm_res_fsl_pos_dice, afni_perm_fsl_res_pos_dice]),
                                  np.mean([afni_perm_res_spm_pos_dice, afni_perm_spm_res_pos_dice]),
                                  1,
                                  np.mean([afni_res_fsl_pos_dice_perm, afni_fsl_res_pos_dice_perm]),
                                  np.mean([afni_res_spm_pos_dice_perm, afni_spm_res_pos_dice_perm])
                                 ]
        dice_coefficients["5"] = [np.mean([afni_res_fsl_perm_pos_dice, afni_fsl_perm_res_pos_dice]),
                                  fsl_rep_perm_pos_dice,
                                  np.mean([fsl_perm_res_spm_pos_dice, fsl_perm_spm_res_pos_dice]),
                                  np.mean([afni_res_fsl_pos_dice_perm, afni_fsl_res_pos_dice_perm]), 
                                  1,
                                  np.mean([fsl_res_spm_pos_dice_perm, fsl_spm_res_pos_dice_perm])
                                 ]
        dice_coefficients["6"] = [np.mean([afni_res_spm_perm_pos_dice, afni_spm_perm_res_pos_dice]),
                                  np.mean([fsl_res_spm_perm_pos_dice, fsl_spm_perm_res_pos_dice]),
                                  spm_rep_perm_pos_dice,
                                  np.mean([afni_res_spm_pos_dice_perm, afni_spm_res_pos_dice_perm]),
                                  np.mean([fsl_res_spm_pos_dice_perm, fsl_spm_res_pos_dice_perm]),
                                  1
                                 ]

        pos_df = pd.DataFrame(dice_coefficients)
        ds109_dice_matrix(pos_df, 'Fig_' + study + '_Dice.png')

        if spm_perm_neg_exc is not None:
            negative_dice_coefficients = dict()
            negative_dice_coefficients["1"] = [1, 
                                      np.mean([afni_res_fsl_neg_dice, afni_fsl_res_neg_dice]),
                                      np.mean([afni_res_spm_neg_dice, afni_spm_res_neg_dice]),
                                      afni_rep_perm_neg_dice,
                                      np.mean([afni_res_fsl_perm_neg_dice, afni_fsl_perm_res_neg_dice]),
                                      np.mean([afni_res_spm_perm_neg_dice, afni_spm_perm_res_neg_dice])
                                     ]
            negative_dice_coefficients["2"] = [np.mean([afni_res_fsl_neg_dice, afni_fsl_res_neg_dice]), 
                                      1,
                                      np.mean([fsl_res_spm_neg_dice, fsl_spm_res_neg_dice]),
                                      np.mean([afni_perm_res_fsl_neg_dice, afni_perm_fsl_res_neg_dice]), 
                                      fsl_rep_perm_neg_dice, 
                                      np.mean([fsl_res_spm_perm_neg_dice, fsl_spm_perm_res_neg_dice])
                                     ]
            negative_dice_coefficients["3"] = [np.mean([afni_res_spm_neg_dice, afni_spm_res_neg_dice]),
                                      np.mean([fsl_res_spm_neg_dice, fsl_spm_res_neg_dice]),
                                      1,
                                      np.mean([afni_perm_res_spm_neg_dice, afni_perm_spm_res_neg_dice]),
                                      np.mean([fsl_perm_res_spm_neg_dice, fsl_perm_spm_res_neg_dice]),
                                      spm_rep_perm_neg_dice
                                      ]
            negative_dice_coefficients["4"] = [afni_rep_perm_neg_dice, 
                                      np.mean([afni_perm_res_fsl_neg_dice, afni_perm_fsl_res_neg_dice]),
                                      np.mean([afni_perm_res_spm_neg_dice, afni_perm_spm_res_neg_dice]),
                                      1,
                                      np.mean([afni_res_fsl_neg_dice_perm, afni_fsl_res_neg_dice_perm]),
                                      np.mean([afni_res_spm_neg_dice_perm, afni_spm_res_neg_dice_perm])
                                     ]
            negative_dice_coefficients["5"] = [np.mean([afni_res_fsl_perm_neg_dice, afni_fsl_perm_res_neg_dice]),
                                      fsl_rep_perm_neg_dice,
                                      np.mean([fsl_perm_res_spm_neg_dice, fsl_perm_spm_res_neg_dice]),
                                      np.mean([afni_res_fsl_neg_dice_perm, afni_fsl_res_neg_dice_perm]), 
                                      1,
                                      np.mean([fsl_res_spm_neg_dice_perm, fsl_spm_res_neg_dice_perm])
                                     ]
            negative_dice_coefficients["6"] = [np.mean([afni_res_spm_perm_neg_dice, afni_spm_perm_res_neg_dice]),
                                      np.mean([fsl_res_spm_perm_neg_dice, fsl_spm_perm_res_neg_dice]),
                                      spm_rep_perm_neg_dice,
                                      np.mean([afni_res_spm_neg_dice_perm, afni_spm_res_neg_dice_perm]),
                                      np.mean([fsl_res_spm_neg_dice_perm, fsl_spm_res_neg_dice_perm]),
                                      1
                                     ]

            neg_df = pd.DataFrame(negative_dice_coefficients)
            negative_dice_matrix(neg_df, 'Fig_' + study + 'neg_Dice.png')
    else:
        ds120_dice_coefficients = dict()
        ds120_dice_coefficients["1"] = [1, np.mean([afni_res_spm_pos_dice, afni_spm_res_pos_dice])]
        ds120_dice_coefficients["2"] = [np.mean([afni_res_spm_pos_dice, afni_spm_res_pos_dice]), 1]
        
        ds120_df = pd.DataFrame(ds120_dice_coefficients)
        ds120_dice_matrix(ds120_df, 'Fig_' + study + '_Dice.png')