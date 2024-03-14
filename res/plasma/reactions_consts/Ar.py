import numpy as np
from numba import jit
from res.plasma.utils import good_form
from res.plasma.reactions_consts.k_from_cr_sec import give_reaction_const

k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)



# Ar + e -> Ar(+) + 2e
A_Ar = 1.235*10.0**(-13)
B_Ar = 0
C_Ar = 18.69*(e/k_b)
@jit(nopython=True)
def give_k_1(T_e):
    return A_Ar * ((T_e/(e/k_b)) ** B_Ar) * np.exp((-1 * C_Ar) / (T_e))
e_th_Ar_plus = 15.6*e

# Ar + e -> e + Ar


# Ar energy-loss reactions

# e + Ar -> Ar[4s_{1/2},4s_{3/2}] + e
@jit(nopython=True)
def give_k_Ar_4s_12_32(T_e):
    return 0.371 * (10.0**(-13.0)) * np.exp((-15.06*(e/k_b))/T_e)
e_th_Ar_4s_12_32 = 11.6*e

# e + Ar -> Ar[3d^{ap}_{3/2}] + e
@jit(nopython=True)
def give_k_Ar_3d_ap_32(T_e):
    return 0.06271 * (10.0**(-13.0)) * np.exp((-14.27*(e/k_b))/T_e)
e_th_Ar_3d_ap_32 = 14.3*e

# e + Ar -> Ar[3d_{3/2}] + e
@jit(nopython=True)
def give_k_Ar_3d_32(T_e):
    return 0.03520 * (10.0**(-13.0)) * np.exp((-15.07*(e/k_b))/T_e)
e_th_Ar_3d_32 = 14.15*e

# e + Ar -> Ar[5s_{3/2}] + e
@jit(nopython=True)
def give_k_Ar_5s_32(T_e):
    return 0.009237 * (10.0**(-13.0)) * np.exp((-15.66*(e/k_b))/T_e)
e_th_Ar_5s_32 = 14.1*e

# e + Ar -> Ar[5s^{ap}_{1/2}] + e
@jit(nopython=True)
def give_k_Ar_5s_ap_12(T_e):
    return 0.002501 * (10.0**(-13.0)) * np.exp((-15.92*(e/k_b))/T_e)
e_th_Ar_5s_ap_12 = 14.3*e

@jit(nopython=True)
def count_Ar_inel_power(T_e):
    Ar_inel_power = give_k_1(T_e)*e_th_Ar_plus + give_k_Ar_4s_12_32(T_e)*e_th_Ar_4s_12_32 + \
                    give_k_Ar_3d_ap_32(T_e)*e_th_Ar_3d_ap_32 + give_k_Ar_3d_32(T_e)*e_th_Ar_3d_32 + \
                    give_k_Ar_5s_32(T_e)*e_th_Ar_5s_32 + give_k_Ar_5s_ap_12(T_e)*e_th_Ar_5s_ap_12
    return Ar_inel_power


# momentum transfer
@jit(nopython=True)
def give_k_Ar_mom(T_e):
    T_ev = T_e / (e / k_b)
    return 0.37376 * (10 ** (-12)) * (T_ev ** (-0.027)) * np.exp(
        (-6.817) / T_ev + 4.433 / (T_ev ** 2) - 1.462 / (T_ev ** 3) + 0.174 / (T_ev ** 4))

