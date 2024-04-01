import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from utils.config import CONTAMINATION, N_NEIGHBORS

from utils.toolbox import describe_function


@describe_function("Isol. Forest")
# function description should agree with METHODS_DESCRIPTIONS in config.py
def get_isolation_forest_outliers_mask(data, contamination=None, \
                                  random_state=42):
    if contamination is None:
        contamination = CONTAMINATION
    
    if data.ndim == 1:
        data_ = data.reshape(len(data),1)
        
    else:
        data_ = data
    
    try:
        np.random.seed(42)
        clf = IsolationForest(contamination=contamination)
        clf.fit(data_)
        predictions = clf.predict(data_)
        anomalies_bool = predictions<0
        return anomalies_bool

    except Exception as e:
        error_msg = 'Error when calculating outliers using isolation forest method.' 
        print(error_msg)
        raise e

@describe_function("Local Outlier Factor")
def get_lof_outlier_mask(data, n_neighbors=N_NEIGHBORS, contamination=CONTAMINATION):
    clf = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    predictions = clf.fit_predict(data)
    anomalies_bool = predictions<0
    return anomalies_bool

