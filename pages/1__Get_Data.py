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
from src.utils.toolbox import get_initial_1d_graphs, \
                              get_2d_distrib_plots


np_data = None
df_data = None

get_data_from = st.sidebar.radio(
    "Get data from:",
    ["Uploading file", "Generate 1d data","Generate 2d data", 'Generate 2d moons data'],
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
    df_data = pd.DataFrame({'0':np_data[:,0], '1':np_data[:,1]})
    

elif get_data_from == 'Generate 2d moons data':
    from sklearn.datasets import make_moons
    np_data, y = make_moons(n_samples=500, noise=0.05, random_state=42)
    df_data = pd.DataFrame({'0':np_data[:,0], '1':np_data[:,1]})
    st.write(np_data)





if np_data is not None:
    
    st.write('Data preview:')
    col1, col2 =st.columns([0.25, 0.75])    
    
    data_dimensions = np_data.shape[1]    
        
    with col1:
        st.write(df_data)

    with col2:
        if data_dimensions == 1:
            fig = get_initial_1d_graphs(np_data)
        elif data_dimensions ==2:
            fig = get_2d_distrib_plots(x=np_data[:,0], y=np_data[:,1], x_label='0 axes' , y_label='1 axes')
        
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

