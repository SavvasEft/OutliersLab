import pandas as pd

import os
import sys
from openpyxl import Workbook

# import odswriter as ods

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from utils.config import METHODS_DESCRIPTIONS, \
                         OUTPUT_FOLDER_PATH

                         



def export_df_to_excel_file(df, fname):
    if fname is None:
        fname = 'output_file'
    wb = Workbook()
    ws = wb.active
    ws.sheet_state = 'visible'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.xlsx")
    with pd.ExcelWriter(filename_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return None

def export_dfs_to_excel_sheets(df_list,sheet_name_list, fname):
    if fname is None:
        fname = 'output_file_multiple_sheets'
    wb = Workbook()
    ws = wb.active
    ws.sheet_state = 'visible'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.xlsx")
    with pd.ExcelWriter(filename_path, engine="openpyxl") as writer:
        for i in range (len(df_list)): 
            df_list[i].to_excel(writer, sheet_name=sheet_name_list[i], index=False)
    return None

# def export_dfs_to_excel_sheets():

#     df1 = pd.DataFrame([1,2,3])
#     fpath = os.path.join(OUTPUT_FOLDER_PATH,'otinane.xlsx')
#     df1.to_excel(fpath)
    # Multiple sheet mode
    # with ods.writer(open("test-multi.ods","wb")) as odsfile:
    #     bears = odsfile.new_sheet("Bears")
    #     bears.writerow(["American Black Bear", "Asiatic Black Bear", "Brown Bear", "Giant Panda", "Qinling Panda",
    #     "Sloth Bear", "Sun Bear", "Polar Bear", "Spectacled Bear"])
    #     sloths = odsfile.new_sheet("Sloths")
    #     sloths.writerow(["Pygmy Three-Toed Sloth", "Maned Sloth", "Pale-Throated Sloth", "Brown-Throated Sloth",
    #     "Linneaeus's Two-Twoed Sloth", "Hoffman's Two-Toed Sloth"])

    return None


def prepare_outlier_report_df(outlier_report_array, methods_list):
    columns = ['Point Index', 'Outlier score']
    
    for method in methods_list:
        if method.description in METHODS_DESCRIPTIONS:
            columns.append(method.description)
        else:
            raise NameError('ERROR: Method description names are ambiguous(methods are used to identify outlier masks). \
                            They should be the same in all following places: 1. When defining the method (with the decorator),\
                            2. On the streamlit page that shows the report and last, \
                            3. in METHODS_DESCRIPTION list in config.py')

    outlier_report_df = pd.DataFrame(outlier_report_array, columns=columns)
    return outlier_report_df

if __name__ == '__main__':
    print(1)
    export_dfs_to_excel_sheets
    print(2)

