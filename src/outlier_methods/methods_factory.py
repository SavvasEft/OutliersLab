import os
import sys
import numpy as np

current_directory =  os.getcwd()
src_directory = os.path.join(os.path.dirname(current_directory), 'src')
sys.path.insert(0, src_directory)  

from outlier_methods.stats_methods import ZScoreMethod, IQRMethod

from outlier_methods.ml_methods import IsolationForestMethod, LocalOutlierFactorMethod

class MethodsFactory:
    methods = {
        "z_score": ZScoreMethod,
        "iqr": IQRMethod, 
        "isolation forest": IsolationForestMethod,
        "local outlier factor": LocalOutlierFactorMethod,
        # other methods...
    }

    @staticmethod
    def apply_method(method_name, *args, **kwargs):
        method_class = MethodsFactory.methods.get(method_name)
        if not method_class:
            raise ValueError(f"No method found for {method_name}")
        return method_class(*args, **kwargs)
    
    @staticmethod
    def combine_outlier_masks(masks_list):
        combined_outlier_mask = np.array([False]*len(masks_list[0]))
        for mask in masks_list:
            combined_outlier_mask[mask]=True
        return combined_outlier_mask