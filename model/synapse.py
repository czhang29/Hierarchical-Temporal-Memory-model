#
# Object called Synapse
#
# attributes:
#           end_1 = a cell in TM space
#           end_2 = a cell in TM space
#           initiators = a tuple listing the pair of cells with the connection
#           perm_val = a float, the permanence value of the connection between cells

# functions:
#       __init__(., end_1, end_2, perm_val = 0)
#       complete_connection(.)

class Synapse:
    def __init__(self, end_1, end_2, perm_val = 0):
        self.end_1 = end_1
        self.end_2 = end_2
        self.initiators = (end_1, end_2)
        self.perm_val = perm_val

    def complete_connection(self):
        #
        # a function that creates the connection between cells in TM space
        #
        if self.end_2.accept_add == True:
            self.end_2.add_synapse(self)
        else:
            raise("Something went wrong for adding synapse to the segments list ")