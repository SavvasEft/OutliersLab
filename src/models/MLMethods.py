import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


def get_isolation_forest_outliers(data, contamination=0.2, random_state=42):
    np.random.seed(42)
    clf = IsolationForest(contamination=0.2)
    clf.fit(data)
    predictions = clf.predict(data)
    anomalies_bool = predictions<0
    return anomalies_bool






