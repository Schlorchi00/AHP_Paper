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
    #! ensure to always work with values.copy() when using across multiple nodes - otherwise is only a reference!
    node_A.calculate_tree()
    print(node_A.get_values())

    TreeNode.print_tree(node_A)

def build_base_tree_1():

    fdir = os.path.dirname(os.path.abspath(__file__))
    simple_dir = os.path.join(fdir, '..', 'data', 'complete_tree')

    ##Level 0
    node_A_f = os.path.join(simple_dir, 'A_weights.xlsx')

    ##Level 1
    node_A1_f = os.path.join(simple_dir, 'A1_weights.xlsx')
    node_A2_f = os.path.join(simple_dir, 'A2_weights.xlsx')
    node_A3_f = os.path.join(simple_dir, 'A3_weights.xlsx')
    #node_A4_f = os.path.join(simple_dir, 'A4_weights.xlsx')

    node_A41_f = os.path.join(simple_dir, 'A41_values.xlsx')

    ##Level 2
    node_A11_f = os.path.join(simple_dir, 'A11_weights.xlsx')
    node_A12_f = os.path.join(simple_dir, 'A12_weights.xlsx')

    #node_A21_f = os.path.join(simple_dir, 'A21_weights.xlsx')
    #node_A22_f = os.path.join(simple_dir, 'A22_weights.xlsx')
    #node_A23_f = os.path.join(simple_dir, 'A23_weights.xlsx')

    node_A211_f = os.path.join(simple_dir, 'A211_values.xlsx')
    node_A221_f = os.path.join(simple_dir, 'A221_values.xlsx')
    node_A231_f = os.path.join(simple_dir, 'A231_values.xlsx')

    #node_A31_f = os.path.join(simple_dir, 'A31_weights.xlsx')
    #node_A32_f = os.path.join(simple_dir, 'A32_weights.xlsx')
    #node_A33_f = os.path.join(simple_dir, 'A33_weights.xlsx')

    node_A311_f = os.path.join(simple_dir, 'A311_values.xlsx')
    node_A321_f = os.path.join(simple_dir, 'A321_values.xlsx')
    node_A331_f = os.path.join(simple_dir, 'A331_values.xlsx')

    ##Level3
    #node_A111_f = os.path.join(simple_dir, 'A111_weights.xlsx')
    #node_A112_f = os.path.join(simple_dir, 'A112_weights.xlsx')
    #node_A113_f = os.path.join(simple_dir, 'A113_weights.xlsx')

    #node_A121_f = os.path.join(simple_dir, 'A121_weights.xlsx')
    #node_A122_f = os.path.join(simple_dir, 'A122_weights.xlsx')
    #node_A123_f = os.path.join(simple_dir, 'A123_weights.xlsx')

    node_A1111_f = os.path.join(simple_dir, 'A1111_values.xlsx')
    node_A1121_f = os.path.join(simple_dir, 'A1121_values.xlsx')
    node_A1131_f = os.path.join(simple_dir, 'A1131_values.xlsx')

    node_A1211_f = os.path.join(simple_dir, 'A1211_values.xlsx')
    node_A1221_f = os.path.join(simple_dir, 'A1221_values.xlsx')
    node_A1231_f = os.path.join(simple_dir, 'A1231_values.xlsx')


    #What the function should be called like

    ##Level 0
    node_A = TreeNode.from_weights(node_A_f, name='Meaningfulness_of_Recycling')

    ##Level 1
    node_A1 = TreeNode.from_weights(node_A1_f, 'Mechanical_Parameters')
    node_A2 = TreeNode.from_weights(node_A2_f, 'Processinfluencing_Parameters')
    node_A3 = TreeNode.from_weights(node_A3_f, 'Ecological_Parameters')
    #node_A4 = TreeNode.from_weights(node_A4_f, 'Economical_Parameters')

    node_A41 = TreeNode.from_values(node_A41_f, 'Economical_Values')

    ##Level 2
    node_A11 = TreeNode.from_weights(node_A11_f, '0_degree')
    node_A12 = TreeNode.from_weights(node_A12_f, '90_0_degree')

    #node_A21 = TreeNode.from_weights(node_A21_f, 'Diameter')
    #node_A22 = TreeNode.from_weights(node_A22_f, 'Ovality')
    #node_A23 = TreeNode.from_weights(node_A23_f, 'MFR')

    node_A211 = TreeNode.from_values(node_A211_f, 'Diameter_values')
    node_A221 = TreeNode.from_values(node_A221_f, 'Ovality_values')
    node_A231 = TreeNode.from_values(node_A231_f , 'MFR_values')

    #node_A31 = TreeNode.from_weights(node_A31_f, 'Human_Health')
    #node_A32 = TreeNode.from_weights(node_A32_f, 'Resources')
    #node_A33 = TreeNode.from_weights(node_A33_f, 'Ecosystems')

    node_A311 = TreeNode.from_values(node_A311_f, 'Human_Health_values')
    node_A321 = TreeNode.from_values(node_A321_f, 'Resources_values')
    node_A331 = TreeNode.from_values(node_A331_f, 'Ecosystems_values')

    ##Level 3
    #node_A111 = TreeNode.from_weights(node_A111_f, 'Tensile_stress_0')
    #node_A112 = TreeNode.from_weights(node_A112_f, 'Tensile_strength_0')
    #node_A113 = TreeNode.from_weights(node_A113_f, 'E_Modulus_0')

    #node_A121 = TreeNode.from_weights(node_A121_f, 'Tensile_stress_90')
    #node_A122 = TreeNode.from_weights(node_A122_f, 'Tensile_strength_90')
    #node_A123 = TreeNode.from_weights(node_A123_f, 'E_Modulus_90')

    node_A1111 = TreeNode.from_values(node_A1111_f, 'Tensile_stress_0_values')
    node_A1121 = TreeNode.from_values(node_A1121_f, 'Tensile_strength_0_values')
    node_A1131 = TreeNode.from_values(node_A1131_f, 'E_Modulus_0_values')

    node_A1211 = TreeNode.from_values(node_A1211_f, 'Tensile_stress_90_values')
    node_A1221 = TreeNode.from_values(node_A1221_f, 'Tensile_strength_90_values')
    node_A1231 = TreeNode.from_values(node_A1231_f, 'E_Modulus_90_values')
    


    # Building the tree structure

    ##Level 1
    node_A.add_child(node_A1)
    node_A.add_child(node_A2)
    node_A.add_child(node_A3)
    #node_A.add_child(node_A4)

    #node_A4.add_child(node_A41)
    node_A.add_child(node_A41)

    ##Level 2
    node_A1.add_child(node_A11)
    node_A1.add_child(node_A12)

    #node_A2.add_child(node_A21)
    #node_A2.add_child(node_A22)
    #node_A2.add_child(node_A23)

    node_A2.add_child(node_A211)
    node_A2.add_child(node_A221)
    node_A2.add_child(node_A231)

    #node_A21.add_child(node_A211)
    #node_A22.add_child(node_A221)
    #node_A23.add_child(node_A231)

    #node_A3.add_child(node_A31)
    #node_A3.add_child(node_A32)
    #node_A3.add_child(node_A33)

    node_A3.add_child(node_A311)
    node_A3.add_child(node_A321)
    node_A3.add_child(node_A331)

    #node_A31.add_child(node_A311)
    #node_A32.add_child(node_A321)
    #node_A33.add_child(node_A331)

    ##Level 3
    node_A11.add_child(node_A1111)
    node_A11.add_child(node_A1121)
    node_A11.add_child(node_A1131)

    node_A12.add_child(node_A1211)
    node_A12.add_child(node_A1221)
    node_A12.add_child(node_A1231)

    #node_A111.add_child(node_A1111)
    #node_A112.add_child(node_A1121)
    #node_A113.add_child(node_A1131)

    #node_A121.add_child(node_A1211)
    #node_A122.add_child(node_A1221)
    #node_A123.add_child(node_A1231)


    #Tree Visualization
    TreeNode.print_tree(node_A)

    # Calculating the tree
    node_A.prepare_tree()
    # ! ensure to always work with values.copy() when using across multiple nodes - otherwise is only a reference!
    node_A.calculate_tree()


if __name__=="__main__":
    build_base_tree_1()
    # args = parse_args()
    # args = default_args()
    # root = build_AHP_tree()
    # root.print_tree()