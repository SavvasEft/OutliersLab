import os
import pandas as pd
import sys
import pytest

current_directory =  os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
modules_folder = os.path.join(parent_directory, 'modules_folderA') 

#grand_parent_directory = path.dirname(parent_directory)

# print (parent_directory)

sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
                                              get_2d_distr_with_outliers


def test_column_data_for_get_1d_distr_with_outliers():
    expected_columns_no = 1
    one_dim_data = get_1d_distr_with_outliers()
    shape1d = one_dim_data.shape
    _, columns_no = shape1d
    assert columns_no==expected_columns_no
    
def test_column_data_for_get_2d_distr_with_outliers():
    expected_columns_no = 2
    one_dim_data = get_2d_distr_with_outliers()
    shape2d = one_dim_data.shape
    _, columns_no = shape2d
    assert columns_no==expected_columns_no