print ('-'*55)
print ('Methods page Starting!!!')
print ('-'*18)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

import os
import sys

st.set_page_config(layout="wide")

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.models.StatsMethods import get_z_score_iter_outlier_plots, \
                                    get_iqr_anomaly_plots, \
                                    get_z_score_iter_outliers_1d_mask, \
                                    get_iqr_outliers_1d_mask

from src.models.MLMethods import get_isolation_forest_outliers_mask
                                    
from src.utils.toolbox import get_initial_1d_graphs, \
                              get_2d_distrib_plots, \
                              combine_outlier_booleans, \
                              draw_scatter_plot_2d, \
                              draw_line_or_point_plot_1d,\
                              get_outliers_report_and_global_outliers_mask
                              
                              
from src.utils.ReportGenerator import prepare_outlier_report_df, \
                                      export_df_to_excel_file, \
                                      export_dfs_to_excel_sheets

from src.utils.config import CONTAMINATION, \
                             METHODS_DESCRIPTIONS, \
                             SUMMARY_OUTPUT_XLSX_FNAME
 

np_data = st.session_state['np_data']
data_dimensions = st.session_state['data_dimensions']
col2 = None

show_z_stats = st.sidebar.checkbox('z-statistics')
show_iqr_stats = st.sidebar.checkbox('IQR method')
show_isolation_forest = st.sidebar.checkbox('Isolation Forest')

show_line_plot = None  #(remove this, show only line plot)

col1, col2 =st.columns([0.6, 0.4])  
with col1:
    st.write('Method details:')
with col2:
    st.write('Final Results:')

show_line_plot = True

methods_list = []

df_list_for_output = []
sheets_name_list_for_output = []

generate_final_report = False
# methods_list = [get_z_score_outliers_1d_mask, \
#                 get_z_score_iter_outliers_1d_mask, \
#                 get_iqr_outliers_1d_mask, \
#                 get_isolation_forest_outliers_mask
#                 ]

if show_z_stats:
    with col1: 
        st.write('-'*16)
        st.header('z-statistics:')
        
        #un-comment when more than 1 dimensions are valid for z-stats, and after delete if elsewhere
        #median_instead_of_mean = st.toggle('Choose median for z-stats')

        if data_dimensions == 1:
            median_instead_of_mean = st.toggle('Choose median for z-stats')
            z_threshold_ax0 = st.slider('Choose threshold for z-scores:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)
            fig = get_z_score_iter_outlier_plots(data = np_data, z_threshold=z_threshold_ax0, \
                                                line_plot=show_line_plot, modified=median_instead_of_mean)
            st.pyplot(fig)

            methods_list.append(get_z_score_iter_outliers_1d_mask)      
            generate_final_report = True
            



        elif data_dimensions != 1:       
            st.write('Currently z-score is only applicable for 1d data. Chosen data have more dimensions')
            # with col1:

            #     z_threshold_ax0 = st.slider('Choose threshold for z-scores for ax0:', min_value=1., \
            #                             max_value = 10., step = 0.25, value = 3.)
            #     fig1 = get_z_score_iter_outlier_plots(data = np_data[:,0], z_threshold=z_threshold_ax0, \
            #                                         line_plot=show_line_plot, modified=median_instead_of_mean)
            #     st.pyplot(fig1)
            

            #     z_threshold_ax1 = st.slider('Choose threshold for z-scores for ax1:', min_value=1., \
            #                             max_value = 10., step = 0.25, value = 3.)
            #     fig2 = get_z_score_iter_outlier_plots(data = np_data[:,1], z_threshold=z_threshold_ax1, \
            #                                         line_plot=show_line_plot, modified=median_instead_of_mean)
            #     st.pyplot(fig2)

        st.write('-'*16)
        
        
if show_iqr_stats:
    with col1:
        st.write('-'*16)
        st.header('IQR:')

    

        if data_dimensions == 1:
            fig = get_iqr_anomaly_plots(data = np_data, line_plot=show_line_plot)
            st.pyplot(fig)

            methods_list.append(get_iqr_outliers_1d_mask)
            generate_final_report = True
            

        else:
           st.write('Currently z-score is only applicable for 1d data. Chosen data have more dimensions')
        # elif data_dimensions == 2:
        #     with col1:
        #         fig01 = get_iqr_anomaly_plots(data = np_data[:,0], line_plot=show_line_plot)
        #         st.pyplot(fig01)
        #     with col2:
        #         fig02 = get_iqr_anomaly_plots(data = np_data[:,1], line_plot=show_line_plot)
        #         st.pyplot(fig02)

        st.write('-'*16)
        






if show_isolation_forest:


    with col1:

        st.write('-'*16)
        st.header('Isolation Forest:')

        # contamination = st.slider('Choose threshold for z-scores:', min_value=0.01, \
        #                             max_value = 0.5, step = 0.02, value = 0.1)
        contamination = CONTAMINATION
        
        data = np_data
        outlier_bool_isolation_forest = get_isolation_forest_outliers_mask(data = np_data, \
                                                                      contamination=contamination)
        if data_dimensions == 1:
            fig_forest_isol = draw_line_or_point_plot_1d(data = np_data, outlier_bool = outlier_bool_isolation_forest, \
                                                            line_plot = show_line_plot)

        elif data_dimensions == 2:
            fig_forest_isol = draw_scatter_plot_2d(data = np_data, outlier_bool = outlier_bool_isolation_forest)

        st.pyplot(fig_forest_isol)
            
        methods_list.append(get_isolation_forest_outliers_mask)  
        generate_final_report = True

        st.write('-'*16)


if generate_final_report:
    with col2:
        
        outlier_report_array, global_outlier_mask = get_outliers_report_and_global_outliers_mask(np_data, methods_list)

        outlier_report = prepare_outlier_report_df(outlier_report_array=outlier_report_array, methods_list=methods_list)
 
        st.write('-'*16)
        st.write('-'*16)
        st.header('Outlier Final Report')
        st.write(outlier_report)    

        save_outlier_report = st.toggle(f'Save as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')
        if save_outlier_report:
            df_list_for_output.append(outlier_report)
            sheets_name_list_for_output.append('Outlier_report')
            st.write('problem with saving pandas')
            
        st.write('**Point index**: Number of row in data that was identified as an outlier by at least one of the chosen methods.')

        st.write('**Outlier Score**: Number of methods that identified the specific data point as outlier')

        for method in methods_list:
            if method.description not in METHODS_DESCRIPTIONS:
                raise NameError('ERROR!!! Method names should agree in: 1. When defining the function, 2. On streamlit page that shows \
                                the report and last 3. in METHODS_DESCRIPTION in config.py. Number 1 and 3 do not agree.')
            if method.description == 'z-score':
                if median_instead_of_mean:
                    long_description = f'modified z-statistics, for modified z-score larger than {z_threshold_ax0}.'
                else:                
                    long_description = f'z-statistics, for z-score larger than {z_threshold_ax0}.'
            elif method.description == 'IQR':
                long_description = f'Inter-Quartile Range method.'
            elif method.description == "Isol. Forest":
                long_description = f'Isolation Forest method.'
            else:
                raise NameError('ERROR!!! Method names should agree in all next three positions: 1. When defining the function,\
                                2. On streamlit page that shows the report and last 3. in METHODS_DESCRIPTION in config.py.\
                                -> Number (2) does not agree with the other two.')                
                       
            st.write( f'**{method.description}**: Outliers (marked with 1) found using {long_description}')
            
        st.write('-'*16)


        st.header('Outliers Found:')
        outliers_found_df = pd.DataFrame(np_data[global_outlier_mask])
        st.write(outliers_found_df)
        save_outliers = st.toggle(f'Save outliers list as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')
        if save_outliers:
            df_list_for_output.append(outliers_found_df)
            sheets_name_list_for_output.append('Outliers')
        st.write('-'*16)        

        st.write('-'*16)

        st.header('Clean data:')
        clean_data_df = pd.DataFrame(np_data[np.invert(global_outlier_mask)])
        st.write(clean_data_df)
        save_clean_data = st.toggle(f'Save clean data as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')
        if save_clean_data:
            df_list_for_output.append(clean_data_df)
            sheets_name_list_for_output.append('Clean_Data')
        st.write('-'*16)        

        st.write('-'*16)


        #TODO: add tickbox to save results

#write data to xlsx:
if len(df_list_for_output)>0:
    export_dfs_to_excel_sheets(df_list=df_list_for_output, \
                               sheet_name_list=sheets_name_list_for_output,
                               fname=SUMMARY_OUTPUT_XLSX_FNAME)
    

print ('-'*18)
print ('Methods page done!!!')
print ('-'*55)
