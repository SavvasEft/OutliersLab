## data:

Data managed by methods should be np.array, with well defined shape: (no_of_points, no_of_features)

Where: The format of the data throughout the tool is defined in src\data_processing\DataReader.py 

## data_index:

data_index is automatically assigned by the tool in each method. 

Data index is an np.array
of shape (no_of_points, ).

i.e. [0,1,2,3,4,5] for 6 data points (of any no of features)


## methods:

Goal:    each method will identify outliers from data.
Output:  'outlier_bool' , an np.array column, of shape (no_of_points, 1), with True and False. Outliers are marked with True being the data points that are identified by method as outliers. 

Outliers (or clean data) are able to be obtained by 'data[outlier_bool]' (or 'data[np.invert(outlier_bool)])'

Where: 
    - simple statistics methods, are functions that are defined in src\models\StatsMethods.py
    - other methods are defined by their name in src\models