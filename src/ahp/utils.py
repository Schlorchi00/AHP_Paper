import pandas as pd

def read_excel(fpath : str, series : bool = False) -> list:
    # multiple workbooks
    with open(fpath, 'rb') as f:
        if not series:
            df = pd.read_excel(f, index_col=0)  # sheet_name=None,
        else:
            df = pd.read_excel(f, index_col=0, header=None).squeeze("columns")
        # df_list = [df.parse(sheet) for sheet in df.sheet_names]
    # return df_list
    return df


##################
# TODO: Utility functions for preprocessing below
##############

def read_from_xlsx():
    raise NotImplementedError("There is another function here called read_excel. maybe use this one")

def write_to_xlsx():
    raise NotImplementedError("Not implemented yet")

#normalization I
def normalize_max(arr,rownumber):
    '''
    normalization, if considering highest value as reference

    :param arr: array of normalizing values
    :param rownumber: size of array to normalize
    :return: normalized array
    '''
    return ((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min())

#normalization II
def normalize_min(arr,rownumber):
    '''
    normalization, if considering smallest value as reference

    :param arr: array of normalizing values
    :param rownumber: size of array to normalize
    :return: normalized array
    '''
    return 1-(((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min()))
