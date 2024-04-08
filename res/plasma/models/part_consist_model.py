import numpy as np

from res.plasma.consts import e, k_b, m_cl
from res.plasma.start_params import W

from res.plasma.utils.utils import good_form

from res.plasma.start_params import p_0, T_gas, R, L, gamma_cl, y_ar, j
from res.plasma.algorithm.for_testing.electron_temperature import count_T_e
from res.plasma.algorithm.for_testing.chemical_kinetic import count_simple_start, count_n_plus_straight, solve_subsistem, count_ions



T_e = 1 * (e / k_b)


n_plus_old = None
n_cl_old = None
delta = 1
delta_T_e = 1
num = 0
Deltas = []
Deltas_cl = []
Deltas_T_e = []

V = np.pi*R*R*L
param_vector = (p_0, T_gas, R, L, gamma_cl, y_ar, W, V)

k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B = count_simple_start(T_e, param_vector, do_print=False)

while (np.abs(delta_T_e) >= 0) and (num <= 15):
    print("Iteration: ", num)
    print()
    if num==0:
        params = m_cl
        n_plus = count_n_plus_straight(j, T_e, params, is_m_eff=True, do_print=False)
    else:
        params = (n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
        n_plus = count_n_plus_straight(j, T_e, params, is_m_eff=False, do_print=True)
    num += 1
    if n_plus_old is None:
        pass
    else:
        delta = (n_plus_old - n_plus) / (n_plus_old + n_plus)
        Deltas.append(np.abs(delta))
    n_plus_old = n_plus

    n_e, n_cl2, n_cl, n_cl_minus = solve_subsistem(k_4, k_5, k_9, k_13, n_plus, A, do_print=True)
    n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, alphas = count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2, k_3,
                                                                k_10, k_11, k_12, k_13, do_print=True)



    n_vector = (n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus)

    k_inp = (k_1, k_2, k_3, k_5, k_13)

    k_s, T_e_new = count_T_e(n_vector, param_vector, do_print=True)

    k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12 = k_s


    if n_cl_old is None:
        pass
    else:
        delta1 = (n_cl_old - n_cl) / (n_cl_old + n_cl)
        Deltas_cl.append(np.abs(delta1))
        delta_T_e = (T_e - T_e_new) / (T_e + T_e_new)
        Deltas_T_e.append(np.abs(delta_T_e))
    n_cl_old = n_cl
    T_e = T_e_new


print("------")
print("n_e = ", good_form(n_e))
print("n_plus =", good_form(n_plus))
print("n_cl_minus =", good_form(n_cl_minus))
print("n_ar_plus =", good_form(n_ar_plus))

import matplotlib.pyplot as plt

plt.semilogy(Deltas_cl, "o", label="n_cl")
plt.semilogy(Deltas, ".", label="n_plus")
plt.semilogy(Deltas_T_e, ".", label="T_e")
# plt.plot(Deltas_cl, "o",label="n_cl")
# plt.plot(Deltas, ".",label="n_plus")
plt.grid()
plt.legend()
plt.show()
