import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import os
import sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_directory) # defined root folder 1 step up

from src.data_processing.DataReader import DataReader




df_data = None
uploaded_type = st.radio(label = 'Choose file type:', options=['.xlsx','.csv'])


def get_initial_graphs(np_data):
    "data: np.array"
    fig, [ax1, ax2] = plt.subplots(2,1)
    ax2.hist(np_data, int(len(np_data)/4))
    ax1.plot(np_data)
    return fig

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


if df_data is not None:

    st.write('Data preview:')
    col1, col2 =st.columns([0.25, 0.75])    
    

    
    with col1:
        st.write(df_data)

    with col2:
        fig = get_initial_graphs(np_data)
        st.pyplot(fig)
    
    if 'df_data' not in st.session_state:
        st.session_state['df_data'] = df_data
    st.session_state['df_data'] = df_data
    
    if 'np_data' not in st.session_state:
        st.session_state['np_data'] = np_data
    st.session_state['np_data'] = np_data
    


    

