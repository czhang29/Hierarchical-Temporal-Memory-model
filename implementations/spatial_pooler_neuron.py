
from scipy import stats
import numpy as np

class Spatial_Pooler_Neuron:
    def __init__(self, pos, input_size):
        self.position = pos
        self.connections = {}
        self.input_size = input_size
        m, n = input_size
        perm_ls = get_normal_distribution(m*n)
        for i in range(m):
            for j in range(n):
                self.connections[(i,j)] = perm_ls[i*n+j]

    def get_active_connections(self, threshold):
        m, n = self.input_size
        matrix = []
        for i in range(m):
            ls = []
            for j in range(n):
                if self.connections[(i,j)] >= threshold:
                    ls.append(1)
                else:
                    ls.append(0)
            matrix.append(ls)

        return matrix

    def update_permenance(self, inc_val, dec_val, change_pos_matrix):
        m, n = self.input_size
        for i in range(m):
            for j in range(n):
                if change_pos_matrix[i][j] == 1:
                    self.connections[(i, j)] = self.connections[(i, j)] + inc_val
                else:
                    self.connections[(i, j)] = self.connections[(i, j)] - dec_val

        return self.connections

def get_normal_distribution(size):
    low = 0
    high = 1
    mean = 0.3
    stddev = 0.5
    num_pop = size
    number = stats.truncnorm.rvs(low, high,
                             loc = mean, scale = stddev,
                             size = num_pop)

    return number