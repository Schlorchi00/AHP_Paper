from ahp.ahp_functions import TreeNode
from argparse import ArgumentParser

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

if __name__=="__main__":
    args = parse_args()
    # args = default_args()
    root = build_AHP_tree()
    root.print_tree()