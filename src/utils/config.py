import os
import sys

current_directory =  os.path.abspath(os.path.dirname(__file__))
grand_parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.insert(0, grand_parent_directory) # defined root folder 1 step up


OUTPUT_FOLDER_PATH = os.path.join(grand_parent_directory, 'output')

# Used as upper upper limit of iterations for z-score iterative method method
ITERATION_MAX_NUM_ZSCORE = 100

# Used in isolation forest & LOF. Valid range: (0,0.5]
CONTAMINATION = 0.1

# Used in LOF method
N_NEIGHBORS = 24
Z_THRESHOLD = 2.5

# option to prepare download button instead of saving in output folder
RUN_ONLINE = True

# Axes name default values for figs:
#For 1d plots
POINT_VALUE_NAME = 'Point Values'
NUMBERED_LABELS_NAME = 'Numbered Labels'

class FNAMES:
    
    SUMMARY_OUTPUT_XLSX_FNAME = 'OutlierReport'
    CLEAN_DATA_CSV_FNAME = 'CleanData'
    BEFORE_VS_AFTER_PLOT_NAME = 'CleanVsRaw_data_plot'
    GLOBAL_OUTLIER_MASK_CSV_FNAME = 'GlobalOutlierMask'
    ZSCORE_PLOT_PNG_NAME = 'ZScore_OutlierPlot'
    IQR_PLOT_PNG_NAME = 'IQR_OutlierPlot'
    EUCL_PLOT_PNG_NAME = 'EuclideanZscore_OutlierPlot'
    ISOL_FOREST_PLOT_PNG_NAME = 'IsolationForest_OutlierPlot'
    LOF_PLOT_PNG_NAME = 'LOF_OutlierPlot'