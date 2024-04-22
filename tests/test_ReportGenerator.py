import os
import pandas as pd
import numpy as np
import sys
import pytest

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)

#grand_parent_directory = path.dirname(parent_directory)


sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.utils.ReportGenerator import export_dfs_to_excel_sheets, \
                                      prepare_mask_report_df, \
                                      calculate_outlier_score_array


def test_xls_output_of_export_dfs_to_excel_sheets():
    df1 = pd.DataFrame({'col1':[1,2,3,4,5]})
    df2 = pd.DataFrame({'col1':[6,7,8,9,10]})
    sheet_names = ['sheet1test', 'sheet2test']
    export_dfs_to_excel_sheets(df_list=[df1,df2],sheet_name_list = sheet_names, fname='file_from_test1')
    file_name_path = os.path.join(parent_directory, 'output', 'file_from_test1.xlsx')
    assert os.path.exists(file_name_path)
    os.remove(file_name_path)
    
def test_prepare_mask_report_df_returns_correct_number_of_columns():
    array_1 = np.array([0,0,1,0])
    masks_list = [array_1,array_1,array_1]
    methods_name_list = [str(i) for i in range (len(masks_list))]
    df = prepare_mask_report_df(masks_list, methods_name_list)   
    assert (len(df.columns)==6)
    
def test_calculate_outlier_score_array_sums_correctly():
    array_1 = np.array([1,2,4,6])
    array_list = [array_1,array_1,array_1]
    expected_output = array_1*3
    calculated_array = calculate_outlier_score_array(masks_list=array_list)
    assert (np.array_equal(calculated_array,expected_output))
    
def test_calculate_outlier_score_array_returns_correct_dimensions():
    array_1 = np.array([1,2,4,6])
    array_list = [array_1,array_1,array_1]
    expected_dim = (len(array_1),)
    calculated_array = calculate_outlier_score_array(masks_list=array_list)
    assert (expected_dim == calculated_array.shape )