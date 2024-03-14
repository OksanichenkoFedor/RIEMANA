import numpy as np
from numba import jit
from res.plasma.utils import good_form
from res.plasma.reactions_consts.k_from_cr_sec import give_reaction_const

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

# Cl + e -> Cl(+) + 2e
A_Cl = 1.0 / (3.6 * 10.0 ** 6.0)
B_Cl = 0.5
C_Cl = 12.96 * (e / k_b)

@jit(nopython=True)
def give0_k_3(T_e):
    T_ev = T_e / (e / k_b)
    x = np.log(T_ev / 12.96)
    return A_Cl * (T_ev ** B_Cl) * np.exp((-1 * C_Cl) / T_e) * (1.419 * (10.0 ** (-7.0)) - 1.864 * (10.0 ** (-8)) * x
                                                                - 5.439 * (10.0 ** (-8)) * x ** 2
                                                                + 3.306 * (10.0 ** (-8)) * x ** 3
                                                                - 3.540 * (10.0 ** (-9)) * x ** 4
                                                                - 2.915 * (10.0 ** (-8)) * x ** 5)

@jit(nopython=True)
def give_k_3(T_e):
    T_ev = T_e / (e / k_b)
    return 3.00 * (10.0 ** (-14)) * (T_ev ** 0.559) * np.exp((-13.21) / T_ev)


# Cl energy-loss reactions

# e + Cl -> Cl[3D] + e
@jit(nopython=True)
def give_k_Cl_3_D(T_e):
    return 1.99 * (10.0 ** (-14)) * np.exp((-10.06*(e/k_b))/T_e)
e_th_Cl_3_D = 11.65*e

# e + Cl -> Cl[4D] + e
@jit(nopython=True)
def give_k_Cl_4_D(T_e):
    return 9.24 * (10.0 ** (-15)) * np.exp((-11.15*(e/k_b))/T_e)
e_th_Cl_4_D = 12.45*e

# e + Cl -> Cl[4P] + e
@jit(nopython=True)
def give_k_Cl_4_P(T_e):
    return 1.6 * (10.0 ** (-14)) * np.exp((-10.29*(e/k_b))/T_e)
e_th_Cl_4_P = 10.85*e

# e + Cl -> Cl[4S] + e
@jit(nopython=True)
def give_k_Cl_4_S(T_e):
    return 1.27 * (10.0 ** (-14)) * np.exp((-10.97*(e/k_b))/T_e)
e_th_Cl_4_S = 9.55*e

# e + Cl -> Cl[5D] + e
@jit(nopython=True)
def give_k_Cl_5_D(T_e):
    return 5.22 * (10.0 ** (-15)) * np.exp((-11.12*(e/k_b))/T_e)
e_th_Cl_5_D = 12.75*e

# e + Cl -> Cl[5P] + e
@jit(nopython=True)
def give_k_Cl_5_P(T_e):
    return 2.79 * (10.0 ** (-15)) * np.exp((-11.06*(e/k_b))/T_e)
e_th_Cl_5_P = 12.15*e

@jit(nopython=True)
def count_Cl_inel_power(T_e):
    Cl_inel_power = give_k_Cl_3_D(T_e)*e_th_Cl_3_D + give_k_Cl_4_D(T_e)*e_th_Cl_4_D + \
                    give_k_Cl_4_P(T_e)*e_th_Cl_4_P + give_k_Cl_4_S(T_e)*e_th_Cl_4_S + \
                    give_k_Cl_5_D(T_e)*e_th_Cl_5_D + give_k_Cl_5_P(T_e)*e_th_Cl_5_P
    return Cl_inel_power

# momentum transfer
@jit(nopython=True)
def give_k_Cl_mom(T_e):
    T_ev = T_e / (e / k_b)
    return 0.28694 * (10 ** (-13)) * (T_ev ** 0.92478) * np.exp(
        (-0.6563) / T_ev + 1.24428 / (T_ev ** 2) - 0.55659 / (T_ev ** 3) + 0.0778167 / (T_ev ** 4))
