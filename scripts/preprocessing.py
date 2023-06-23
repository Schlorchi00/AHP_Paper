import os.path
import openpyxl
import numpy as np
from ahp.utils import *
from argparse import ArgumentParser

"""
    Usage:
        1. activate environment in command line `conda activate <env_name>`
        2. run in command line from parent folder (e.g. the one above scripts) python scripts/preprocessing.py -i data/ecology_format/LCA_PLA_Cuboid.xlsx
        3. OPTIONAL - to use scaling, which is in SECOND SHEET of the file, use --scaling or -s argument
        4. OPTIONAL - to store as xlsx files, provide additional -o argument with a directory. P.ex. `[...] -o data/test_output`
"""

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)
    parser.add_argument("-o", "--output", type=str, help="Directory where the <value> files should be output to. Default None, \
                        if None, will print to command line", default=None)
    parser.add_argument("--scaling","-s", action="store_true", help="Whether a second sheet will be supplied that provides scaling for the parameters")
    args = parser.parse_args()
    return vars(args)

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

def create_df(df_path):
    """
    modifies a workbook into a suitable dataframe
    :param wb: workbook
    :return: dataframe
    """
    # reusing previous functions from utils
    df = read_excel(df_path, False)
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
        if quad and pd.notna(quad):
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
    if pd.notna(mi):
        row = row - mi
    else:
        row = row - row.min()
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
    assert (df > 0).any().any(), "Dataframe has negative values. Check for consistency"
    assert (df <= 1.0).any().any(), "Dataframe has values larger than 1. Check for consistency"
    return True

if __name__=="__main__":
    args = parse_args()
    #read files TODO: Check correctness regarding amount of leaf nodes
    # df_path_eco = read_domain('ecology_format', 'LCA_PLA_Cuboid.xlsx')
    #create df
    df_eco, p_node_name_eco = create_df(args["input"])
    if args["scaling"]:
        scale_df = get_scaling(args["input"])
        # apply the scaling
        df2 = apply_scaling(df_eco, scale_df)
    else:
        # case when the normal values are used to generate the values
        df2 = empty_scaling(df_eco)
    check_consistency(df2)
    if args["output"]:
        write_value_excel(df2, args["output"])
    else:
        print("No output directory supplied. Dataframe to write into Excels looks like:")
        print(df2)

    