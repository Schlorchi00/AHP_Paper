from ahp.ahp_functions import TreeNode
from argparse import ArgumentParser
import os.path

def parse_args():
    parser = ArgumentParser(description="File for running an ahp.")
    parser.add_argument("-i", "--input", type=str, help="Location of the file listing the excel files", required=True)
    args = parser.parse_args()
    return vars(args)

def default_args():
    args = {}
    args["input"] = "blablabla"
    return args

def build_AHP_tree():
    '''
    Creation of a hierarchical tree structure

    :return: visualized tree
    '''

    ##0 Level
    root = TreeNode('Meaningfullness_of_Recycling')

    ##1 Level

    mech = TreeNode('Mechanical_Parameters')
    root.add_child(mech)
    proc = TreeNode('Process_Parameters')
    root.add_child(proc)
    ecol = TreeNode('Ecology_Parameters')
    root.add_child(ecol)
    econ = TreeNode('Economic_Parameters')
    root.add_child(econ)

    ##2 Level

    zero = TreeNode('0_degree')
    mech.add_child(zero)
    ninety = TreeNode('90_0_degree')
    mech.add_child(ninety)

    diam = TreeNode('Diameter')
    proc.add_child(diam)
    oval = TreeNode('Ovality')
    proc.add_child(oval)
    mfr = TreeNode('MFR')
    proc.add_child(mfr)

    health = TreeNode('Human_Health')
    ecol.add_child(health)
    res = TreeNode('Resources')
    ecol.add_child(res)
    ecosys = TreeNode('Ecosystems')
    ecol.add_child(ecosys)

    econ_nom = TreeNode('Normalized_Cost_Data')
    econ.add_child(econ_nom)

    ##3 Level
    zero_strain = TreeNode('0_Tensile_Strain')
    zero.add_child(zero_strain)
    zero_stress = TreeNode('0_Tensile_Stress')
    zero.add_child(zero_stress)
    zero_mod = TreeNode('0_E_Modulus')
    zero.add_child(zero_mod)

    ninety_strain = TreeNode('90_0_Tensile_Strain')
    ninety.add_child(ninety_strain)
    ninety_stress = TreeNode('90_0_Tensile_Stress')
    ninety.add_child(ninety_stress)
    ninety_mod = TreeNode('90_0_E_Modulus')
    ninety.add_child(ninety_mod)

    diam_norm = TreeNode('Normalized_Diameter_Data')
    diam.add_child(diam_norm)
    oval_norm = TreeNode('Normalized_Ovality_Data')
    oval.add_child(oval_norm)
    mfr_norm = TreeNode('Normalized_MFR_Data')
    mfr.add_child(mfr_norm)

    health_norm = TreeNode('Normalized_Human_Health_Data')
    health.add_child(health_norm)
    res_norm = TreeNode('Normalized_Resources_Data')
    res.add_child(res_norm)
    ecosys_norm = TreeNode('Normalized_Ecosystem_Data')
    ecosys.add_child(ecosys_norm)

    ##4 Level

    zero_strain_norm = TreeNode('Normalized_0_Tensile_Strain_Data')
    zero_strain.add_child(zero_strain_norm)
    zero_stress_norm = TreeNode('Normalized_0_Tensile_Stress_Data')
    zero_stress.add_child(zero_stress_norm)
    zero_mod_norm = TreeNode('Normalized_0_Tensile_E_Modulus_Data')
    zero_mod.add_child(zero_mod_norm)

    ninety_strain_norm = TreeNode('Normalized_90_0_Tensile_Strain_Data')
    ninety_strain.add_child(ninety_strain_norm)
    ninety_stress_norm = TreeNode('Normalized_90_0_Tensile_Stress_Data')
    ninety_stress.add_child(ninety_stress_norm)
    ninety_mod_norm = TreeNode('Normalized_90_0_Tensile_E_Modulus_Data')
    ninety_mod.add_child(ninety_mod_norm)

    return root

def build_base_tree():
    """
        Function to build a basic tree with 3 nodes, 1 root, 2 children - 3 alternatives
        Option 2: 2 alternatives, 3 children
        * Name the node
        * insert as children
        TODO:
            * get one weight matrix
                * from excel
                * hand define
            * set the flag for "Calculated" on the children
                * insert fictionary s values for the alternatives
    """
    fdir = os.path.dirname(os.path.abspath(__file__))
    simple_dir = os.path.join(fdir, '..', 'data', 'simple_tree')
    node_A_f = os.path.join(simple_dir, 'A_weights.xlsx')
    node_B_f = os.path.join(simple_dir, 'B_values.xlsx')
    node_C_f = os.path.join(simple_dir, 'C_values.xlsx')

    # What the functions should be called like
    node_A = TreeNode.from_weights(node_A_f, name="Node A")
    node_B = TreeNode.from_values(node_B_f, "Node B")
    node_C = TreeNode.from_values(node_C_f, "Node C")

    # Building the tree structure
    node_A.add_child(node_B)
    node_A.add_child(node_C)

    print("Is node_A a leaf? {}".format(
        node_A.is_leaf()
    ))
    print("Is node_B a leaf? {}".format(
        node_B.is_leaf()
    ))
    print("Is node_C a leaf? {}".format(
        node_C.is_leaf()
    ))

    # Calculating the tree
    node_A.prepare_tree()
    node_A.calculate_tree()


if __name__=="__main__":
    build_base_tree()
    # args = parse_args()
    # args = default_args()
    # root = build_AHP_tree()
    # root.print_tree()