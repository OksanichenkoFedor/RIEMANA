import numpy as np
from numba import jit

from res.plasma.algorithm.with_aclr.beta_s import count_beta_s

from res.plasma.reactions.consts import m_cl, m_cl2, m_ar, e, k_b, e_sgs, pol_ar, pol_cl2, pol_cl


@jit(nopython=True)
def count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus):
    m_eff = ((n_cl2_plus / m_cl2 + n_cl_plus / m_cl + n_ar_plus / m_ar) / (n_plus)) ** (-1)
    return m_eff


@jit(nopython=True)
def count_T_i(P, T_gas):
    if P * (10.0 / 1.333) < 1:
        return (e / k_b) * 0.5
    T_i = T_gas + ((e / k_b) * 0.5 - T_gas) / (P * (10.0 / 1.333))
    return T_i


@jit(nopython=True)
def count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i):
    sigma_cl2 = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl2) / (T_i * k_b))
    sigma_cl = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl) / (T_i * k_b))
    sigma_ar = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_ar) / (T_i * k_b))
    lambda_cl_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_cl2_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_ar_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_mean = (lambda_cl_plus * n_cl_plus + lambda_ar_plus * n_ar_plus + lambda_cl2_plus * n_cl2_plus) / (n_plus)
    return lambda_mean


@jit(nopython=True)
def count_v(T_e, beta_s, m_eff, gamma_T):
    v = np.sqrt((T_e * k_b * (1 + beta_s)) / (m_eff * (1 + beta_s * gamma_T)))
    return v


@jit(nopython=True)
def count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s):
    D_i = lambda_mean * np.sqrt((T_i * k_b) / (2 * m_eff)) * ((1 + gamma_T + beta_s * gamma_T) / (1 + beta_s * gamma_T))
    return D_i


@jit(nopython=True)
def count_tau_eff(T_e, n_vector, param_vector):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    p_0, T_gas, R, L, gamma_cl, y_ar, W, V = param_vector
    T_i = count_T_i(p_0, T_gas)
    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i)
    v = count_v(T_e, beta_s, m_eff, gamma_T)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i)

    v_cl2_plus = count_v(T_e, beta_s, m_cl2, gamma_T)
    v_cl_plus = count_v(T_e, beta_s, m_cl, gamma_T)
    v_ar_plus = count_v(T_e, beta_s, m_ar, gamma_T)
    tau_eff = (v_cl2_plus * n_cl2_plus + v_cl_plus * n_cl_plus + v_ar_plus * n_ar_plus) / d_c
    return tau_eff


@jit(nopython=True)
def count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i):
    h_L, h_R = count_h_LR(beta_s, gamma_T, R, L, lambda_mean, v, D_i)
    d_c = (0.5 * R * L) / (R * h_L + L * h_R)
    return d_c


@jit(nopython=True)
def count_h_LR(beta_s, gamma_T, R, L, lambda_mean, v, D_i):
    h_L = ((gamma_T + 2 * beta_s * 1) / (gamma_T * (1 + beta_s))) * 0.86 * (
            (3 + L / (2 * lambda_mean) + ((0.86 * L * v) / (np.pi * gamma_T * D_i)) ** 2) ** (-0.5))
    h_R = ((gamma_T + 3 * beta_s * 1) / (gamma_T * (1 + beta_s))) * 0.80 * (
            (4 + R / (1 * lambda_mean) + ((0.80 * R * v) / (2.405 * 0.43 * gamma_T * D_i)) ** 2) ** (-0.5))
    return h_L, h_R


@jit(nopython=True)
def count_j(n_vector, param_vector, T_e):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    p_0, T_gas, R, L, gamma_cl, y_ar, W, V = param_vector
    T_i = count_T_i(p_0, T_gas)
    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i)
    v = count_v(T_e, beta_s, m_eff, gamma_T)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s)
    h_L, _ = count_h_LR(beta_s, gamma_T, R, L, lambda_mean, v, D_i)

    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i)
    j_cl_plus = h_L * n_cl_plus * count_v(T_e, beta_s, m_cl, gamma_T)
    j_cl2_plus = h_L * n_cl2_plus * count_v(T_e, beta_s, m_cl2, gamma_T)
    j_ar_plus = h_L * n_ar_plus * count_v(T_e, beta_s, m_ar, gamma_T)
    j_cl = 0.25 * n_cl * np.sqrt((2 * k_b * T_i) / m_cl)

    return j_cl, j_ar_plus, j_cl_plus, j_cl2_plus
