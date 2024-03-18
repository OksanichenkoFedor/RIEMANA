from numba import njit
import numpy as np

@njit()
def custom_choise(Ps):
    #if Ps.sum()!=1:
    #    int("b")
    num = np.random.random()
    sum = 0
    for i in range(len(Ps)):
        sum+=Ps[i]
        if num<sum:
            return i