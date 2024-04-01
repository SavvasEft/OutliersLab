import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.data_processing.DataReader import DataReader
from src.data_processing.DataGenerator import get_1d_distr_with_outliers, \
                                              get_2d_distr_with_outliers, \
                                              get_4d_data_norm, \
                                              get_4d_data_5clusters
                                              
from src.utils.toolbox import get_initial_1d_graphs, \
                              get_joint_plot_for_2d_data
                              
from src.utils.ReduceDimensions import reduce_to_2d_PCA


np_data = None
df_data = None


get_data_from = st.sidebar.radio(
    "Get data from:",
    ["Uploading file", "Generate 1d data","Generate 2d data", 'Generate 4d data','Generate 2d moons data', \
        'Generate 4d data with 5 clusters'],
    index=0,
)


if get_data_from == 'Uploading file':
    uploaded_type = st.radio(label = 'Choose file type:', options=['.xlsx','.csv'], index=None)

    if uploaded_type is not None:
        feature_names_in_first_row = st.toggle(f'First Row has column names (attributes).')
        index_in_first_column = st.toggle(f'First Column has indices (instance labels).')

        header=0 if feature_names_in_first_row else None
        index_col=0 if index_in_first_column else None
        
    if uploaded_type=='.xlsx': 
        uploaded_data = st.file_uploader('Upload file here', type= ['.xlsx'])
        if uploaded_data is not None:
            df_data = pd.read_excel(uploaded_data, header=header)
            np_data = df_data.to_numpy()
            
    elif uploaded_type=='.csv':
        uploaded_data = st.file_uploader('Upload file here', type= ['.csv'])
        if uploaded_data is not None:
            df_data = pd.read_csv(uploaded_data, header=header, index_col=index_col)           
            np_data = df_data.to_numpy()


    
    
    
elif get_data_from == 'Generate 1d data':
    np_data = get_1d_distr_with_outliers()
    df_data = pd.DataFrame(np_data)
    

elif get_data_from == 'Generate 2d data':
    np_data = get_2d_distr_with_outliers()
    df_data = pd.DataFrame({'0':np_data[:,0], '1':np_data[:,1]})


elif get_data_from == 'Generate 4d data':
    np_data = get_4d_data_norm()
    df_data = pd.DataFrame({'1':np_data[:,0],
                            '2':np_data[:,1],
                            '3':np_data[:,2],
                            '4':np_data[:,3]})


elif get_data_from == 'Generate 4d data with 5 clusters':
    np_data, _ = get_4d_data_5clusters()
    df_data = pd.DataFrame({'1':np_data[:,0],
                        '2':np_data[:,1],
                        '3':np_data[:,2],
                        '4':np_data[:,3]})


elif get_data_from == 'Generate 2d moons data':
    from sklearn.datasets import make_moons
    np_data, y = make_moons(n_samples=500, noise=0.05, random_state=42)
    df_data = pd.DataFrame({'0':np_data[:,0], '1':np_data[:,1]})






if np_data is not None:
    st.write('---')
    st.header('Data preview')
    col1, col2 =st.columns([0.25, 0.75])    
    data_dimensions = np_data.shape[1]    
    
        
        
    with col1:

        st.write(f'Number of points: {len(df_data)}')
  
        st.write(df_data)
   
    with col2:
        if data_dimensions == 1:
            fig = get_initial_1d_graphs(np_data)
        elif data_dimensions ==2:
           fig = get_joint_plot_for_2d_data(data_df=df_data)
        else:
            reduced_data = reduce_to_2d_PCA(np_data)
            reduced_data_df = pd.DataFrame(reduced_data)
            
            fig = get_joint_plot_for_2d_data(data_df=reduced_data_df, \
                                             x_label = 'Principal Component 1', \
                                             y_label = 'Principal Component 2')

    
            st.write('*Reduced dimensions to 2d (PCA) for visualization')
        
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
    
    
