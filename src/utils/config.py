import os
import sys
current_directory =  os.path.abspath(os.path.dirname(__file__))
grand_parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.insert(0, grand_parent_directory) # defined root folder 1 step up

OUTPUT_FOLDER_PATH = os.path.join(grand_parent_directory, 'output')

# Used as upper upper limit of iterations for z-score iterative method method
ITERATION_MAX_NUM_ZSCORE = 10

# Used in isolation forest. Valid range: (0,0.5]
CONTAMINATION = 0.1

# Used for reminder, for raising exception and reminding to modify
# method description in all places that it is used
METHODS_DESCRIPTIONS = ['z-score', \
                        'IQR', \
                        'Isol. Forest', \
                        'Local Outlier Factor']

SUMMARY_OUTPUT_XLSX_FNAME = 'outlier_report'

#file name for csv output:
CLEAN_DATA_FILENAME = 'clean_data'

