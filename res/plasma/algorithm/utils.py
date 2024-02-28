import numpy as np

from res.plasma.consts import m_cl, m_cl2, m_ar, e, k_b, e_sgs, pol_ar, pol_cl2, pol_cl

from res.plasma.utils import good_form


def count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False):
    m_eff = ((n_cl2_plus / m_cl2 + n_cl_plus / m_cl + n_ar_plus / m_ar) / (n_plus)) ** (-1)
    if do_print:
        print("m_eff: ", m_eff * (1.673 * 10.0 ** (-27)) ** (-1))
    return m_eff


def count_T_i(P, T_gas, do_print=False):
    T_i = T_gas + ((e / k_b) * 0.5 - T_gas) / (P * (10.0 / 1.333))
    if do_print:
        print("T_i: ", good_form(T_i))
    return T_i


def count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False):
    sigma_cl2 = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl2) / (T_i * k_b))
    sigma_cl = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl) / (T_i * k_b))
    sigma_ar = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_ar) / (T_i * k_b))
    lambda_cl_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_cl2_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_ar_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_mean = (lambda_cl_plus * n_cl_plus + lambda_ar_plus * n_ar_plus + lambda_cl2_plus * n_cl2_plus) / (n_plus)
    if do_print:
        print("sigma_cl2: ", good_form(sigma_cl2))
        print("sigma_cl: ", good_form(sigma_cl))
        print("sigma_ar: ", good_form(sigma_ar))
        print("lambda_cl_plus: ", good_form(lambda_cl_plus))
        print("lambda_cl2_plus: ", good_form(lambda_cl2_plus))
        print("lambda_ar_plus: ", good_form(lambda_ar_plus))
        print("lambda_mean: ", good_form(lambda_mean))
    return lambda_mean


def count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False):
    beta = n_cl_minus / n_e
    gamma_T = T_e / T_i
    beta_s = beta
    delta = 1
    num = 0
    while delta > 10.0 ** (-5):
        num += 1
        beta_s_new = beta * np.exp(((1 - gamma_T) * (1 + beta_s)) / (2 * (1 + beta_s * gamma_T)))
        delta = np.abs(beta_s_new - beta_s) / (beta_s_new + beta_s)
        beta_s = beta_s_new
    if do_print:
        print("beta: ", round(beta, 5))
        print("gamma_T: ", round(gamma_T, 5))
        print("beta_s: ", round(beta_s, 5))
        print("Num iterations: ", num)
    return beta, gamma_T, beta_s


def count_v(T_e, beta_s, m_eff, gamma_T, do_print=False):
    v = np.sqrt((T_e * k_b * (1 + beta_s)) / (m_eff * (1 + beta_s * gamma_T)))
    if do_print:
        print("v: ", good_form(v))
    return v


def count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False):
    D_i = lambda_mean * np.sqrt((T_i * k_b) / (2 * m_eff)) * ((1 + gamma_T + beta_s * gamma_T) / (1 + beta_s * gamma_T))
    if do_print:
        print("D_i: ", good_form(D_i))
    return D_i


def count_tau_eff(T_e, n_vector, param_vector, do_print=False):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    p_0, T_gas, R, L, gamma_cl, y_ar, W, V = param_vector
    T_i = count_T_i(p_0, T_gas, do_print=False)
    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    v = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False)

    v_cl2_plus = count_v(T_e, beta_s, m_cl2, gamma_T, do_print=False)
    v_cl_plus = count_v(T_e, beta_s, m_cl, gamma_T, do_print=False)
    v_ar_plus = count_v(T_e, beta_s, m_ar, gamma_T, do_print=False)
    tau_eff = (v_cl2_plus * n_cl2_plus + v_cl_plus * n_cl_plus + v_ar_plus * n_ar_plus) / d_c
    if do_print:
        print("tau_eff: ", good_form(tau_eff))
        print("v_cl2_plus: ", good_form(v_cl2_plus))
        print("v_cl_plus: ", good_form(v_cl_plus))
        print("v_ar_plus: ", good_form(v_ar_plus))
    return tau_eff


def count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False):
    h_L = ((gamma_T + 2 * gamma_T * beta_s) / (gamma_T * (1 + beta_s))) * 0.86 * (
            (3 + L / (2 * lambda_mean) + ((0.86 * L * v) / (np.pi * gamma_T * D_i)) ** 2) ** (-0.5))
    h_R = ((gamma_T + 3 * gamma_T * beta_s) / (gamma_T * (1 + beta_s))) * 0.80 * (
            (4 + R / (1 * lambda_mean) + ((0.80 * R * v) / (2.405 * 0.43 * gamma_T * D_i)) ** 2) ** (-0.5))
    d_c = (0.5 * R * L) / (R * h_L + L * h_R)
    if do_print:
        print("h_L: ", round(h_L, 4))
        print("h_R: ", round(h_R, 4))
        print("d_c: ", good_form(d_c))
    return d_c
