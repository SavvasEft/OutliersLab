import numpy as np
from sklearn.datasets import make_blobs

def get_1d_distr_with_outliers():
    x1 = np.random.normal(0,1,1000)
    x2 = np.random.normal(0,5,30)
    data_1d = np.append(x1, x2)
    np.random.shuffle(data_1d)
    data_1d = np.reshape(data_1d, (1030,1))  
    return data_1d

def get_2d_distr_with_outliers():
    x1 = np.random.normal(-3,3,500)
    x2 = np.random.normal(9,0.7,150)
    x = np.append(x1, x2)
    y1 = np.random.normal(-3,3,500)
    y2 = np.random.normal(5,3,150)
    y = np.append(y1, y2)
    data_2d = np.array([x,y])
    np.random.shuffle(data_2d)
    return data_2d.T

def get_4d_data_norm():
    data = np.random.randn(16000)
    data = data.reshape(4000,4)
    return data

def get_4d_data_5clusters():
    data, labels = make_blobs(n_samples=1100,n_features=4, centers=5)
    return data, labels