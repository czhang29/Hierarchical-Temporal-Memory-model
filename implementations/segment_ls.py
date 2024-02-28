

class Segments():
    def __init__(self,i, j, k):
        self.initiator = (i, j, k)
        self.segment_ls = []

    def add_segment(self, seg):
        self.segment_ls.append(seg)

    def get_max_overlap_score(self, active_cells_dict):
        max_score = 0
        for i in self.segment_ls:
            if i.get_overlap_cells(active_cells_dict) > max_score:
                max_score = i.get_overlap_cells(active_cells_dict)

        return max_score

    def perm_above_pred_state_threshold(self, pred_state_threshold):
        above = False
        for i in self.segment_ls:
            if i.sum_perm_values() > pred_state_threshold:
                above = True
        return above


    def update_perm(self, cell_ls, add_val, dec_val):
        for i in self.segment_ls:
            i.search_and_adjust(cell_ls, add_val, dec_val)
