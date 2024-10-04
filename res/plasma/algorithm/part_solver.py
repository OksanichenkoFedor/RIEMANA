import numpy as np
from numba import jit

from res.plasma.reactions.consts import e, k_b

from res.plasma.algorithm.chemical_kinetic import solve_subsistem_consist, count_ions, count_simple_start
from res.plasma.algorithm.electron_temperature import count_T_e

@jit(nopython=True)
def solve_part(n_e, param_vector):
    T_e = 5 * (e / k_b)
    k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B = count_simple_start(T_e, param_vector, do_print=False)
    delta_T_e = 1
    Deltas_T_e = []
    num = 0
    strict_solve = 0
    while delta_T_e >= 10.0 ** (-5):
        num+=1

        n_plus, n_cl2, n_cl, n_cl_minus = solve_subsistem_consist(n_e, k_4, k_5, k_9, k_13, A, do_print=False)

        n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, alphas = count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2,
                                                                    k_3,
                                                                    k_10, k_11, k_12, k_13, do_print=False)


        n_vector = (n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus)

        k_inp = (k_1, k_2, k_3, k_5, k_13)
        k_s, T_e_new = count_T_e(n_vector, param_vector, strict_solve=strict_solve, do_print=False)


        k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12 = k_s

        delta_T_e = np.abs((T_e - T_e_new) / (T_e + T_e_new))
        Deltas_T_e.append(delta_T_e)
        T_e = T_e_new
    return T_e, n_vector, Deltas_T_e