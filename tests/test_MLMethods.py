# import os
# import pandas as pd
# import sys
# import pytest
# import numpy as np

# current_directory =  os.path.abspath(os.path.dirname(__file__))
# parent_directory = os.path.dirname(current_directory)

# sys.path.insert(0, parent_directory) # defined root folder 1 step up

# from src.models.MLMethods import get_isolation_forest_outliers_mask

# from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
#                                               get_2d_distr_with_outliers 
                                              
# one_dim_data = get_1d_distr_with_outliers()
# two_dim_data = get_2d_distr_with_outliers()

# @pytest.mark.parametrize("data", 
#                         (one_dim_data,two_dim_data)   
# )    
# def test_get_isolation_forest_outliers_mask_returns_1dimensional_array(data):
#     bool_array = get_isolation_forest_outliers_mask(data)
#     dimens = bool_array.ndim
#     assert dimens==1

def test_NEEDUPDATE():
    assert False