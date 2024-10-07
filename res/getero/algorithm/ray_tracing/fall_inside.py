import numpy as np


from res.getero.algorithm.ray_tracing.bvh import bvh_count_collision_point
from res.getero.algorithm.ray_tracing.utils import count_angle
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_fall_inside(border_arr, curr_vec, NodeList, curr_segment):
    zero_p_x = border_arr.shape[0]*0.5
    zero_p_y = 0
    test_angle = count_angle(zero_p_y - curr_vec[1], zero_p_x - curr_vec[0])
    #print("test_angle: ",test_angle/np.pi)
    _, _, _, _, num = bvh_count_collision_point(NodeList, curr_vec, test_angle, curr_segment)

    if num%2==1:
        print("We are inside!!! Upper should be CREATE")
        print(num)
    return num%2==1