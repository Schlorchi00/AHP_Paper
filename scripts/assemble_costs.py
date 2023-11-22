"""
    Script to assemble the costs from multiple data
"""

from ahp.cost_calculation import total_cost, read_sheets
import itertools
import pandas as pd
import os.path
from argparse import ArgumentParser
from ahp.utils import write_cost_excel
import logging
import warnings

# logging.getLogger("pandas").setLevel(logging.ERROR)

def parse_args():
    parser = ArgumentParser(description="Script for combining multiple xlsx sheets that have been output by the cost_combination script into a format usable for preprocessing.\
                            Will use the filename for the name of the material. Standard materials can be appended through the name - value pairing")
    parser.add_argument("-i", "--input", type=str,  required=True, action="append", help="Locations of the excel files. Accepts multiple arguments. Will use the filename for the name of the material")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output location of the file. If None given, will write to terminal")
    
    args = parser.parse_args()
    return vars(args)

# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()

    # set paths
    path_costtable = args['input']
    sd = {}
    for pth in path_costtable:
        basename = os.path.basename(pth).split(".")[0]
        with open(pth, 'rb') as f:
            df_dict = pd.read_excel(f,sheet_name="economical_params", header=0, index_col=0)
        val = df_dict["cost_weighted"]["sum"]
        sd[basename] = val
    df = pd.DataFrame.from_dict(data=sd, orient="index", columns=["total_cost_filament"]).T

    if args["output"]:
        df_scaling = pd.DataFrame(data=pd.NA, index=df.index, columns=["Min", "Max", "Inversion"])
        logging.warning("Scaling sheet appended to {}. Please correct values before using for preprocessing!".format(args["output"]))
        with pd.ExcelWriter(args["output"]) as writer:
            df.to_excel(writer, sheet_name="economical_params")
            df_scaling.to_excel(writer, sheet_name="Scaling")
    else:
        print(df)