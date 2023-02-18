### AHP FUNCTIONS


########################################################################################################################
##import libraries

import numpy as np
# import scipy.sparse.linalg as sc

########################################################################################################################
##constants

#random indices for consistency check (Saaty)

########################################################################################################################
##calculation functions




########################################################################################################################

#tree structure AHP
class TreeNode:

    RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1,49]

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
    def consistency_check(self, arr_criteria, criteria_number):
        '''
        Performs the consistency check of the ongoing matrix operations

        :param arr_criteria: matrix with pairwise compared values
        :param criteria_number: size of the matrix
        :param RI: random indices
        :return: consistency result
        '''

        lambdamax = np.amax(np.linalg.eigvals(arr_criteria).real)
        CI =(lambdamax - criteria_number) / (criteria_number -1)
        CR = CI/self.RI[criteria_number-1]

        return CR

    #calculation of priority vector
    def priority_vector(self, arr_criteria):
        '''
        Calculation of the priority vector

        :param arr_criteria: matrix with pairwise compared values
        :return: priority vector
        '''
        # val,vec = sc.eigs(arr_criteria, k=1, which='LM')
        val, vec = np.linalg.eig(arr_criteria)
        eigcriteria = np.real(vec)
        w = eigcriteria/np.sum(eigcriteria)
        w = np.array(w).ravel()

        return w

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

    def calculate_tree(self):
        """
            Function to calculate the tree from the bottom up.
            If s is not fully calculated, then calulate recursively on children
        """
        if len(self.s) is not len(self.children):
            for child in self.children:
                child.calculate_tree()
        else:
            self.s = self._calculate_s(a, w)
            self.parent.calculate_tree()
        

    def _calculate_s(self, a: np.ndarray, w : np.ndarray) -> np.ndarray:
        return a @ w