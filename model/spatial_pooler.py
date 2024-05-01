
from spatial_pooler_neuron import *
import numpy as np

#
# object: Spatial_Pooler
# 
# attributes:
#           perm_connect_threshold = a float between 0 and 1, default is 0.5, that represents strength of connection 
#                                   between input and spatial pooler element 
#           perm_inc_val = a float between 0 and 1, default is 0.3, which represents how much to increase strength 
#                                   of connection during learning
#           perm_dec_val = a float between 0 and 1, default is 0.1, which represents how much to decrease 
#                                   strength of connection during learning
#           activate_threshold = a positive integer, default is 4, that represents the number of connections 
#                                   with permanence value above perm_connect_threshold in order for a column to become active
#           cells_dict = a dictionary, which will contain the spatial pooler neurons, keys are indices of where those neurons live
#           m, n = integers, representing the number of rows and columns of the spatial pooler -- 
#                                   the spatial pooler size can be different than the input elements of the sequence; 
#                                   often it is bigger
#           input_output_mapping = a dictionary, which will contain the information that maps each input to certain 
#                                   elements in the spatial pooler
#
# functions:
#        __init__(., pooler_size, input_size, perm_connect_threshold, perm_inc_val, perm_dec_val, activate_threshold)
#       learn_one_input(., input_matrix)
#       transform(., sequence_of_matrix)

class Spatial_Pooler():
    def __init__(self, pooler_size = (10,10),input_size = (7,7), perm_connect_threshold=0.5, perm_inc_val=0.3, perm_dec_val=0.1, activate_threshold=4):

        self.perm_connect_threshold = perm_connect_threshold
        self.perm_inc_val = perm_inc_val
        self.perm_dec_val = perm_dec_val
        self.activate_threshold = activate_threshold

        self.cells_dict = {}
        self.m,self.n = pooler_size
        
        # initialize the cells_dict with spatial pooler neurons
        for i in range(self.m):
            for j in range(self.n):
                self.cells_dict[(i,j)] = Spatial_Pooler_Neuron((i,j),input_size)

        self.input_output_mapping = {}

    def learn_one_input(self, input_matrix):
        # 
        # a function that has the spatial pooler learn from one input at a time
        #
        # arguments:
        #       input_matrix, a list or an ndarray of the encoded sequence element
        #
        # returns: 
        #       selected_columns_ls, a list of the activated elements of the spatial pooler based on thresholds
        
        selected_columns_ls = []

        # get active connections for each cell 
        for cell in self.cells_dict:
            
            col_matrix = self.cells_dict[cell].get_active_connections(self.perm_connect_threshold)
            result_matrix = np.multiply(col_matrix, input_matrix)
            
            # overlap score for each cell using matrix multiplication
            ones_count = sum(sum(result_matrix))
            
            # select activated columns
            if ones_count >= self.activate_threshold:
                selected_columns_ls.append(self.cells_dict[cell])

        # update perm value
        for col in selected_columns_ls:
            col.update_permenance(self.perm_inc_val, self.perm_dec_val, input_matrix)

        return selected_columns_ls

    def transform(self, sequence_of_matrix):
        # 
        # a function that takes in a sequence of encoded data and transforms them to a spatial pooler, one element at a time
        #
        # arguments:
        #       sequence_of_matrix, a list or an ndarray of the encoded sequence element
        #
        # returns: 
        #       matrix_ls = a list of lists containing the corresponding spatial pooler elements that are activated by a particular sequence element
        #       self.input_output_mapping = a dictionary containing the mapping of elements in input to elements in SP
        
        matrix_ls = []
        
        # figure out which spatial pooler elements are activated after each element in the sequence
        for i in range(len(sequence_of_matrix)):
            activated_cells = self.learn_one_input(sequence_of_matrix[i])

            if sequence_of_matrix[i] not in list(self.input_output_mapping.keys()):
                for row in range(len(sequence_of_matrix[i])):
                    if 1 in sequence_of_matrix[i][row]:
                        self.input_output_mapping[row] = []

            tmp_ls = []
            # exporting the position of activated cells 
            for cell in activated_cells:                
                tmp_ls.append(cell.position)
                
            for row in range(len(sequence_of_matrix[i])):
                if 1 in sequence_of_matrix[i][row]:
                    self.input_output_mapping[row] = tmp_ls
            matrix_ls.append(tmp_ls)
            
        return matrix_ls, self.input_output_mapping
