import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from utils.config import CONTAMINATION

from utils.toolbox import describe_function


@describe_function("Isol. Forest")
# function description should agree with METHODS_DESCRIPTIONS in config.py
def get_isolation_forest_outliers_mask(data, contamination=CONTAMINATION, \
                                  random_state=42):
    
    if data.ndim == 1:
        data_ = data.reshape(len(data),1)
        
    else:
        data_ = data
    
    try:
        np.random.seed(42)
        clf = IsolationForest(contamination=CONTAMINATION)
        clf.fit(data_)
        predictions = clf.predict(data_)
        anomalies_bool = predictions<0
        return anomalies_bool

    except Exception as e:
        error_msg = 'Error when calculating outliers using isolation forest method.' 
        print(error_msg)
        raise e



