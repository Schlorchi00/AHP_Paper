"""
    File for definining the AHP classes.
"""
import numpy as np
import pandas as pd


class AHP:

    # Placeholder for the consistency ratio values
    CR = [0, 0, 0, 0]

    def __init__(self, arr : np.ndarray, indices : list) -> None:
        self.arr = self._calc_arr(arr)
        self.indices = indices
        

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
    def from_df(cls, df : pd.DataFrame):
        """
            Function to get an AHP element from a 
        """
        raise NotImplementedError("Function to get an ahp")

class AHPTree:
    def __init__(self) -> None:
        raise NotImplementedError("Not Implemented yet. Look at basic trees and how to set these up")
