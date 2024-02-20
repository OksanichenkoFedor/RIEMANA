import numpy as np

from res.plasma.utils import good_form
from res.plasma.consts import *
from res.plasma.reaction_consts import give_k_1, give_k_2, give_k_3, give_k_4, give_k_5, give_k_13, give_k_getero

def solve_subsistem(k_4, k_5, k_ii, k_9, k_13, n_plus, A, do_print=False):
    b = (2 * k_4 + k_5) * k_ii * n_plus * n_plus - 2 * k_9 * (A * (k_5+k_13) + k_ii * n_plus)
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

def count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3, k_ii, k_10, k_11, k_12, k_13, do_print=False):
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


def count_T_i(P,T_gas, do_print=False):
    T_i = T_gas + ((e/k_b)*0.5-T_gas)/(P*(10.0/1.333))
    if do_print:
        print("T_i: ",good_form(T_i))
    return T_i

def count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False):
    sigma_cl2 = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl2) / (T_i * k_b))
    sigma_cl = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_cl) / (T_i * k_b))
    sigma_ar = 0.0001 * np.pi * e_sgs * np.sqrt((2.0 * (10.0 ** 6.0) * pol_ar) / (T_i * k_b))
    lambda_cl_plus = (sigma_cl*n_cl + sigma_ar*n_ar + sigma_cl2*n_cl2)**(-1.0)
    lambda_cl2_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_ar_plus = (sigma_cl * n_cl + sigma_ar * n_ar + sigma_cl2 * n_cl2) ** (-1.0)
    lambda_mean = (lambda_cl_plus*n_cl_plus + lambda_ar_plus*n_ar_plus + lambda_cl2_plus*n_cl2_plus)/(n_plus)
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
    beta = n_cl_minus/n_e
    gamma_T = T_e/T_i
    beta_s = beta
    delta = 1
    while delta>10.0**(-4):
        beta_s_new = beta*np.exp(((1-gamma_T)*(1+beta_s))/(2*(1+beta_s*gamma_T)))
        delta = np.abs(beta_s_new-beta_s)/(beta_s_new+beta_s)
        beta_s = beta_s_new
    if do_print:
        print("beta: ", round(beta, 5))
        print("gamma_T: ", round(gamma_T, 5))
        print("beta_s: ", round(beta_s, 5))
    return beta, gamma_T, beta_s

def count_v(T_e, beta_s, m_eff, gamma_T, do_print=False):
    v = np.sqrt((T_e*k_b*(1+beta_s))/(m_eff*(1+beta_s*gamma_T)))
    if do_print:
        print("v: ",good_form(v))
    return v

def count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False):
    D_i = lambda_mean*np.sqrt((T_i*k_b)/(2*m_eff))*((1+gamma_T+beta_s*gamma_T)/(1+beta_s*gamma_T))
    if do_print:
        print("D_i: ", good_form(D_i))
    return D_i

def count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False):
    h_L = ((gamma_T + 2 * gamma_T * beta_s) / (gamma_T * (1 + beta_s))) * 0.86 * (
                (3 + L / (2 * lambda_mean) + ((0.86 * L * v) / (np.pi * gamma_T * D_i)) ** 2) ** (-0.5))
    h_R = ((gamma_T + 3 * gamma_T * beta_s) / (gamma_T * (1 + beta_s))) * 0.80 * (
                (4 + R / (1 * lambda_mean) + ((0.80 * R * v) / (2.405 * 0.43 * gamma_T * D_i)) ** 2) ** (-0.5))
    d_c = (0.5*R*L)/(R*h_L+L*h_R)
    if do_print:
        print("h_L: ", round(h_L, 4))
        print("h_R: ", round(h_R, 4))
        print("d_c: ", good_form(d_c))
    return d_c

def count_T_e(beta, beta_s, gamma_T, d_c, m_eff, n_cl2, n_cl, n_ar, n_e, k_ii, k_1, k_2, k_3, k_5, k_13, do_print=False):
    v_new = (d_c/(2+2*beta))*(2*(k_2*n_cl2+k_3*n_cl+k_1*n_ar)+(k_13-k_5)*n_cl2-beta*(1+beta)*n_e*k_ii)
    T_e = (m_eff*v_new*v_new*(1+beta_s*gamma_T))/((1+beta_s)*k_b)
    if do_print:
        print(v_new)
        print("v_new: ", good_form(v_new))
        print("T_e(eV): ", round(T_e * (k_b / e),3))
    return T_e

def count_ks(T_e,d_c, m_cl, m_cl2, m_ar, beta_s, gamma_T, gamma_cl, do_print=False):
    k_1 = give_k_1(T_e)
    k_2 = give_k_2(T_e)
    k_3 = give_k_3(T_e)
    k_4 = give_k_4(T_e)
    k_5 = give_k_5(T_e)
    k_13 = give_k_13(T_e)
    k_9 = give_k_getero(T_e, m_cl, beta_s, gamma_T, d_c, gamma=gamma_cl)
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
        print("k_13: ", good_form(k_13))
    return k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12






