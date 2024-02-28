
import random

class Segment():
    def __init__(self, i,j, k, x= 10, y=10, z=5, max_synapses_count = 7,connected_cells=[], perm_value_range=(0,1)):
        self.initiator = (i,j,k)
        self.x = x
        self.y = y
        self.z = z
        self.max_synapses_count = max_synapses_count
        self.perm_value_range = perm_value_range
        self.connected_cells = connected_cells
        self.connections = self.initialize_cells()

    def initialize_cells(self):
        synapses = {}
        if len(self.connected_cells) == 0:
            for i in range(random.randint(1,self.max_synapses_count)):
                cell = (random.randint(0,self.x-1), random.randint(0,self.y-1), random.randint(0,self.z-1))
                if cell not in synapses :
                    synapses[cell] = self.initialize_perm_value()

        else:
            for i in self.connected_cells:
                synapses[i] = self.initialize_perm_value()
        return synapses

    def initialize_perm_value(self):
        return random.uniform(self.perm_value_range[0],self.perm_value_range[1])

    def sum_perm_values(self):
        sum = 0
        for synapse in self.connections:
            sum += self.connections[synapse]

        return sum

    def get_overlap_cells(self, active_cells_dict):
        score = 0

        for cell in self.connections:
            if (cell[0], cell[1]) in active_cells_dict:
                if cell[2] in active_cells_dict[(cell[0], cell[1])]:
                    score +=1

        return score

    def search_and_adjust(self, cells_ls, inc_val, dec_val):
        for i in self.connections:
            if i not in cells_ls:
                self.connections[i] -= dec_val
            else:
                self.connections[i] += inc_val

        return self.connections

    # def get_max_overlap_cells(self):
