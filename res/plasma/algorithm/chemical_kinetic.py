import numpy as np

from res.plasma.consts import e, k_b, m_cl, m_cl2, m_ar

from res.plasma.utils import good_form

from res.plasma.reactions_consts.Ar import give_k_1
from res.plasma.reactions_consts.Cl import give_k_3
from res.plasma.reactions_consts.Cl2 import give_k_2
from res.plasma.reactions_consts.Cl2 import give_k_4, give_k_5, give_k_13
from res.plasma.reactions_consts.common_reactions import k_ii

from res.plasma.algorithm.utils import count_m_eff


def count_simple_start(start_T_e, param_vector, do_print=False):
    p_0, T_gas, R, L, gamma_cl, y_ar, _, _ = param_vector

    A = (p_0 / (k_b * T_gas)) * (1 - y_ar)
    B = (p_0 / (k_b * T_gas)) * y_ar
    V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

    k_1 = give_k_1(start_T_e)  # Ar + e -> Ar(+) + 2e
    k_2 = give_k_2(start_T_e)  # Cl2 + e -> Cl2(+) + 2e
    k_3 = give_k_3(start_T_e)  # Cl + e -> Cl(+) + 2e
    k_4 = give_k_4(start_T_e)  # Cl2 + e -> Cl + Cl + 2e
    k_5 = give_k_5(start_T_e)  # Cl2 + e -> Cl + Cl(-)
    k_13 = give_k_13(start_T_e)  # Cl2 + e -> Cl(+) + Cl(-) + e

    k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl

    k_10 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_cl)
    k_11 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_cl2)
    k_12 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * start_T_e) / m_ar)

    if do_print:
        print("k_1: ", good_form(k_1))
        print("k_2: ", good_form(k_2))
        print("k_3 (Efremov): ", k_3)
        # print("k_3 (Hsu): ", good_form(give0_k_3(start_T_e)))
        print("k_4: ", good_form(k_4))
        print("k_5: ", good_form(k_5))
        print("k_ii: ", good_form(k_ii))
        print("k_9: ", good_form(k_9))
        print("k_10: ", good_form(k_10))
        print("k_11: ", good_form(k_11))
        print("k_12: ", good_form(k_12))
        print("k_13: ", good_form(k_13))
        print("v_t: ", good_form(V_T))
        print("A: ", good_form(A))
        print("b: ", good_form(B))

    return k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B


def count_n_plus_straight(j, T_e, params, is_m_eff=False, do_print=False):
    if is_m_eff:
        m_eff = params
    else:
        n_plus, n_cl2_plus, n_cl_plus, n_ar_plus = params
        m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)
    n_plus = (j / (0.61 * e)) * np.sqrt(m_eff / (k_b * T_e))
    if do_print:
        print("n_plus: ", good_form(n_plus))
    return n_plus


def solve_subsistem_consist(n_e, k_4, k_5, k_9, k_13, A, do_print=False):
    a = 2 * k_9 * k_ii + (2 * k_4 + k_5) * k_ii * n_e
    b = n_e * n_e * (2 * k_4 + k_5) * k_ii + k_ii * 2 * k_9 * n_e
    c = 2 * k_9 * n_e * A * (k_5 + k_13)
    n_plus = (b + np.sqrt(b ** 2 + 4 * a * c)) / (2 * a)
    n_cl2 = (2 * A * k_9) / (2 * k_9 + (2 * k_4 + k_5) * n_e)
    n_cl = 2 * A - 2 * n_cl2
    n_cl_minus = n_plus - n_e
    if do_print:
        print("n_plus: ", good_form(n_plus))
        print("n_cl2: ", good_form(n_cl2))
        print("n_cl: ", good_form(n_cl))
        print("n_cl_minus: ", good_form(n_cl_minus))
    return n_plus, n_cl2, n_cl, n_cl_minus


def solve_subsistem(k_4, k_5, k_9, k_13, n_plus, A, do_print=False):
    b = (2 * k_4 + k_5) * k_ii * n_plus * n_plus - 2 * k_9 * (A * (k_5 + k_13) + k_ii * n_plus)
    ac = 2 * k_9 * (k_ii ** 2) * (n_plus ** 3) * (2 * k_4 + k_5)
    n_e = (b + np.sqrt(b * b + 4 * ac)) / (2 * (2 * k_4 + k_5) * k_ii * n_plus)
    n_cl2 = (2 * A * k_9) / (2 * k_9 + (2 * k_4 + k_5) * n_e)
    n_cl = 2 * A - 2 * n_cl2
    n_cl_minus = n_plus - n_e
    if do_print:
        print("n_e: ", good_form(n_e))
        print("n_cl2: ", good_form(n_cl2))
        print("n_cl: ", good_form(n_cl))
        print("n_cl_minus: ", good_form(n_cl_minus))
    return n_e, n_cl2, n_cl, n_cl_minus


def count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3, k_10, k_11, k_12, k_13, do_print=False):
    n_cl_plus = ((k_3 * n_cl + k_13 * n_cl2) * n_e) / (k_ii * n_cl_minus + k_10)
    n_cl2_plus = (k_2 * n_cl2 * n_e) / (k_ii * n_cl_minus + k_11)
    n_ar_plus = (B * k_1 * n_e) / (k_ii * n_cl_minus + k_1 * n_e + k_12)
    alpha = n_plus / (n_cl_plus + n_cl2_plus + n_ar_plus)

    n_cl_plus = alpha * n_cl_plus
    n_cl2_plus = alpha * n_cl2_plus
    n_ar_plus = alpha * n_ar_plus
    n_ar = B  # - n_ar_plus

    alpha_cl_plus = n_cl_plus / n_plus
    alpha_cl2_plus = n_cl2_plus / n_plus
    alpha_ar_plus = n_ar_plus / n_plus
    if do_print:
        print("alpha: ", round(alpha, 10))
        print("n_cl_plus: ", good_form(n_cl_plus))
        print("n_cl2_plus: ", good_form(n_cl2_plus))
        print("n_ar_plus: ", good_form(n_ar_plus))
        print("n_ar: ", good_form(n_ar))
        print("alpha_cl_plus: ", round(alpha_cl_plus, 3))
        print("alpha_cl2_plus: ", round(alpha_cl2_plus, 3))
        print("alpha_ar_plus: ", round(alpha_ar_plus, 3))
    return n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, (alpha_cl_plus, alpha_cl2_plus, alpha_ar_plus)


def count_ks_chem(T_e, do_print=False):
    k_1 = give_k_1(T_e)
    k_2 = give_k_2(T_e)
    k_3 = give_k_3(T_e)
    k_4 = give_k_4(T_e)
    k_5 = give_k_5(T_e)
    k_13 = give_k_13(T_e)
    if do_print:
        print("k_1: ", good_form(k_1))
        print("k_2: ", good_form(k_2))
        print("k_3: ", good_form(k_3))
        print("k_4: ", good_form(k_4))
        print("k_5: ", good_form(k_5))
        print("k_13: ", good_form(k_13))
    return (k_1, k_2, k_3, k_4, k_5, k_13)
