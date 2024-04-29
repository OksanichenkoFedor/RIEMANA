from numba import njit

@njit()
def find_index(border_layer, x, y):
    ind = -1
    for i in range(len(border_layer)):
        if border_layer[i][0] == x and border_layer[i][1] == y:
            ind = i
    return ind