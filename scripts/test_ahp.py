from ahp.ahp_functions import TreeNode
from argparse import ArgumentParser
import logging

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the directory from which the tree should be created", required=True)  # default file is data/test_ahp.xlsx
    args = parser.parse_args()
    return vars(args)

def plot_complete_tree(tree : TreeNode) -> None:
    """
        Example function to plot a completely calculated tree. Plotting Tree with lambdas and values
    """
    treepl = tree.plot_tree()
    treepl.view("testview")

if __name__=="__main__":
    # Uncomment for debugging purposes
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('matplotlib.font_manager').disabled = True
    args = parse_args()

    # 1. Reading in the tree
    ahp = TreeNode.tree_from_directory(args["input"])

    # 2. Calculating the tree
    ahp.prepare_tree()
    ahp.check_integrity()
    ahp.calculate_tree()
    print("Final Results:\n{}".format(ahp.calculate_tree()))
    
    # 3. Visualising results
    # a. plotting lambdas and values as tree
    plot_complete_tree(ahp)

    # b. Plotting value bar charts - uncomment for use
    # ahp.plot_values()
    # for c in ahp.children:
    #     c.plot_values()
    
    # c. Plotting weights tree - uncomment for use
    # ahp.plot_weights_tree()

    # 4. Storing results - uncomment for use
    # ahp.save_values("test_output.xlsx")
    # ahp.save_lambda("test_lambda.xlsx")