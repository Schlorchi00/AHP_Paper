### AHP FUNCTIONS


########################################################################################################################
##import libraries

import numpy as np
import scipy.sparse.linalg as sc

########################################################################################################################
##constants

#random indices for consistency check (Saaty)
RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1,49]

########################################################################################################################
##calculation functions

#consistency check for pairwise comparison matrix of the criteria
def consistency_check(arr_criteria, criteria_number,RI):
    '''
    Performs the consistency check of the ongoing matrix operations

    :param arr_criteria: matrix with pairwise compared values
    :param criteria_number: size of the matrix
    :param RI: random indices
    :return: consistency result
    '''

    lambdamax = np.amax(np.linalg.eigvals(arr_criteria).real)
    CI =(lambdamax - criteria_number) / (criteria_number -1)
    CR = CI/RI[criteria_number-1]

    return CR

#calculation of priority vector
def priority_vector(arr_criteria):
    '''
    Calculation of the priority vector

    :param arr_criteria: matrix with pairwise compared values
    :return: priority vector
    '''
    val,vec = sc.eigs(arr_criteria, k=1, which='LM')
    eigcriteria = np.real(vec)
    w = eigcriteria/np.sum(eigcriteria)
    w = np.array(w).ravel()

    return w

#normalization I
def normalize_1(arr,rownumber):
    '''
    normalization, if considering highest value as reference

    :param arr: array of normalizing values
    :param rownumber: size of array to normalize
    :return: normalized array
    '''
    return ((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min())

#normalization II
def normalize_2(arr,rownumber):
    '''
    normalization, if considering smallest value as reference

    :param arr: array of normalizing values
    :param rownumber: size of array to normalize
    :return: normalized array
    '''
    return 1-(((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min()))


########################################################################################################################

#tree structure AHP
class TreeNode:
    def __init__(self, data):
        '''
        Initialization of the hierarchical tree structure

        :param data: any data representing the nodes
        '''
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        '''
        Creation of a child node

        :param child: declaration of child
        :return: list of node children regarding a parent
        '''
        child.parent = self
        self.children.append(child)

    def get_level(self):
        '''
        Definition of hierarchy based on levels

        :return: level count
        '''
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        '''
        Visualization of the hierarchical tree
        '''
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + '|__' if self.parent else ''
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

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

root = build_AHP_tree()
root.print_tree()
pass