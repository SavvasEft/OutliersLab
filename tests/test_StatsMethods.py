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
                                    get_iqr_outliers_1d_mask, \
                                    get_euclidean_distance, \
                                    get_distance_z_score_mask
                                    
                                    
                                    
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
    
def test_get_euclidean_distance_calculates_correct_distance():
    array = np.array([[0,6,0],[4,0,0]])
    point = np.array([0,0,0])
    expected_distance = np.array([6.,4.])
    assert (np.array_equal(get_euclidean_distance(array, point), expected_distance))
    
def test_get_euclidean_distance_returns_correct_dimensions():
    array1 = np.array([[0,6,0],[4,0,0]])
    point1 = np.array([0,0,0])
    array2 = np.array([[0,6,3,4,5],[5,4,3,0,0],[5,4,3,2,0]])
    point2 = np.array([0,0,0,0,0])
    exp_shape1 = (2,)
    exp_shape2 = (3,)
    assert (get_euclidean_distance(array1,point1).shape==exp_shape1)
    assert (get_euclidean_distance(array2,point2).shape==exp_shape2)
    
def test_get_euclidean_z_score_mask_returns_correct_dimensions():
    array1 = np.array([[0,6,0],[4,2,0],[4,2,6],[4,2,5]])
    array2 = np.array([[0,6,3,4,5],[5,4,3,0,0],[5,4,3,2,0]])
    exp_shape1 = (4,)
    exp_shape2 = (3,)
    assert (get_distance_z_score_mask(array1, distance_function = get_euclidean_distance).shape==exp_shape1)
    assert (get_distance_z_score_mask(array2, distance_function = get_euclidean_distance).shape==exp_shape2)
