

# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import scipy.stats as stats


from functools import lru_cache

import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
src_directory = os.path.dirname(current_directory)
sys.path.insert(0, src_directory) 

from outlier_methods.outlier_detector_base import DetectorBase

#from utils.config import ITERATION_MAX_NUM_ZSCORE #, \
#                         #METHODS_DESCRIPTIONS

ITERATION_MAX_NUM_ZSCORE=5

class ZScoreMethod:
    
    def __init__(self, z_threshold, modified=False):
        self.z_threshold = z_threshold
        self.modified = modified
        self.name = 'z-score'
        
    def get_1d_mask(self, data:np.ndarray):

        if data.ndim == 1:
            columns = 1
        elif data.ndim==2:
            _,columns = data.shape
    
        try:
            if columns == 1:
                if self.modified:
                    median=np.median(data)
                    MAD = stats.median_abs_deviation(data, scale=1)
                    z_score = stats.norm.ppf(.75)*(data-median) / MAD
                    
                else:
                    mean = np.mean(data)
                    std =  np.std(data)
                    z_score = (data - mean) / std
            
                anomalies_mask = np.abs(z_score) > self.z_threshold
                anomalies_mask = np.squeeze(anomalies_mask)
                return anomalies_mask
            
            else:
                error_msg = "Data dimensions error. Z-score calculation for 1d can take arrays of shape (R,1) or (R,)"
                print (error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            print('Error when calculating outliers using get_1d_mask.')
            raise e


    def get_outlier_mask_after_multiple_iterations(self, data):
        iter_data = np.array(data, copy=True)
        iter = 0
        outliers_bool = self.get_1d_mask(data = iter_data)
        iteration_found_outliers = sum(outliers_bool)>0
        while iter<ITERATION_MAX_NUM_ZSCORE and iteration_found_outliers:
            iter_outliers_bool = self.get_1d_mask(data = iter_data)
            outliers_bool[iter_outliers_bool]=True
            iteration_found_outliers = sum(iter_outliers_bool)>0
            iter +=1
        return outliers_bool
    
    #@lru_cache(maxsize=128)
    def get_outlier_mask(self, data, z_threshold = None):
        if z_threshold is None:
            z_threshold = self.z_threshold
        return self.get_outlier_mask_after_multiple_iterations(data=data)
        
    
    def get_z_score_iter_outlier_plots(self, data, z_threshold=2, bins = 50, line_plot=False):
        "data: np.array"
        fig, ax = plt.subplots(2,1)       
        index = np.arange(len(data)).reshape(len(data),1)
        outlier_mask = self.get_outlier_mask(data)
        
        outlier_indexes = index[outlier_mask]
        outliers = data[outlier_mask]
        clean_data = data[np.invert(outlier_mask)] 

        if not self.modified:
            x_std = np.std(clean_data)
            mean = clean_data.mean()
            print (mean)
            print (f'{x_std=}') 
            print (clean_data.max())
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
        if not self.modified:
            fig.suptitle('Results from z-score method (iterative)', fontsize=14)   
        else:
            fig.suptitle('Results from modified z-score method (iterative)', fontsize=14)   
        return fig