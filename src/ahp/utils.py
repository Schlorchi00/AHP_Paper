import pandas as pd
import os.path

def uniquify(path : str) -> str:
    """
        Function to turn a path into a unique path if it already exists
    """
    filen, ext = os.path.splitext(path)
    counter = 1
    # addstr = "youalmostdeletedyourdatayoudummy"
    while os.path.exists(path):
        path = filen + "(" + str(counter) + ")" + ext
        counter +=1 
    
    return path


def read_excel(fpath : str, series : bool = False) -> list:
    # multiple workbooks
    with pd.ExcelFile(fpath) as f:
        if not series:
            df = pd.read_excel(f, index_col=0)  # sheet_name=None,
            sheet_name = None
        else:
            df = pd.read_excel(f, index_col=0).squeeze("columns")   #header=None
            sheet_name = f.sheet_names[0]
        # df_list = [df.parse(sheet) for sheet in df.sheet_names]
    # return df_list
    return df, sheet_name

def write_value_excel(df : pd.DataFrame, output_folder : str):
    """
        test file to write a dataframe from recorded values into series excels
    """
    assert os.path.isdir(output_folder), "{} not a directory. needs to be a directory for files to be written".format(output_folder)
    for vn in df.index.to_list():
        ser = df.loc[vn]
        out_fname = os.path.join(output_folder, vn + ".xlsx")
        with pd.ExcelWriter(out_fname) as writer:
            ser.to_excel(writer, sheet_name=vn)
    print("Written {} files to {}".format(len(df.index.to_list()), output_folder))

def write_cost_excel(df : pd.DataFrame, output_path : str):
    """
        Function to write the value dictionary to an output folder
    """
    pass

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
