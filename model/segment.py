
import random
from synapse import Synapse

#
# Object is Segment: a singular cell (the focus) and a list of synapses to other cells (the secondary)
#
# attributes:
#           initiator = a tuple describing the location of focus cell in TM space
#           x = an integer, default is 10, representing the number of rows in TM space
#           y = an integer, default is 10, representing the number of columns in TM space
#           z = an integer, default is 5, representing the height of TM space
#           max_synapses_count = an integer, default is 7, for the maximum number of synapses per cell
#           perm_value_range = a tuple representing the min and max value permanences for each synapse can be
#           connected_cells = a list containing the location of cells that are connected to focus cell
#           connections = a dictionary containing synapses

# functions:
#           initialize_cells(. , this_Segments, temporal_memory_space)
#           fill_segment(. , this_Segments, temporal_memory_space, connecting_cells
#           add_synapse(. , synapse)
#           initialize_perm_value(.)
#           sum_perm_values(.)
#           get_overlap_cells(., active_cells_dict)
#           search_and_adjust(., cells_ls, inc_val, dec_val)
#           get_connections(.)
class Segment():
    def __init__(self, i, j, k, x= 10, y= 10, z= 5, max_synapses_count = 7,connected_cells = [], perm_value_range = (0,1)):
        self.initiator = (i,j,k)
        self.x = x
        self.y = y
        self.z = z
        self.max_synapses_count = max_synapses_count
        self.perm_value_range = perm_value_range
        self.connected_cells = connected_cells
        self.connections = {}

    def initialize_cells(self, this_Segments, temporal_memory_space):
        #
        # a function that randomly selects neighboring cells for connections
        #
        # arguments:
        #       this_Segments = the list of segments associated with this focus cell
        #       temporal_memory_space = a dictionary, listing all cells in TM space by location 
        #

        # if the connections dictionary is empty, fill it up
        if len(self.connections) == 0:
            for i in range(random.randint(1,self.max_synapses_count)):
                # select a cell at random
                cell = (random.randint(0,self.x-1), random.randint(0,self.y-1), random.randint(0,self.z-1))
                # if the randomly selected cell does not match the initiator index for this Segment object
                if cell != self.initiator:
                    # then create a synapse between the random cell in TM space and this_Segments dictionary
                    end_2 = temporal_memory_space[cell[0], cell[1]][cell[2]]
                    s = Synapse(this_Segments, end_2, self.initialize_perm_value())
                    # add a connection if one does not already exist in the connections dictionary
                    if s not in self.connections:
                        s.complete_connection()
                        self.connections[s] = s.perm_val
        # if the connections dictionary is not empty
        else:
            # randomly done to simulate the description in HTM papers
            while len(self.connections) < random.randint(1,self.max_synapses_count):
                cell = (random.randint(0, self.x - 1), random.randint(0, self.y - 1), random.randint(0, self.z - 1))
                if cell != self.initiator:
                    end_2 = temporal_memory_space[cell[0], cell[1]][cell[2]]
                    s = Synapse(this_Segments, end_2, self.initialize_perm_value())
                    if s not in self.connections:
                        s.complete_connection()
                        self.connections[s] = s.perm_val

    def fill_segment(self, this_Segments, temporal_memory_space, connecting_cells):
        #
        # 
        # arguments:
        #           this_Segments = the list of segments associated with this focus cell
        #           temporal_memory_space = a TM object (a hypercube representing cortical columns and neurons in brain)
        #           connecting_cells = a list of segments objects (a list of a list of segments associated with this focus)
        #
        for cell in connecting_cells:
            # if cell (the index of the cell in 3d space) is not the current segments index
            if cell != self.initiator:
                # create a synapse between the this_Segments cell and the cell in TM space 
                end_2 = temporal_memory_space[cell[0], cell[1]][cell[2]]
                s = Synapse(this_Segments, end_2, self.initialize_perm_value())
                # and if the synapse is not already in the connections dictionary, add it
                if s not in self.connections:
                    s.complete_connection()
                    self.connections[s] = s.perm_val

    def add_synapse(self, synapse):
        #
        # a function that adds a synapse to the current segment's connections dictionary
        # 
        # arguments:
        #           synapse = a synapse object
        #
        self.connections[synapse] = synapse.perm_val

    def initialize_perm_value(self):
        #
        # a function that selects at random a permanence value for this segment, based on the uniform distribution
        #
        return random.uniform(self.perm_value_range[0],self.perm_value_range[1])
        # return 0

    def sum_perm_values(self):
        #
        # a function that adds up all permanence values associated with this segment (the current cell and its connections)
        #
        # returns:
        #
        #       sum = a float, representing the total permanence value for this segment of connections
        sum = 0
        for synapse in self.connections:
            sum += self.connections[synapse]

        return sum
    
    def get_overlap_cells(self, active_cells_dict):
        #
        # a function that determines how many cells in this segment are active
        #
        # arguments:
        #           active_cells_dict = a dictionary of cells in TM space that are active
        #
        # returns:
        #           score = an integer that represents the number of cells that are active and in this segment
        #
        score = 0

        active_cells_ls = []

        for i in active_cells_dict:
            # print(active_cells_dict[i])i
            for j in active_cells_dict[i]:
                active_cells_ls.append(j.initiator)

        for cell in self.connections:
            if cell.end_1.initiator in active_cells_ls or cell.end_2.initiator in active_cells_ls:
                score +=1
            # if (cell[0], cell[1]) in active_cells_dict:
            #     if cell[2] in active_cells_dict[(cell[0], cell[1])]:
            #         score +=1

        return score

    def search_and_adjust(self, cells_ls, inc_val, dec_val):
        #
        # a function that checks whether the focus cell's segment connections are contained in the list of active cells;
        # If yes, then increase the permanence values; if not, then decrease the permanence values
        #
        # arguments:
        #           cells_ls = list of active cells in TM space
        #           inc_val = a float, how much to increase permanence by
        #           dec_val = a float, how much to decrease permanence by
        #
        # returns:
        #          connections = the updated permanence values for the connections of this segment
        for i in self.connections:
            ends = i.initiators
            if ends[0] in cells_ls or ends[1] in cells_ls:
                self.connections[i] += inc_val
                i.perm_val = self.connections[i]
            else:
                self.connections[i] -= inc_val
                i.perm_val = self.connections[i]

        return self.connections

    def get_connections(self):
        #
        # a function that retrieves the dictionary containing the synapses for this segment object
        #
        # returns:
        #       output_ls = a list of tuples describing which cells are connected based on location in TM space
        #
        output_ls = []
        for i in self.connections:
            output_ls.append(i.initiator)

        return output_ls
