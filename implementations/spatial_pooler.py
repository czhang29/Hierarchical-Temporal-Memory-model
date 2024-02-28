
from spatial_pooler_neuron import *
import numpy as np

## next step: implement boosting


class Spatial_Pooler():
    def __init__(self, pooler_size = (10,10),input_size = (7,7), perm_connect_threshold=0.5, perm_inc_val=0.3, perm_dec_val=0.1, activate_threshold=4):

        self.perm_connect_threshold = perm_connect_threshold
        self.perm_inc_val = perm_inc_val
        self.perm_dec_val = perm_dec_val
        self.activate_threshold = activate_threshold

        self.cells_dict = {}
        self.m,self.n = pooler_size
        # m_in, n_in = input_size
        for i in range(self.m):
            for j in range(self.n):
                self.cells_dict[(i,j)] = Spatial_Pooler_Neuron((i,j),input_size)

        # print(self.cells_dict)


    def learn_one_input(self, input_matrix):
        # pass
        selected_columns_ls = []

        # get active connections for each cell

        for cell in self.cells_dict:
            # print(cell)
            col_matrix = self.cells_dict[cell].get_active_connections(self.perm_connect_threshold)
            result_matrix = np.multiply(col_matrix, input_matrix)
            # print(col_matrix)
            # print(input_matrix)
            # print(result_matrix)
            # overlap score for each cell using matrix multiplication
            ones_count = sum(sum(result_matrix))
            # print(ones_count)

            # select activated columns
            if ones_count >= self.activate_threshold:
                # print(cell)
                # print(self.cells_dict[cell])
                selected_columns_ls.append(self.cells_dict[cell])

        # update perm value

        for col in selected_columns_ls:
            # print(col.position)
            col.update_permenance(self.perm_inc_val, self.perm_dec_val, input_matrix)

        return selected_columns_ls

    #
    # def learn(self, sequence_of_matrix):
    #     output_ls = []
    #     for i in sequence_of_matrix:
    #         output_ls.append(self.learn_one_input(i))
    #
    #     return output_ls


    def transform(self, sequence_of_matrix):
        matrix_ls = []
        for i in range(len(sequence_of_matrix)):
            activated_cells = self.learn_one_input(sequence_of_matrix[i])
            # print(activated_cells)
            matrix_ls.append([])
            for cell in activated_cells:
                # exporting the position of activated cells instead of whole matrix
                # print(cell.position)
                # print(cell.position)
                matrix_ls[i].append(cell.position)
                # print(matrix_ls)

        return matrix_ls
# print(Spatial_Pooler((10,10), (7,7)).cells_dict)

