import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as stats

from typing import Tuple

import os
import sys

current_directory =  os.path.abspath(os.path.dirname(__file__))
src_directory = os.path.dirname(current_directory)
sys.path.insert(0, src_directory) 

from outlier_methods.outlier_detector_base import DetectorBase

from utils.config import ITERATION_MAX_NUM_ZSCORE

class ZScoreMethod(DetectorBase):
    
#                         
    def __init__(self, z_threshold=3, modified=False):
        self.z_threshold = z_threshold
        self.modified = modified
        self.name = 'z-score'

    def get_outlier_mask(self, data):
        return self.get_outlier_mask_after_multiple_iterations(data=data)
    
    
    def get_plot(self, data, bins = 50, outliers_mask = None, line_plot=True):
        return self.get_z_score_plots(data=data, outliers_mask = outliers_mask, \
            line_plot=line_plot)


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
        outlier_indexes = []
        iter_index = np.arange(len(iter_data)).reshape(len(iter_data),1)

        iter = 0
        iter_outliers_mask = self.get_1d_mask(data = iter_data)
        iteration_found_outliers = sum(iter_outliers_mask)>0
        outlier_indexes += iter_index[iter_outliers_mask].tolist()
        iter_index = iter_index[np.invert(iter_outliers_mask)]
        iter_data = iter_data[np.invert(iter_outliers_mask)]
        iter +=1
        while iter<ITERATION_MAX_NUM_ZSCORE and iteration_found_outliers:
            iter_outliers_mask = self.get_1d_mask(data = iter_data)
            iteration_found_outliers = sum(iter_outliers_mask)>0
            outlier_indexes += iter_index[iter_outliers_mask].tolist()
            iter_index = iter_index[np.invert(iter_outliers_mask)]
            iter_data = iter_data[np.invert(iter_outliers_mask)]
            iter +=1
            
        else:
            if iter == ITERATION_MAX_NUM_ZSCORE:
                print ('Reached maximum number of iterations for z-score method without converging')

            elif not iteration_found_outliers:
                print ('z-score iterative method converged')
            
            else:
                error_msg = f"Error while performing z-score iterations. Iterative z-score method did not converge, problem with iteration {iter}"
                print (error_msg)
                raise ValueError(error_msg)

        outliers_mask = np.array([False]*len(data))
        
        outliers_mask[outlier_indexes]=True
        return outliers_mask
           
    def get_z_score_plots(self, data, outliers_mask = None, bins = 50, line_plot=True):
        "data: np.array"
        fig, ax = plt.subplots(2,1)       
        index = np.arange(len(data)).reshape(len(data),1)
        if outliers_mask is None:
            outliers_mask = self.get_outlier_mask(data)    
        outlier_indexes = index[outliers_mask]
        outliers = data[outliers_mask]
        clean_data = data[np.invert(outliers_mask)] 

        if self.modified:
            from statsmodels import robust
            x_std = stats.median_abs_deviation(clean_data, scale=1)
            mean = np.median(clean_data)
            plot_threshold=self.z_threshold/stats.norm.ppf(.75)*x_std
        else:
            x_std = np.std(clean_data)
            mean = clean_data.mean()
            plot_threshold=self.z_threshold*x_std
        
        if line_plot:
            ax[0].plot(data)
        else:
            ax[0].scatter(x=index, y=data)
        ax[0].scatter(outlier_indexes,y=outliers, color = 'red')
        ax[0].axhline(mean+plot_threshold, color = 'red', lw=0.8, ls='--')
        ax[0].axhline(mean-plot_threshold, color = 'red', lw=0.8, ls='--')
        ax[0].axhline(mean, color = 'green', lw=0.8, ls='-')
        ax[0].set_xlabel('Point Number labels')
        ax[0].set_ylabel('Point Values')
        
        ax[1].hist(data, bins = bins)
        ax[1].axvline(mean+plot_threshold, color = 'red', lw=0.8, ls='--')
        ax[1].axvline(mean-plot_threshold, color = 'red', lw=0.8, ls='--')
        ax[1].axvline(mean, color = 'green', lw=0.8, ls='--')
        ax[1].set_ylabel('Point Counts')
        ax[1].set_xlabel('Point Values')
        
        plt.subplots_adjust(hspace=0.5)
        if not self.modified:
            fig.suptitle('Results from z-score method (iterative)', fontsize=14)   
        else:
            fig.suptitle('Results from modified z-score method (iterative)', fontsize=14)   
        return fig
    
    
    
class IQRMethod(DetectorBase):
    
    def get_outlier_mask(self, data: np.ndarray) -> np.ndarray:
        return self.get_iqr_outliers_1d_mask(data=data)
    
    def get_plot(self, data: np.ndarray, outliers_mask=None):
        return self.get_iqr_anomaly_plots(data=data, outliers_mask=outliers_mask)
    
    def get_iqr_outliers_1d_mask(self, data: np.ndarray) -> np.ndarray: 
        if data.ndim == 1:
            columns = 1
        elif data.ndim==2:
            _,columns = data.shape
        
        try:
            if columns==1:
                lower_limit, upper_limit = self.get_iqr_limits(data=data)
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

    def get_iqr_limits(self, data: np.ndarray) -> Tuple[np.float64, np.float64]:
        first_quar = np.percentile(data, 25)
        third_quar = np.percentile(data, 75)
        iqr = third_quar - first_quar
        lower_limit = first_quar - 1.5 * iqr
        upper_limit = third_quar + 1.5 * iqr 
        print (type(upper_limit))
        return lower_limit, upper_limit

    def get_iqr_anomaly_plots(self, data, outliers_mask=None, bins = 50, line_plot=True):

        import seaborn as sns
        
        lower_limit, upper_limit = self.get_iqr_limits(data=data)
        index = np.arange(len(data)).reshape(len(data),1)
        if outliers_mask is None:
            outliers_mask = self.get_outlier_mask(data)
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
        fig.suptitle('Results from IQR method', fontsize=14)   
        return fig
