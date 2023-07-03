"""
    Input format:
        * data/cost/PLA_cost_table.xlsx
    Output format:
        * data/cost_format/Cost_PLA.xlsx
            * PLA_Virgin - is one input value
            * PLA_recycled - kommt aus input_format
                * benutzt berechnungen in cost_calculation
            * PLA_recycled industrial - kommt aus input format, aber mit anderen werten.
        * 2 x input XLSX - werden genau gleich berechnet
        * 1 x fixer wert - von command line
        * Format was rauskommt sollte im gleichen format sein wie die anderen VALUES-RAW excel, vor Skalierung!
    NEXT STEP:
        * soll den gleichen verlauf gehen wie die anderen dateien durch scripts/preprocessing

    TODO NIKO:
        * cost of spare parts ist normalerweise "cost spare parts" und in Extrusion "cost of spare parts" -> name muss gleich sein!!
        * gleieches fuer machine_purchase_cost -> machine_purchase cost
    
"""

from ahp.cost_calculation import total_cost, read_sheets
import pandas as pd
import os.path
from argparse import ArgumentParser
from ahp.utils import write_cost_excel

def parse_args():
    parser = ArgumentParser(description="File for running a cost calculation. Inputs can be provided over multiple excel files, or as a name-value pair. Use --input for providing excel files as a list (append by using --input <file1> --input <file2>\
                            Use name-value pairs by using multiple --name and multiple --value tags. Must be same length and in order, otherwise will throw error.")
    parser.add_argument("-i", "--input", type=str,  required=True, action="append", help="Location of the cost excel file. Accepts multiple arguments")
    parser.add_argument("-n", "--name", action="append", help="Name of a material - will be used in output file. Caution - keep order!")
    parser.add_argument("-v", "--value", action="append", help="Value of material - will be used in output file. Caution - keep order!")
    parser.add_argument("-t", "--time", help="Whether to use time or energy for operational cost calculation. Defaults to energy.", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output location of the file. If None given, will write to terminal")
    parser.add_argument("-s", "--scale", type=float, required=True, action="append", help="Weight of recycling mass in kg - to rescale to euros per kg")
    args = parser.parse_args()
    return vars(args)


# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()
    # set path
    path_costtable = args['input']

    ns = args["name"]
    print(ns)
    vs = args["value"]
    print(vs)
    assert len(ns) == len(vs), "Not the correct number of values provided for names. Check if number coincides"
    ns_vs = {ns[i] : float(vs[i]) for i in range(len(ns))}

    # scaling values
    scales = args["scale"]
    assert len(scales) == len(path_costtable), "Not the correct number of scales given for input files. Check that a scale is given for each input file"

    # load data from excel workbook
    for i, pth in enumerate(path_costtable):
        basename = os.path.basename(pth).split(".")[0]
        wbs = read_sheets(pth)

        # Calculate the total cost
        tot_cost = total_cost(wbs, args["time"])
        
        tot_cost /= scales[i]
        # add it to the dictionary
        ns_vs[basename] = tot_cost

    df = pd.Series(ns_vs).to_frame().T
    df.index = ["total_cost_filament"]

    if args["output"]:
        with pd.ExcelWriter(args["output"]) as writer:
            df.to_excel(writer)
    else:
        print(df)

#TODO: 3) modify input cost table?
#TODO: 4) how do we operate with two material combinations (PP+Support), (PLA+Support)?


