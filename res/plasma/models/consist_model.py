import numpy as np
import matplotlib.pyplot as plt

from res.plasma.consts import e, k_b

from res.plasma.algorithm.part_solver import solve_part
from res.plasma.algorithm.energy_loss import count_n_e

from res.plasma.utils import good_form


def run_consist_model(p_0, T_gas, R, L, gamma_cl, y_ar, W, plot_error=False, simple=False):
    print(y_ar)
    V = np.pi * R * R * L
    param_vector = (p_0, T_gas, R, L, gamma_cl, y_ar, W, V)
    T_e = 5 * (e / k_b)
    n_e = 1.0 * 10.00 ** (16)

    n_cl_old = None
    delta_n_e = 1
    delta_T_e = 1
    num = 0
    Deltas = []
    Deltas_cl = []
    Deltas_T_e = []
    Deltas_n_e = []

    while (np.abs(delta_n_e) >= 10.0 ** (-8.0)) and (num <= 20):
        #print("###")
        num += 1

        T_e, n_vector, Deltas_T_e_add = solve_part(n_e, param_vector)
        Deltas_T_e = Deltas_T_e + Deltas_T_e_add

        # cчитаем n_e
        #print("n_e")

        n_e_new, inel_parts, el_parts, el_part, inel_part, W_ion, W_e = count_n_e(T_e, n_vector, param_vector, do_print=False)

        delta_n_e = (n_e - n_e_new) / (n_e + n_e_new)
        Deltas_n_e.append(np.abs(delta_n_e))
        #print("delta_n_e: ", delta_n_e)
        print("n_e: ",good_form(n_e))
        #print("T_e: ", round(T_e*(k_b/e), 3))
        n_e = n_e_new

    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e1, n_cl_minus = n_vector

    res = {
        "T_e": T_e,
        "n_plus": n_plus,
        "n_e": n_e,
        "n_cl_minus": n_cl_minus,
        "n_cl": n_cl,
        "Deltas_T_e": Deltas_T_e,
        "Deltas_n_e": Deltas_n_e,
        "W_e": W_e,
        "W_ion": W_ion,
        "W_el": el_part*n_e_new,
        "W_inel": inel_part * n_e_new,
        "W_el_Ar": el_parts[0],
        "W_el_Cl2": el_parts[1],
        "W_el_Cl": el_parts[2],
        "W_inel_Ar": inel_parts[0],
        "W_inel_Cl2": inel_parts[1],
        "W_inel_Cl": inel_parts[2]
    }

    print(num)
    if plot_error:
        #plt.semilogy(Deltas_cl, "o", label="n_cl")
        #plt.semilogy(Deltas, ".", label="n_plus")
        #plt.semilogy(Deltas_T_e, label="T_e")
        plt.semilogy(Deltas_n_e, ".", label="n_e")
        plt.title("Динамика ошибки от номера итерации")
        plt.grid()
        plt.legend()
        plt.show()
    return res
