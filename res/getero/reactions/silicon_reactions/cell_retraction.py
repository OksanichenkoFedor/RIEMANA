import numpy as np

from res.getero.algorithm.dynamic_profile import give_coords_from_num
from res.getero.algorithm.utils import custom_choise
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angle, isotropic_retraction):
    is_around = np.zeros(8)
    koeffs = np.zeros(8)
    for i in range(8):
        new_x, new_y = give_coords_from_num(i, curr_x, curr_y)
        if new_x==is_full_arr.shape[0] or new_x==-1:
            is_around[i] = 0
        elif new_y==is_full_arr.shape[1] or new_y==-1:
            is_around[i] = 0
        elif is_full_arr[new_x, new_y]:
            is_around[i] = 1
        else:
            is_around[i] = 0
        if is_around[i]==0:
            koeffs[i] = 0
        else:
            delta_angle = angle-i*0.25*np.pi
            koeffs[i] = 0.5+0.5*np.cos(delta_angle)

    if isotropic_retraction:
        beta = 0
    else:
        beta = 10000
    koeffs = np.exp((koeffs - np.max(koeffs)) * beta) * is_around

    koeffs = koeffs / koeffs.sum()
    for i in range(counter_arr.shape[0]):
        num_adds = integer_ratio(koeffs, counter_arr[i, curr_x, curr_y])
        for j in range(8):
            new_x, new_y = give_coords_from_num(j, curr_x, curr_y)
            if -1<new_x<counter_arr.shape[1] and -1<new_y<counter_arr.shape[2]:
                counter_arr[i, new_x, new_y]+=num_adds[j]

    is_full_arr[curr_x, curr_y] = 0
    counter_arr[0, curr_x, curr_y] = 0
    counter_arr[1, curr_x, curr_y] = 0
    counter_arr[2, curr_x, curr_y] = 0
    counter_arr[3, curr_x, curr_y] = 0
    return koeffs





@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def integer_ratio(koeffs,num):

    result = np.zeros(koeffs.shape)
    deltas = np.zeros(koeffs.shape)
    for i in range(len(result)):
        result[i] = int(koeffs[i]*num)
        deltas[i] = koeffs[i]*num - result[i]
    num_add = round(np.sum(deltas))
    for i in range(num_add):
        deltas = deltas/np.sum(deltas)
        ind = custom_choise(deltas)
        if deltas[int(ind)]==0.0:
            print("incorrect add of particle cell_retraction")
        result[int(ind)]+=1
        deltas[int(ind)]=0.0
    return result