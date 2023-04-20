import os.path
from ahp.utils import *

def print_something():
    print("Use this structure to develop functions. Only move to utils when done")

if __name__=="__main__":
    print_something()
    ppath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    datadir = os.path.join(ppath, 'data')
    # preprocess here

    # read files
    read_from_xlsx()

    # write to excel file
    write_to_xlsx()