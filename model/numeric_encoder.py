import numpy as np

#
# a function that takes a sequence of real numbers and encodes it into a sparse, binary matrix
#
# arguments: data, a list containing the elements of a numeric sequence
#
# returns: output_ls, a list containing the sparse, binary encoding of the elements of a numeric sequence
#
def numeric_encoder(data):

    # determine range of numeric sequence
    [n,m] = [np.min(data), np.max(data)]
    # break that range up into 10 subintervals
    i = 0; N = 10; h = (m-n)/N
    output_ls = []
    
    for k in range(len(data)): 
        
        temp = [0 for j in range(N+1)]
        # check to see which subinterval the sequence element is in
        for i in range(N+1):
            if (k >= (n + i*h)) & (k < (n + (i+1)*h)):
                        # put a 1 in that subinterval
                        temp[i] = 1

            i+=1

    output_ls.append(temp)

    return output_ls 

