import numpy as np

from res.plasma.utils import good_form
from res.plasma.consts import *

def solve_subsistem(k_4,k_5,k_ii, k_9, n_plus, A, do_print=False):
    b = (2 * k_4 + k_5) * k_ii * n_plus * n_plus - 2 * k_9 * (A * k_5 + k_ii * n_plus)
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

def count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3, k_ii, k_10, k_11, k_12, do_print=False):
    n_cl_plus = (k_3 * n_cl * n_e) / (k_ii * n_cl_minus + k_10)
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


def count_Ti(P,T_gas):
    print(P*(10.0/1.333))
    return T_gas + ((e/k_b)*0.5-T_gas)/(P*(10.0/1.333))

def count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i):
    sigma_cl2 = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl2) / (T_i * k_b))
    sigma_cl = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl) / (T_i * k_b))
    sigma_ar = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_ar) / (T_i * k_b))
    lambda_cl_plus = (sigma_cl*n_cl + sigma_ar*n_ar + sigma_cl2*n_cl2)**(-1.0)
    lambda_cl2_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_ar_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_mean = (lambda_cl_plus*n_cl_plus + lambda_ar_plus*n_ar_plus + lambda_cl2_plus*n_cl2_plus)/(n_plus)
    return lambda_mean

def count_beta_s(n_e, n_cl_minus, T_e, T_i):
    beta = n_cl_minus/n_e
    gamma_T = T_e/T_i
    print("Gamma: ", gamma_T)
    print("Beta: ", beta)
    print("---")
    beta_s = beta
    delta = 1
    while delta>10.0**(-4):
        beta_s_new = beta*np.exp(((1-gamma_T)*(1+beta_s))/(2*(1+beta_s*gamma_T)))
        delta = np.abs(beta_s_new-beta_s)/(beta_s_new+beta_s)
        print(delta)
        beta_s = beta_s_new
    return beta, gamma_T, beta_s

def count_v_old(T_e, beta_s, m_i, gamma_T):
    return np.sqrt()





