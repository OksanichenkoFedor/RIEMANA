import numpy as np
from numba import jit

from res.plasma.reactions.consts import e, k_b, m_ar, m_cl2, m_cl
from res.plasma.reactions.common_reactions import give_k_getero, k_ii
from res.plasma.reactions.reactions_conts import give_k
from res.plasma.algorithm.with_aclr.chemical_kinetic import count_m_eff, count_ks_chem
from res.plasma.algorithm.with_aclr.beta_s import count_beta_s

from res.plasma.algorithm.with_aclr.utils import count_T_i, count_lambda, count_v, count_d_c, count_D_i


@jit(nopython=True)
def count_ks(T_e, n_vector, param_vector, chem_data, chem_connector):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _, _, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)

    T_i = count_T_i(p_0, T_gas)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i)
    v = count_v(T_e, beta_s, m_eff, gamma_T)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i)
    V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

    k_1, k_2, k_3, k_4, k_5, k_13 = count_ks_chem(T_e, chem_data, chem_connector)

    k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl
    k_10 = give_k_getero(T_e, m_cl, beta_s, gamma_T, d_c)
    k_11 = give_k_getero(T_e, m_cl2, beta_s, gamma_T, d_c)
    k_12 = give_k_getero(T_e, m_ar, beta_s, gamma_T, d_c)

    return (k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12)


@jit(nopython=True)
def count_left_fTe(T_e, n_cl2, n_cl, n_ar, param_123):
    k_1 = give_k(param_123[0], T_e)
    k_2 = give_k(param_123[1], T_e)
    k_3 = give_k(param_123[2], T_e)
    return 2 * (k_2 * n_cl2 + k_3 * n_cl + k_1 * n_ar)


@jit(nopython=True)
def count_right_fTe(T_e, n_vector, mini_param_vector, param_513):
    p_0, T_gas, R, L, m_eff = mini_param_vector
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    k_5 = give_k(param_513[0],T_e)
    k_13 = give_k(param_513[1],T_e)
    T_i = count_T_i(p_0, T_gas)

    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i)
    v_cl_plus = count_v(T_e, beta_s, m_cl, gamma_T)
    v_cl2_plus = count_v(T_e, beta_s, m_cl2, gamma_T)
    v_ar_plus = count_v(T_e, beta_s, m_ar, gamma_T)
    v = (n_cl_plus * v_cl_plus + n_cl2_plus * v_cl2_plus + n_ar_plus * v_ar_plus) / n_plus
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i)
    return (k_5 - k_13) * n_cl2 + ((2 * v) / (d_c) + k_ii * beta * n_e) * (1 + beta)


@jit(nopython=True)
def count_T_e(n_vector, param_vector, chem_data, chem_connector):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _, _, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
    mini_param_vector = (p_0, T_gas, R, L, m_eff)
    delta = 1
    left_T_e = 0.5 * (e / k_b)
    right_T_e = 5 * (e / k_b)
    num = 0
    vec1_2_3 = np.array([1, 2, 3])
    vec5_13 = np.array([5, 13])

    while np.abs(delta) > 10.0 ** (-10):
        num += 1
        curr_T_e = (left_T_e + right_T_e) / 2.0
        left_part = count_left_fTe(curr_T_e, n_cl2, n_cl, n_ar, chem_data[chem_connector[vec1_2_3]])
        right_part = count_right_fTe(curr_T_e, n_vector, mini_param_vector, chem_data[chem_connector[vec5_13]])
        delta = (right_part - left_part) / np.abs(right_part + left_part)
        if delta > 0:
            left_T_e = curr_T_e
        else:
            right_T_e = curr_T_e
    curr_T_e = curr_T_e * (1.0 + 0.0 * (2 * np.random.random() - 1))
    k_s = count_ks(curr_T_e, n_vector, param_vector, chem_data, chem_connector)

    return k_s, curr_T_e
