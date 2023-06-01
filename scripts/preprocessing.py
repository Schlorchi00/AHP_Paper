import os.path
import openpyxl
import numpy as np
from ahp.utils import *
from argparse import ArgumentParser

"""
        ! Required for Preprocessing
            * from an excel file
        
        ! Structure Data
            * Expected Table structure:
                                Atlernative I   Alternative II  ... Alternative n
                    Param I         Value           Value       ...     Value
                    Param II        ...
                    Param III       ...                                     
                    Param ...n      ...
                    
                    Sheetname = Parentnode name
                    
                    
        ! Preprocessing should be 
        TODO:
            * [ ] save normalized .xlsx -file
                * [ ] transform param matrix into 1 x len(altneratives) 
                    * [ ] check which normalization method is required
                    * [ ] apply normalization method
                        * [ ] define if minimum or maximum threshold is required (maybe with flag)
                        * [ ] set thresholds in first and last column (maybe other module)
                            * [ ] Extract params (other module) #TODO: Tables in one format /Sheetname Change to parent node name
                            + [ ] Store them in dictionary
                                * load  .xlsx - file
                                
            * [ ] save total cost .xlsx - file
                * [ ] horizontal stack of alternatives 
                    * [ ] Get standard (virgin) alternative
                    * [ ] Get unmodified (lab calculation) alternative(s) 
                    * [ ] Get modified (industrial calculation) alternative(s)
                        * [ ] calculation of unmodified alternative -> cost calculation
                        * [ ] calculation of modified alternative -> how to change cost calculation script (other module)
                            

                
"""

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)
    parser.add_argument("-o", "--output", type=str, help="Directory where the <value> files should be output to. Default None, \
                        if None, will print to command line", default=None)
    parser.add_argument("--scaling", action="store_true", help="Whether a second sheet will be supplied that provides scaling for the parameters")
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

def get_scaling(df_path):
    """
        gets the scaling from the SECOND sheet name
    """
    scale_df = pd.read_excel(df_path, 1, index_col=0, header=0).squeeze("columns")
    return scale_df

def apply_scaling(df : pd.DataFrame, df_scale : pd.DataFrame) -> pd.DataFrame:
    """
        Function to apply the scaling according to the values set out by the scaling
    """
    df2 = df.copy(deep=True)
    # print(df2)
    for idx, row in df.iterrows():
        print(idx)
        mi = df_scale.at[idx, "Min"]
        ma = df_scale.at[idx, "Max"]
        inv = df_scale.at[idx, "Inversion"]
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
        print(row)
        df2.loc[idx,:] = row
    # print(df2)
    return df2

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

if __name__=="__main__":
    
    #read files TODO: Check correctness regarding amount of leaf nodes
    df_path_eco = read_domain('ecology_format', 'LCA_PLA_Cuboid.xlsx')

    scaling = False  # late TODO: move to arg
    #create df
    df_eco, p_node_name_eco = create_df(df_path_eco)
    if scaling:
        scale_df = get_scaling(df_path_eco)
        # apply the scaling
        df2 = apply_scaling(df_eco, scale_df)
    else:
        # case when the normal values are used to generate the values
        df2 = empty_scaling(df_eco)
        print(df2)
    check_consistency(df2)

    # Write to excel
    # TODO: Continue here
    