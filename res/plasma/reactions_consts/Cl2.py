import numpy as np
from numba import jit
from res.plasma.utils import good_form

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

# Cl2 + e -> Cl2(+) + 2e
A_Cl2 = 9.21 * 10.0 ** (-14)
B_Cl2 = 0
C_Cl2 = 12.9 * (e / k_b)


@jit(nopython=True)
def give_k_2(T_e):
    return A_Cl2 * ((T_e / (e / k_b)) ** B_Cl2) * np.exp((-1 * C_Cl2) / (T_e))


e_th_Cl2_plus = 11.48 * e

# Cl2 + e -> Cl + Cl + e
A_Cl2_dis = 3.8 * 10.0 ** (-14)
B_Cl2_dis = 0
C_Cl2_dis = 3.824 * (e / k_b)


@jit(nopython=True)
def give_k_4(T_e):
    return A_Cl2_dis * ((T_e / (e / k_b)) ** B_Cl2_dis) * np.exp((-1 * C_Cl2_dis) / (T_e))


# её уже учли для потерей энергии

# Cl2 + e -> Cl + Cl(-)
A_Cl2_min = 3.69 * 10.0 ** (-16)
B_Cl2_min = 0


@jit(nopython=True)
def give_k_5(T_e):
    T_ev = T_e / (e / k_b)
    return A_Cl2_min * np.exp(
        -(1.68 / T_ev) + 1.457 / (T_ev ** 2) - 0.44 / (T_ev ** 3) + 0.0572 / (T_ev ** 4) - 0.0026 / (T_ev ** 5))


# она безпороговая


# Cl2 + e -> Cl(+) + Cl(-) + e
A_Cl_plus_minus = 8.55 * 10.0 ** (-16)
B_Cl_plus_minus = 0
C_Cl_plus_minus = 12.65 * (e / k_b)


@jit(nopython=True)
def give_k_13(T_e):
    T_ev = T_e / (e / k_b)
    return A_Cl_plus_minus * ((T_e / (e / k_b)) ** B_Cl_plus_minus) * np.exp((-1 * C_Cl_plus_minus) / (T_e))


e_th_13 = 12.65 * e


# Cl2 energy-loss reactions

# e + Cl2 -> Cl2[b3_PI_u] + e
@jit(nopython=True)
def give_k_Cl2_b3_PI_u(T_e):
    T_ev = T_e / (e / k_b)
    return 6.13 * (10.0 ** (-16)) * np.exp(2.74 / T_ev - 6.85 / (T_ev ** 2) + 3.69 / (T_ev ** 3) +
                                           0.856 / (T_ev ** 4) + 0.0711 / (T_ev ** 5))


e_th_Cl2_b3_PI_u = 3.36 * e


# e + Cl2 -> Cl2[1_PI_u] + e
@jit(nopython=True)
def give_k_Cl2_1_PI_u(T_e):
    return 3.8 * (10.0 ** (-14)) * np.exp((-3.824 * (e / k_b)) / T_e)


e_th_Cl2_1_PI_u = 4.3 * e


# e + Cl2 -> Cl2[1_PI_g] + e
@jit(nopython=True)
def give_k_Cl2_1_PI_g(T_e):
    return 9.74 * (10.0 ** (-15)) * np.exp((-10.71 * (e / k_b)) / T_e)


e_th_Cl2_1_PI_g = 6.4 * e


# e + Cl2 -> Cl2[1_SIGMA_u] + e
@jit(nopython=True)
def give_k_Cl2_1_SIGMA_u(T_e):
    return 2.12 * (10.0 ** (-15)) * np.exp((-11.16 * (e / k_b)) / T_e)


e_th_Cl2_1_SIGMA_u = 7 * e


# e + Cl2 -> Cl2[Ryd] + e
@jit(nopython=True)
def give_k_Cl2_Ryd(T_e):
    return 4.30 * (10.0 ** (-14)) * np.exp((-12.76 * (e / k_b)) / T_e)


e_th_Cl2_Ryd = 9.5 * e


# e + Cl2 -> Cl2[v1] + e
@jit(nopython=True)
def give_k_Cl2_v1(T_e):
    T_ev = T_e * (k_b / e)
    return 4.35 * (10.0 ** (-16)) * (T_ev ** (-1.48)) * np.exp((-0.76) / T_ev)


e_th_Cl2_v1 = 0.07 * e


# e + Cl2 -> Cl2[v2] + e
@jit(nopython=True)
def give_k_Cl2_v2(T_e):
    T_ev = T_e * (k_b / e)
    return 8.1 * (10.0 ** (-17)) * (T_ev ** (-1.48)) * np.exp((-0.68) / T_ev)


e_th_Cl2_v2 = 0.14 * e


# e + Cl2 -> Cl2[v3] + e
@jit(nopython=True)
def give_k_Cl2_v3(T_e):
    T_ev = T_e * (k_b / e)
    return 2.39 * (10.0 ** (-17)) * (T_ev ** (-1.49)) * np.exp((-0.64) / T_ev)


e_th_Cl2_v3 = 0.21 * e


@jit(nopython=True)
def count_Cl2_inel_power(T_e):
    Cl2_inel_power = give_k_Cl2_b3_PI_u(T_e) * e_th_Cl2_b3_PI_u + give_k_Cl2_1_PI_u(T_e) * e_th_Cl2_1_PI_u + \
                     give_k_Cl2_1_PI_g(T_e) * e_th_Cl2_1_PI_g + give_k_Cl2_1_SIGMA_u(T_e) * e_th_Cl2_1_SIGMA_u + \
                     give_k_13(T_e) * e_th_13 + give_k_Cl2_Ryd(T_e) * e_th_Cl2_Ryd + \
                     give_k_Cl2_v1(T_e) * e_th_Cl2_v1 + give_k_Cl2_v2(T_e) * e_th_Cl2_v2 + give_k_Cl2_v3(
        T_e) * e_th_Cl2_v3
    return Cl2_inel_power


# momentum transfer
@jit(nopython=True)
def give_k_Cl2_mom(T_e):
    T_ev = T_e / (e / k_b)
    return 4.47 * (10.0 ** (-13.0)) * np.exp(-2.17 / T_ev + 0.362 / (T_ev ** 2) - 0.0196 / (T_ev ** 3))
