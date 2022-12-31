import pandas as pd

def read_excel(fpath : str) -> list:
    # multiple workbooks
    with open(fpath, 'rb') as f:
        df = pd.read_excel(f, sheet_name=None, index_col=0)
        # df_list = [df.parse(sheet) for sheet in df.sheet_names]
    # return df_list
    return df
