import os.path
import openpyxl
import numpy as np
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

def norm_values(leaf_values, flag=0):
    """
    Normalization of leaf values
    :param leaf_values: list of leaf values
    :param flag: integer: 0 = normalization_max (default); else: normalization_min
    :return: normalized array of leaf values
    """

    leaf_values_arr = np.array(leaf_values)
    row_amount = list(range(len(leaf_values_arr)))

    if flag == 0:
        leaf_values_arr_norm = normalize_max(leaf_values_arr, row_amount)

    else:
        leaf_values_arr_norm = normalize_min(leaf_values_arr, row_amount)

    return leaf_values_arr_norm

def min_max_threshold(leaf_value_list, value_params):
    """
    extension of value list with min and max threshold
    :param leaf_value_list: list of leaf values
    :param value_params: list of parameter names
    :return: extended value list
    """

    for i in range(len(leaf_value_list)):

        min_val = float(input('Whats the minimum value for {} ?'.format(value_params[i])))
        max_val = float(input('Whats the maximum value for {} ?'.format(value_params[i])))
        eco_leaf_values[i].insert(0, min_val)
        eco_leaf_values[i].append(max_val)

    return leaf_value_list


if __name__=="__main__":

    print_something()

    #read files TODO: Check correctness regarding amount of leaf nodes

    df_path_eco = read_domain('ecology_format', 'LCA_PLA_Cuboid.xlsx')

    #create df
    df_eco, p_node_name_eco = create_df(df_path_eco)

    #extract params

    eco_params, eco_alternatives, eco_leaf_values = extract_params(df_eco)

    #add min-max-treshold

    eco_leaf_values_ext = min_max_threshold(eco_leaf_values, eco_params)

    #normalization procedure

    #TODO: normalization flag -> user-decided?
    eco_leaf_values_norm = norm_values(eco_leaf_values, 1)


    #transform
    '''
    def myfunction(x):
    return x[0] + x[1]**2 + x[2]**3

    print(np.apply_along_axis(myfunction, axis=1, arr=myarray))
    
    transform each row into a 1 x len(array) vector
    save row as excel with param_name
    
    '''







    # preprocess here

    # read files
    #read_from_xlsx()

    # write to excel file
    #write_to_xlsx()