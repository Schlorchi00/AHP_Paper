"""
    File for definining the AHP classes.
"""
import numpy as np
import pandas as pd
from src.ahp.utils import read_excel

class AHP:

    # Placeholder for the consistency ratio values
    CR = [0, 0, 0, 0]

    # Accepteable values
    pos = [i for i in range(1,10)]
    neg = [1./i for i in range(2,10)]
    ACCEPTED = np.array(neg[::-1] + pos)
    def __init__(self, arr : np.ndarray, indices : list, name : str = None) -> None:
        self.arr = self._calc_arr(arr)
        self.indices = indices
        self.name = name

    @classmethod
    def _calc_arr(cls, arr : np.ndarray) -> np.ndarray:
        """
            Calculates the matrix by using the values of the upper triangular matrix for the lower triangular matrix
        """
        i_lower = np.tril_indices(arr.shape[0], -1)
        arr[i_lower] = 1./ arr.T[i_lower]
        cls.__check_vals(arr)
        return arr

    @classmethod
    def __check_vals(cls, arr : np.ndarray) -> bool:
        """
            Function to check the values of the array, if they are within defined ranges
            TODO: use the numpy tolerance checks here
        """
        unq_vals = np.unique(arr)
        
        set_in = set(arr.flatten())
        set_test = set(cls.ACCEPTED)
        # assert set_in.issubset(set_test), f"Input values not a subset of valid values: {cls.ACCEPTED}"
        return True
        
    def is_consistent(self) -> bool:
        """
            Function to calculate whether an array is consistent
        """
        raise NotImplementedError("Function to get consistency is not implemented yet")

    @classmethod
    def from_df(cls, df : pd.DataFrame, name=None):
        """
            Function to get an AHP element from a 
        """
        return cls(df.values, df.columns.to_list(), name = name)
    
    @classmethod
    def from_file(cls, path : str):
        """
            Function to get AHP matrices from a file.
            Reads every workbook
        """
        dfdict = read_excel(path)
        ahplist = [AHP.from_df(df, name) for name, df in dfdict.items()]
        return ahplist
        
class AHPTree:
    def __init__(self) -> None:
        raise NotImplementedError("Not Implemented yet. Look at basic trees and how to set these up")
