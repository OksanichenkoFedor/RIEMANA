import numpy as np
import matplotlib.pyplot as plt

from res.plasma.utils import good_form
from res.plasma.consts import e, k_b, m_ar, m_cl2, m_cl
from res.plasma.reactions_consts.common_reactions import give_k_getero, k_ii
from res.plasma.reactions_consts.Ar import give_k_1
from res.plasma.reactions_consts.Cl import give_k_3
from res.plasma.reactions_consts.Cl2 import give_k_2
from res.plasma.reactions_consts.Cl2 import give_k_5, give_k_13
from res.plasma.algorithm.for_testing.chemical_kinetic import count_m_eff, count_ks_chem
from res.plasma.algorithm.for_testing.beta_s import count_beta_s

from res.plasma.algorithm.for_testing.utils import count_T_i, count_lambda, count_v, count_d_c, count_D_i


def count_ks(T_e, n_vector, param_vector, do_print=False, simple=False):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _, _, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)

    T_i = count_T_i(p_0, T_gas, do_print=False)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    v = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False)
    V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

    k_1, k_2, k_3, k_4, k_5, k_13 = count_ks_chem(T_e, do_print=False)

    k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl
    k_10 = give_k_getero(T_e, m_cl, beta_s, gamma_T, d_c)
    k_11 = give_k_getero(T_e, m_cl2, beta_s, gamma_T, d_c)
    k_12 = give_k_getero(T_e, m_ar, beta_s, gamma_T, d_c)
    if do_print:
        print("k_1: ", good_form(k_1))
        print("k_2: ", good_form(k_2))
        print("k_3: ", good_form(k_3))
        print("k_4: ", good_form(k_4))
        print("k_5: ", good_form(k_5))
        print("k_9: ", good_form(k_9))
        print("k_10: ", good_form(k_10))
        print("k_11: ", good_form(k_11))
        print("k_12: ", good_form(k_12))
    return (k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12)


def count_left_fTe(T_e, n_cl2, n_cl, n_ar):
    k_1 = give_k_1(T_e)
    k_2 = give_k_2(T_e)
    k_3 = give_k_3(T_e)
    return 2 * (k_2 * n_cl2 + k_3 * n_cl + k_1 * n_ar)


def count_right_fTe(T_e, n_vector, mini_param_vector):
    p_0, T_gas, R, L, m_eff = mini_param_vector
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    k_5 = give_k_5(T_e)
    k_13 = give_k_13(T_e)
    T_i = count_T_i(p_0, T_gas, do_print=False)

    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    #v_old = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    v_cl_plus = count_v(T_e, beta_s, m_cl, gamma_T, do_print=False)
    v_cl2_plus = count_v(T_e, beta_s, m_cl2, gamma_T, do_print=False)
    v_ar_plus = count_v(T_e, beta_s, m_ar, gamma_T, do_print=False)
    v = (n_cl_plus * v_cl_plus + n_cl2_plus * v_cl2_plus + n_ar_plus * v_ar_plus) / n_plus
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False)
    return (k_5 - k_13) * n_cl2 + ((2 * v) / (d_c) + k_ii * beta * n_e) * (1 + beta)


def count_T_e(n_vector, param_vector, strict_solve,do_print=False):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _, _, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)
    mini_param_vector = (p_0, T_gas, R, L, m_eff)
    #gamma_crit = count_min_gamma_T(n_cl_minus/n_e)
    #T_crit = gamma_crit*count_T_i(p_0,T_gas)
    delta = 1
    left_T_e = 0.5 * (e / k_b)
    right_T_e = 5 * (e / k_b)
    if strict_solve == 1:
        left_T_e = T_crit
    elif strict_solve == 2:
        right_T_e = T_crit
    num = 0
    plot = False
    if plot:
        plt.figure(figsize=(9,6))
        Ls = []
        Rs = []
        Ts = np.arange(left_T_e, right_T_e, 0.01 * (e / k_b))
        for i in range(len(Ts)):
            Ls.append(count_left_fTe(Ts[i], n_cl2, n_cl, n_ar))
            Rs.append(count_right_fTe(Ts[i], n_vector, mini_param_vector))
        plt.plot(np.array(Ts)*(k_b/e),Ls,label="левая часть уравнения баланса ионов")
        plt.semilogy(np.array(Ts)*(k_b/e),Rs,label="правая часть уравнения баланса ионов")
        plt.xlabel("$T_e ,эВ$", size=15)
        plt.legend()
        plt.grid()

    while np.abs(delta) > 10.0 ** (-10):
        num += 1
        curr_T_e = (left_T_e + right_T_e) / 2.0
        left_part = count_left_fTe(curr_T_e, n_cl2, n_cl, n_ar)
        right_part = count_right_fTe(curr_T_e, n_vector, mini_param_vector)
        delta = (right_part - left_part) / np.abs(right_part + left_part)
        if delta > 0:
            left_T_e = curr_T_e
        else:
            right_T_e = curr_T_e
    if plot and None:
        plt.axvline(x=curr_T_e, color="g")
        plt.axvline(x=T_crit, color="k")
    if plot:
        plt.show()
    curr_T_e = curr_T_e*(1.0+0.0*(2*np.random.random()-1))
    if do_print:
        print("Num iters (count T_e): ", num)
        print("T_e(eV): ", round(curr_T_e * (k_b / e), 3))
    #print("k_s")
    k_s = count_ks(curr_T_e, n_vector, param_vector, do_print=False)

    return k_s, curr_T_e
