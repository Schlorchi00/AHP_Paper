from ahp.ahp import AHP
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)  # default file is data/test_ahp.xlsx
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    args = parse_args()
    ahplist = AHP.from_file(args["input"])
    