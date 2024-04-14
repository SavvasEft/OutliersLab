import os
import sys

current_directory =  os.getcwd()
src_directory = os.path.join(os.path.dirname(current_directory), 'src')
sys.path.insert(0, src_directory)  

from outlier_methods.stats_methods import ZScoreMethod




class MethodsFactory:
    methods = {
        "z_score": ZScoreMethod,
        # other methods...
    }

    @staticmethod
    def apply_method(method_name, *args, **kwargs):
        method_class = OutlierDetectionFactory.methods.get(method_name)
        if not method_class:
            raise ValueError(f"No method found for {method_name}")
        return method_class(*args, **kwargs)