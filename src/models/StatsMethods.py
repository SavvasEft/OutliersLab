import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns






def z_score_anomaly_indexes(data, z_threshold=2):
    "data: np.array"
    #for 1d data
    mean = np.mean(data)
    std =  np.std(data)
    z_score = (data - mean) / std
    anomalies_boll = np.abs(z_score) > z_threshold
    anomaly_indexes = np.where(anomalies_boll)
    return anomaly_indexes
    
def get_z_score_anomaly_plots(data, z_threshold=2, bins = 50):
    "data: np.array"
    #bins = int(len(data)/4)
    fig, [ax1, ax2] = plt.subplots(2,1)
    x_mean = data.mean()
    x_std = np.std(data)
    x_z1 = x_mean - z_threshold * x_std 
    x_z2 = x_mean + z_threshold * x_std 

    anomaly_indexes = z_score_anomaly_indexes(data, z_threshold=z_threshold)
    ax2.hist(data, bins = bins)
    ax2.axvline(x_z1, color = 'red', lw=0.8, ls='--')
    ax2.axvline(x_z2, color = 'red', lw=0.8, ls='--')
    ax1.plot(data)
    ax1.scatter(anomaly_indexes,y=[data[i] for i in anomaly_indexes], color = 'red')
    return fig



def get_iqr_limits(data):
    first_quar = np.percentile(data, 25)
    third_quar = np.percentile(data, 75)
    iqr = third_quar - first_quar   
    lower_limit = first_quar - 1.5 * iqr
    upper_limit = third_quar + 1.5 * iqr 
    return lower_limit, upper_limit

def iqr_anomaly_indexes(data):
    # Find IQR
    lower_limit, upper_limit = get_iqr_limits(data)
    outliers_index = np.where((data < lower_limit) | (data > upper_limit))[0]
    return outliers_index
    
def get_iqr_anomaly_plots(data, bins = 50):
    lower_limit, upper_limit = get_iqr_limits(data)
    outliers_index = iqr_anomaly_indexes(data)
    outliers = data[outliers_index]
    
    fig, axs = plt.subplots(3,1)   
    axs[0].plot(data)
    axs[0].scatter(outliers_index, outliers, color ='red')

    #sns.boxplot draws whiskers to the farthest datapoint within upper & lower limits 
    sns.boxplot(data=data, orient = 'h', ax=axs[1])
    # axs[1].plot([upper_limit,upper_limit],[-0.5,0.5], 'r--')
    # axs[1].plot([lower_limit,lower_limit],[-0.5,0.5], 'r--')

    axs[2].hist(data, bins=bins)
    axs[2].plot([lower_limit,lower_limit],[0,np.max(np.histogram(data, bins=50)[0])], 'r--')
    axs[2].plot([upper_limit,upper_limit],[0,np.max(np.histogram(data, bins=50)[0])], 'r--')

    return fig