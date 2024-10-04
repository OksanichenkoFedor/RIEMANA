import numpy as np
import matplotlib.pyplot as plt

from res.plasma.reactions.consts import e, k_b
from res.plasma.algorithm.electron_temperature import count_T_e
from res.plasma.algorithm.energy_loss import count_n_e
from res.plasma.algorithm.chemical_kinetic import count_simple_start, solve_subsistem_consist, count_ions
from res.plasma.algorithm.utils import count_T_i




def run_consist_model(p_0, T_gas, R, L, gamma_cl, y_ar, W, consts,plot_error=False):


    chem_data, chem_connector, inel_data, inel_connector, el_data, el_connector, ar_vec, cl2_vec, cl_vec = consts

    V = np.pi * R * R * L
    param_vector = (p_0, T_gas, R, L, gamma_cl, y_ar, W, V)
    T_e = 5 * (e / k_b)
    n_e = 1.0 * 10.00 ** (16)

    n_cl_old = None
    delta_n_e = 1
    num = 0
    Deltas = []
    Deltas_cl = []
    Deltas_T_e = []
    Deltas_n_e = []

    k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B = count_simple_start(T_e, param_vector, chem_data, chem_connector)

    while (np.abs(delta_n_e) >= 10.0 ** (-15.0)) and (num <= 20):
        num += 1

        n_plus, n_cl2, n_cl, n_cl_minus = solve_subsistem_consist(n_e, k_4, k_5, k_9, k_13, A)

        n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, alphas = count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2,
                                                                    k_3, k_10, k_11, k_12, k_13)

        n_vector = (n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus)

        k_inp = (k_1, k_2, k_3, k_5, k_13)

        n_e_new, inel_parts, el_parts, el_part, inel_part, W_ion, W_e = count_n_e(T_e, n_vector, param_vector,
                                                                                  inel_data, inel_connector,
                                                                                  el_data, el_connector,
                                                                                  ar_vec, cl2_vec, cl_vec)
        delta_n_e = (n_e - n_e_new) / (n_e + n_e_new)
        Deltas_n_e.append(np.abs(delta_n_e))
        n_e = n_e_new

        n_vector = (n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus)

        k_s, T_e_new, js = count_T_e(n_vector, param_vector, chem_data, chem_connector)
        j_cl, j_ar_plus, j_cl_plus, j_cl2_plus = js

        k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12 = k_s





        if n_cl_old is None:
            pass
        else:
            delta1 = (n_cl_old - n_cl) / (n_cl_old + n_cl)
            Deltas_cl.append(np.abs(delta1))
            delta_T_e = (T_e - T_e_new) / (T_e + T_e_new)
            Deltas_T_e.append(np.abs(delta_T_e))
        n_cl_old = n_cl
        T_e = T_e_new

    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e1, n_cl_minus = n_vector

    res = {
        "T_e": T_e,
        "n_plus": n_plus,
        "n_e": n_e,
        "n_cl_minus": n_cl_minus,
        "n_cl_plus": n_cl_plus,
        "n_cl": n_cl,
        "n_cl2": n_cl2,
        "n_cl2_plus": n_cl2_plus,
        "n_ar": n_ar,
        "n_ar_plus": n_ar_plus,
        "Deltas_T_e": Deltas_T_e,
        "Deltas_n_e": Deltas_n_e,
        "W_e": W_e,
        "W_ion": W_ion,
        "W_el": el_part * n_e_new,
        "W_inel": inel_part * n_e_new,
        "W_el_Ar": el_parts[0],
        "W_el_Cl2": el_parts[1],
        "W_el_Cl": el_parts[2],
        "W_inel_Ar": inel_parts[0],
        "W_inel_Cl2": inel_parts[1],
        "W_inel_Cl": inel_parts[2],
        "j_cl": j_cl,
        "j_ar_plus": j_ar_plus,
        "j_cl_plus": j_cl_plus,
        "j_cl2_plus": j_cl2_plus,
        "T_i": count_T_i(p_0, T_gas)*(k_b/e)
    }

    if plot_error:
        plt.semilogy(Deltas_cl, "o", label="n_cl")
        plt.semilogy(Deltas, ".", label="n_plus")
        plt.semilogy(Deltas_T_e, ".", label="T_e")
        plt.semilogy(Deltas_n_e, ".", label="n_e")
        plt.title("Динамика ошибки от номера итерации")
        plt.grid()
        plt.legend()
        plt.show()
    return res