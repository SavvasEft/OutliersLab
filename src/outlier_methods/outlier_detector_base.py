from abc import ABC, abstractmethod

import numpy as np

class DetectorBase(ABC):

    @abstractmethod
    def get_outlier_mask(self, data:np.ndarray):
        pass
    
    @abstractmethod
    def get_plot(self, data:np.ndarray, outlier_mask:np.ndarray):
        pass