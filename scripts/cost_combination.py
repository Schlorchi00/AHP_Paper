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
    parser = ArgumentParser(description="File for running a cost combination of multiple materials into a single material. Inputs can be provided over multiple excel files, or as a name-value pair. Use --input for providing excel files as a list (append by using --input <file1> --input <file2>\
                            Use name-value-weight pairs by using multiple --name, --value and --weight tags. Must be same length and in order, otherwise will throw error.")
    parser.add_argument("-i", "--input", type=str,  required=False, action="append", help="Location of the cost excel file. Accepts multiple arguments")
    parser.add_argument("-n", "--name", action="append", help="Name of a material - will be used in output file. Caution - keep order!")
    parser.add_argument("-v", "--value", action="append", help="Value of material - will be used in output file. Caution - keep order!")
    parser.add_argument("-wn", "--weightnames", action="append", help="Percentage weight of the material for the named materials. Has to sum to 1 with weightinputs! Caution - keep order!")
    parser.add_argument("-wi", "--weightinputs", action="append", help="Percentage weight of the material for the input files. Has to sum to 1 with weightnames! Caution - keep order, only f input files!")
    parser.add_argument("-t", "--time", help="Whether to use time or energy for operational cost calculation. Defaults to energy.", action="store_true")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output location of the file. If None given, will write to terminal")
    parser.add_argument("-s", "--scale", type=int, required=False, action="append", help="Weight of recycling mass in g - to rescale to euros per g. Round to nearest integer")
    args = parser.parse_args()
    return vars(args)

def _to_float(l : list) -> list[float]:
    return [float(v) for v in l]

def comb_list(wsi, wsn) -> list:
    return itertools.chain.from_iterable((wsi or [], wsn or []))

# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()
    # set path
    path_costtable = args['input']

    ns = args["name"]
    # print(ns)

    vs = args["value"]
    vs = _to_float(vs) if vs else []

    wsn = args["weightnames"]
    wsn = _to_float(wsn) if wsn else []
    wsi = args["weightinputs"]
    wsi = _to_float(wsi) if wsi else []

    assert abs(sum(comb_list(wsi, wsn)) - 1.) <= 0.001, "Weights do not sum to 1, sum to : {}. Double Check".format(sum(wsn + wsi))
    assert len(wsn) == len(ns) , "Weights are {} items, names are: {}. Have to be the same length".format(len(wsn), len(ns))

    if path_costtable:
        assert len(wsi) == len(path_costtable), "Weights are {} items, input files are: {}. Have to be the same length".format(len(wsn), len(path_costtable))
    # print(vs)
    # df = pd.DataFrame(columns=["cost_per_gram" ,"weight", "cost_weighted"])
    d = {}

    if ns:
        assert len(ns) == len(vs), "Not the correct number of values provided for names. Check if number coincides"
        for i, n in enumerate(ns):
            sd = {}
            sd["cost_per_gram"] = vs[i]
            sd["weight"] = wsn[i]
            sd["cost_weighted"] = wsn[i] * vs[i]
            d[n] = sd
        # ns_vs = {ns[i] : float(vs[i]) * float(wsn[i]) for i in range(len(ns))}
    # # scaling values
    scales = args["scale"]
    if path_costtable:
        assert len(scales) == len(path_costtable), "Not the correct number of scales given for input files. Check that a scale is given for each input file"

    # load data from excel workbook

    if path_costtable:
        for i, pth in enumerate(path_costtable):
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                basename = os.path.basename(pth).split(".")[0]
                wbs = read_sheets(pth)
                sd = {}
                # Calculate the total cost
                tot_cost = total_cost(wbs, args["time"])
                tot_cost_g = tot_cost / scales[i]
                logging.info("Material: {}\nTotal Cost: {}\nTotal Cost per g: {}".format(
                    basename, tot_cost, tot_cost_g
                ))
                # add it to the dictionary
                sd["cost_per_gram"] = tot_cost_g
                sd["weight"] = wsi[i]
                sd["cost_weighted"] = wsi[i] * tot_cost_g
                d[basename] = sd
                # ns_vs[basename] = tot_cost_g * wsi[i]

    df = pd.DataFrame.from_dict(d, orient="index")
    df.loc["sum", :] = df.sum(axis=0)
    if args["output"]:
        output_folder = args["output"]
        assert os.path.isdir( output_folder), "{} not a directory. needs to be a directory for files to be written".format(output_folder)
        out_fname = os.path.join(output_folder, df.index[0] + ".xlsx")
        out_fname  = uniquify(out_fname)
        with pd.ExcelWriter(out_fname, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="economical_params")
        logging.info("Written sheet to: {}".format(args["output"]))
    else:
        print(df)
