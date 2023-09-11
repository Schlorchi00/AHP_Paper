from ahp.ahp_functions import TreeNode
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the directory from which the tree should be created", required=True)  # default file is data/test_ahp.xlsx
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    args = parse_args()
    ahp = TreeNode.tree_from_directory(args["input"])

    ahp.prepare_tree()
    ahp.check_integrity()
    ahp.calculate_tree()
    print("Final Results: {}".format(ahp.calculate_tree()))

    