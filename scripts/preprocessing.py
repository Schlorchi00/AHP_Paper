import os.path
import openpyxl
from ahp.utils import *


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


def print_something():
    print("Use this structure to develop functions. Only move to utils when done")

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

#create data frames

def create_df(df_path):
    """
    modifies a workbook into a suitable dataframe
    :param wb: workbook
    :return: dataframe
    """
    wb = openpyxl.load_workbook(df_path)

    if not wb.sheetnames == None:

        df = pd.read_excel(df_path)
        df.drop(df.index[0])
        p_node_name = wb.sheetnames
        df = df.set_index(df.columns[0])

        return df, p_node_name

def extract_params(df):
    """
    extract params, alternativ, and leaf values
    :param df: dataframe of the parameters
    :return: list of params, alternatives and leaf values
    """
    df = df.T
    param_dict = df.to_dict()
    dict_params = list(param_dict.keys())
    dict_alternatives = list(param_dict[next(iter(param_dict))].keys())

    leaf_values = []

    for key, value in param_dict.items():

        leaf_values.append(list(value.values()))

    return dict_params, dict_alternatives, leaf_values






if __name__=="__main__":

    print_something()

    #read files TODO: Check correctness regarding amount of leaf nodes

    df_path_eco = read_domain('ecology_format', 'LCA_PLA_Cuboid.xlsx')
    #create df
    df_eco, p_node_name_eco = create_df(df_path_eco)

    #extract params

    eco_params, eco_alternatives, eco_leaf_values = extract_params(df_eco)








    # preprocess here

    # read files
    #read_from_xlsx()

    # write to excel file
    #write_to_xlsx()