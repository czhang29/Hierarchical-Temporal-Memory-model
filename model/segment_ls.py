
from segment import Segment

#
# Object called Segments - list of all the segments for focus cell
#
# attributes:
#           initiator = a tuple for location of focus cell in TM space
#           segment_ls = a list of segment objects for focus cell
#           current_segment = an integer, keeping track of which segment in the list we are analyzing
#           x = an integer, default is 10, representing the number of rows in TM space
#           y = an integer, default is 10, representing the number of columns in TM space
#           z = an integer, default is 5, representing the height of TM space
#           max_synapses_count = an integer, default is 7, for the maximum number of synapses per cell

# functions:
#           initialize_segment(., memory_space)
#           add_segment(., connecting_cells = [])
#           add_synapse(., synapse)
#           get_max_overlap_score(., active_cells_dict)
#           perm_above_pred_state_threshold(., pred_state_threshold)
#           update_perm(., cell_ls, add_val, dec_val)
#           get_segments_as_list(.)
class Segments():
    def __init__(self,i, j, k, x, y, z, max_synapses_count):
        self.initiator = (i, j, k)
        self.segment_ls = [Segment(i, j, k, x, y, z, max_synapses_count)]
        self.current_segment = 0
        self.accept_add = True
        self.x = x
        self.y = y
        self.z = z
        self.max_synapses_count = max_synapses_count

    def initialize_segment(self, memory_space):
        #
        # a function that initializes the list of segments for focus cell based on the entirety of TM space
        #
        # arguments:
        #           memory_space = a dictionary containing cell information for TM space
        # 
        self.memory_space = memory_space
        self.segment_ls[0].initialize_cells(self, self.memory_space)
        
    def add_segment(self, connecting_cells = []):
        #
        # a function that adds a segment to this segment list for the focus cell
        #
        # arguments:
        #           connecting_cells = a list of the cells that are actually connected to focus cell
        #
        
        self.segment_ls.append(Segment(self.initiator[0], self.initiator[1], self.initiator[2], self.x, self.y, self.z, self.max_synapses_count))
        self.current_segment += 1
        self.segment_ls[self.current_segment].fill_segment(self, self.memory_space, connecting_cells)

    def add_synapse(self, synapse):
        #
        # a function that adds a synapse to a segment object for the focus cell
        #
        self.segment_ls[self.current_segment].add_synapse(synapse)

    def get_max_overlap_score(self, active_cells_dict):
        #
        # a function that gets the overlap score between active cells and every segment in focus cell's list
        #
        # arguments:
        #           active_cells_dict = a dictionary of cells in TM space that are active
        #
        # returns: 
        #           max_score = an integer that represents the maximum number of cells that are active and 
        #  
        max_score = 0
        for i in self.segment_ls:
            if i.get_overlap_cells(active_cells_dict) > max_score:
                max_score = i.get_overlap_cells(active_cells_dict)

        return max_score

    def perm_above_pred_state_threshold(self, pred_state_threshold):
        #
        # a function that determines if any of the segments for the focus cell are above a threshold
        #
        # arguments:
        #           pred_state_threshold = a float, between 0 and 1, representing the threshold between 
        #                                   predictive state and active state
        # returns:
        #           above = a logical operator, true if there is a segment that meets the threshold, false if not

        above = False
        for i in self.segment_ls:
            if i.sum_perm_values() > pred_state_threshold:
                above = True
        return above

    def update_perm(self, cell_ls, add_val, dec_val):
        #
        # a function that updates the permanence values for each segment in the list
        #
        # arguments:
        #           cell_ls = a list of the active cells in TM space
        #           add_val = a float, between 0 and 1, the amount to add to the permanence for segments 
        #           dec_val = a float, between 0 and 1, the amount to remove from permanence for segments 
        for i in self.segment_ls:
            # checks whether the focus cell's segment connections are contained in the list of active cells
            # if yes, then increases the permanence values; if not, then decreases the permanence values
            i.search_and_adjust(cell_ls, add_val, dec_val)

    def get_segments_as_list(self):
        #
        # a function that retrieves the segments for focus cell as a list
        #
        # returns:
        #         output_ls = a list containing the segment objects associated with focus cell
        #
        output_ls = []
        for i in self.segment_ls:
            output_ls.append(i.get_connections())

        return output_ls
