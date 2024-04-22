# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import scipy.stats as stats

import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from typing import Tuple

import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
src_directory = os.path.dirname(current_directory)
sys.path.insert(0, src_directory) 

from outlier_methods.outlier_detector_base import DetectorBase

from utils.config import CONTAMINATION, N_NEIGHBORS

from utils.toolbox import get_plot_with_1d_or_2d_data_with_mask

class IsolationForestMethod(DetectorBase):

    def __init__(self,contamination=CONTAMINATION):
        self.contamination=contamination
    
       
    def get_outlier_mask(self, data):
        try:
            if data.ndim == 1:
                data_ = data.reshape(len(data),1)
                
            else:
                data_ = data

            np.random.seed(42)
            clf = IsolationForest(contamination=self.contamination)
            clf.fit(data_)
            predictions = clf.predict(data_)
            outliers_mask = predictions<0
            return outliers_mask

        except Exception as e:
            error_msg = 'Error when calculating outliers using isolation forest method.' 
            print(error_msg)
            raise e
        
    # def get_plot(self, data, outliers_mask=None, show_line_plot=True):
        
    #     if outliers_mask is None:
    #         outliers_mask=self.get_outlier_mask(data=data)

    #     data_dimensions = data.shape[1]
        
    #     graph_title = 'Results from Isolation Forest'
    #     if data_dimensions == 1:    
    #         isol_plot = draw_line_or_point_plot_1d(data = data, outlier_bool = outliers_mask, \
    #                                                line_plot = show_line_plot,  \
    #                                                title = graph_title)
    
    #     elif data_dimensions == 2:
    #         isol_plot = draw_scatter_plot_2d(data = data, outlier_bool = outliers_mask, title = graph_title )

    #     else:
    #         raise ValueError('Dimensions of data passed in graphs should be 1 or 2.')

    #     return isol_plot
    
    def get_plot(self, data, outliers_mask=None, line_plot=True):
        """data should be 1d or 2d. If data comes from a dimensionality reduction method, 
        then an outliers_mask should also be passed, otherwise the method will be applied
        in the dimension-reduced data
        """      
        if outliers_mask is None:
            outliers_mask = self.get_outlier_mask(data=data)
        title = 'Results from Isolation Forest'
        plot = get_plot_with_1d_or_2d_data_with_mask(data, outliers_mask, title = title, line_plot=line_plot)
        return plot


class LocalOutlierFactorMethod(DetectorBase):
    
    def __init__(self, n_neighbors=N_NEIGHBORS, contamination=CONTAMINATION):
        self.n_neighbors = n_neighbors
        self.contamination = contamination
    
    def get_outlier_mask(self, data):
        clf = LocalOutlierFactor(n_neighbors=self.n_neighbors, contamination=self.contamination)
        predictions = clf.fit_predict(data)
        outliers_mask = predictions<0
        return outliers_mask
    
    def get_plot(self, data, outliers_mask=None, line_plot=True):
        """data should be 1d or 2d. If data comes from a dimensionality reduction method, 
        then an outliers_mask should also be passed, otherwise the method will be applied
        in the dimension-reduced data
        """
        if outliers_mask is None:
            outliers_mask = self.get_outlier_mask(data=data)
        title = 'Results from Local Outlier Factor'
        plot = get_plot_with_1d_or_2d_data_with_mask(data=data, outliers_mask=outliers_mask, \
                                                     title = title, line_plot=line_plot)
        return plot