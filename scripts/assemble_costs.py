"""
    Script to assemble the costs from multiple data
"""

from src.ahp.cost_calculation import total_cost, read_sheets
import itertools
import pandas as pd
import os.path
from argparse import ArgumentParser
from src.ahp.utils import write_cost_excel, uniquify
import logging
import warnings

# logging.getLogger("pandas").setLevel(logging.ERROR)

def parse_args():
    parser = ArgumentParser(description="Script for combining multiple xlsx sheets that have been output by the cost_combination script into a format usable for preprocessing.\
                            Will use the filename for the name of the material. Standard materials can be appended through the name - value pairing")
    parser.add_argument("-i", "--input", type=str,  required=True, action="append", help="Locations of the excel files. Accepts multiple arguments. Will use the filename for the name of the material")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output location of the file. If None given, will write to terminal")
    parser.add_argument("-n", "--name", action="append", help="Name of a material - will be used in output file. Caution - keep order!")
    parser.add_argument("-v", "--value", action="append", help="Value of material - will be used in output file. Caution - keep order!")
    args = parser.parse_args()
    return vars(args)

# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()

    # read in files
    path_costtable = args['input']
    sd = {}
    for pth in path_costtable:
        basename = os.path.basename(pth).split(".")[0]
        with open(pth, 'rb') as f:
            df_dict = pd.read_excel(f,sheet_name="economical_params", header=0, index_col=0)
        val = df_dict["cost_weighted"]["sum"]
        sd[basename] = val

    # read in name - value pairs
    ns = args["name"]
    vs = args["value"]
    if ns:
        assert len(ns) == len(vs), "Not the correct number of values provided for names. Check if number coincides"
        for i, n in enumerate(ns):
            sd[n] = float(vs[i])

    df = pd.DataFrame.from_dict(data=sd, orient="index", columns=["economical"]).T

    if args["output"]:
        output_folder = args["output"]
        out_fname = os.path.join(output_folder + df.index[0] + ".xlsx")
        out_fname = uniquify(out_fname)
        df_scaling = pd.DataFrame(data=pd.NA, index=df.index, columns=["Min", "Max", "Inversion"])
        logging.warning("Scaling sheet appended to {}. Please correct values before using for preprocessing!".format(args["output"]))
        with pd.ExcelWriter(out_fname, engine = 'openpyxl') as writer:
            df.to_excel(writer, sheet_name="economical_params")
            df_scaling.to_excel(writer, sheet_name="Scaling")
    else:
        print(df)