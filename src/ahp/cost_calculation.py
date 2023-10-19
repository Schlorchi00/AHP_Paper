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
    ser = df['machine_cost']
    v1 = ser['machine_purchase_cost_[€]'][0]
    v2 = ser['production_time_[y]'][0]
    # ! CHECK IF THIS value below IS CORRECT
    # todo: Changed into machine_life_span
    v3 = ser['machine_life_span_[y]'][0]
    mach_Pc = _mach_purch_cost(v1, v2, v3)
    return mach_Pc

def _mach_purch_cost(v1: int, v2 : int, v3 : int):
    return v1 * v2 / (0.95 * 24 * 365 * v3)

# def maschine_purchase_cost(df_process):
#     """
#     calculates the relative purchase cost of the machine
#     :param df_process: dataframe values of the process/machine
#     :return: purchase machine cost
#     """

#     return (df_process.iloc[:,0].values*df_process.iloc[:,1].values)/(0.95*24*365*df_process.iloc[:,3].values)

def operational_cost(df : pd.DataFrame, time : bool):
    """
        returns the operational cost. If time is False, uses energy. If time is True, uses time values from the dataframe 
    """
    ser = df['operational_cost']
    if time:
        val_1 = ser['production_time_[y]'][0]
        val_2 = ser['operational_rate_time_[y/kWh]'][0]
    else:
        val_1 = ser['production_energy_[kWh]'][0]
        val_2 = ser['operational_rate_energy_[€/kWh]'][0]
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
    ser = df['material_cost']
    c1 = ser['production_mass_[kg]'][0]
    c2 = ser['material_rate_[€/kg]'][0] #TODO: €/g
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
    ser = df['labour_cost']
    v1 = ser['praeprocess_[h]'][0]
    v2 = ser['process_[h]'][0]
    v3 = ser['postprocess_[h]'][0]
    v4 = ser['labour_rate_[€/h]'][0]
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
    ser = df['maintenance_cost']
    ser1 = df['labour_cost']
    v1 = ser['cost_spare_parts_[€]'][0]
    v2 = ser['labour_time_[h]'][0]
    v3 = ser1['labour_rate_[€/h]'][0]
    v4 = ser['production_time_[y]'][0]
    v5 = ser['machine_life_span_[y]'][0]
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


def cost_position(df : pd.DataFrame, time : bool):
    """
    Accumulates the cost position of the machine regarding all cost position elements
    :param df_process: dataframe values of the process/machine
    :return: overall cost of one cost position
    TODO: could pass the series in here instead of the dfs. Check first if machine purchase cost v3 is correct
    """

    mpc = mach_purch_cost(df)
    oc = operational_cost(df, time=time)
    mc = material_cost(df)
    lc = labour_cost(df)
    mtc = maintenance_cost(df)
    mtc = _isnotna(mtc)
    mpc = _isnotna(mpc)
    lc = _isnotna(lc)
    oc = _isnotna(oc)
    mc = _isnotna(mc)
    return mpc + oc + mc + lc + mtc

def _isnotna(val):
    return 0. if np.isnan(val) else val

def total_cost(wbs : dict[pd.DataFrame], time: bool):
    """
    calculates the cost of all cost positions
    :param df_list: list of all cost positions
    :return: total cost of the process cost
    """

    tot_cost = 0
    for k, df in wbs.items():
        tot_cost += cost_position(df, time=time)

    return tot_cost







