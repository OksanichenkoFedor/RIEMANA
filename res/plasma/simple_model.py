import numpy as np
import time
from reaction_consts import *

p_0 = 1.333*1
T_0 = 300
T_gas = 600
j = 10
k_ii = 5.0 * 10.0 ** (-14)
y_ar = 0.0
T_e = 3*(e/k_b)
gamma_cl = 0.6  # вот это надо найти

R = 0.25  # это параметры пхт реактора от НИИТМ
L = 0.325  # это параметры пхт реактора от НИИТМ

m_cl = 35.5 * 1.673 * 10.0 ** (-27)
m_cl2 = 71 * 1.673 * 10.0 ** (-27)
m_ar = 40 * 1.673 * 10.0 ** (-27)

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

A = (p_0 / (k_b * T_gas)) * (1 - y_ar)
B = (p_0 / (k_b * T_gas)) * y_ar
V_T = np.sqrt(2 * k_b * T_gas / m_cl)

k_9 = ((R + L) / (2 * R * L)) * V_T * gamma_cl


def count_el_reaction_const(curr_A, curr_B, curr_C):
    return curr_A * (T_e ** curr_B) * np.exp((-1 * curr_C) / (T_e))


k_1 = count_el_reaction_const(A_Ar, B_Ar, C_Ar)  # Ar + e -> Ar(+) + 2e
k_2 = count_el_reaction_const(A_Cl2, B_Cl2, C_Cl2)  # Cl2 + e -> Cl2(+) + 2e
k_3 = count_el_reaction_const(A_Cl, B_Cl, C_Cl)  # Cl + e -> Cl(+) + 2e
k_4 = count_el_reaction_const(A_Cl2_dis, B_Cl2_dis, C_Cl2_dis)  # Cl2 + e -> Cl + Cl + 2e
k_5 = count_el_reaction_const(A_Cl2_min, B_Cl2_min, C_Cl2_min)  # Cl2 + e -> Cl + Cl(-)


m_eff = m_cl
n_plus_old = None
delta = 1
num = 0
Deltas = []
while (np.abs(delta) > 10**(-20)) and (num<=100):
    num+=1
    n_plus = (j/(0.61*e))*np.sqrt(m_eff/(k_b*T_e))
    if n_plus_old is None:
        pass
    else:
        delta = (n_plus_old-n_plus)/(n_plus_old+n_plus)
        #print(delta)
        Deltas.append(delta)
    n_plus_old = n_plus
    #print("n_plus: ",n_plus)
    b = (2*k_4+k_5)*k_ii*n_plus*n_plus - 2*k_9*(A*k_5+k_ii*n_plus)
    ac = 2*k_9*(k_ii**2)*(n_plus**3)*(2*k_4+k_5)
    n_e = (b+np.sqrt(b*b+4*ac))/(2*(2*k_4+k_5)*k_ii*n_plus)
    #print("n_e: ",n_e)
    n_cl2 = (2*A*k_9)/(2*k_9+2*(2*k_4+k_5))

    n_cl = 2*A - 2*n_cl2

    n_cl_minus = n_plus - n_e

    n_cl_plus = (k_3*n_cl*n_e)/(k_ii*n_cl_minus)

    n_cl2_plus = (k_2*n_cl2*n_e)/(k_ii*n_cl_minus)

    n_ar = (B*k_ii*n_cl_minus)/(k_ii*n_cl_minus+k_1*n_e)

    n_ar_plus = (B*k_1*n_e)/(k_ii*n_cl_minus+k_1*n_e)

    m_eff = ((n_cl2_plus/m_cl2 + n_cl_plus/m_cl + n_ar_plus/m_ar)/(n_plus))**(-1)


import matplotlib.pyplot as plt

plt.semilogy(Deltas,".")
plt.grid()
plt.show()
print("n_e =",round(n_e/(10**14),3),"* 10^14 м^(-3)")
print("n_plus =",round(n_plus/(10**15),3),"* 10^15 м^(-3)")
print("n_cl_minus =",round(n_cl_minus/(10**15),3),"* 10^15 м^(-3)")


