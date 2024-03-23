## data:

Data managed by methods should be np.array, with well defined shape: (no_of_points, no_of_features). 

In case of 1 feature only, 1-column data, dimensions should be (no_of_points, 1) and not (no_of_points, )

X{array-like, sparse matrix} of shape (n_samples, n_features)

Where: The format of the data throughout the tool is defined in src\data_processing\DataReader.py

## data_index:

data_index is automatically assigned by the tool in each method. 

Data index is an np.array
of shape (no_of_points, 1).

i.e. [0,1,2,3,4,5] for 6 data points (of any no of features)


## methods:

Goal:    each method will identify outliers from data.
Output:  'outlier_bool' , an np.array column, of shape (no_of_points, ), with True and False.
         the specific format allows to filter easily 1d and 2d array by boolean index

Outliers are marked with True, non_outliers with False.

Outliers (or clean data) are able to be obtained by 'data[outlier_bool]' (or 'data[np.invert(outlier_bool)])'

Where: 
    - statistic methods, are functions that are defined in src\models\StatsMethods.py
    (currently z-score & IQR)
    - other methods are defined by their name in src\models
    (currently isolation forest)