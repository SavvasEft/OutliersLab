import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import os
import sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

print ('here we go')

from src.models.StatsMethods import get_z_score_anomaly_plots, \
                                    get_iqr_anomaly_plots

np_data = st.session_state['np_data']

show_z_stats = st.sidebar.checkbox('Show z-stats')

show_iqr_stats = st.sidebar.checkbox('Show IQR stats')

if show_z_stats:
    z_threshold = st.slider('Choose threshold for z-scores:', min_value=1., \
                            max_value = 10., step = 0.25, value = 3.)
    fig = get_z_score_anomaly_plots(data = np_data, z_threshold=z_threshold)
    st.pyplot(fig)
    
if show_iqr_stats:
    fig = get_iqr_anomaly_plots(data = np_data)
    st.pyplot(fig)