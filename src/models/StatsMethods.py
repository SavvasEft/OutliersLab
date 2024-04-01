import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from utils.config import ITERATION_MAX_NUM_ZSCORE #, \
                         #METHODS_DESCRIPTIONS

from utils.toolbox import describe_function

def get_z_score_outliers_1d_mask(data, z_threshold=2, modified=False):
    "data: np.array"

    if data.ndim == 1:
        columns = 1
    elif data.ndim==2:
        _,columns = data.shape

    try:
        if columns == 1:
            if modified:
                median=np.median(data)
                MAD = stats.median_abs_deviation(data, scale=1)
                z_score = stats.norm.ppf(.75)*(data-median) / MAD
                
            else:
                mean = np.mean(data)
                std =  np.std(data)
                z_score = (data - mean) / std
        
            anomalies_mask = np.abs(z_score) > z_threshold
            anomalies_mask = np.squeeze(anomalies_mask)
            return anomalies_mask
        
        else:
            error_msg = "Data dimensions error. Z-score calculation for 1d can take arrays of shape (R,1) or (R,) s"
            print (error_msg)
            raise ValueError(error_msg)

    except Exception as e:
        print('Error when calculating outliers using 1d z-score.')
        raise e
    

@describe_function("z-score")
# function description should agree with METHODS_DESCRIPTIONS in config.py
def get_z_score_iter_outliers_1d_mask(data,z_threshold=2, modified=False):
    outlier_indexes = []
    iter_data = np.array(data, copy=True)
    iter_index = np.arange(len(data)).reshape(len(data),1)
    len_outlier_indexes = 5 #anything > 0 to start the loop
    iter = 0
    outliers_bool = get_z_score_outliers_1d_mask(iter_data, z_threshold=z_threshold,  modified=modified)
    found_outliers = sum(outliers_bool)>0
    while iter<ITERATION_MAX_NUM_ZSCORE and found_outliers:
        iter_outliers_bool = get_z_score_outliers_1d_mask(iter_data, z_threshold=z_threshold,  modified=modified)
        outliers_bool[iter_outliers_bool]=True
        found_outliers = sum(iter_outliers_bool)>0
        iter +=1
    return outliers_bool

def get_z_score_iter_outlier_plots(data, outlier_mask, z_threshold=2, bins = 50, line_plot=False, modified=False):
    "data: np.array"
    fig, ax = plt.subplots(2,1)       
    index = np.arange(len(data)).reshape(len(data),1)
    outlier_indexes = index[outlier_mask]
    outliers = data[outlier_mask]
    clean_data = data[np.invert(outlier_mask)] 

    if not modified:
        x_std = np.std(clean_data)
        mean = clean_data.mean()
    else:
        from statsmodels import robust
        x_std = stats.median_abs_deviation(clean_data, scale=1)
        mean = np.median(clean_data)
        z_threshold=z_threshold/stats.norm.ppf(.75)
        
    if line_plot:
        ax[0].plot(data)
    else:
        ax[0].scatter(x=index, y=data)
    ax[0].scatter(outlier_indexes,y=outliers, color = 'red')
    ax[0].axhline(mean+z_threshold*x_std, color = 'red', lw=0.8, ls='--')
    ax[0].axhline(mean-z_threshold*x_std, color = 'red', lw=0.8, ls='--')
    ax[0].axhline(mean, color = 'green', lw=0.8, ls='-')
    ax[0].set_xlabel('Point Number labels')
    ax[0].set_ylabel('Point Values')
    
    ax[1].hist(data, bins = bins)
    ax[1].axvline(mean+z_threshold*x_std, color = 'red', lw=0.8, ls='--')
    ax[1].axvline(mean-z_threshold*x_std, color = 'red', lw=0.8, ls='--')
    ax[1].axvline(mean, color = 'green', lw=0.8, ls='--')
    ax[1].set_ylabel('Point Counts')
    ax[1].set_xlabel('Point Values')
    
    plt.subplots_adjust(hspace=0.5)
    if not modified:
        fig.suptitle('Results from z-score method (iterative)', fontsize=14)   
    else:
        fig.suptitle('Results from modified z-score method (iterative)', fontsize=14)   

    return fig

def get_iqr_limits(data):
    first_quar = np.percentile(data, 25)
    third_quar = np.percentile(data, 75)
    iqr = third_quar - first_quar   
    lower_limit = first_quar - 1.5 * iqr
    upper_limit = third_quar + 1.5 * iqr 
    return lower_limit, upper_limit

@describe_function("IQR")
# function description should agree with METHODS_DESCRIPTIONS in config.py
def get_iqr_outliers_1d_mask(data):
    if data.ndim == 1:
        columns = 1
    elif data.ndim==2:
        _,columns = data.shape
    
    try:
        if columns==1:
            lower_limit, upper_limit = get_iqr_limits(data)
            outlier_mask = (data < lower_limit) | (data > upper_limit)
            outlier_mask = np.squeeze(outlier_mask)
            return outlier_mask
        
        else:
            error_msg = "Data dimensions error. IQR-score calculation for 1d can take arrays of shape (R,1) or (R,) s"
            print (error_msg)
            raise ValueError(error_msg)

    except Exception as e:
        print('Error when calculating outliers using 1d IQR method.')
        raise e
    
    

def get_iqr_anomaly_plots(data, outliers_mask, bins = 50, line_plot=False):
    lower_limit, upper_limit = get_iqr_limits(data)
    index = np.arange(len(data)).reshape(len(data),1)
    if outliers_mask is None:
        outliers_mask = get_iqr_outliers_1d_mask(data)
    outliers_index = index[outliers_mask]
    outliers = data[outliers_index]
    fig, axs = plt.subplots(3,1)
    if line_plot:
        axs[0].plot(data)
    else:
        axs[0].scatter(y=data, x=np.arange(len(data)))
    axs[0].scatter(outliers_index, outliers, color ='red')
    axs[0].set_ylabel('Point Values')
    axs[0].set_xlabel('Point Number labels')

    #sns.boxplot draws whiskers to the farthest datapoint within upper & lower limits
    #thus lower & upper limits drawn may not agree with the whiskers in boxplots.

    sns.boxplot(data=data, orient = 'h', ax=axs[1])
    axs[1].set_xlabel('Point Values')  

    axs[2].hist(data, bins=bins)
    axs[2].plot([lower_limit,lower_limit],[0,np.max(np.histogram(data, bins=50)[0])], 'r--')
    axs[2].plot([upper_limit,upper_limit],[0,np.max(np.histogram(data, bins=50)[0])], 'r--')
    axs[2].set_xlabel('Point Values')  
    axs[2].set_ylabel('Point Coutns')  

    plt.subplots_adjust(hspace=0.7)
    fig.suptitle('Results from IQR method (non-iterative)', fontsize=14)   

    return fig
