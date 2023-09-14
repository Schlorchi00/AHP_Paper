
from argparse import ArgumentParser
from ahp.preprocessing import *
from ahp.utils import write_value_excel

"""
    Usage:
        1. activate environment in command line `conda activate <env_name>`
        2. run in command line from parent folder (e.g. the one above scripts) python scripts/preprocessing.py -i data/ecology_format/LCA_PLA_Cuboid.xlsx
        3. OPTIONAL - to use scaling, which is in SECOND SHEET of the file, use --scaling or -s argument
        4. OPTIONAL - to store as xlsx files, provide additional -o argument with a directory. P.ex. `[...] -o data/test_output`
"""

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)
    parser.add_argument("-o", "--output", type=str, help="Directory where the <value> files should be output to. Default None, \
                        if None, will print to command line", default=None)
    parser.add_argument("--scaling","-s", action="store_true", help="Whether a second sheet will be supplied that provides scaling for the parameters")
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    args = parse_args()
    #read files TODO: Check correctness regarding amount of leaf nodes
    # df_path_eco = read_domain('ecology_format', 'LCA_PLA_Cuboid.xlsx')
    #create df
    df_eco, p_node_name_eco = create_df(args["input"])
    if args["scaling"]:
        scale_df = get_scaling(args["input"])
        # apply the scaling
        df2 = apply_scaling(df_eco, scale_df)
    else:
        # case when the normal values are used to generate the values
        df2 = empty_scaling(df_eco)
    check_consistency(df2)
    if args["output"]:
        write_value_excel(df2, args["output"])
    else:
        print("No output directory supplied. Dataframe to write into Excels looks like:")
        print(df2)

    