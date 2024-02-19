import numpy as np
import time
from res.plasma.reaction_consts import *

p_0 = 1.333 * 1
T_0 = 300
T_gas = 600
j = 19.6
k_ii = 5.0 * 10.0 ** (-14)
y_ar = 0.0
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
    return curr_A * ((T_e/(e/k_b)) ** curr_B) * np.exp((-1 * curr_C) / (T_e))


k_1 = count_el_reaction_const(A_Ar, B_Ar, C_Ar)  # Ar + e -> Ar(+) + 2e
k_2 = count_el_reaction_const(A_Cl2, B_Cl2, C_Cl2)  # Cl2 + e -> Cl2(+) + 2e
k_3 = give_k_3(T_e)  # Cl + e -> Cl(+) + 2e
k_4 = count_el_reaction_const(A_Cl2_dis, B_Cl2_dis, C_Cl2_dis)  # Cl2 + e -> Cl + Cl + 2e
k_5 = give_k_5(T_e)  # Cl2 + e -> Cl + Cl(-)


def good_form(num):
    if num == 0.0:
        return "0.0"
    elif str(num) == "inf":
        return "inf"
    # print(num)
    integ = int(np.log(num) / np.log(10))
    ost = num / (10.0 ** (integ))
    return str(round(ost, 5)) + "*10^" + str(integ)


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
print("v_t: ", good_form(V_T))

m_eff = m_cl
n_plus_old = None
delta = 1
num = 0
Deltas = []
while (np.abs(delta) > 10 ** (-20)) and (num <= 100):
    print("Iteration: ", num)
    print()
    num += 1
    n_plus = (j / (0.61 * e)) * np.sqrt(m_eff / (k_b * T_e))
    if n_plus_old is None:
        pass
    else:
        delta = (n_plus_old - n_plus) / (n_plus_old + n_plus)
        print(delta)
        Deltas.append(np.abs(delta))
    n_plus_old = n_plus
    print("n_plus: ", good_form(n_plus))
    b = (2 * k_4 + k_5) * k_ii * n_plus * n_plus - 2 * k_9 * (A * k_5 + k_ii * n_plus)
    ac = 2 * k_9 * (k_ii ** 2) * (n_plus ** 3) * (2 * k_4 + k_5)
    n_e = (b + np.sqrt(b * b + 4 * ac)) / (2 * (2 * k_4 + k_5) * k_ii * n_plus)
    print("n_e: ", good_form(n_e))
    n_cl2 = (2 * A * k_9) / (2 * k_9 + (2 * k_4 + k_5) * n_e)
    print("n_cl2: ", good_form(n_cl2))
    n_cl = 2 * A - 2 * n_cl2
    print("n_cl: ", good_form(n_cl))
    n_cl_minus = n_plus - n_e
    print("n_cl_minus: ", good_form(n_cl_minus))
    n_cl_plus = (k_3 * n_cl * n_e) / (k_ii * n_cl_minus + k_10)

    n_cl2_plus = (k_2 * n_cl2 * n_e) / (k_ii * n_cl_minus + k_11)

    n_ar_plus = (B * k_1 * n_e) / (k_ii * n_cl_minus + k_1 * n_e + k_12)
    alpha = n_plus / (n_cl_plus + n_cl2_plus + n_ar_plus)
    print("alpha: ", round(alpha, 10))
    n_cl_plus = alpha * n_cl_plus
    print("n_cl_plus: ", good_form(n_cl_plus))
    n_cl2_plus = alpha * n_cl2_plus
    print("n_cl2_plus: ", good_form(n_cl2_plus))
    n_ar_plus = alpha * n_ar_plus
    print("n_ar_plus: ", good_form(n_ar_plus))
    n_ar = B - n_ar_plus
    print("n_ar: ", good_form(n_ar))
    alpha_cl_plus = n_cl_plus/n_plus
    print("alpha_cl_plus: ", round(alpha_cl_plus,3))
    alpha_cl2_plus = n_cl2_plus / n_plus
    print("alpha_cl2_plus: ", round(alpha_cl2_plus, 3))
    alpha_ar_plus = n_ar_plus / n_plus
    print("alpha_ar_plus: ", round(alpha_ar_plus, 3))

    m_eff = ((n_cl2_plus / m_cl2 + n_cl_plus / m_cl + n_ar_plus / m_ar) / (n_plus)) ** (-1)
    print("m_eff: ", m_eff * (1.673 * 10.0 ** (-27)) ** (-1))

print("------")
print("n_e = ", good_form(n_e))
print("n_plus =", good_form(n_plus))
print("n_cl_minus =", good_form(n_cl_minus))

import matplotlib.pyplot as plt

plt.semilogy(Deltas, ".")
plt.grid()
plt.show()
