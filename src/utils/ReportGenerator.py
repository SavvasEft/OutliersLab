import pandas as pd
import numpy as np

import os
import sys
from openpyxl import Workbook

# import odswriter as ods

current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from utils.config import OUTPUT_FOLDER_PATH

from outlier_methods.methods_factory import MethodsFactory

########
def get_quantitative_data_from_mask_report(df:pd.DataFrame) -> dict:
    outliers_num = df['Global Outlier Mask'].sum()
    data_points_num = len(df['Global Outlier Mask'])
    outliers_prc = round(outliers_num * 100 / data_points_num,1)
    description = {'outliers_num':outliers_num, \
                    'data_points_num':data_points_num, \
                    'outliers_prc':outliers_prc}
    return description
    
def prepare_mask_report_df(masks_list, methods_name_list):
    column_names = ['Point Index', 'Outlier score', 'Global Outlier Mask']
    for method in methods_name_list:
        column_names.append(method)
    index = np.arange(len(masks_list[0]))
    outlier_score = calculate_outlier_score_array(masks_list=masks_list)
    global_mask = MethodsFactory.combine_outlier_masks(masks_list=masks_list)
    df_columns = [index, outlier_score, global_mask]
    for mask in masks_list: 
        df_columns.append(mask)
    data_dic = dict(zip(column_names,df_columns))
    report_df = pd.DataFrame(data_dic)
    return report_df
     
def calculate_outlier_score_array(masks_list):
    if len(masks_list)>1:
        outlier_score = np.sum(masks_list, axis = 0)
    else: 
        outlier_score = masks_list[0]
    outlier_score = outlier_score.astype(int)
    return outlier_score


#########

def export_df_to_excel_file(df, fname):
    if fname is None:
        fname = 'output_xlsx_file'
    wb = Workbook()
    ws = wb.active
    ws.sheet_state = 'visible'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.xlsx")
    with pd.ExcelWriter(filename_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return None

def export_df_to_csv_file(df,fname,header=False):
    if fname is None:
        fname = 'output_csv_file'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.csv")
    df.to_csv(filename_path, header=header, index=False)
    
    
def export_dfs_to_excel_sheets(df_list,sheet_name_list, fname, \
                               header_bool_list=None):
    if fname is None:
        fname = 'output_file_multiple_sheets'

    if header_bool_list is None:
        header = True
    
    wb = Workbook()
    ws = wb.active
    ws.sheet_state = 'visible'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.xlsx")
    with pd.ExcelWriter(filename_path, engine="openpyxl") as writer:
        if header_bool_list is not None:
            for df_file, sheet_name, header in zip(df_list, sheet_name_list, header_bool_list):                
                df_file.to_excel(writer, sheet_name=sheet_name, \
                    index=False, header=header)
        else:
            for i in range (len(df_list)): 
                df_list[i].to_excel(writer, sheet_name=sheet_name_list[i], \
                    index=False, header=header)
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

def export_plt_fig(fig, fname=None):
    import matplotlib.pyplot as plt
    if fname is None:
        fname = 'fig1'
    filename_path = os.path.join(OUTPUT_FOLDER_PATH, f"{fname}.png")
    fig.savefig(filename_path)
    return None