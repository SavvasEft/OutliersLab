print ('---'*35)
print ('--')
print ('Methods page Starting...')
print ('--')

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

import os
import sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.outlier_methods.methods_factory import MethodsFactory
from src.utils.reduce_dimensions import reduce_to_2d_PCA                                                  
from src.utils.toolbox import get_before_vs_after_plot
from src.utils.ReportGenerator import export_dfs_to_excel_sheets, \
                                      export_df_to_csv_file, \
                                      export_plt_fig, \
                                      prepare_mask_report_df, \
                                      get_quantitative_data_from_mask_report
from src.utils.config import CONTAMINATION, \
                             N_NEIGHBORS, \
                             Z_THRESHOLD
                             
from src.utils.config import FNAMES

st.set_page_config(layout="wide")

np_data = st.session_state['np_data']
data_dimensions = st.session_state['data_dimensions']
reduced_data = st.session_state['reduced_data']

show_line_plot = True

df_list_for_output = []
sheets_name_list_for_output = []
header_bool_list = []
generate_final_report = False
outlier_masks_applied = []
methods_applied_names = []

show_z_stats = st.sidebar.checkbox('z-statistics')
show_iqr_stats = st.sidebar.checkbox('IQR method')
show_euclidean_z_score_stats = st.sidebar.checkbox('Euclidean z-score method', value=True)
show_isolation_forest = st.sidebar.checkbox('Isolation Forest', value=True)
show_lof = st.sidebar.checkbox('Local Outlier Factor', value=True)

col1, col2 =st.columns([0.6, 0.4])  
with col1:
    st.header('Outlier Detection')
    st.write('Tune chosen algorithms')
    st.write('---')

with col2:
    st.header('Findings')
    st.write('Outliers found when chosen methods are combined')
    details_on = st.toggle('Show details')
    st.write('---')

if show_z_stats:
    with col1: 
        st.header('z-statistics:')
        
        if data_dimensions == 1:
            median_instead_of_mean = st.toggle('Choose median for z-stats', value=True)
            z_threshold_ax0 = st.slider('Choose z-threshold for z-scores:', min_value=1., \
                                    max_value = 10., step = 0.25, value = 3.)

            
            method_name = 'z_score'
            z_score = MethodsFactory.apply_method(method_name = method_name, \
                                                   z_threshold = z_threshold_ax0, \
                                                   modified=median_instead_of_mean)
            z_score_mask = z_score.get_outlier_mask(data=np_data)
            z_score_plot = z_score.get_plot(data=np_data)
            st.pyplot(z_score_plot)
            outlier_masks_applied.append(z_score_mask)
            methods_applied_names.append(method_name)
            generate_final_report = True
            st.write('*Method assumes gaussian-like distribution of data')
            save_zscore_plot = st.toggle(f'Save plot as {FNAMES.ZSCORE_PLOT_PNG_NAME}.png', value=False)
            if save_zscore_plot:
                export_plt_fig(z_score_plot, fname=FNAMES.ZSCORE_PLOT_PNG_NAME)
            print ('--Calculated outliers using z-statistics.')

        elif data_dimensions != 1:       
            st.write('Currently z-score is only applicable for 1d data. Chosen data have more dimensions')
        st.write('---')
        
if show_iqr_stats:
    with col1:
        st.header('IQR:')

        if data_dimensions == 1:
            method_name='iqr'
            iqr_object = MethodsFactory.apply_method(method_name=method_name)
            iqr_mask = iqr_object.get_outlier_mask(data=np_data) 
            iqr_plot = iqr_object.get_plot(data=np_data, outliers_mask=iqr_mask)
            st.pyplot(iqr_plot)
            outlier_masks_applied.append(iqr_mask)
            methods_applied_names.append(method_name)
            generate_final_report = True
            print ('--Calculated outliers using IQR.')
            st.write('*Method assumes gaussian-like distribution of data')
            save_iqr_plot = st.toggle(f'Save plot as {FNAMES.IQR_PLOT_PNG_NAME}.png', value=False)
            if save_iqr_plot:
                export_plt_fig(iqr_plot, fname=FNAMES.IQR_PLOT_PNG_NAME)


        else:
           st.write('Currently z-score is only applicable for 1d data. Chosen data have more dimensions')
        st.write('---')

if show_euclidean_z_score_stats:
    with col1:
        st.header('Euclidean distance z-score method:')
        z_threshold_ax0_eucl_dist = st.slider('Choose z-threshold for Euclidean z-scores:', min_value=1., \
                                max_value = 10., step = 0.25, value = Z_THRESHOLD)
        method_name = 'euclidean distance'
        eucl_obj = MethodsFactory.apply_method(method_name = method_name, \
                                                z_threshold = z_threshold_ax0_eucl_dist)
        eucl_mask = eucl_obj.get_outlier_mask(data=np_data)
        eucl_plot = eucl_obj.get_plot(data=np_data)
        st.pyplot(eucl_plot)
        outlier_masks_applied.append(eucl_mask)
        methods_applied_names.append(method_name)
        generate_final_report = True
        print ('--Calculated outliers using euclidean z-statistics.')
        st.write('*Method assumes gaussian-like distribution of euclidean distances between data and their mean')
        save_eucl_plot = st.toggle(f'Save plot as {FNAMES.EUCL_PLOT_PNG_NAME}.png', value=False)
        if save_eucl_plot:
            export_plt_fig(eucl_plot, fname=FNAMES.EUCL_PLOT_PNG_NAME)

        st.write('---')

if show_isolation_forest:
    with col1:
        st.header('Isolation Forest:')
        isol_contamination_options = ['auto', 'manual']
        isol_contamination_option = st.radio('Define isolation forest contamination factor', isol_contamination_options, )
        if isol_contamination_option == 'auto':
            contamination = 'auto'
        else:    
            contamination = st.slider('Proportion of outliers:', min_value=0.01, \
                                        max_value = 0.5, step = 0.01, value = CONTAMINATION)
        method_name = 'isolation forest'
        isol_forest_obj = MethodsFactory.apply_method(method_name=method_name, contamination=contamination)
        isol_forest_mask = isol_forest_obj.get_outlier_mask(data=np_data)

        if data_dimensions<3:
            plot_data = np_data
        else:
            plot_data = reduced_data
       
        isol_forest_plot = isol_forest_obj.get_plot(data=plot_data, outliers_mask=isol_forest_mask)
        st.pyplot(isol_forest_plot)
        st.write('*Reduced dimensions to 2d (PCA) for visualization.')
        outlier_masks_applied.append(isol_forest_mask)
        methods_applied_names.append(method_name)
        generate_final_report = True
        save_isol_forest_plot = st.toggle(f'Save plot as {FNAMES.ISOL_FOREST_PLOT_PNG_NAME}.png', value=False)
        if save_isol_forest_plot:
            export_plt_fig(isol_forest_plot, fname=FNAMES.ISOL_FOREST_PLOT_PNG_NAME)
        st.write('---')

    print ('--Calculated outliers using Isolation forest method.')
    
    
if show_lof:
    with col1:
        st.header('Local Outlier Factor:')
        lof_contamination_options = ['auto', 'manual']
        lof_contamination_option = st.radio('Define local outlier factor contamination factor', lof_contamination_options, )
        if lof_contamination_option == 'auto':
            contamination_lof = 'auto'
        else:    
            contamination_lof = st.slider('Proportion of outliers:', min_value=0.01, \
                                        max_value = 0.5, step = 0.01, value = CONTAMINATION)
        
 
        n_neighbors = st.slider('Min number of neighbors for data points: ', min_value=1, \
                                    max_value = 500, step = 1, value = N_NEIGHBORS)
        method_name = 'local outlier factor'
        lof_obj = MethodsFactory.apply_method(method_name=method_name, contamination = contamination_lof,\
                                              n_neighbors = n_neighbors )
        lof_mask = lof_obj.get_outlier_mask(data=np_data)
        if data_dimensions<3:
            plot_data = np_data
        else:
            plot_data = reduced_data
        lof_plot = lof_obj.get_plot(data=plot_data, outliers_mask=lof_mask)
        st.pyplot(lof_plot)
        outlier_masks_applied.append(lof_mask)
        methods_applied_names.append(method_name)
        generate_final_report = True
        save_lof_plot = st.toggle(f'Save plot as {FNAMES.LOF_PLOT_PNG_NAME}.png', value=False)
        if save_lof_plot:
            export_plt_fig(lof_plot, fname=FNAMES.LOF_PLOT_PNG_NAME)

        st.write('---')    
    print ('--Calculated outliers using Local Outlier Factor method.')


if generate_final_report:
    with col2:
        combined_outlier_mask = MethodsFactory.combine_outlier_masks(masks_list = outlier_masks_applied)
        clean_data = np_data[np.invert(combined_outlier_mask)]
        clean_data_df = pd.DataFrame(clean_data)
        outliers_found = np_data[combined_outlier_mask]
        outliers_found_df = pd.DataFrame(outliers_found)
        combined_outlier_mask_df = pd.DataFrame(combined_outlier_mask)
        outlier_report_df = prepare_mask_report_df(masks_list=outlier_masks_applied, methods_name_list=methods_applied_names)
        outlier_descr = get_quantitative_data_from_mask_report(outlier_report_df)
        no_of_points, _ = np_data.shape
        st.header(f"{outlier_descr['outliers_prc']} % of data are outliers.")
        st.write(f"- {outlier_descr['outliers_num']} outlier points out of total {outlier_descr['data_points_num']}")
        if details_on:
            for method, mask  in zip(methods_applied_names,outlier_masks_applied):
                outlier_num_from_method = sum(mask)
                outlier_prc = round(outlier_num_from_method*100/no_of_points,1)
                st.write(f'- {outlier_num_from_method}  ({outlier_prc}%) found using {method}')


        st.write('---')
        st.header('Outlier Report') 
        st.write('Report on each point with outlier scores, methods that identified point as outlier, and the final decision if a point is an outlier or not based on chosen methods.')
        st.write(outlier_report_df)
        st.write('**Point index**: Number of row in raw data.')
        st.write('**Outlier Score**: Number of methods that identified the specific data point as outlier')
        st.write('**Global Outlier Mask**: An outlier mask of all the points. True if any one of chosen methods identified point as an outlier')
        st.write('Other columns with descriptive method names show if point was identified as outlier (True) from the method or not (False)')      
        st.write('---')


        if data_dimensions>2:
            reduced_dim_data = reduce_to_2d_PCA(np_data)
            reduced_dim_clean_data = reduced_data[np.invert(combined_outlier_mask)]
            clean_vs_raw_data_plot = get_before_vs_after_plot(data=reduced_dim_data, clean_data=reduced_dim_clean_data,\
                                        data_dim = 2)
        elif data_dimensions<3:
            clean_vs_raw_data_plot = get_before_vs_after_plot(data=np_data, clean_data=clean_data, data_dim = data_dimensions)

        if details_on:                                
            st.pyplot(clean_vs_raw_data_plot)
            if data_dimensions>2:
                st.write('*Reduced dimensions to 2d (PCA) for visualization.')
            st.write('---')

        st.header('Saving options')
        prepare_xls_report = st.toggle(f'Save Outlier Report in {FNAMES.SUMMARY_OUTPUT_XLSX_FNAME}.xlsx', value=True)
        save_clean_data_as_csv = st.toggle(f'Save Clean Data as {FNAMES.CLEAN_DATA_CSV_FNAME}.csv', value=True)
        save_global_outlier_mask_as_csv = st.toggle(f'Save Global Outlier Mask as {FNAMES.GLOBAL_OUTLIER_MASK_CSV_FNAME}.csv', value=True)
        save_clean_vs_raw_data_plot = st.toggle(f'Save clean Vs raw data plot as  {FNAMES.BEFORE_VS_AFTER_PLOT_NAME}.png', value=True)

        if prepare_xls_report:
            st.subheader('Sheets included in the Outlier Report xlsx File:')

            save_outlier_report = st.toggle('Outlier Report', value=True)
            if save_outlier_report:
                df_list_for_output.append(outlier_report_df)
                sheets_name_list_for_output.append('Outlier Report')
                header_bool_list.append(True)
                
            save_clean_data_as_sheet = st.toggle(f'Clean data', value=True)
            if save_clean_data_as_sheet:
                df_list_for_output.append(clean_data_df)
                sheets_name_list_for_output.append('Clean Data')
                header_bool_list.append(False)

            save_outliers_mask_as_sheet = st.toggle(f'Global Outliers Mask', value=True)
            if save_outliers_mask_as_sheet:
                df_list_for_output.append(combined_outlier_mask_df)
                sheets_name_list_for_output.append('Global Outliers Mask')
                header_bool_list.append(False)

            save_outliers_as_sheet = st.toggle('Outliers', value=True)
            if save_outliers_as_sheet:
                df_list_for_output.append(outliers_found_df)
                sheets_name_list_for_output.append('Outliers')
                header_bool_list.append(False)
            
            st.write('---')

#Export files:
    if len(df_list_for_output)>0:
        export_dfs_to_excel_sheets(df_list=df_list_for_output, \
                                sheet_name_list=sheets_name_list_for_output, \
                                fname=FNAMES.SUMMARY_OUTPUT_XLSX_FNAME, \
                                header_bool_list=header_bool_list)

    if save_clean_data_as_csv:
        export_df_to_csv_file(df = clean_data_df, fname = FNAMES.CLEAN_DATA_CSV_FNAME)
    
    if details_on:
        if save_clean_vs_raw_data_plot:
            export_plt_fig(clean_vs_raw_data_plot, fname=FNAMES.BEFORE_VS_AFTER_PLOT_NAME)
    
st.write('---')        

    

print ('--')
print ('Methods page done!!!')
print ('--')
print ('---'*35)

