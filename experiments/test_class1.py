import os
import pandas as pd
import sys

current_directory =  os.getcwd()
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

class test_class1:
    def __init__(self, data_file):
        self.data_file = data_file
        print ('='*10)
        print (self.data_file[-4:])
        print ('='*10)