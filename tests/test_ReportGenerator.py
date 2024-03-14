import os
import pandas as pd
import sys
import pytest

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)

#grand_parent_directory = path.dirname(parent_directory)


sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.utils.ReportGenerator import export_dfs_to_excel_sheets


def test_xls_output_of_export_dfs_to_excel_sheets():
    df1 = pd.DataFrame({'col1':[1,2,3,4,5]})
    df2 = pd.DataFrame({'col1':[6,7,8,9,10]})
    sheet_names = ['sheet1test', 'sheet2test']
    export_dfs_to_excel_sheets(df_list=[df1,df2],sheet_name_list = sheet_names, xls_filename='file_from_test1')
    file_name_path = os.path.join(parent_directory, 'findings', 'file_from_test1.xlsx')
    assert os.path.exists(file_name_path)
    os.remove(file_name_path)
