import pandas as pd
import os


current_directory =  os.path.abspath(os.path.dirname(__file__))
grand_parent_directory = os.path.dirname(os.path.dirname(current_directory))
output_folder_path = os.path.join(grand_parent_directory, 'findings')

      
def export_dfs_to_excel_sheets(df_list,sheet_name_list, xls_filename):
    filename_path = os.path.join(output_folder_path, f"{xls_filename}.xlsx")
    with pd.ExcelWriter(filename_path) as writer:
        for i in range (len(df_list)): 
            df_list[i].to_excel(writer, sheet_name=sheet_name_list[i], index=False)


def create_df_report_from_dfs_given():
    pass