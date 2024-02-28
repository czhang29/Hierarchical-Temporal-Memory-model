
import random
from spatial_pooler import *
from segment import *
from segment_ls import Segments

class Temporal_Memory():
    def __init__(self, spatial_pooler_dim = (10,10), cells_per_column = 5, max_synapses_count = 7, pred_state_threshold = 0.5, learn_inc_val = 0.1, learn_dec_val=0.1):
        self.x, self.y = spatial_pooler_dim
        self.z = cells_per_column
        # {col_index:{cell_index: [connected cells]}}
        self.max_synapses_count = max_synapses_count
        self.memory_space = self.initialize_space()
        self.pred_state_threshold = pred_state_threshold
        self.learn_inc_val = learn_inc_val
        self.learn_dec_val = learn_dec_val
        self.predictive_cells = {}
        self.active_cells = {}
        self.learning_cells = {}
        self.prev_learning_cells = {}
        self.entry_count = 0

    def initialize_space(self):
        output_dict = {}
        # temp_dict ={(2,2):{3:3}}
        # print(temp_dict[(2,2)][3])
        for i in range(self.x):
            for j in range(self.y):
                output_dict[(i,j)] = {}
                for k in range(self.z):
                    # print(output_dict[(i, j)][k])
                    output_dict[(i, j)][k] = Segments(i,j,k)
                    output_dict[(i, j)][k].add_segment(Segment(i, j, k, x=self.x, y=self.y, z= self.z, max_synapses_count = self.max_synapses_count))
                    # print(output_dict[(i, j)][k])

        return output_dict

    def learn_one_input(self, spatial_pooler_matrix):
        # The spatial pooler matrix has the activated cells position instead of the entire matrix in 0,1
        self.entry_count +=1
        self.active_cells = {}
        self.prev_learning_cells = self.learning_cells
        # print(self.prev_learning_cells)
        self.learning_cells = {}
        count = 0

        for col in spatial_pooler_matrix:
            if col in self.predictive_cells:
                count += 1
                potential_ls = self.predictive_cells[col]
                if len(potential_ls) > 1:
                    self.active_cells[col] = [potential_ls[random.randint(0,len(potential_ls)-1)]]
                    # assign this as winner cell
                    self.learning_cells[col] = self.active_cells[col][0]
                    # print("a")
                    # print(self.active_cells[col][0])
                else:
                    self.active_cells[col] = [potential_ls[0]]
                    self.learning_cells[col] = self.active_cells[col][0]
                    # print("b")
                    # print(self.active_cells[col][0])
            else:
                self.active_cells[col] = [self.memory_space[col][i] for i in range(self.z)]
                # check the overlap_score and assign winner cell
                max_overlap_cells = []
                max_score = 0
                for i in range(self.z):
                    score = self.memory_space[col][i].get_max_overlap_score(self.active_cells)
                    if score > max_score:
                        max_score = score
                        max_overlap_cells = self.memory_space[col][i]
                    elif score == max_score:
                        max_overlap_cells.append(self.memory_space[col][i])
                    else:
                        continue
                if len(max_overlap_cells) >1:
                    self.learning_cells[col] = max_overlap_cells[random.randint(0,len(max_overlap_cells)-1)]
                    # print("c")
                    # print(max_overlap_cells[random.randint(0,len(max_overlap_cells)-1)])

                else:
                    self.learning_cells[col] = max_overlap_cells[0]
                    # print("d")
                    # print(max_overlap_cells[0])
        if self.entry_count != 1:
            # print(self.entry_count)
            # print(len(self.predictive_cells))
            print(len(self.active_cells))
            result = (self.entry_count,count / len(self.predictive_cells) * 100)
        else:
            print(len(self.active_cells))
            result = (1,100)

        ## Update perm value between prev learning cell and current active cells
        if len(self.prev_learning_cells) > 0:
            for col in self.prev_learning_cells:
                cell = self.prev_learning_cells[col]
                # print("This is")
                # print(cell)
                connecting_cells = []
                for j in self.active_cells:
                    active_cells_of_col = self.active_cells[j]
                    # print(active_cells_of_col)
                    for k in active_cells_of_col:
                        connecting_cells.append(k.initiator)
                # print(self.memory_space[col])
                # seg=self.memory_space[col][cell]
                # print(len(cell))
                seg = cell
                # print(seg)
                seg.update_perm(connecting_cells, self.learn_inc_val, self.learn_dec_val)
                seg.add_segment(Segment(col[0], col[1], cell, connected_cells=connecting_cells))


        self.predictive_cells = {}
        for col in self.memory_space:
            for cell in self.memory_space[col]:
                above = self.memory_space[col][cell].perm_above_pred_state_threshold(self.pred_state_threshold)
                if above:
                    if col not in self.predictive_cells:
                        self.predictive_cells[col] = [self.memory_space[col][cell]]
                    else:
                        self.predictive_cells[col].append(self.memory_space[col][cell])


        return result


    def learn(self, matrix_ls):
        iter_ls = []
        percentage_ls = []
        for i in matrix_ls:
            iter, learn_percentage = self.learn_one_input(i)
            if iter != 1:
                iter_ls.append(iter)
                percentage_ls.append(learn_percentage)

        return iter_ls, percentage_ls
        # return self.memory_space