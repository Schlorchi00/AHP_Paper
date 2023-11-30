import os.path
import numpy as np
import pandas as pd

from ahp.utils import read_excel


def read_domain(subdomain, filename, data = 'data'):
    """
    loads excel files and creates workbook
    :param subdomain: string of the name regarding the subdomain
    :param filename: string of filename.xlsx
    :param data: string of the foldername
    :return: workbook
    """

    ppath = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    datadir = os.path.join(ppath, '..', data, subdomain)
    df_path = os.path.join(datadir,filename)
    return df_path

def create_df(df_path) -> tuple[pd.DataFrame, str]:
    """
    modifies a workbook into a suitable dataframe
    :param wb: workbook
    :return: dataframe
    """
    # reusing previous functions from utils
    df, _ = read_excel(df_path, False)
    # returning the sheet name for the node name
    dff = pd.ExcelFile(df_path).sheet_names[0]
    # adding the argument whether scaling is used
    return df, dff

#TODO: What if best value is a value in between

def get_scaling(df_path) -> pd.DataFrame:
    """
        gets the scaling from the SECOND sheet name
    """
    scale_df = pd.read_excel(df_path, 1, index_col=0, header=0).squeeze("columns")
    return scale_df

def apply_scaling(df : pd.DataFrame, df_scale : pd.DataFrame) -> pd.DataFrame:
    """
        Function to apply the scaling according to the values set out by the scaling.
        If "Optimum" is supplied, only "Threshold" will be considered as second option.

    """
    df2 = df.copy(deep=True)
    # print(df2)
    for idx, row in df.iterrows():
        # print(idx)
        mi = df_scale.at[idx, "Min"]
        ma = df_scale.at[idx, "Max"]
        inv = df_scale.at[idx, "Inversion"]
        try:
            quad = df_scale.at[idx, "Optimal"]
            thr = df_scale.at[idx, "Threshold"]
        except KeyError:
            quad = None
            thr = None
        # Quadratic scaling or linear scaling
        if pd.notna(quad) and pd.api.types.is_numeric_dtype(quad):
            row = apply_quadratic_scaling(row, quad, thr)
        else:
            row = apply_linear_scaling(row, mi, ma, inv)
        # this could be turned into functional programming... if we want to
        df2.loc[idx,:] = row
    return df2

def apply_linear_scaling(row, mi, ma, inv):
    """
        Linear scaling function.
        Parameters:
            * row
            * minimum
            * maximum
            * inversion
    """
    if not pd.notna(mi):
        mi = row.min()        
    row = row - mi
    ma -= mi
    if pd.notna(ma):
        row = row / ma
    else:
        row = row / row.max()
    if inv and pd.notna(inv):
        row = 1 - row
    return row

def apply_quadratic_scaling(row, quad, thr):
    """
        Applying the quadratic scaling function
    """
    row = (row - quad).abs()    # calculate absolute distance to the optimal value - already a min-scaling
    if thr and pd.notna(thr):   # if a threshold is supplied, turn every value larger than the threshold to a 1.
        # row[row >= thr] = 1.
        # perform maximum scaling here
        row = row / thr
        row[row >= 1.] = 1.
    else:
        # if no threshold is supplied - minimum is always the value in "quad" - which is already used. basically have to perform maximum scaling now
        row = row / row.max()
    
    # always invert
    row = 1 - row
    return row

def empty_scaling(df : pd.DataFrame) -> pd.DataFrame:
    """
        Function to return empty scaling. No inversion, no min max values, nothing
    """
    df2 = df.sub(df.min(axis=1), axis=0)
    df2 = df2.div(df2.max(axis=1), axis=0)
    return df2

def check_consistency(df : pd.DataFrame):
    assert not (df < 0).any().any(), "Dataframe has negative values. Check for consistency"
    assert not (df > 1.0).any().any(), "Dataframe has values larger than 1. Check for consistency"
