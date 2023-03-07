### AHP FUNCTIONS


########################################################################################################################
##import libraries

import numpy as np
from ahp.utils import read_excel
import pandas as pd
# import scipy.sparse.linalg as sc

########################################################################################################################
##constants

#random indices for consistency check (Saaty)

########################################################################################################################
##calculation functions




########################################################################################################################

#tree structure AHP
class TreeNode:

    """
        ! Required - AHP matrix -- w -- is necessary for each Node. to be defined
            * from an array
            * from an excel file
        ! TreeNode Data should be 
        TODO:
            * [ ] Calculate the tree
                * [ ] calculate from bottom up
                * [ ] if a node is calculated, it has a  -- s -- list
                    * [ ] initialise s als None
                    * [ ] if s is None - recursively calculate all children
                        * [ ] all nodes need a flag whether they are calculated -- multiplied s with w
                        * [ ] Alternatively - the parent may have a flag when all children are ready - define over list? 

                * [ ] Calculate random 2, 3, 4 matries to fill in as weights for each node
            * Try with simple easy structure 
                * 1 top node, 2 children
                    * per hand nachrechnen - maximal 3 alternatives
                    * ausschliesslich natuerliche zahlen
                    * ranges 0 - 1 in 0.1er schritten 
    """

    RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1,49]

    def __init__(self, name: str, weights : pd.DataFrame =  None, values : pd.Series = None):
        '''
        Initialization of the hierarchical tree structure

        :param data: any data representing the nodes
        '''
        self.name = name
        self.weights = weights
        self.values = values
        self.children = []
        self.parent = None
        self.lam = None         # Placeholder for the eigenvector

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

    def __repr__(self) -> str:
        if self.is_root():
            returnstr = "Name {}\nRoot Node\nWeights:\n{}".format(
                self.name, self.weights
            )
        elif self.is_leaf():
            returnstr = "Name {}\nLeaf node\nValues:\n{}".format(
                self.name, self.values
            )
        else:
            returnstr = "Name {}\nWeights:\n{}".format(
                self.name, self.weights
            )
        return returnstr

    def __len__(self):
        """
            Placeholder for actual length here
        """
        return len(self.children)

    def __getitem__(self, index):
        """
            function to index with []. May have to accept a tuple here
        """
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    #consistency check for pairwise comparison matrix of the criteria
    def consistency_check(self):
        '''
        Performs the consistency check of the ongoing matrix operations

        :param arr_criteria: matrix with pairwise compared values
        :param criteria_number: size of the matrix
        :param RI: random indices
        :return: consistency result
        '''
        if self.is_leaf():
            raise ValueError("Cannot perform consistency check on leaf nodes")
        criteria_number = self.weights.shape[0]     # square matrix - guaranteed to be same for 0 and 1
        arr_criteria = self.weights
        lambdamax = np.amax(np.linalg.eigvals(arr_criteria).real)
        CI =(lambdamax - criteria_number) / (criteria_number -1)
        CR = CI/self.RI[criteria_number-1]

        return CR

    def is_consistent(self):
        """
            Function to check whether the matrix is consistent according to the comparison matrix
            TODO - when is this done?
        """
        raise NotImplementedError("Not clear when the matrix is deemed consistent. CR has to be what??? Smaller than 1.0?")
        cr = self.consistency_check()
        # if cr > 1.0???? what is the number that should be here

    #calculation of priority vector
    def priority_vector(self):
        '''
        Calculation of the priority vector

        :param arr_criteria: matrix with pairwise compared values
        :return: priority vector
        '''
        # val,vec = sc.eigs(arr_criteria, k=1, which='LM')
        arr_criteria = self.weights
        val, vec = np.linalg.eig(arr_criteria)
        return vec[:, np.argmax(val)]

    #normalization I
    def normalize_max(self, arr,rownumber):
        '''
        normalization, if considering highest value as reference

        :param arr: array of normalizing values
        :param rownumber: size of array to normalize
        :return: normalized array
        '''
        return ((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min())

    #normalization II
    def normalize_min(self, arr,rownumber):
        '''
        normalization, if considering smallest value as reference

        :param arr: array of normalizing values
        :param rownumber: size of array to normalize
        :return: normalized array
        '''
        return 1-(((arr[rownumber,:])-arr[rownumber,:].min())/(arr[rownumber,:].max()-arr[rownumber,:].min()))

    def prepare_tree(self):
        """
            Preparing the tree - by naming the "values" series according to the bottom most children.
            TODO: calculate the eigenvectors of the weight matrix and check whether that is correct
        """
        if not self.is_root():
            raise ValueError("Should be called on the root node")
        self.__prepare_values()

    def __set_lambda(self):
        """
            Function to set the lambda vector.
        """
        if self.lam is None:
            lamb = self.priority_vector()
            self.lam = lamb


    def __set_values(self, vals : pd.Series):
        """
            Function to set the value vector to 0
        """
        # set the value vector
        if self.values is None:
            self.values = vals.copy()
            # 0 the values
            self.values[:] = 0

            # set an intermediate df for the calculation
            self._inter_df = pd.DataFrame(0., columns =[child.name for child in self.children], index = vals.index.to_list())
        # else:
        #     raise ValueError("Values already set")

    def __prepare_values(self):
        """
            Guaranteed to be called first on the root node.
        """
        if self.parent and self.parent.values is None:
            self.parent.__set_values(self.values)
        if self.children:
            self.__set_lambda()
            for child in self.children:
                child.__prepare_values()

    def __values_set(self):
        """
            Check whether the values are actually set up correctly - and not just np.nan, as set in __set_values()
        """
        return False if not self.values.all() else True

    def calculate_tree(self):
        """
            Function to calculate the tree from the bottom up.
            Should be called from a leaf
            If is not fully calculated, then calulate recursively on children
        """
        # All leaf nodes are calculated by default - otherwise there should be an error before
        if not self.is_calculated():
            for child in self.children:
                child.calulate_tree()
            #! ensure that the tree is traversed from bottom up here - descend back down
            raise ValueError("Should be called on a leaf node.")
        else:
            self.parent.inter_df[:,self.name] = self.values.copy()
        # if not self.parent.is_calculated():
        #     self.parent.calculate_tree()
        # self.parent._calculate_s()
        # self.parent.calculate_tree()
        # return
        # # TODO: check what these things do
        # if len(self.s) is not len(self.children):
        #     for child in self.children:
        #         child.calculate_tree()
        # else:
        #     self.s = self._calculate_s(a, w)
        #     self.parent.calculate_tree()
    
    def fill_values(self):
        """
            Inserting the values of the intermediate dataframe
        """
        for child in self.children:
            self._inter_df[:,child.name] = child.values.copy()

    def _calculate_s(self):
        """
            Function to actually calculate the value dataframe.
            TODO : ensure correct column naming
        """
        self.values = self._inter_df @ self.lam
    
    def _is_calculated(self):
        """
            Returns true if all column sums are not 0
        """
        return self.values.sum(0).all()

    def is_leaf(self):
        """
            Simple check to see if a Node is a leaf
        """
        return False if self.children else True

    def is_root(self):
        return False if self.parent else True

    def is_ready(self):
        """
            function to tell if the node is ready for calculation.
            E.G. if "values" is filled
        """
        pass


    def check_integrity(self):
        """
            Function to check the integrity of a Tree. Should be able to be called from any Node (or Root).
            Checks that:
                1. All nodes that are NOT leaf nodes (e.g. have children) only have weight matrices defined
                2. ALL nodes that are Leaf nodes (e.g. have no children) have values defined
        """
        raise NotImplementedError

    
    @classmethod
    def from_weights(cls, fpath : str, name : str):
        """
            Function to get a TreeNode from a path to an Excel specifying weights.
            Stores as a pandas DataFrame.
            Should not be used for Leaf Nodes, only for higher levels.
            Will perform integrity check (whether consistency ratio is met)
        """
        df = read_excel(fpath, series=False)
        nd = cls(name = name, weights=df)

        return nd


    @classmethod
    def from_values(cls, fpath : str, name : str):
        """
            Function to get a TreeNode from a path to an Excel specifying values.
            Stores as a pandas Series.
            Should only be used for Leaf Nodes!
            Will perform integrity check (all **values** between 0 and 1)
        """
        ser = read_excel(fpath, series=True)

        nd = cls(name = name, values=ser)

        return nd
