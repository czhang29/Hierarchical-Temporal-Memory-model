
def encode(num):
    output_ls = []
    for i in range(7):
        if i == num-1:
            output_ls.append([1,1,1,1,1,1,1])
        else:
            output_ls.append([0,0,0,0,0,0,0])

    return output_ls