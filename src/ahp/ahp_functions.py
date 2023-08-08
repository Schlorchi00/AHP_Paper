### AHP FUNCTIONS


########################################################################################################################
##import libraries

import numpy as np
from ahp.utils import read_excel
import pandas as pd
import logging
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

                * [ ] Calculate random 2, 3, 4 matrices to fill in as weights for each node
            * Try with simple easy structure 
                * 1 top node, 2 children
                    * per hand nachrechnen - maximal 3 alternatives
                    * ausschliesslich natuerliche zahlen
                    * ranges 0 - 1 in 0.1er schritten 
    """

    RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1,49]
    CONSISTENCY_THRESHOLD = 0.1

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
        self._inter_df = None   # Placeholder for intermediate calculations - debugging

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
        print(prefix + self.name)
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
    def is_consistent(self):
        '''
        Performs the consistency check of the ongoing matrix operations

        :param arr_criteria: matrix with pairwise compared values
        :param criteria_number: size of the matrix
        :param RI: random indices
        :return: Boolean - is consistent
        '''
        criteria_number = self.get_dimensions()    # square matrix - guaranteed to be same for 0 and 1
        arr_criteria = self.weights
        val, _ = np.linalg.eig(arr_criteria)
        lambdamax = np.argmax(val)
        # lambdamax = np.amax(np.linalg.eigvals(arr_criteria).real)
        CI =(lambdamax - criteria_number) / (criteria_number -1)
        CR = CI/self.RI[criteria_number]
        return True if CR <= self.CONSISTENCY_THRESHOLD else False

    def get_dimensions(self):
        """
            Function to get square matrix dimension
        """
        return self.weights.shape[0]

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
        mv = vec[:, np.argmax(val)]
        mvr = mv.real
        mvn = mvr / np.sum(mvr)
        return mvn

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

    # Getting the values
    def get_values(self):
        """
            Function to get the values
        """
        return self.values

    ###############################
    # Section on preparing the tree
    ###############################
    def prepare_tree(self):
        """
            Preparing the tree - by naming the "values" series according to the bottom most children.
        """
        if not self.is_root():
            raise ValueError("Should be called on the root node")
        self.__prepare_values()


    def __prepare_values(self):
        """
            Guaranteed to be called first on the root node.
            sets intermediate dataframes in parent nodes
            sets the lambda vector in parent nodes
            sets the intermediate dataframe values
        """
        for child in self.children:
            child.__prepare_values()
        if not self.is_root() and not self.parent.is_prepared():
            # set the values vector on the parent
            self.parent.__set_values(self.values)
            # calculate lambda on the parent
            # self.parent.__set_lambda()
        # set the _inter_df 
        if not self.is_leaf():
            self.fill_values()
            logging.debug("Fill values debug line")

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
            logging.debug(self._inter_df) 
    
    def fill_values(self):
        """
            Inserting the values of the intermediate dataframe
        """
        for child in self.children:
            logging.debug(self._inter_df.loc[:,child.name])
            self._inter_df.loc[:,child.name] = child.values.copy()


    #################################
    # Section on calculating the tree
    #################################
    def calculate_tree(self):
        """
            Outer function to call __calculate_tree() on root 
        """
        if not self.is_root():
            raise ValueError("Has to be called on root.")
        return self.__calculate_tree()

    def __calculate_tree(self):
        """
            Function to calculate the tree from the bottom up.
            Called on root
            post-order tree traversal, see here: https://stackoverflow.com/questions/20062527/scan-tree-structure-from-bottom-up
        """
        
        for child in self.children:
            child.__calculate_tree()
        if not self.is_leaf():
            self._calculate_values()
            if not self.is_root():
                self.set_parent_inter_df()
            logging.debug("Values after calculation for node {} \n{}".format(self.name, self.values))

    def _calculate_values(self):
        """
            Function to actually calculate the value dataframe.
        """
        self.values = self._inter_df @ self.lam
        logging.debug("Test Debug line for val calculation. Set breakpoint here to inspect value setting")

    def scale_values(self, mode="sum"):
        if not self.is_root(): raise ValueError("Only scale the root node")
        else:
            return self._scale_values(mode)

    def _scale_values(self, mode="max") -> pd.Series:
        """
            Function to scale the value df.
            Either scale by maximum or by sum
        """
        if mode == "max":
            return self.values / self.values.max()
        elif mode == "sum":
            return self.values / self.values.sum()
        else: raise ValueError("Unknown scale. Use max or sum")

    def set_parent_inter_df(self):
        """
            Function to set the parent inter_df AFTER the vales have been calculated
        """
        self.parent._inter_df[self.name] = self.values
        logging.debug("Setting the own values into the parent inter_df")

    ########################
    # State checking functions
    #########################
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
        """
            Simple check to see if a Node is the root node
        """
        return False if self.parent else True

    def is_prepared(self):
        """
            function to tell if the node is ready for calculation.
            E.G. if "values" is filled or if it is a leaf
        """
        return True if self._inter_df is not None or self.is_leaf() else False
    
    def __values_set(self):
        """
            Check whether the values are actually set up correctly - and not just np.nan, as set in __set_values()
        """
        return False if not self.values.all() else True


    def check_integrity(self):
        """
            Function to check the integrity of a Tree. Should be able to be called from any Node (or Root).
            Checks that:
                1. All nodes that are NOT leaf nodes (e.g. have children) only have weight matrices defined
                2. ALL nodes that are Leaf nodes (e.g. have no children) have values defined
        """
        if not self.is_root(): raise ValueError("Should be called on the root node")
        self._check_integrity()

    def _check_integrity(self):
        for child in self.children:
            child._check_integrity()
        
        # leaf nodes: check values, other ones: check lambda
        if self.is_leaf():
            self._check_values()
        else:
            self._check_lambda()
        
    def _check_values(self):
        if not (np.all(self.values <= 1.)) and (np.all(self.values >= 0.)):
            logging.warning("Dataframe for calculation for {} not correct should be between 0 and 1, is :\n{}".format(self.name, self._inter_df))

    def _check_lambda(self):
        if not np.isclose(self.lam.sum(), 1.):
            logging.warning("Lambda of node {} does not sum to one. Values are: {}. Double check weight excel".format(self.name, self.lam))

    # functional bottom up traversal
    # def functional_post_order(self, f : function):
    #     for child in self.children:
    #         self.functional_post_order(child, f)
    #     f(self)

    # def functional_pre_order(self, f : function):
    #     f(self)
    #     for child in self.children:
    #         self.functional_pre_order(child, f)


    ####################
    # Outer Init Methods
    ####################
    @classmethod
    def from_weights(cls, fpath : str, name : str):
        """
            Function to get a TreeNode from a path to an Excel specifying weights.
            Stores as a pandas DataFrame.
            Should not be used for Leaf Nodes, only for higher levels.
            Will perform integrity check (whether consistency ratio is met)
        """
        df, _ = read_excel(fpath, series=False)
        nd = cls(name = name, weights=df)
        if not nd.is_consistent():
            raise ValueError("Node is not consistent. Please choose other values")
        nd.__set_lambda()
        return nd


    @classmethod
    def from_values(cls, fpath : str, name : str = None):
        """
            Function to get a TreeNode from a path to an Excel specifying values.
            Stores as a pandas Series.
            Should only be used for Leaf Nodes!
            Will perform integrity check (all **values** between 0 and 1)
        """
        ser, sheet_name = read_excel(fpath, series=True)
        if name is None:
            name = sheet_name
        nd = cls(name = name, values=ser)

        return nd
