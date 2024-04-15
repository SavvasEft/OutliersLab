import os
import sys

current_directory =  os.path.abspath(os.path.dirname(__file__))
grand_parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.insert(0, grand_parent_directory) # defined root folder 1 step up

# from StatsMethods import get_z_score_iter_outliers_1d_mask, \
#                          get_iqr_outliers_1d_mask, \
#                          get_eucl_z_score_iterative_method_mas, \
#                          get_lof_outlier_mask

# from MLMethods import get_isolation_forest_outliers_mask, \
#                       get_lof_outlier_mask
                         

OUTPUT_FOLDER_PATH = os.path.join(grand_parent_directory, 'output')

# Used as upper upper limit of iterations for z-score iterative method method
ITERATION_MAX_NUM_ZSCORE = 100

# Used in isolation forest & LOF. Valid range: (0,0.5]
CONTAMINATION = 0.1

# Used in LOF method
N_NEIGHBORS = 24


# Used for reminder, for raising exception and reminding to modify
# method description in all places that it is used
# METHODS_DICT = {
#                 'z-score' : get_z_score_iter_outliers_1d_mask,\
#                 'IQR' : get_iqr_outliers_1d_mask,\
#                 'eucl. z-score': get_eucl_z_score_iterative_method_mask,\
#                 'Isol. Forest': get_isolation_forest_outliers_mask,\
#                 'Local Outlier Factor': get_lof_outlier_mask
# }
                         


METHODS_DESCRIPTIONS = ['z-score', \
                        'IQR', \
                        'eucl. z-score', \
                        'Isol. Forest', \
                        'Local Outlier Factor']

SUMMARY_OUTPUT_XLSX_FNAME = 'outlier_report'

#file name for csv output:
CLEAN_DATA_FILENAME = 'clean_data'

BEFORE_VS_AFTER_GRAPH_NAME = 'cleanVsdirty_data_plot'

# Axes name default values for figs:
#For 1d graphs
POINT_VALUE_NAME = 'Point Values'
NUMBERED_LABELS_NAME = 'Numbered Labels'
