import random
from cathy_encoder import *
from numeric_encoder import *
from spatial_pooler import *
import matplotlib.pyplot as plt
from temporal_memory_v3 import *

def test_case_1():
    input_ls = []
    sample = [[1, 5, 7, 3, 2]]
    sample_size = 1

    # take the elements of the sample and make sequence that repeats that pattern in a list
    for i in range(30):
        for j in sample[random.randint(0, sample_size-1)]:
            input_ls.append(j)

    return input_ls

# def random_selected_test():
#     input_ls = []
#     for i in range(50):
#         input_ls.append(random.randint(1, 7))
#     return input_ls

def run_HTM(input_ls):
    
    # Step 1: Encode the numeric sequence into a sequence of sparse, binary elements
    encoded_ls = []
    for elem in input_ls:
        e = encode(elem)
        encoded_ls.append(e) 
    # print(encoded_ls) # outputs a sequence of sparse, binary representations just as expected

    # Step 2: Determine the Spatial Pooler representation of the sequence of inputs (identifies the cortical columns activated)
    pooler_ls, mapping = Spatial_Pooler().transform(encoded_ls)
    #print(pooler_ls) # a list of lists of tuples representing the location of activated columns, as expected
    #print("\n")
    #print(mapping) # maps those list of tuples to the input elements, as expected
    
    # Step 3: Learning with Temporal Memory Loop
    
    # This is where we are getting output that we are not expecting.  Lines 224 to 239 are the output we're struggling with.
    iter_ls, percentage_ls = Temporal_Memory(spatial_pooler_input_output_mapping=mapping).learn(pooler_ls)
    plt.plot(iter_ls, percentage_ls)
    plt.show()
    

run_HTM(test_case_1())