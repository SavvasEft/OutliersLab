import pandas as pd
import numpy as np
import matplotlib.pyplot as plt







def z_score_anomaly_indexes(data, z_threshold=2):
    "data: np.array"
    #for 1d data
    mean = np.mean(data)
    std =  np.std(data)
    z_score = (data - mean) / std
    anomalies_boll = np.abs(z_score) > z_threshold
    anomaly_indexes = np.where(anomalies_boll)
    return anomaly_indexes
    
def get_z_stat_anomaly_plots(data, z_threshold=2):
    "data: np.array"
    fig, [ax1, ax2] = plt.subplots(2,1)
    x_mean = data.mean()
    x_std = np.std(data)
    x_z1 = x_mean - z_threshold * x_std 
    x_z2 = x_mean + z_threshold * x_std 

    anomaly_indexes = z_score_anomaly_indexes(data, z_threshold=z_threshold)
    ax2.hist(data, int(len(data)/4))
    ax2.axvline(x_z1, color = 'red', lw=0.8, ls='--')
    ax2.axvline(x_z2, color = 'red', lw=0.8, ls='--')
    ax1.plot(data)
    ax1.scatter(anomaly_indexes,y=[data[i] for i in anomaly_indexes], color = 'red')
    return fig