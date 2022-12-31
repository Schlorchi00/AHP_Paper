"""
    File for definining the AHP classes.
"""
import numpy as np
import pandas as pd
from ahp.utils import read_excel

class AHP:

    # Placeholder for the consistency ratio values
    CR = [0, 0, 0, 0]

    def __init__(self, arr : np.ndarray, indices : list, name : str = None) -> None:
        self.arr = self._calc_arr(arr)
        self.indices = indices
        self.name = name

    @classmethod
    def _calc_arr(cls, arr : np.ndarray) -> np.ndarray:
        raise NotImplementedError("Function to calculate the lower triangular matrix not implemented yet")

    @classmethod
    def __check_vals(cls, arr : np.ndarray) -> bool:
        """
            Function to check the values of the array, if they are within defined ranges
        """
        raise NotImplementedError("Functionto check value ranges and consistencies is not implemented yet")

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
        raise NotImplementedError("Function to get an ahp")
    
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
