import numpy as np

def get_1d_distr_with_outliers():
    x1 = np.random.normal(0,1,1000)
    x2 = np.random.normal(0,5,30)
    data_1d = np.append(x1, x2)
    np.random.shuffle(data_1d)
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

    return data_2d