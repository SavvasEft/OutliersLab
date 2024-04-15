print ('-'*55)
print ('Methods page Starting!!!')
print ('--')

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
                                    get_iqr_outliers_1d_mask, \
                                    get_eucl_z_score_iterative_method_mask, \
                                    get_euclidean_distance, \
                                    get_eucl_z_score_iter_outlier_plots
                                    

from src.models.MLMethods import get_isolation_forest_outliers_mask, \
                                 get_lof_outlier_mask

from src.outlier_methods.methods_factory import MethodsFactory
                                    
from src.utils.toolbox import draw_scatter_plot_2d, \
                              draw_line_or_point_plot_1d,\
                              get_outliers_report_and_global_outliers_mask, \
                              get_before_vs_after_plot
                              
                              
from src.utils.ReportGenerator import prepare_outlier_report_df, \
                                      export_dfs_to_excel_sheets, \
                                      export_df_to_csv_file, \
                                      export_plt_fig, \
                                      prepare_mask_report_df
                                      

from src.utils.config import CONTAMINATION, \
                             METHODS_DESCRIPTIONS, \
                             SUMMARY_OUTPUT_XLSX_FNAME, \
                             CLEAN_DATA_FILENAME , \
                             N_NEIGHBORS, \
                             BEFORE_VS_AFTER_GRAPH_NAME
                             
from src.utils.ReduceDimensions import reduce_to_2d_PCA                
 
 
from src.outlier_methods.methods_factory import MethodsFactory

np_data = st.session_state['np_data']
data_dimensions = st.session_state['data_dimensions']
reduced_data = st.session_state['reduced_data']

col2 = None
show_z_stats = st.sidebar.checkbox('z-statistics')
show_iqr_stats = st.sidebar.checkbox('IQR method')
show_euclidean_z_score_stats = st.sidebar.checkbox('Euclidean z-score method')
show_isolation_forest = st.sidebar.checkbox('Isolation Forest')
show_lof = st.sidebar.checkbox('Local Outlier Factor')

show_line_plot = True

df_list_for_output = []
sheets_name_list_for_output = []
header_bool_list = []
chosen_methods_list = []
outlier_masks_per_chosen_method = []
generate_final_report = False
# chosen_methods_list = [get_z_score_outliers_1d_mask, \
#                 get_z_score_iter_outliers_1d_mask, \
#                 get_iqr_outliers_1d_mask, \
#                 get_isolation_forest_outliers_mask
#                 ]

outlier_masks_applied = []
methods_applied_names = []



col1, col2 =st.columns([0.6, 0.4])  
with col1:
    st.header('Outlier Detection')
    st.write('Tune Algorithms & Plot Findings')
    st.write('---')
with col2:
    st.header('Results')
    st.write('Combining chosen methods')
    st.write('---')


if show_z_stats:
    with col1: 
        st.header('z-statistics:')

        
        #un-comment when more than 1 dimensions are valid for z-stats, and after delete if elsewhere
        #median_instead_of_mean = st.toggle('Choose median for z-stats')

        if data_dimensions == 1:
            median_instead_of_mean = st.toggle('Choose median for z-stats', value=True)
            z_threshold_ax0 = st.slider('Choose threshold for z-scores:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)

########################################
            #Factory Method:
            
            method_name = 'z_score'
            z_score = MethodsFactory.apply_method(method_name = method_name, \
                                                   z_threshold = z_threshold_ax0, \
                                                   modified=median_instead_of_mean)
            z_score_mask = z_score.get_outlier_mask(data=np_data)
            fig_ = z_score.get_plot(data=np_data)
            
            # z_score_outlier_mask = get_z_score_iter_outliers_1d_mask(data = np_data, z_threshold=z_threshold_ax0)
            # fig = get_z_score_iter_outlier_plots(data = np_data, outlier_mask=z_score_outlier_mask , z_threshold=z_threshold_ax0, \
            #                                     line_plot=show_line_plot, modified=median_instead_of_mean)
            st.pyplot(fig_)

            outlier_masks_applied.append(z_score_mask)
            methods_applied_names.append(method_name)
            # chosen_methods_list.append(get_z_score_iter_outliers_1d_mask)

#########################################
#########################################
            #Old method to be depracated
            z_score_outlier_mask = get_z_score_iter_outliers_1d_mask(data = np_data, z_threshold=z_threshold_ax0)
            fig = get_z_score_iter_outlier_plots(data = np_data, outlier_mask=z_score_outlier_mask , z_threshold=z_threshold_ax0, \
                                                line_plot=show_line_plot, modified=median_instead_of_mean)
            st.pyplot(fig)

            chosen_methods_list.append(get_z_score_iter_outliers_1d_mask)
            outlier_masks_per_chosen_method.append(z_score_outlier_mask)  

#########################################

            generate_final_report = True
            print ('--Calculated outliers using z-statistics.')
            st.write('*Method assumes gaussian distribution of data')

            



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

        st.write('---')
        
        
if show_iqr_stats:
    with col1:
        st.header('IQR:')

        if data_dimensions == 1:
            iqr_outlier_mask = get_iqr_outliers_1d_mask(np_data)
            fig = get_iqr_anomaly_plots(data = np_data, outliers_mask = iqr_outlier_mask, line_plot=show_line_plot)
            st.pyplot(fig)

            chosen_methods_list.append(get_iqr_outliers_1d_mask)
            outlier_masks_per_chosen_method.append(iqr_outlier_mask)
            generate_final_report = True
            print ('--Calculated outliers using IQR.')
            st.write('*Method assumes gaussian distribution of data')

        else:
           st.write('Currently z-score is only applicable for 1d data. Chosen data have more dimensions')
        # elif data_dimensions == 2:
        #     with col1:
        #         fig01 = get_iqr_anomaly_plots(data = np_data[:,0], line_plot=show_line_plot)
        #         st.pyplot(fig01)
        #     with col2:
        #         fig02 = get_iqr_anomaly_plots(data = np_data[:,1], line_plot=show_line_plot)
        #         st.pyplot(fig02)

        st.write('---')

if show_euclidean_z_score_stats:
    with col1:
        st.header('Euclidean z-score statistics:')
        #median_instead_of_mean_ = st.toggle('Choose median for z-stats ', value=True)
        z_threshold_ax0_eucl_dist = st.slider('Choose threshold for Euclidean z-scores:', min_value=1., \
                                max_value = 10., step = 0.25, value = 3.)
        z_score_eucl_outlier_mask = get_eucl_z_score_iterative_method_mask(data = np_data, z_threshold=z_threshold_ax0_eucl_dist)
        eucl_dist_data = get_euclidean_distance(np_data,np_data.mean(axis=0))
        fig = get_eucl_z_score_iter_outlier_plots(data = eucl_dist_data, outlier_mask=z_score_eucl_outlier_mask,  \
                                            z_threshold=z_threshold_ax0_eucl_dist, line_plot=show_line_plot, modified=False)
        st.pyplot(fig)

        chosen_methods_list.append(get_eucl_z_score_iterative_method_mask)    
        outlier_masks_per_chosen_method.append(z_score_eucl_outlier_mask)  
        generate_final_report = True
        print ('--Calculated outliers using euclidean z-statistics.')
        st.write('*Method assumes gaussian distribution of euclidean distances between data and their mean')

            




if show_isolation_forest:
    with col1:

        st.header('Isolation Forest:')

        contamination = st.slider('Proportion of outliers:', min_value=0.01, \
                                    max_value = 0.5, step = 0.01, value = CONTAMINATION)

        

        data = np_data
        outlier_mask_isolation_forest = get_isolation_forest_outliers_mask(data = np_data, \
                                                                            contamination=contamination)

        if data_dimensions == 1:
            fig_forest_isol = draw_line_or_point_plot_1d(data = np_data, outlier_bool = outlier_mask_isolation_forest, \
                                                        line_plot = show_line_plot,  \
                                                        title = 'Outliers found using Isolation Forest')

        elif data_dimensions == 2:
            fig_forest_isol = draw_scatter_plot_2d(data = np_data, outlier_bool =outlier_mask_isolation_forest)

        else:
            fig_forest_isol = draw_scatter_plot_2d(data = reduced_data, outlier_bool =outlier_mask_isolation_forest)
            st.write('*Reduced dimensions to 2d (PCA) for visualization.')


        st.pyplot(fig_forest_isol)
            
        chosen_methods_list.append(get_isolation_forest_outliers_mask)  
        outlier_masks_per_chosen_method.append(outlier_mask_isolation_forest)
        generate_final_report = True
    print ('--Calculated outliers using Isolation forest method.')
    st.write('---')
    
    
if show_lof:
    with col1:
        st.header('Local Outlier Factor:')
        
        contamination_lof = st.slider('Proportion of outliers: ', min_value=0.01, \
                                    max_value = 0.5, step = 0.01, value = CONTAMINATION)
        
        n_neighbors = st.slider('Min number of neighbors for data points: ', min_value=1, \
                                    max_value = 500, step = 1, value = N_NEIGHBORS)
        
        data = np_data
        outlier_mask_lof = get_lof_outlier_mask(data = np_data, \
                                                contamination=contamination_lof, \
                                                n_neighbors=n_neighbors)
        if data_dimensions == 1:
            fig_lof = draw_line_or_point_plot_1d(data = np_data, outlier_bool = outlier_mask_lof, \
                                                 line_plot = show_line_plot, 
                                                 title = 'Outliers found using Local Outlier Factor')

        elif data_dimensions == 2:
            fig_lof = draw_scatter_plot_2d(data = np_data, outlier_bool = outlier_mask_lof)

        else:
            fig_lof = draw_scatter_plot_2d(data = reduced_data, outlier_bool =outlier_mask_lof)
            st.write('*Reduced dimensions to 2d (PCA) for visualization.')

        st.pyplot(fig_lof)

        
        chosen_methods_list.append(get_lof_outlier_mask)
        outlier_masks_per_chosen_method.append(outlier_mask_lof)
        generate_final_report = True
        
    print ('--Calculated outliers using Local Outlier Factor method.')
    st.write('---')    


if generate_final_report:
    with col2:
        
        ######################################
        #Using MethodsFactory, generate df from all chosen methods: 
        combined_outlier_mask = MethodsFactory.combine_outlier_masks(masks_list = outlier_masks_applied)
        print ('-'*8)
        df = prepare_mask_report_df(masks_list=outlier_masks_applied, methods_name_list=methods_applied_names)
        st.write(df)
        print ('-'*8)
        ######################################
        
        
        
        
        outlier_report_array, global_outlier_mask = get_outliers_report_and_global_outliers_mask(np_data, outlier_masks_list=outlier_masks_per_chosen_method)
        print (f"------{outlier_report_array.shape}")
        outlier_report = prepare_outlier_report_df(outlier_report_array=outlier_report_array, methods_list=chosen_methods_list)
 
        
        outliers_number = len(outlier_report)
        raw_data_points_number = len(np_data)
        outliers_prc = round(outliers_number/raw_data_points_number*100,1)
        
        clean_data = np_data[np.invert(global_outlier_mask)]
        clean_data_df = pd.DataFrame(clean_data)
        
        st.header(f'{outliers_prc}% of data are outliers.')
        st.write(f'Number of data points checked: {raw_data_points_number}')
        st.write(f'Outliers found: {outliers_number}')    
        
        if data_dimensions>2:
            
            reduced_dim_data = reduce_to_2d_PCA(np_data)
            reduced_dim_clean_data = reduced_data[np.invert(global_outlier_mask)]
            fig = get_before_vs_after_plot(data=reduced_dim_data, clean_data=reduced_dim_clean_data,\
                                           data_dim = 2)
            st.write('*Reduced dimensions to 2d (PCA) for visualization.')
            
        elif data_dimensions<3:
            fig = get_before_vs_after_plot(data=np_data, clean_data=clean_data, data_dim = data_dimensions)
                      
        st.pyplot(fig)
        save_clean_vs_data_dirty_graph = st.toggle(f'Save graph as {BEFORE_VS_AFTER_GRAPH_NAME}.png')


        st.write('-'*16)       
        st.header('Outlier Final Report')      
        st.write(outlier_report)    

        save_outlier_report = st.toggle(f'Save as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')
        if save_outlier_report:
            df_list_for_output.append(outlier_report)
            sheets_name_list_for_output.append('Outlier_report')
            header_bool_list.append(True)

            
        st.write('**Point index**: Number of row in data that was identified as an outlier by at least one of the chosen methods.')

        st.write('**Outlier Score**: Number of methods that identified the specific data point as outlier')

        
        #TODO: CHANGE this with a dic in config to automate the long description generation... 
        for method in chosen_methods_list:
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
            elif method.description == 'eucl. z-score':
                long_description = f'Euclidean z-score method.'
            elif method.description == "Isol. Forest":
                long_description = f'Isolation Forest method.'
            elif method.description == "Local Outlier Factor":
                long_description = f'Local Outlier Factor method.'
            else:
                raise NameError('ERROR!!! Method names should agree in all next three positions: 1. When defining the function,\
                                2. On streamlit page that shows the report and last 3. in METHODS_DESCRIPTION in config.py.\
                                -> Number (2) does not agree with the other two.')                
                       
            st.write( f'**{method.description}**: Outliers (marked with 1) found using {long_description}')
            
        st.write('-'*16)


        st.header('Outliers Found:')
        outliers_found_df = pd.DataFrame(np_data[global_outlier_mask])
        st.write(outliers_found_df)
        save_outliers = st.toggle(f'Save outliers as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')
        if save_outliers:
            df_list_for_output.append(outliers_found_df)
            sheets_name_list_for_output.append('Outliers')
            header_bool_list.append(False)
        st.write('-'*16)        

        st.write('-'*16)

        st.header('Clean data:')

        
        if data_dimensions == 1:
            a = None
            #plot 1d clean data
        elif data_dimensions == 2:
            a = None
            #plot 2d clean data
        else:
            a = None
            # reduce dimensions to two
            # plot 2d data
                    
                
        st.write(clean_data_df)

        save_clean_data_as_sheet = st.toggle(f'Save clean data as sheet in {SUMMARY_OUTPUT_XLSX_FNAME}.xlsx')

        save_clean_data_as_csv = st.toggle(f'Save clean data as {CLEAN_DATA_FILENAME}.csv')


        if save_clean_data_as_sheet:
            df_list_for_output.append(clean_data_df)
            sheets_name_list_for_output.append('Clean_Data')
            header_bool_list.append(False)

        if save_clean_data_as_csv:
            export_df_to_csv_file(df = clean_data_df, fname = CLEAN_DATA_FILENAME)
            
        if save_clean_vs_data_dirty_graph:
            export_plt_fig(fig, fname=BEFORE_VS_AFTER_GRAPH_NAME)
            
        st.write('-'*16)        

        st.write('-'*16)


#write data to xlsx:
if len(df_list_for_output)>0:
    export_dfs_to_excel_sheets(df_list=df_list_for_output, \
                               sheet_name_list=sheets_name_list_for_output, \
                               fname=SUMMARY_OUTPUT_XLSX_FNAME, \
                               header_bool_list=header_bool_list)
    

print ('--')
print ('Methods page done!!!')
print ('---'*55)


#TODO:  simplify the procedure of adding a method to the page. 
#       Problem to solve: finetuning for different mehtods may require different parameters
#       Possible solution: add if functions to add/remove sliders/tick boxes for different methods 