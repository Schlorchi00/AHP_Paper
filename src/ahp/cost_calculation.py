import numpy as np
import pandas as pd
import os.path

def read_sheets(path : str) -> dict:
    """
        Function to read ALL sheets from a file and return as a pandas df
        specifically for the cost format
    """
    with open(path, 'rb') as f:
        df_dict = pd.read_excel(f,sheet_name=None, header=[0,1])  # sheet_name=None
    # TODO: changing the index
    # basename = _get_basename(path)
    # for df in df_dict:
    #     df['material'] = basename
    #     df.set_index('material')
    return df_dict

def _get_basename(path : str) -> str:
    return os.path.basename(path).split('.')[0]

##### Calculation Section
def mach_purch_cost(df : pd.DataFrame):
    rc = df.iloc[:,3]
    pc = df.iloc[:,1]
    am = df.iloc[:,2]
    mach_Pc = _mach_purch_cost(rc, pc, am)
    return mach_Pc

def _mach_purch_cost(running_cost: int, purchase_cost : int, amortization : int):
    return amortization * purchase_cost / (0.95 * 24 * 365 * running_cost)

# def maschine_purchase_cost(df_process):
#     """
#     calculates the relative purchase cost of the machine
#     :param df_process: dataframe values of the process/machine
#     :return: purchase machine cost
#     """

#     return (df_process.iloc[:,0].values*df_process.iloc[:,1].values)/(0.95*24*365*df_process.iloc[:,3].values)

def operational_cost(df : pd.DataFrame, time : bool=False):
    """
        returns the operational cost. If time is False, uses energy. If time is True, uses time values from the dataframe 
    """
    if time:
        val_1 = df.iloc[3]
        val_2 = df.iloc[5]
    else:
        val_1 = df.iloc[4]
        val_2 = df.iloc[6]
    return _operational_cost(val_1, val_2)

def _operational_cost(val_1, val_2):
    """
        calculates the machine cost regarding
    """
    return val_1 * val_2

# def operational_cost(df_process, int):

#     """
#     calculates the operational cost of the maschine process
#     :param df_process: dataframe values of the process/machine
#     :param int: 0 - calculates the machine cost regarding time; 1 - calculates the machine cost regarding energy
#     :return: operational cost
#     """
#     #cost calculation regarding time
#     if int == 0:
#         return df_process.iloc[:,3]*df_process.iloc[:,5]
#     #cost calculaiton regarding energy
#     else:
#         return df_process.iloc[:,4]*df_process.iloc[:,6]


def material_cost(df : pd.DataFrame):
    c1 = df.iloc[11]
    c2 = df.iloc[12]
    mc = _material_cost(c1 , c2)
    return mc

def _material_cost(c1 : int, c2 : int):
    return c1 * c2

# def material_cost(df_process):
#     """
#     calculates the material cost used for the machine process
#     :param df_process: dataframe values of the process/machine
#     :return: material cost
#     """

#     return df_process.iloc[:,11]*df_process.iloc[:,12]

def labour_cost(df : pd.DataFrame):
    """
        calculates labour cost
    """
    v1 = df.iloc[7]
    v2 = df.iloc[8]
    v3 = df.iloc[9]
    v4 = df.iloc[10]
    return _labour_cost(v1, v2, v3, v4)

def _labour_cost(v1, v2, v3, v4):
    """
        calculation of labour cost
    """
    return (v1 + v2 + v3) / v4

# def labour_cost(df_process):
#     """
#     calculates the labour cost regarding prae, proc, post
#     :param df_process: dataframe values of the process/machine
#     :return: labour cost
#     """

#     return (df_process.iloc[:,7]+df_process.iloc[:,8]+df_process.iloc[:,9])/df_process.iloc[:,10]

def maintenance_cost(df : pd.DataFrame):
    """
        Function to calculate the maintenance cost
    """
    v1 = df.iloc[13]
    v2 = df.iloc[14]
    v3 = df.iloc[17]
    v4 = df.iloc[15]
    v5 = df.iloc[16]
    return _maintenance_cost(v1,  v2, v3, v4, v5)

def _maintenance_cost(v1, v2, v3, v4, v5):
    return ((v1 + v2 * v3) * v4) / (0.95 * 24 * 365 * v5)

# def maintenance_cost(df_process):
#     """
#     calculates the maintenance cost
#     :param df_process: dataframe values of the process/machine
#     :return: maintenance cost
#     """

#     return ((df_process.iloc[:,13]+df_process.iloc[:,14]*df_process.iloc[:,17])*df_process.iloc[:,15])\
#            /(0.95*24*365*df_process.iloc[:,16])


def cost_position(df_process):
    """
    Accumulates the cost position of the machine regarding all cost position elements
    :param df_process: dataframe values of the process/machine
    :return: overall cost of one cost position
    """

    mpc = maschine_purchase_cost(df_process)
    oc = operational_cost(df_process, 1)
    mc = material_cost(df_process)
    lc = labour_cost(df_process)
    mtc = maintenance_cost(df_process)

    return mpc + oc + mc + lc + mtc

def total_cost(df_list):
    """
    calculates the cost of all cost positions
    :param df_list: list of all cost positions
    :return: total cost of the process cost
    """

    tot_cost = 0
    for el in df_list:
        cost_pos = cost_position(el)
        tot_cost +=cost_pos

    return tot_cost[0]







