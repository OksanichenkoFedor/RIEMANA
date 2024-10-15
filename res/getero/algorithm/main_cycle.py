import numba as nb
import numpy as np
from res.utils.wrapper import clever_njit


from res.getero.ray_tracing.bvh.particle_processing import process_one_particle as segm_pp
from res.getero.ray_tracing.cell_by_cell.particle_processing import process_one_particle as cbc_pp
from res.getero.ray_tracing.cell_by_cell.old_pc import process_one_particle as old_cbc_pp

from res.utils.config import do_njit, cache, parallel

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_particles(counter_arr, is_full_arr, border_layer_arr, params_arr, Si_num, xsize, ysize, R, test, do_half,
                      max_value=-1.0, NodeList=np.zeros((10,7)), type="cell by cell", num_one_side_points=0, seed=-1):
    if test:
        arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                       nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    else:
        arr_x, arr_y, rarr_x, rarr_y = None, None, None, None

    returned_particles = np.zeros(11)
    for i in range(len(params_arr)):
        curr_params_arr = params_arr[i]
        if type=="cell by cell":
            cbc_pp(counter_arr, is_full_arr, border_layer_arr,
                   returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                   curr_params_arr, Si_num, xsize, ysize, R, test, do_half, max_value, num_one_side_points, seed)
        elif type=="old cell by cell":
            old_cbc_pp(counter_arr, is_full_arr, border_layer_arr,
                       returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                       curr_params_arr, Si_num, xsize, ysize, R, test, do_half, max_value, num_one_side_points)
        elif type=="line search":
            NodeList = segm_pp(counter_arr, is_full_arr, border_layer_arr, NodeList, returned_particles, arr_x, arr_y,
                               rarr_x, rarr_y, curr_params_arr, Si_num, xsize, ysize, R, test, do_half, max_value,
                               "line search", num_one_side_points, seed)
        elif type=="bvh":
            NodeList = segm_pp(counter_arr, is_full_arr, border_layer_arr, NodeList,
                   returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                   curr_params_arr, Si_num, xsize, ysize, R, test, do_half, max_value, "bvh",
                               num_one_side_points, seed)
        else:
            print("process_particles, wrong type: ", type)
    return returned_particles, arr_x, arr_y, rarr_x, rarr_y, NodeList