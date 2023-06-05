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
"""

import openpyxl

from ahp.cost_calculation import create_df, total_cost

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="File for running a cost calculation.")
    parser.add_argument("-i", "--input", type=str, help="Location of the cost excel file", required=True)
    args = parser.parse_args()
    return vars(args)


# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()
    # set path
    path_costtable = args['input']

    # load data from excel workbook
    wb = openpyxl.load_workbook(path_costtable)
    shredd = wb['shredding']
    extr = wb['extrusion']
    gran = wb['granulate']
    con = wb['conditioning']

    # create df
    df_shredd = create_df(shredd)
    df_extr = create_df(extr)
    df_gran = create_df(gran)
    df_con = create_df(con)

    cost_list = [df_shredd, df_extr, df_gran, df_con]

    tot_cost = total_cost(cost_list)
    print(tot_cost)







