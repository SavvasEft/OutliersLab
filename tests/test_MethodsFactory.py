import os
import pandas as pd
import sys
import pytest
import numpy as np

current_directory =  os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.dirname(current_directory)

sys.path.insert(0, main_directory) # defined root folder 1 step up
                                             
                                             
from src.outlier_methods.methods_factory import MethodsFactory

def test_combine_outlier_masks_returns_outliers_in_correct_position():
    mask1 = np.array([False]*15)
    mask2 = np.array([False]*15)

    mask1[[2,3,4]] = True
    mask2[[4,5,6]] = True

    mask_list = [mask1, mask2]

    combined_mask = MethodsFactory.combine_outlier_masks(mask_list)
    expected_mask = np.array([False]*15)
    expected_mask[[2,3,4,5,6]]=True
    assert np.array_equal(combined_mask, expected_mask)

def test_combine_outlier_masks_returns_mask_of_correct_dimensions():
    mask1 = np.array([False]*15)
    mask2 = np.array([False]*15)

    mask1[[2,3,4]] = True
    mask2[[4,5,6]] = True

    mask_list = [mask1, mask2]
    combined_mask = MethodsFactory.combine_outlier_masks(mask_list)
    combined_mask_shape  = combined_mask.shape
    expected_mask_shape  = (15,)
    assert combined_mask_shape==expected_mask_shape 