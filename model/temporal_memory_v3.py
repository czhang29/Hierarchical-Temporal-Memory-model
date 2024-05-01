import random
from spatial_pooler import *
from segment import *
from segment_ls import Segments


#
# Object called Temporal_Memory
#
# attributes are:
#       x, y, z = integers representing size of temporal memory space
#       max_synapses_counts = integer for the maximum number of synapses per cell during initialization
#       memory_space = a list of segments objects, representing the TM space
#       pred_state_threshold = float, between 0 and 1, the threshold of total permanences that determine whether
#                           a cell is in predictive state or not
#       learn_inc_values = float, between 0 and 1, by how much connection permanences are increased during learning
#       learn_dec_values = float, between 0 and 1, by how much connection permanences are decreased during learning
#       spatial_pooler_output_input_mapping = a dictionary mapping spatial pooler elements back to input elements
#       input_output_mapping = a dictionary mapping the input elements to spatial pooler elements
#       predictive_cells = a dictionary listing all the TM cells that are in the predictive state at time T
#       active_cells = a dictionary listing all the TM cells that are in the active state at time T
#                       (a subset of the predictive_cells)
#       learning_cells = a dictionary listing all the TM cells that are in the learning state at time T
#                       (a subset of the active_cells)
#       prev_learning_cells = a dictionary listing the TM cells that _were_ in the learning state at time T-1
#       entry_count = an int that represents where in the sequence of data we are
#       current_learning_matrix = list of activated cell in learning state positions at time T
#       previous_learning_matrix = list of activated cell in learning state positions at time T-1

# functions for this object are:
#           __init__(., spatial_pooler_input_output_mapping, spatial_pooler_dim, cells_per_column, max_synapses_count,
#                   pred_state_threshold, learn_inc_val, learn_dec_val)
#           initialize_space(.)
#           initialize_input_output_mapping(.)
#           reverse_mapping(., mapping)
#           check_similarities_between_predictive_cells(., dict_1, dict_2)
#           learn_one_input(.)
#           learn(., matrix_ls)


class Temporal_Memory():
    def __init__(self, spatial_pooler_input_output_mapping={}, spatial_pooler_dim=(10, 10),
                 cells_per_column=5, max_synapses_count=7,
                 pred_state_threshold=0.7, learn_inc_val=0.1, learn_dec_val=0.2):

        # define dimension of the cube
        self.x, self.y = spatial_pooler_dim
        self.z = cells_per_column

        # how many cells to connect to when randomly initialize the first segment
        self.max_synapses_count = max_synapses_count

        # the main ds for the data: {col_index: cell_index{Segments object that is a list of Segment objects}}
        self.memory_space = self.initialize_space()

        # values for updating the permanence values
        self.pred_state_threshold = pred_state_threshold
        self.learn_inc_val = learn_inc_val
        self.learn_dec_val = learn_dec_val

        # get the dict: {spatial_pooler_encoder_of_the_number: the_number}
        self.spatial_pooler_output_input_mapping = self.reverse_mapping(spatial_pooler_input_output_mapping)

        # get the dict: {spatial_pooler_encoder_of_the_number:
        # [list of predictive celln configuration predicting this number]}
        self.input_output_mapping = self.initialize_input_output_mapping()

        # predictive_cells dict: {col_index: [list of predictive cells in the column]}
        self.predictive_cells = {}

        # active_cells dict: {col_index: [list of active cells in the column]}
        self.active_cells = {}

        #  learning_cells dict: {col_index: [list of learning cells in the column]}
        self.learning_cells = {}

        # a variable to maintain the learning cells from last step
        self.prev_learning_cells = {}

        # keeps track of which element in the input sequence we currently on
        self.entry_count = 0

        # the current spatial pooler encoding the servse as input for the current step
        self.current_learning_matrix = []

        # the spatial pooler encoding that servse as input for the previous step
        self.previous_learning_matrix = []

    def initialize_space(self):
        #
        # a function that initializes the temporal memory space
        #
        # returns: output_dict = a dictionary with keys being the index of SP elements and values being lists of segment objects

        output_dict = {}

        # initialize the memory space
        for i in range(self.x):
            for j in range(self.y):
                output_dict[(i, j)] = {}
                for k in range(self.z):
                    # initialize the Segments object
                    output_dict[(i, j)][k] = Segments(i, j, k, x=self.x, y=self.y, z=self.z,
                                                      max_synapses_count=self.max_synapses_count)

        # add values to the Segments
        for i in range(self.x):
            for j in range(self.y):
                for k in range(self.z):
                    output_dict[(i, j)][k].initialize_segment(output_dict)

        return output_dict

    def reverse_mapping(self, mapping):
        #
        # a function that takes in the SP input-output mapping dictionary and reverse that mapping so we know
        # which SP elements match to which input data elements
        #
        # arguments:
        #       mapping = a dictionary whose keys are the input data elements and whose values are the SP indices of the elements
        #                   connected to the input data elements (meeting the permanence threshold)
        #
        # returns: output_dict, a dictionary whose keys are the SP elements and whose values are the keys of the argument mapping
        #

        output_dict = {}
        for i in list(mapping.keys()):
            output_dict[tuple(mapping[i])] = i

        return output_dict

    def initialize_input_output_mapping(self):
        #
        # a function that initializes a dictionary which will contain the mapping of elements in the spatial pooler to the elements in TM,
        # essentially helping us map the input data elements to elements in TM
        #
        # returns: output_dict, a dictionary with keys corresponding to the keys in SP output-input mapping dict
        #                       and values that are empty lists, for now

        output_dict = {}
        for i in list(self.spatial_pooler_output_input_mapping.keys()):
            output_dict[i] = []

        return output_dict

    def check_similarities_between_predictive_cells(self, dict_1, dict_2):
        #
        # a function that checks the overlap between two dictionaries
        #
        # arguments:
        #           dict_1 = a dictionary
        #           dict_2 = a dictionary
        #
        # returns:
        #           TRUE/FALSE = a logical operator that states whether or not the dicts are similar based on prediction score
        #           percentage = a float, between 0 and 1, reflects how much of the dicts are the same
        #

        ls_1 = []
        ls_2 = []

        # check which dictionary has the most keys, the bigger one becomes ref_ls, and the other one becomes test_ls
        for i in dict_1:
            for cell in dict_1[i]:
                # the initiator attribute is the position of the cell
                ls_1.append(cell.initiator)

        for i in dict_2:
            for cell in dict_2[i]:
                # the initiator attribute is the position of the cell
                ls_2.append(cell.initiator)

        if len(ls_1) >= len(ls_2):
            ref_ls = ls_1
            test_ls = ls_2

        else:
            ref_ls = ls_2
            test_ls = ls_1

        # get the number of overlap elements between the two dictionaries and if over 90%, return True
        overlap_count = 0
        for i in test_ls:
            if i in ref_ls:
                overlap_count += 1

        percentage = overlap_count * 100 / len(ref_ls)
        if percentage > 90:
            return True, percentage
        else:
            return False, percentage

    def learn_one_input(self):
        #
        # a function that goes through a learning phase after one singular input
        #
        # returns:
        #       self.entry_count = an integer, an attribute for Temporal_Memory, which represents the index of this sequence element
        #       predict_percentage = a float that describes how well the predictive cells cover the active cell set

        # The spatial pooler matrix has the activated cell positions instead of the entire binary matrix
        spatial_pooler_matrix = self.current_learning_matrix

        # initialize the memory dictionaries
        self.entry_count += 1
        self.active_cells = {}
        self.prev_learning_cells = self.learning_cells  # save previous time step of learning cells
        self.learning_cells = {}  # reset learning cells for this time step
        predict_percentage = 0

        max_percentage = 0
        outcome = None

        # if we've already gone through a learning step
        if self.previous_learning_matrix != []:
            # reset the max_percentage and outcome
            # given the predictive cells config, predict what the input is at this step
            # by looking at the similarities between this predictive cells config and the already known active ones

            for i in self.input_output_mapping:
                for j in self.input_output_mapping[i]:

                    similar, percentage = self.check_similarities_between_predictive_cells(j, self.predictive_cells)

                    if percentage >= max_percentage:
                        max_percentage = percentage
                        outcome = (i, j)

                    predict_percentage = max_percentage

            # print(
            #     "Actual is: " + str(
            #         self.spatial_pooler_output_input_mapping[tuple(self.current_learning_matrix)] + 1))

            # print(outcome)
            if outcome != None:
                # print("True encoding: " + str(self.current_learning_matrix))
                print(
                    "Actual is: " + str(
                        self.spatial_pooler_output_input_mapping[tuple(self.previous_learning_matrix)] + 1))
                print("Predicted as: " + str(self.spatial_pooler_output_input_mapping[outcome[0]] + 1))
                print("Percent Similarity is: " + str(max_percentage))

            else:
                print("undefined")
                print("Actual is: " + str(
                    self.spatial_pooler_output_input_mapping[tuple(self.previous_learning_matrix)] + 1))

            # as long as this is not the first step, add the predictive cells config to be one of the values of the
            # input_output_mapping at key being the current spatial pooler matrix
            add = True
            # for i in self.input_output_mapping[tuple(self.current_learning_matrix)]:
            #     similar, percentage = self.check_similarities_between_predictive_cells(i, self.predictive_cells)
            #     if similar:
            #         add = False
            # if add:
            #     self.input_output_mapping[tuple(self.current_learning_matrix)].append(self.predictive_cells)

            if add:
                self.input_output_mapping[tuple(self.current_learning_matrix)] = [self.predictive_cells]

        # get the active cells and the learning cells at this step
        for col in spatial_pooler_matrix:
            # if there is a predictive cell in the activated column, then select that as active and as learning
            if col in self.predictive_cells:
                potential_ls = self.predictive_cells[col]

                # if more than one predictive cell in that column, then randomly select
                # assign this as winner cell
                if len(potential_ls) > 1:
                    self.active_cells[col] = [potential_ls[random.randint(0, len(potential_ls) - 1)]]
                # if there is none, add the list for learning winner(s)
                else:
                    self.active_cells[col] = [potential_ls[0]]

            # if no predictive cell, then burst the entire column
            else:
                self.active_cells[col] = [self.memory_space[col][i] for i in range(self.z)]

        # Update perm value between prev learning cell and current active cells
        for col in spatial_pooler_matrix:
            # If there is a predictive cell in the activated column, then select that as active and as learning
            if col in self.predictive_cells:
                potential_ls = self.predictive_cells[col]

                # if there is more than one cell in the list, randomly select for learning winner
                if len(potential_ls) > 1:
                    self.learning_cells[col] = self.active_cells[col][0]
                # if there is none, add the list for learning winner(s)
                else:
                    self.learning_cells[col] = self.active_cells[col][0]

            else:

                # check the overlap_score and assign winner cell
                max_overlap_cells = []
                max_score = 0
                for i in range(self.z):
                    score = self.memory_space[col][i].get_max_overlap_score(self.active_cells)
                    if score > max_score:
                        max_score = score
                        max_overlap_cells = [self.memory_space[col][i]]
                    elif score == max_score:
                        max_overlap_cells.append(self.memory_space[col][i])
                    else:
                        continue

                # if there is more than one cell in the list, randomly select for learning winner
                if len(max_overlap_cells) > 1:
                    self.learning_cells[col] = max_overlap_cells[random.randint(0, len(max_overlap_cells) - 1)]

                # if there is none, add the list for learning winner(s)
                else:
                    self.learning_cells[col] = max_overlap_cells[0]

        # if there were any learning cells from the previous time step
        if len(self.prev_learning_cells) > 0:
            for col in self.prev_learning_cells:
                cell = self.prev_learning_cells[col]
                connecting_cells = []

                # determine their connecting cells and record position
                for j in self.active_cells:
                    active_cells_of_col = self.active_cells[j]

                    for k in active_cells_of_col:
                        # the initiator attribute is the position of the cell
                        connecting_cells.append(k.initiator)

                seg = cell
                # update the permanence for the cells: if connected to the learning cells from previous step, increase;
                # update the permanence for the cells: if NOT connected to the learning cells from previous step, decrease;
                seg.update_perm(connecting_cells, self.learn_inc_val, self.learn_dec_val)
                # add the list of connected cells to the segment object
                seg.add_segment(connecting_cells=connecting_cells)

        self.pred_state_threshold += 0.2
        #
        # get the predictive cells config for this step
        # any cell that has one Segment above a cetrain threshold
        self.predictive_cells = {}
        for col in self.memory_space:
            for cell in self.memory_space[col]:
                # check if any column cells have permanence above the threshold
                above = self.memory_space[col][cell].perm_above_pred_state_threshold(self.pred_state_threshold)
                # if True, then add those column cells to the list of predictive cells for next time step
                if above:
                    # if the column does not have any cells in the list of predictive cells
                    if col not in self.predictive_cells:
                        # then add the cells meeting the threshold to the list of predictive cells for the column
                        self.predictive_cells[col] = [self.memory_space[col][cell]]
                    # if the column does have cells in the list of predictive cells
                    else:
                        # then add them to the list of predictive cells
                        self.predictive_cells[col].append(self.memory_space[col][cell])

        return self.entry_count, predict_percentage

    def learn(self, matrix_ls):
        #
        # a function that does one learning step for each input from the data sequence
        #
        # arguments:
        #           matrix_ls = list of stuff
        #
        # returns:
        #           iter_ls = a list of integers, representing the index in the sequence each input is
        #           percentage_ls = a list of floats, representing percentages of how well the method predicted the step

        iter_ls = []
        percentage_ls = []
        for i in matrix_ls:
            # in other words, if we have information on the active cells at the time step T-1
            if self.current_learning_matrix != []:
                # save the time step info
                self.previous_learning_matrix = self.current_learning_matrix
            # set the current active cells list to the newly found active cells info
            self.current_learning_matrix = i

            # go through a learning process for time step T
            iter, learn_percentage = self.learn_one_input()

            if iter != 1:
                iter_ls.append(iter)
                percentage_ls.append(learn_percentage)

        return iter_ls, percentage_ls