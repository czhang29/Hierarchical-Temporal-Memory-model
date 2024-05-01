
from scipy import stats
import numpy as np

# object: Spatial_Pooler_Neuron
# 
# attributes:
#           position = a set of coordinates (x,y)
#           connections = a dictionary of connections
#           input_size = an integer or a pair (m,n) describing the size of an element in the sequential data input
#          
# functions:
#          __init__(self, pos, input_size)
#          get_active_connections(self, threshold)
#          update_permenance(self, inc_val, dec_val, change_pos_matrix)

class Spatial_Pooler_Neuron:
    def __init__(self, pos, input_size):
        self.position = pos
        self.connections = {}
        self.input_size = input_size
        m, n = input_size
        # initialize permanence values
        perm_ls = get_normal_distribution(m*n)
        
        # for every element in the input, add a key to connections dictionary that is the location of that element
        # and give the dictionary value there a permenance
        for i in range(m):
            for j in range(n):
                self.connections[(i,j)] = perm_ls[i*n+j]

    def get_active_connections(self, threshold):
        #
        # a function that determines which connections from input to SP are active based on threshold
        #
        # arguments:
        #           threshold = a float between 0 and 1
        #
        # returns:
        #           matrix = a list of 1's and 0's indicating which elements in the input have active connections
        #
        
        m, n = self.input_size
        matrix = []
        for i in range(m):
            ls = []
            for j in range(n):
                # check dictionary of permanence values
                # if permanence at index (i,j) is at or above threshold, add 1 to temp list called ls
                # otherwise add 0
                if self.connections[(i,j)] >= threshold:
                    ls.append(1)
                else:
                    ls.append(0)
            matrix.append(ls)

        return matrix

    def update_permenance(self, inc_val, dec_val, change_pos_matrix):
        #
        # a function that updates permanence of connections based on ??
        #
        # arguments:
        #           inc_val = a float that determines how much to increase a permanence 
        #           dec_val = a float that determines how much to decrease a permanence
        #           change_pos_matrix = a list or an ndarray of the encoded sequence element
        #
        # returns:
        #        connections = the updated permanence values
        
        m, n = self.input_size
        for i in range(m):
            for j in range(n):
                # if the input has a 1 at this element, then increase the permanence
                # if not, then decrease permanence
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