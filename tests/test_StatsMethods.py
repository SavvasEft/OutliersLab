import os
import pandas as pd
import sys
import pytest

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)

#grand_parent_directory = path.dirname(parent_directory)

sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.models.StatsMethods import get_z_score_iter_outliers_1d, \
                                    get_z_score_outliers_1d, \
                                    get_iqr_outliers_1d
                                    
from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
                                              get_2d_distr_with_outliers 
                                              

one_dim_data = get_1d_distr_with_outliers()
two_dim_data = get_2d_distr_with_outliers()


def test_get_z_score_iter_outliers_1d_produces_column_array():
    expected_columns_no = 1
    bool_array = get_z_score_iter_outliers_1d(one_dim_data)
    shape = bool_array.shape
    _, columns_no = shape
    assert columns_no==expected_columns_no
       
def test_get_z_score_outliers_1d_produces_column_array():
    expected_columns_no = 1
    bool_array = get_z_score_outliers_1d(one_dim_data)
    shape = bool_array.shape
    _, columns_no = shape
    assert columns_no==expected_columns_no

def test_get_iqr_outliers_1d_produces_column_array():
    expected_columns_no = 1
    bool_array = get_iqr_outliers_1d(one_dim_data)
    shape = bool_array.shape
    _, columns_no = shape
    assert columns_no==expected_columns_no