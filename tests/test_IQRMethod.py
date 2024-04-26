import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys

current_directory =  os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)

sys.path.insert(0, parent_directory) # defined root folder 1 step 


from src.outlier_methods.stats_methods import IQRMethod

def test_get_iqr_limits_values_are_expected_values():
    state42 = np.random.RandomState(42)
    data = state42.standard_normal(size=500)
    iqr_object = IQRMethod()
    t1, t2 = iqr_object.get_iqr_limits(data=data)
    assert(t1==-2.7059433923616356)
    assert(t2==2.6424192420326538)

def test_get_iqr_outliers_1d_mask_is_expected_one():
    state42 = np.random.RandomState(42)
    data = state42.standard_normal(size=500)
    iqr_object = IQRMethod()
    mask = iqr_object.get_outlier_mask(data=data)
    true_positions = [179, 209, 262, 478]
    for position in true_positions:
        assert(mask[position]) 
    
