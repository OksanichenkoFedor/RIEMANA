import numpy as np
import time
from res.plasma.reaction_consts import *
from res.plasma.algo_parts import solve_subsistem, count_ions, count_T_i, count_lambda, count_beta_s, count_v
from res.plasma.algo_parts import count_D_i, count_d_c, count_T_e, count_ks
from res.plasma.utils import good_form

p_0 = 1.333 * 1
T_0 = 300
T_gas = 600
j = 19.6
k_ii = 5.0 * 10.0 ** (-14)
y_ar = 0.0
# T_e = 2.16 * (e / k_b)
T_e = 2.16 * (e / k_b)
gamma_cl = 0.05  # вот это надо найти

R = 0.25  # это параметры пхт реактора от НИИТМ
L = 0.325  # это параметры пхт реактора от НИИТМ

m_cl = 35.5 * 1.673 * 10.0 ** (-27)
m_cl2 = 71 * 1.673 * 10.0 ** (-27)
m_ar = 40 * 1.673 * 10.0 ** (-27)

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

A = (p_0 / (k_b * T_gas)) * (1 - y_ar)
B = (p_0 / (k_b * T_gas)) * y_ar
V_T = np.sqrt(8.0 * k_b * T_gas / (np.pi * m_cl))

k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl

k_10 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * T_e) / m_cl)
k_11 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * T_e) / m_cl2)
k_12 = ((R + L) / (2 * R * L)) * np.sqrt((k_b * T_e) / m_ar)


def count_el_reaction_const(curr_A, curr_B, curr_C):
    return curr_A * ((T_e / (e / k_b)) ** curr_B) * np.exp((-1 * curr_C) / (T_e))


k_1 = give_k_1(T_e)  # Ar + e -> Ar(+) + 2e
k_2 = give_k_2(T_e)  # Cl2 + e -> Cl2(+) + 2e
k_3 = give_k_3(T_e)  # Cl + e -> Cl(+) + 2e
k_4 = give_k_4(T_e)  # Cl2 + e -> Cl + Cl + 2e
k_5 = give_k_5(T_e)  # Cl2 + e -> Cl + Cl(-)
k_13 = give_k_13(T_e)  # Cl2 + e -> Cl(+) + Cl(-) + e

print("k_1: ", good_form(k_1))
print("k_2: ", good_form(k_2))
print("k_3 (Efremov): ", good_form(give_k_3(T_e)))
print("k_3 (Hsu): ", good_form(give0_k_3(T_e)))
print("k_4: ", good_form(k_4))
print("k_5: ", good_form(k_5))
print("k_ii: ", good_form(k_ii))
print("k_9: ", good_form(k_9))
print("k_10: ", good_form(k_10))
print("k_11: ", good_form(k_11))
print("k_12: ", good_form(k_12))
print("k_13: ", good_form(k_13))
print("v_t: ", good_form(V_T))

m_eff = m_cl
n_plus_old = None
n_cl_old = None
delta = 1
delta_T_e = 1
num = 0
Deltas = []
Deltas_cl = []
Deltas_T_e = []
while (np.abs(delta_T_e) >= 0) and (num <= 100):
    print("Iteration: ", num)
    print()
    num += 1
    n_plus = (j / (0.61 * e)) * np.sqrt(m_eff / (k_b * T_e))
    if n_plus_old is None:
        pass
    else:
        delta = (n_plus_old - n_plus) / (n_plus_old + n_plus)
        Deltas.append(np.abs(delta))
    n_plus_old = n_plus

    print("n_plus: ", good_form(n_plus))

    n_e, n_cl2, n_cl, n_cl_minus = solve_subsistem(k_4, k_5, k_ii, k_9, k_13, n_plus, A, do_print=False)
    n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, alphas = count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3,
                                                                k_ii, k_10, k_11, k_12, k_13, do_print=False)
    alpha_cl_plus, alpha_cl2_plus, alpha_ar_plus = alphas
    m_eff = ((n_cl2_plus / m_cl2 + n_cl_plus / m_cl + n_ar_plus / m_ar) / (n_plus)) ** (-1)
    print("m_eff: ", m_eff * (1.673 * 10.0 ** (-27)) ** (-1))

    T_i = count_T_i(p_0, T_gas, do_print=False)
    lambda_mean = count_lambda(n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, T_i, do_print=False)
    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e, T_i, do_print=False)
    v_old = count_v(T_e, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v_old, D_i, do_print=False)

    T_e_new = count_T_e(beta, beta_s, gamma_T, d_c, m_eff, n_cl2, n_cl, n_ar, n_e, k_ii, k_1, k_2, k_3, k_5,
                        k_13, do_print=True)

    beta, gamma_T, beta_s = count_beta_s(n_e, n_cl_minus, T_e_new, T_i, do_print=False)
    v_new = count_v(T_e_new, beta_s, m_eff, gamma_T, do_print=False)
    D_i = count_D_i(lambda_mean, m_eff, T_i, gamma_T, beta_s, do_print=False)
    d_c = count_d_c(beta_s, gamma_T, R, L, lambda_mean, v_new, D_i, do_print=False)






    if n_cl_old is None:
        pass
    else:
        delta1 = (n_cl_old - n_cl) / (n_cl_old + n_cl)
        Deltas_cl.append(np.abs(delta1))
        delta_T_e = (T_e - T_e_new) / (T_e + T_e_new)
        Deltas_T_e.append(np.abs(delta_T_e))
    n_cl_old = n_cl
    if np.abs(delta)<10.0**(-7):
        print("dfdfdfdfdfdfdfefdfdfdfdfdfdfdfdfdfdf")
        k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12 = count_ks(T_e, d_c, m_cl, m_cl2, m_ar, beta_s, gamma_T,
                                                                    gamma_cl, do_print=False)
        T_e = T_e_new

print("------")
print("n_e = ", good_form(n_e))
print("n_plus =", good_form(n_plus))
print("n_cl_minus =", good_form(n_cl_minus))

import matplotlib.pyplot as plt

print(len(Deltas), len(Deltas_cl))
plt.semilogy(Deltas_cl, "o", label="n_cl")
plt.semilogy(Deltas, ".", label="n_plus")
plt.semilogy(Deltas_T_e, ".", label="T_e")
# plt.plot(Deltas_cl, "o",label="n_cl")
# plt.plot(Deltas, ".",label="n_plus")
plt.grid()
plt.legend()
plt.show()
