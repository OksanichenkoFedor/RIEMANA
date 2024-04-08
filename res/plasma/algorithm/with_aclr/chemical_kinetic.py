import numpy as np
from numba import jit

from res.plasma.reactions.consts import e, k_b, m_cl, m_cl2, m_ar

from res.plasma.reactions.common_reactions import k_ii

from res.plasma.algorithm.with_aclr.utils import count_m_eff
from res.plasma.reactions.reactions_conts import give_k

@jit(nopython=True)
def count_ks_chem(T_e, chem_data, chem_connector):
    k_1 = give_k(chem_data[chem_connector[1]], T_e)  # Ar + e -> Ar(+) + 2e
    k_2 = give_k(chem_data[chem_connector[2]], T_e)  # Cl2 + e -> Cl2(+) + 2e
    k_3 = give_k(chem_data[chem_connector[3]], T_e)  # Cl + e -> Cl(+) + 2e
    k_4 = give_k(chem_data[chem_connector[4]], T_e)  # Cl2 + e -> Cl + Cl + 2e
    k_5 = give_k(chem_data[chem_connector[5]], T_e)  # Cl2 + e -> Cl + Cl(-)
    k_13 = give_k(chem_data[chem_connector[13]], T_e)  # Cl2 + e -> Cl(+) + Cl(-) + e
    return (k_1, k_2, k_3, k_4, k_5, k_13)

@jit(nopython=True)
def count_simple_start(start_T_e, param_vector, chem_data, chem_connector):
    p_0, T_gas, R, L, gamma_cl, y_ar, _, _ = param_vector

    A = (p_0 / (k_b * T_gas)) * (1 - y_ar)
    B = (p_0 / (k_b * T_gas)) * y_ar
    V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

    k_1, k_2, k_3, k_4, k_5, k_13 = count_ks_chem(start_T_e, chem_data, chem_connector)

    k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl

    k_10 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_cl)
    k_11 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_cl2)
    k_12 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_ar)

    return k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B

@jit(nopython=True)
def count_n_plus_straight(j, T_e, params, is_m_eff=False):
    if is_m_eff:
        m_eff = params
    else:
        n_plus, n_cl2_plus, n_cl_plus, n_ar_plus = params
        m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
    n_plus = (j / (0.61 * e)) * np.sqrt(m_eff / (k_b * T_e))
    return n_plus

@jit(nopython=True)
def solve_subsistem_consist(n_e, k_4, k_5, k_9, k_13, A):
    a = 2 * k_9 * k_ii + (2 * k_4 + k_5) * k_ii * n_e
    b = n_e * n_e * (2 * k_4 + k_5) * k_ii + k_ii * 2 * k_9 * n_e
    c = 2 * k_9 * n_e * A * (k_5 + k_13)
    n_plus = (b + np.sqrt(b ** 2 + 4 * a * c)) / (2 * a)
    n_cl2 = (2 * A * k_9) / (2 * k_9 + (2 * k_4 + k_5) * n_e)
    n_cl = 2 * A - 2 * n_cl2
    n_cl_minus = n_plus - n_e
    return n_plus, n_cl2, n_cl, n_cl_minus

@jit(nopython=True)
def solve_subsistem(k_4, k_5, k_9, k_13, n_plus, A):
    b = (2 * k_4 + k_5) * k_ii * n_plus * n_plus - 2 * k_9 * (A * (k_5 + k_13) + k_ii * n_plus)
    ac = 2 * k_9 * (k_ii ** 2) * (n_plus ** 3) * (2 * k_4 + k_5)
    n_e = (b + np.sqrt(b * b + 4 * ac)) / (2 * (2 * k_4 + k_5) * k_ii * n_plus)
    n_cl2 = (2 * A * k_9) / (2 * k_9 + (2 * k_4 + k_5) * n_e)
    n_cl = 2 * A - 2 * n_cl2
    n_cl_minus = n_plus - n_e
    return n_e, n_cl2, n_cl, n_cl_minus

@jit(nopython=True)
def count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3, k_10, k_11, k_12, k_13):
    n_cl_plus = ((k_3 * n_cl + k_13 * n_cl2) * n_e) / (k_ii * n_cl_minus + k_10)
    n_cl2_plus = (k_2 * n_cl2 * n_e) / (k_ii * n_cl_minus + k_11)
    n_ar_plus = (B * k_1 * n_e) / (k_ii * n_cl_minus + k_1 * n_e + k_12)
    alpha = n_plus / (n_cl_plus + n_cl2_plus + n_ar_plus)

    n_cl_plus = alpha * n_cl_plus
    n_cl2_plus = alpha * n_cl2_plus
    n_ar_plus = alpha * n_ar_plus
    n_ar = B - n_ar_plus

    alpha_cl_plus = n_cl_plus / n_plus
    alpha_cl2_plus = n_cl2_plus / n_plus
    alpha_ar_plus = n_ar_plus / n_plus
    return n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, (alpha_cl_plus, alpha_cl2_plus, alpha_ar_plus)
