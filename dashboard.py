print ('---'*35)
print ('--')
print ('Dashboard Homepage starting...')
print ('--')

import streamlit as st

st.header('Welcome to Outliers Lab!')
st.markdown("""
- Outliers Lab helps you identify outliers in your dataset, or in a toy-dataset.  
""", unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")
st.subheader('Getting started:')

st.markdown("""
- Choose **"Get Data"** in the menu on the left to upload your data (or choose between toy-datasets).  
""", unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")

parent_directory = os.path.dirname(os.path.dirname(__file__))
st.write(parent_directory)

st.subheader('Checklist for uploaded data:')
 
st.markdown("""

- [ ] File format: **.csv** or **.xlsx** .
- [ ] File size: **smaller than 200Mb**.
- [ ] Data in **tabular form**. <br>
    Columns : features,<br> 
    Rows : data instances
- [ ] Data should **not have missing data**.
- [ ] ***Data to be analyzed*** (read next paragraph) are **numeric**.


Data can also include indices and/or column names. If they do, then when uploaded, user should choose from the options: **'First row has column names'**  and/or **'First column has indices'** accordingly.
***Data to be analyzed*** depend on the choices of the user.
""", unsafe_allow_html=True)


st.text("")
st.text("")
st.text("")


st.subheader('Features at a Glance:')
st.text("")

st.markdown("""
- **Upload a dataset or experiment with toy-datasets**  
    - 📁 Upload any numerical dataset you have. Currently we support .csv and .xlsx files.
    - 🔍 Don't have a dataset and want to explore the various outlier detection methods? Choose between toy-datasets available.
    <br>
    <br>
- **Various Outlier Detection Methods**  
    - 🔬 Quickly explore various methods to find the most suitable one for your dataset. 
    - 🛠️ Fine-tune each method and evaluate the results with intuitive visualizations.
    - 🧭 Identify which methods perform well on what kind of data by exploring its performance on toy-datasets.  
    <br>
    <br>
- **Combining Detection Methods**  
    - 🔗 Not satisfied with one? Choose various methods and combine them to have a better result.
    <br>
    <br>
- **Export Options**  
    - 💾 Conveniently save and export your findings. Options include:
        - Clean your data data post-analysis.
        - Generate a detailed outlier report.
        - Export visual graphs for presentations.
        - Save outlier labels for further processing in yout workflow.
""", unsafe_allow_html=True)


print ('--')
print ('Dashboard homepage done!!!')
print ('--')
print ('---'*35)