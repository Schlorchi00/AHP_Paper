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
