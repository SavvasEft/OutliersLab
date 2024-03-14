import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


import os
import sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.data_processing.DataReader import DataReader
from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
                                              get_2d_distr_with_outliers

##Helper functions for plots:
def get_initial_1d_graphs(np_data):
    "data: np.array"
    fig, [ax1, ax2] = plt.subplots(2,1)
    ax2.hist(np_data, int(len(np_data)/4))
    ax1.plot(np_data)
    return fig


def scatter_hist_for_2d_data(x, y, ax, ax_histx, ax_histy, x_label, y_label):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y)
    
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')
    

def get_initial_2d_distrib_plots(x, y, x_label, y_label):
    # Start with a square Figure.
    fig = plt.figure(figsize=(6, 6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal axes and the main axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                        left=0.1, right=0.9, bottom=0.1, top=0.9,
                        wspace=0.05, hspace=0.05)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    # Draw the scatter plot and marginals.
    return scatter_hist_for_2d_data(x, y, ax, ax_histx, ax_histy, x_label, y_label)

### End of helper functions


np_data = None
df_data = None

get_data_from = st.sidebar.radio(
    "Get data from:",
    ["Uploading file", "Generate 1d data","Generate 2d data"],
    index=0,
)

if get_data_from == 'Uploading file':
    uploaded_type = st.radio(label = 'Choose file type:', options=['.xlsx','.csv'])

    if uploaded_type=='.xlsx': 
        uploaded_data = st.file_uploader('Upload file here', type= ['.xlsx'])
        if uploaded_data is not None:
            df_data = pd.read_excel(uploaded_data, header=None)
            np_data = df_data.to_numpy()
            
    elif uploaded_type=='.csv':
        uploaded_data = st.file_uploader('Upload file here', type= ['.csv'])
        if uploaded_data is not None:
            df_data = pd.read_csv(uploaded_data, header=None)
            np_data = df_data.to_numpy()

elif get_data_from == 'Generate 1d data':
    np_data = get_1d_distr_with_outliers()
    df_data = pd.DataFrame(np_data)

elif get_data_from == 'Generate 2d data':
    np_data = get_2d_distr_with_outliers()
    df_data = pd.DataFrame({'0':np_data[0], '1':np_data[1]})






if np_data is not None:
    
    st.write('Data preview:')
    col1, col2 =st.columns([0.25, 0.75])    
    
    data_dimensions = np_data.ndim    
        
    with col1:
        st.write(df_data)

    with col2:
        if data_dimensions == 1:
            fig = get_initial_1d_graphs(np_data)
        elif data_dimensions ==2:
            fig = get_initial_2d_distrib_plots(x=np_data[0], y=np_data[1], x_label='0 axes' , y_label='1 axes')
        
        st.pyplot(fig)
    
    if 'df_data' not in st.session_state:
        st.session_state['df_data'] = df_data
    st.session_state['df_data'] = df_data
    
    if 'np_data' not in st.session_state:
        st.session_state['np_data'] = np_data
    st.session_state['np_data'] = np_data
    
    if 'data_dimensions' not in st.session_state:
        st.session_state['data_dimensions'] = data_dimensions
    st.session_state['data_dimensions'] = data_dimensions


    

