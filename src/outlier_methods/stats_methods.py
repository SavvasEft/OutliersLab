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

from utils.config import ITERATION_MAX_NUM_ZSCORE, Z_THRESHOLD

class ZScoreMethod(DetectorBase):
    
#                         
    def __init__(self, z_threshold=Z_THRESHOLD, modified=False):
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


class EuclideanDistZScoreMethod(DetectorBase):

    def __init__(self,z_threshold=Z_THRESHOLD, max_iter=ITERATION_MAX_NUM_ZSCORE):
        self.z_threshold = z_threshold
        self.max_iter = max_iter

    def get_outlier_mask(self, data: np.ndarray, z_threshold = None, \
                         max_iter = None) -> np.ndarray:
        if z_threshold is None:
            z_threshold = self.z_threshold
        if max_iter is None:
            max_iter = self.max_iter
        return self.get_outlier_mask_after_iterative_z_cutoffs(array=data, \
                                                               z_threshold = z_threshold, \
                                                               max_iter = max_iter)


    def get_plot(self, data: np.ndarray, outlier_mask=None, z_threshold=None,\
                                            bins = 50, line_plot=True):
        if z_threshold is None:
            z_threshold = self.z_threshold
        return  self.get_eucl_z_score_iter_outlier_plot(data=data, outlier_mask=outlier_mask, z_threshold=z_threshold,\
                                            bins = bins, line_plot=line_plot)
        
    def get_outlier_mask_after_iterative_z_cutoffs(self, array,z_threshold, max_iter):   
        iter=0
        clean_array = np.copy(array)
        survived_index = np.arange(len(clean_array))
        iterative_outlier_index = np.array([])
        final_outlier_mask = np.array([False]*len(clean_array))
        outliers_found=1
        while iter<=max_iter and outliers_found>0 and len(clean_array)>1:
            outlier_mask=self.get_outlier_mask_for_z_threshold(array=clean_array, z_threshold=z_threshold)
            clean_array=clean_array[np.invert(outlier_mask)]
            outlier_index = survived_index[outlier_mask]
            survived_index=survived_index[np.invert(outlier_mask)]       
            iterative_outlier_index = np.append(iterative_outlier_index, outlier_index)
            outliers_found = np.sum(outlier_mask)
            iter+=1
        for index in iterative_outlier_index:
            final_outlier_mask[int(index)]=True
        return final_outlier_mask
    
    def get_eucl_z_score_iter_outlier_plot(self, data: np.ndarray, outlier_mask=None, z_threshold=None,\
                                            bins = 50, line_plot=True):

        if z_threshold is None:
            z_threshold = self.z_threshold


        fig, ax = plt.subplots(2,1)       
        index = np.arange(len(data)).reshape(len(data),1)
        if outlier_mask is None:
            outlier_mask = self.get_outlier_mask(data=data, z_threshold = self.z_threshold, \
                                                 max_iter = self.max_iter)
        outlier_indexes = index[outlier_mask]
        outliers = data[outlier_mask]
        clean_data = data[np.invert(outlier_mask)] 

        x_std = np.std(clean_data)
        mean = np.mean(clean_data)

        euclidean_distances = self.get_euclidean_distance_from_mean(data)
        euclidean_mean_distance = np.mean(euclidean_distances)
        euclidean_distances_outliers = euclidean_distances[outlier_mask]
        euclidean_clean_distances = euclidean_distances[np.invert(outlier_mask)] 
        eucl_dist_std = np.std(euclidean_clean_distances)

        if line_plot:
            ax[0].plot(euclidean_distances)
        else:
            ax[0].scatter(x=index, y=euclidean_distances)

        ax[0].scatter(outlier_indexes,y=euclidean_distances_outliers, color = 'red')
        ax[0].axhline(euclidean_mean_distance+z_threshold*eucl_dist_std, color = 'red', lw=0.8, ls='--')
        #if mean - threshold is positive, show line 
        if euclidean_mean_distance-z_threshold*eucl_dist_std>0:
            ax[0].axhline(euclidean_mean_distance-z_threshold*eucl_dist_std, color = 'red', lw=0.8, ls='--')
        ax[0].axhline(euclidean_mean_distance, color = 'green', lw=0.8, ls='-')
        ax[0].set_xlabel('Point Number labels')
        ax[0].set_ylabel('Euclidean Distance from mean')
        
        
        ax[1].hist(euclidean_distances, bins = bins)
        ax[1].axvline(euclidean_mean_distance+z_threshold*eucl_dist_std, color = 'red', lw=0.8, ls='--')
        #if mean - threshold is positive, show line 
        if euclidean_mean_distance-z_threshold*eucl_dist_std>0:
            ax[1].axvline(euclidean_mean_distance-z_threshold*eucl_dist_std, color = 'red', lw=0.8, ls='--')

        ax[1].axvline(euclidean_mean_distance, color = 'green', lw=0.8, ls='--')
        ax[1].set_ylabel('Point Counts')
        ax[1].set_xlabel('Euclidean distance')
        
        plt.subplots_adjust(hspace=0.5)
        fig.suptitle('Results from z-score method on Euclidean distance from mean (iterative)', fontsize=14)   
        return fig

    def get_outlier_mask_for_z_threshold(self, array, z_threshold):
        euclid_dist=self.get_euclidean_distance_from_mean(array)
        sigma_array= self.transform_array_to_z_score(euclid_dist)
        return np.abs(sigma_array)>z_threshold

    def get_euclidean_distance_from_mean(self,array):
        mean_point = np.mean(array,axis=0)
        mean_norm = array - mean_point
        dif_sq = mean_norm**2
        if len(array.shape)==1:
            eucl_dist = np.sqrt(dif_sq)       
        elif len(array.shape) == 2:
            dim_sq_sum = np.sum(dif_sq,axis=-1)
            eucl_dist = np.sqrt(dim_sq_sum)
        return eucl_dist
    
    def transform_array_to_z_score(self,array):
        #make sure aray is 1d:
        if len(array.shape)!=1:
            raise ValueError("array should be 1d")
        else:  
            mean_value = np.mean(array, axis=0)
            stdev = np.std(array)
            z_score_array = (array-mean_value)/stdev
        return z_score_array


    
