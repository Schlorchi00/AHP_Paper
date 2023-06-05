import numpy as np
import pandas as pd
import openpyxl



#create data frames

def create_df(wb):
    """
    modifies a workbook into a suitable dataframe
    :param wb: workbook
    :return: dataframe
    """

    df = pd.DataFrame(wb.values)
    df = df.rename(columns=df.iloc[1])
    df = df.iloc[2:,:].reset_index(drop=True)

    return df


def maschine_purchase_cost(df_process):
    """
    calculates the relative purchase cost of the machine
    :param df_process: dataframe values of the process/machine
    :return: purchase machine cost
    """

    return (df_process.iloc[:,0].values*df_process.iloc[:,1].values)/(0.95*24*365*df_process.iloc[:,3].values)

def mach_purch_cost(df):
    rc = df.iloc[:,3]
    pc = df.iloc[:,1]
    am = df.iloc[:,2]
    mach_Pc = _mach_purch_cost(rc, pc, am)
    return mach_Pc

def _mach_purch_cost(running_cost: int, purchase_cost : int, amortization : int):
    return amortization * purchase_cost / (0.95 * 24 * 365 * running_cost)

def operational_cost(df_process, int):

    """
    calculates the operational cost of the maschine process
    :param df_process: dataframe values of the process/machine
    :param int: 0 - calculates the machine cost regarding time; 1 - calculates the machine cost regarding energy
    :return: operational cost
    """

    #cost calculation regarding time
    if int == 0:
        return df_process.iloc[:,3]*df_process.iloc[:,5]

    #cost calculaiton regarding energy
    else:
        return df_process.iloc[:,4]*df_process.iloc[:,6]


def material_cost(df_process):
    """
    calculates the material cost used for the machine process
    :param df_process: dataframe values of the process/machine
    :return: material cost
    """

    return df_process.iloc[:,11]*df_process.iloc[:,12]

def material_cost(df):
    mc = _material_cost(df.iloc[11], df.iloc[12])
    return mc

def _material_cost(c1 : int, c2 : int):
    return c1 * c2

def labour_cost(df_process):
    """
    calculates the labour cost regarding prae, proc, post
    :param df_process: dataframe values of the process/machine
    :return: labour cost
    """

    return (df_process.iloc[:,7]+df_process.iloc[:,8]+df_process.iloc[:,9])/df_process.iloc[:,10]



def maintenance_cost(df_process):
    """
    calculates the maintenance cost
    :param df_process: dataframe values of the process/machine
    :return: maintenance cost
    """

    return ((df_process.iloc[:,13]+df_process.iloc[:,14]*df_process.iloc[:,17])*df_process.iloc[:,15])\
           /(0.95*24*365*df_process.iloc[:,16])


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







