import os
import pandas as pd
import numpy as np
import sys
import pytest

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)

#grand_parent_directory = path.dirname(parent_directory)

sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.models.StatsMethods import get_z_score_iter_outliers_1d_mask, \
                                    get_z_score_outliers_1d_mask, \
                                    get_iqr_outliers_1d_mask
                                    
from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
                                              get_2d_distr_with_outliers 
                                              

one_dim_data = get_1d_distr_with_outliers()
two_dim_data = get_2d_distr_with_outliers()


def test_get_z_score_iter_outliers_1d_mask_returns_1dimensional_array():
    bool_array = get_z_score_iter_outliers_1d_mask(one_dim_data)
    dimen = bool_array.ndim
    assert dimen==1
       
def test_get_z_score_outliers_1d_mask_returns_1dimensional_array():
    bool_array = get_z_score_outliers_1d_mask(one_dim_data)
    dimen = bool_array.ndim
    assert dimen==1
    
def test_get_iqr_outliers_1d_mask_returns_1dimensional_array():
    bool_array = get_iqr_outliers_1d_mask(one_dim_data)
    dimen = bool_array.ndim
    assert dimen==1