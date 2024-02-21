import numpy as np

from res.plasma.utils import good_form
from res.plasma.consts import *
from res.plasma.reaction_consts import give_k_1, give_k_2, give_k_3, give_k_4, give_k_5, give_k_13, give_k_getero, k_ii


def count_simple_start(start_T_e, param_vector, do_print=False):
    p_0, T_gas, R, L, gamma_cl, y_ar = param_vector

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
        #print("k_3 (Hsu): ", good_form(give0_k_3(start_T_e)))
        print("k_4: ", good_form(k_4))
        print("k_5: ", good_form(k_5))
        print("k_ii: ", good_form(k_ii))
        print("k_9: ", good_form(k_9))
        print("k_10: ", good_form(k_10))
        print("k_11: ", good_form(k_11))
        print("k_12: ", good_form(k_12))
        print("k_13: ", good_form(k_13))
        print("v_t: ", good_form(V_T))
        print("A: ",good_form(A))
        print("b: ",good_form(B))

    return k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B

def count_n_plus(j, T_e, params ,is_m_eff=False, do_print=False):
    if is_m_eff:
        m_eff = params
    else:
        n_plus, n_cl2_plus, n_cl_plus, n_ar_plus = params
        m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)
    n_plus = (j / (0.61 * e)) * np.sqrt(m_eff / (k_b * T_e))
    if do_print:
        print("n_plus: ", good_form(n_plus))
    return n_plus

def solve_subsistem(k_4, k_5, k_9, k_13, n_plus, A, do_print=False):
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

def count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3, k_10, k_11, k_12, k_13, do_print=False):
    n_cl_plus = ((k_3 * n_cl + k_13 * n_cl2) * n_e) / (k_ii * n_cl_minus + k_10)
    n_cl2_plus = (k_2 * n_cl2 * n_e) / (k_ii * n_cl_minus + k_11)
    n_ar_plus = (B * k_1 * n_e) / (k_ii * n_cl_minus + k_1 * n_e + k_12)
    alpha = n_plus / (n_cl_plus + n_cl2_plus + n_ar_plus)

    n_cl_plus = alpha * n_cl_plus
    n_cl2_plus = alpha * n_cl2_plus
    n_ar_plus = alpha * n_ar_plus
    n_ar = B# - n_ar_plus

    alpha_cl_plus = n_cl_plus / n_plus
    alpha_cl2_plus = n_cl2_plus / n_plus
    alpha_ar_plus = n_ar_plus / n_plus
    print("alpha: ", round(alpha, 10))
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

def count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False):
    m_eff = ((n_cl2_plus / m_cl2 + n_cl_plus / m_cl + n_ar_plus / m_ar) / (n_plus)) ** (-1)
    if do_print:
        print("m_eff: ", m_eff * (1.673 * 10.0 ** (-27)) ** (-1))
    return m_eff

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
    num = 0
    while delta>10.0**(-5):
        num+=1
        beta_s_new = beta*np.exp(((1-gamma_T)*(1+beta_s))/(2*(1+beta_s*gamma_T)))
        delta = np.abs(beta_s_new-beta_s)/(beta_s_new+beta_s)
        beta_s = beta_s_new
    if do_print:
        print("beta: ", round(beta, 5))
        print("gamma_T: ", round(gamma_T, 5))
        print("beta_s: ", round(beta_s, 5))
        print("Num iterations: ",num)
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

def count_ks(T_e, n_vector, param_vector, do_print=False):

    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)

    T_i = count_T_i(p_0, T_gas, do_print=False)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    v = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False)
    V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

    k_1 = give_k_1(T_e)
    k_2 = give_k_2(T_e)
    k_3 = give_k_3(T_e)
    k_4 = give_k_4(T_e)
    k_5 = give_k_5(T_e)
    k_13 = give_k_13(T_e)
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
        print("k_13: ", good_form(k_13))
    return (k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12)

def count_left(T_e, n_cl2, n_cl, n_ar):
    k_1 = give_k_1(T_e)
    k_2 = give_k_2(T_e)
    k_3 = give_k_3(T_e)
    return 2*(k_2*n_cl2 + k_3*n_cl + k_1*n_ar)

def count_right(T_e, n_vector, mini_param_vector):
    p_0, T_gas, R, L, m_eff = mini_param_vector
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    k_5 = give_k_5(T_e)
    k_13 = give_k_5(T_e)
    T_i = count_T_i(p_0, T_gas, do_print=False)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    v = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v, D_i, do_print=False)
    return (k_5 - k_13)*n_cl2 + ((2*v)/(d_c) + k_ii*beta*n_e)*(1+beta)

def count_T_e(n_vector, param_vector, do_print=False):
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector

    p_0, T_gas, R, L, gamma_cl, _ = param_vector

    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)

    mini_param_vector = (p_0, T_gas, R, L, m_eff)

    delta = 1
    print("@@@")
    left_T_e = 0.5*(e/k_b)
    right_T_e = 5*(e/k_b)
    num = 0
    while np.abs(delta)>10.0**(-6):
        num+=1
        curr_T_e = (left_T_e+right_T_e)/2.0
        left_part = count_left(curr_T_e, n_cl2, n_cl, n_ar)
        right_part = count_right(curr_T_e, n_vector, mini_param_vector)
        delta = (right_part-left_part)/(right_part+left_part)
        if delta>0:
            left_T_e = curr_T_e
        else:
            right_T_e = curr_T_e

    if do_print:
        print("Num iters (count T_e): ", num)
        print("T_e(eV): ",round(curr_T_e*(k_b/e),3))


    k_s = count_ks(curr_T_e, n_vector, param_vector, do_print=True)

    return k_s, curr_T_e










