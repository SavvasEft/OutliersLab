import os
import pandas as pd

import matplotlib.pyplot as plt

from src.data_processing import DataReader

class UnsupportedFileTypeError(Exception):
    """Exception raised when an unsupported file type is provided."""
    pass


class DataReader:
    
    def __init__(self, datafile):
        self.datafile=datafile
        
    def get_user_data_df(self):
        try:
            if self.file_is_xlsx():
                try:
                    return pd.read_excel(self.datafile)
                except ValueError as e:
                    raise ValueError(f"Error reading the Excel file: {e}")
            elif self.file_is_csv():
                try:
                    return pd.read_csv(self.datafile)
                except pd.errors.ParserError as e:
                    raise pd.errors.ParserError(f"Error parsing CSV file: {e}")
            else:
                raise UnsupportedFileTypeError("File type is not supported. Please use .csv or .xlsx files.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.datafile} was not found.")
        except Exception as e:
            raise Exception(f"Error occurred while reading file: {e}")


    def file_is_xlsx(self):
        return self.datafile[-4:]=='.xlsx'

    def file_is_csv(self):
        return self.datafile[-3:]=='.csv'




    def uploaded_xlsx_file_from_streamlit(self):
        try:
            return self.file_name.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        except Exception:
            return False
        
    def uploaded_csv_file_from_streamlit(self):
        try:
            return self.datafile.type == "text/csv"
        except Exception:
            return False
 
    def get_user_data_df_from_streamlit_upload(self, col_number = None):
        try:
            print ('1')
            if self.uploaded_xlsx_file_from_streamlit():
                print ('a'*30)
                df = pd.read_excel(io = self.file_name)
                logger.info('>>>reading excel file done')
            elif self.uploaded_csv_file_from_streamlit():
                logger.info('>>>reading csv file...')
                self.file_name.seek(0)
                df = pd.read_csv(self.file_name, usecols = [col_number])
                logger.info('>>>reading csv file done')
            return df 
        except:
            pass
        
        
