from ahp.ahp_functions import TreeNode
from argparse import ArgumentParser
import logging

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the directory from which the tree should be created", required=True)  # default file is data/test_ahp.xlsx
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('matplotlib.font_manager').disabled = True

    args = parse_args()
    ahp = TreeNode.tree_from_directory(args["input"])

    ahp.prepare_tree()
    ahp.check_integrity()
    ahp.calculate_tree()
    print("Final Results:\n{}".format(ahp.calculate_tree()))

    # for c in ahp.children:
    #     c.plot_values()
    # ahp.plot_values()
    ahp.plot_weights()