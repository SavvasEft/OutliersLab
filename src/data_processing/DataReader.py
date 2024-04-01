import pandas as pd
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
        return self.datafile[-5:]=='.xlsx'

    def file_is_csv(self):
        return self.datafile[-4:]=='.csv'



        
