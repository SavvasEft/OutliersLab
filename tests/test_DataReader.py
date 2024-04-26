import os
import pandas as pd
import sys
import pytest

current_directory =  os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
modules_folder = os.path.join(parent_directory, 'modules_folderA') 

#grand_parent_directory = path.dirname(parent_directory)


sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.data_processing.DataReader import DataReader




#defining files for testing:
current_folder = os.path.dirname(__file__)
xlsx_file_name = 'xlsx_file.xlsx'
csv_file_name = 'csv_file.csv'
xlsx_file_path = os.path.join(current_folder, 'test_files', xlsx_file_name)
csv_file_path = os.path.join(current_folder, 'test_files', csv_file_name)
txt_file_path = os.path.join(current_folder, 'test_files', 'txt_file.txt')



# print (xlsx_file_path)

def test_reader_returns_dataframe():
    data_reader_object = DataReader(xlsx_file_path)
    data_df = data_reader_object.get_user_data_df()
    assert (isinstance(data_df, pd.core.frame.DataFrame))

def test_reader_can_read_xlsx_files():
    data_reader_object = DataReader(xlsx_file_path)
    data_df = data_reader_object.get_user_data_df()
    expected_df = pd.DataFrame({'col1':[1,2,3,4],
                                'col2':[5,6,7,8]})
    pd.util.testing.assert_frame_equal(data_df, expected_df)
    
def test_reader_can_read_csv_files():
    data_reader_object = DataReader(csv_file_path)
    data_df = data_reader_object.get_user_data_df()
    expected_df = pd.DataFrame({'col1':[1,2,3,4],
                                'col2':[5,6,7,8]})
    pd.util.testing.assert_frame_equal(data_df, expected_df)

def test_reader_raises_error_for_non_csv_or_xlsx_files():
    data_reader_object = DataReader(txt_file_path)  
    with pytest.raises(Exception) as exc_info:   
        data_reader_object.get_user_data_df()
    assert str(exc_info.value) == 'Error occurred while reading file: File type is not supported. Please use .csv or .xlsx files.'

