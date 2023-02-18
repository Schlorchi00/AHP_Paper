from ahp.utils import read_excel 
from argparse import ArgumentParser
import yaml

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    args = parse_args()
    with open(args['input'], 'r') as f:
        file_list = yaml.safe_load(f)

    sl = []
    for fl in file_list:
        fcontent = read_excel(fl)
        print(fcontent)

    print("Test Debug Line")
