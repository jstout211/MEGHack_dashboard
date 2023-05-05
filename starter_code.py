#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:46:59 2023

@author: jstout
"""

import os, os.path as op
import pandas as pd
import glob
import mne
from mne.viz import Brain
import nibabel as nib
import numpy as np
import seaborn as sns
import pylab
import nibabel as nib

import statsmodels.api as sm
import statsmodels.formula.api as smf


'''
!!!!!!!!!!!!!!!!!
This code has been taken from elsewhere and may not run without modification
!!!!!!!!!!!!!!!!!!!!!!!
'''

# =============================================================================
# 
# =============================================================================
def filter_parcel_data(dframe, parcel_name=None, column_name=None):
    '''Return single parcel information for stats testing'''
    tmp=dframe[dframe.Parcel==parcel_name]
    if ('age' in dframe.columns) and ('sex' in dframe.columns):
        return tmp[[column_name, 'age', 'sex']].dropna()
    else:
        return tmp[[column_name]].dropna()

def proc_parcel_regression(dframe):
    '''Takes merged dataframe (subj_vars + parcel data)
    and performs regression of variables using statsmodels'''
    
    #Initialize regression dataframe
    rdframe = pd.DataFrame(columns=['parcel_name', 'coeff','rsquared_adj'])
    rdframe.parcel_name = dframe.Parcel.unique()

    for idx, row in rdframe.iterrows():
        parc = row['parcel_name']
        tmp=filter_parcel_data(dframe, parcel_name=parc, 
                               column_name='AlphaPeak')
        results = smf.ols('AlphaPeak ~ age', data=tmp).fit()
        rdframe.loc[idx, 'rsquared_adj']=results.rsquared_adj
        rdframe.loc[idx, 'coeff']=results.params['age']
    
    return rdframe


def display_regression_coefs(stats_dframe, 
                             subject_id='fsaverage',
                             parc_name='aparc_sub',
                             subjects_dir=None,
                             image_outpath=None, 
                             col_id=None, 
                             rel_scaling=False, 
                             fmin=None,
                             fmax=None):
    '''Plot the statistics on the brain
    parc_name:
        aparc or aparc_sub currently supported
    
    '''
   
    if subjects_dir != None: os.environ['SUBJECTS_DIR']=subjects_dir
    hemi = "lh"
    surf = "inflated"
    
    brain = Brain(subject_id, hemi, surf, background="white")
    
    aparc_file = os.path.join(os.environ["SUBJECTS_DIR"],
                              subject_id, "label",
                              hemi + f".{parc_name}.annot") 
    labels, ctab, names = nib.freesurfer.read_annot(aparc_file)
    
    names2=[i.decode() for i in names] #convert from binary
    if 'corpuscallosum' in names2: names2.remove('corpuscallosum')
    if 'unknown' in names2: names2.remove('unknown')
    
    # Placeholder - must be larger than number of ROIs
    roi_data = np.zeros(600)
    roi_data[:] = np.nan
    
    for idx,name in enumerate(names2):
        roi_data[idx]=stats_dframe.loc[name+'-'+hemi, col_id]
    	
    vtx_data = roi_data[labels]
    vtx_data[labels == -1] = 0
    
    thresh=.001
    vtx_data[np.abs(vtx_data)<thresh]=0
    fmin = stats_dframe[col_id].min()
    fmax = stats_dframe[col_id].max()
    brain.add_data(vtx_data, colormap="jet", fmin=fmin, fmax=fmax)
    
    if image_outpath != None:
        brain.save_image(image_outpath)



# =============================================================================
# Average images
# =============================================================================
#Alpha Peak
display_regression_coefs(stats_dframe, col_id='AlphaPeak') 

#Delta
display_regression_coefs(stats_dframe, col_id='[1, 3]') 

#Theta
display_regression_coefs(stats_dframe, col_id='[3, 6]')

#Alpha
display_regression_coefs(stats_dframe, col_id='[8, 12]')

#Beta
display_regression_coefs(stats_dframe, col_id='[13, 35]')

#Low Gamma
display_regression_coefs(stats_dframe, col_id='[35, 55]')

# =============================================================================
# 
# =============================================================================

# Make regressors

def proc_parcel_regression(dframe, col_id='AlphaPeak'):
    '''Takes merged dataframe (subj_vars + parcel data)
    and performs regression of variables using statsmodels'''
    
    #Initialize regression dataframe
    rdframe = pd.DataFrame(columns=['Parcel', 'coeff','rsquared_adj'])
    rdframe.Parcel = dframe.Parcel.unique()

    for idx, row in rdframe.iterrows():
        parc = row['Parcel'] #'parcel_name']
        tmp=filter_parcel_data(dframe, parcel_name=parc, 
                               column_name=col_id)
        results = smf.ols(f'{col_id} ~ age', data=tmp).fit()
        rdframe.loc[idx, 'rsquared_adj']=results.rsquared_adj
        rdframe.loc[idx, 'coeff']=results.params['age']
    rdframe.set_index('Parcel', inplace=True)
    return rdframe


#AlphaPeak
rdframe=proc_parcel_regression(final.dropna(subset=['AlphaPeak']))
display_regression_coefs(rdframe, col_id='rsquared_adj')

#Delta
rdframe=proc_parcel_regression(final, col_id='Delta')
display_regression_coefs(rdframe, col_id='rsquared_adj')

#Theta
rdframe=proc_parcel_regression(final, col_id='Theta')
display_regression_coefs(rdframe, col_id='rsquared_adj')

#Alpha
rdframe=proc_parcel_regression(final, col_id='Alpha')
display_regression_coefs(rdframe, col_id='rsquared_adj')

#Beta
rdframe=proc_parcel_regression(final, col_id='Beta')
display_regression_coefs(rdframe, col_id='rsquared_adj')

#L_Gamma
rdframe=proc_parcel_regression(final, col_id='L_Gamma')
display_regression_coefs(rdframe, col_id='rsquared_adj')

# =============================================================================
# Final number counts
# =============================================================================
test = final.groupby(['group']).subject.apply(set)
for group, subject in test.iteritems():
    print(f'{group} has {len(subject)}')
    
final.groupby(['group']).age.agg([np.mean, np.median, np.min, np.max])

test2=final.groupby(['group', 'subject']).first()
test2.reset_index(inplace=True)