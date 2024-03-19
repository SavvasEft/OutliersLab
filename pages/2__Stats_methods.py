import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import os
import sys

st.set_page_config(layout="wide")

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

print ('here we go')

from src.models.StatsMethods import get_z_score_iter_outlier_plots, \
                                    get_iqr_anomaly_plots, \
                                    get_z_score_iter_outliers_1d, \
                                    get_iqr_outliers_1d
                                    
from src.utils.toolbox import get_initial_1d_graphs, \
                              get_2d_distrib_plots, \
                              combine_outlier_booleans


np_data = st.session_state['np_data']
data_dimensions = st.session_state['data_dimensions']
col2 = None

show_z_stats = st.sidebar.checkbox('Show z-stats')
show_iqr_stats = st.sidebar.checkbox('Show IQR stats')
show_line_plot = None

if data_dimensions == 2:
    col1, col2, col3 =st.columns([0.33, 0.33, 1-0.66])  

if show_z_stats:
    median_instead_of_mean = st.sidebar.toggle('Choose median for z-stats')
    if data_dimensions == 1:
        if show_line_plot is None:
            show_line_plot = st.sidebar.toggle('Show line plot')            

        
        
        z_threshold_ax0 = st.slider('Choose threshold for z-scores:', min_value=1., \
                                max_value = 10., step = 0.25, value = 3.)
        fig = get_z_score_iter_outlier_plots(data = np_data, z_threshold=z_threshold_ax0, \
                                             line_plot=show_line_plot, modified=median_instead_of_mean)
        st.pyplot(fig)
        

    elif data_dimensions == 2:       
        with col1:
            if show_line_plot is None:
                show_line_plot = st.sidebar.toggle('Show line plot')
            st.write('Analyzing axes 0:')
            z_threshold_ax0 = st.slider('Choose threshold for z-scores for ax0:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)
            fig1 = get_z_score_iter_outlier_plots(data = np_data[0], z_threshold=z_threshold_ax0, \
                                                  line_plot=show_line_plot, modified=median_instead_of_mean)
            st.pyplot(fig1)
        with col2:
            
            st.write('Analyzing axes 1:')
            z_threshold_ax1 = st.slider('Choose threshold for z-scores for ax1:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)
            fig2 = get_z_score_iter_outlier_plots(data = np_data[1], z_threshold=z_threshold_ax1, \
                                                  line_plot=show_line_plot, modified=median_instead_of_mean)
            st.pyplot(fig2)

    
if show_iqr_stats:

    if data_dimensions == 1:
        if show_line_plot is None:
            show_line_plot = st.sidebar.toggle('Show line plot')
        fig = get_iqr_anomaly_plots(data = np_data, line_plot=show_line_plot)
        st.pyplot(fig)

    elif data_dimensions == 2:
        if show_line_plot is None:
            show_line_plot = st.sidebar.toggle('Show line plot')

        if col2 is None:

            with col1:
                st.write('Analyzing axes 0:')
            with col2:
                st.write('Analyzing axes 1:')
            with col3:
                st.write('Combining the two axes:')

        with col1:
            fig01 = get_iqr_anomaly_plots(data = np_data[0], line_plot=show_line_plot)
            st.pyplot(fig01)
        with col2:
            fig02 = get_iqr_anomaly_plots(data = np_data[1], line_plot=show_line_plot)
            st.pyplot(fig02)

if data_dimensions == 2:
    
    with col3:
        st.write('Combine outliers from the two axes')
        outlier_bool_to_combine = []
        if show_z_stats:
            add_ax0_zscore = st.toggle('Add axes 0 z-score outliers')
            add_ax1_zscore = st.toggle('Add axes 1 z-score outliers')

            if add_ax0_zscore:
                data_ax = np_data[0]
                outlier_bool_ax0_zscore = get_z_score_iter_outliers_1d(data=data_ax,z_threshold=z_threshold_ax0)                   
                outlier_bool_to_combine.append(outlier_bool_ax0_zscore)
            if add_ax1_zscore:
                data_ax = np_data[1]
                outlier_bool_ax0_zscore = get_z_score_iter_outliers_1d(data=data_ax,z_threshold=z_threshold_ax1)                   
                outlier_bool_to_combine.append(outlier_bool_ax0_zscore)

        if show_iqr_stats:
            add_ax0_iqr = st.toggle('Add axes 0 iqr outliers')
            add_ax1_iqr = st.toggle('Add axes 1 iqr outliers')


            if add_ax0_iqr:
                data_ax = np_data[0]
                outlier_bool_ax0_zscore = get_iqr_outliers_1d(data=data_ax)                   
                outlier_bool_to_combine.append(outlier_bool_ax0_zscore)
            if add_ax1_iqr:
                data_ax = np_data[1]
                outlier_bool_ax0_zscore = get_iqr_outliers_1d(data=data_ax)                   
                outlier_bool_to_combine.append(outlier_bool_ax0_zscore)

 
                
                

            
            
            outlier_bool_combined=None
            

            if len(outlier_bool_to_combine) > 0:
                outlier_bool_combined = combine_outlier_booleans(outlier_bool_to_combine[0])
                for one_outlier_bool in outlier_bool_to_combine:

                    outlier_bool_combined = combine_outlier_booleans(one_outlier_bool, outlier_bool_combined)

            fig03 = get_2d_distrib_plots(x=np_data[0], y=np_data[1], x_label='0 axes' , y_label='1 axes', outlier_bool=outlier_bool_combined)
            st.pyplot(fig03)

        
