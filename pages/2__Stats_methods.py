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
data_dimensions = st.session_state['data_dimensions']
col2 = None

show_z_stats = st.sidebar.checkbox('Show z-stats')
show_iqr_stats = st.sidebar.checkbox('Show IQR stats')

if show_z_stats:

    if data_dimensions == 1:
        z_threshold = st.slider('Choose threshold for z-scores:', min_value=1., \
                                max_value = 10., step = 0.25, value = 3.)
        
        fig = get_z_score_anomaly_plots(data = np_data, z_threshold=z_threshold)
        st.pyplot(fig)
        
    elif data_dimensions == 2:
        col1, col2 =st.columns([0.5, 0.5])  
        
        with col1:
            st.write('Analyzing axes 0:')
            z_threshold_ax1 = st.slider('Choose threshold for z-scores for ax1:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)
            fig1 = get_z_score_anomaly_plots(data = np_data[0], z_threshold=z_threshold_ax1)
            st.pyplot(fig1)
        with col2:
            
            st.write('Analyzing axes 1:')
            z_threshold_ax2 = st.slider('Choose threshold for z-scores for ax2:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)
            fig2 = get_z_score_anomaly_plots(data = np_data[1], z_threshold=z_threshold_ax2)
            st.pyplot(fig2)

    
if show_iqr_stats:

    if data_dimensions == 1:
        fig = get_iqr_anomaly_plots(data = np_data)
        st.pyplot(fig)

    elif data_dimensions == 2:
        if col2 is None:
            col1, col2 =st.columns([0.5, 0.5])
            with col1:
                st.write('Analyzing axes 0:')
            with col2:
                st.write('Analyzing axes 1:')

        with col1:
            fig01 = get_iqr_anomaly_plots(data = np_data[0])
            st.pyplot(fig01)
        with col2:
            fig02 = get_iqr_anomaly_plots(data = np_data[1])
            st.pyplot(fig02)
