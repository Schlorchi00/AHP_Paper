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

# import openpyxl

from ahp.cost_calculation import total_cost, read_sheets
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="File for running a cost calculation.")
    parser.add_argument("-i", "--input", type=str, help="Location of the cost excel file", required=True)
    parser.add_argument("-t", "--time", help="Whether to use time or energy for operational cost calculation. Defaults to energy.", action="store_true")
    args = parser.parse_args()
    return vars(args)


# call main function - safeguard for external includes
if __name__ == "__main__":
    args=parse_args()
    # set path
    path_costtable = args['input']

    # load data from excel workbook
    wbs = read_sheets(path_costtable)

    # Calculate the total cost
    tot_cost = total_cost(wbs, args["time"])
    print(tot_cost)







