import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def get_z_score_outliers_1d(data, z_threshold=2):
    "data: np.array"
    #for 1d data
    mean = np.mean(data)
    std =  np.std(data)
    z_score = (data - mean) / std
    anomalies_bool = np.abs(z_score) > z_threshold
    return anomalies_bool

def get_z_score_iter_outliers_1d(data,z_threshold=2):
    outlier_indexes = []
    iter_data = np.array(data, copy=True)
    iter_index = np.arange(len(data))
    len_outlier_indexes = 5
    iter = 0
    while iter<10 and len_outlier_indexes>0:
        iter_outliers_bool = get_z_score_outliers_1d(iter_data, z_threshold=z_threshold)
        iter_outlier_index = iter_index[iter_outliers_bool]
        len_outlier_indexes = len(iter_outlier_index)
        outlier_indexes.append(iter_outlier_index)
        iter_data = iter_data[np.invert(iter_outliers_bool)]
        iter_index = iter_index[np.invert(iter_outliers_bool)]
        iter +=1

    outlier_indexes = np.concatenate(outlier_indexes)       
    outlier_bool = np.array([False]*len(data))
    outlier_bool[outlier_indexes]=True
    return outlier_bool

def get_z_score_iter_outlier_plots(data, z_threshold=2, bins = 50, line_plot=False):
    "data: np.array"
    #bins = int(len(data)/4)
    fig, ax = plt.subplots(2,1)       
    index = np.arange(len(data))
    outlier_bool = get_z_score_iter_outliers_1d(data, z_threshold=z_threshold)
    outlier_indexes = index[outlier_bool]
    outliers = data[outlier_bool]
    clean_data = data[np.invert(outlier_bool)] 
    mean = clean_data.mean()
    x_std = np.std(clean_data)

    if line_plot:
        ax[0].plot(data)
    else:
        ax[0].scatter(x=index, y=data)
    ax[0].scatter(outlier_indexes,y=outliers, color = 'red')
    # ax1.axhline(mean+min_outlier_distance, color = 'red', lw=0.8, ls='--')
    # ax1.axhline(mean-min_outlier_distance, color = 'red', lw=0.8, ls='--')
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
    fig.suptitle('Results from z-score method (iterative)', fontsize=14)   
    return fig

def get_iqr_limits(data):
    first_quar = np.percentile(data, 25)
    third_quar = np.percentile(data, 75)
    iqr = third_quar - first_quar   
    lower_limit = first_quar - 1.5 * iqr
    upper_limit = third_quar + 1.5 * iqr 
    return lower_limit, upper_limit

def get_iqr_outliers_1d(data):
    lower_limit, upper_limit = get_iqr_limits(data)
    outlier_bool = (data < lower_limit) | (data > upper_limit)
    return outlier_bool

def get_iqr_anomaly_plots(data, bins = 50, line_plot=False):
    lower_limit, upper_limit = get_iqr_limits(data)
    index = np.arange(len(data))
    outliers_bool = get_iqr_outliers_1d(data)
    outliers_index = index[outliers_bool]
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
