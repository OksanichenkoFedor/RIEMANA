import numpy as np

#HSU Cl2 plasma model (http://iopscience.iop.org/0022-3727/39/15/009)

# k = A*(T_e**B)*np.exp((-1*C)/(T_e))



k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)

k_ii = 5.0 * 10.0 ** (-14)

# Ar + e -> Ar(+) + 2e
A_Ar = 1.235*10.0**(-13)
B_Ar = 0
C_Ar = 18.69*(e/k_b)
def give_k_1(T_e):
    return A_Ar * ((T_e/(e/k_b)) ** B_Ar) * np.exp((-1 * C_Ar) / (T_e))
# Cl2 + e -> Cl2(+) + 2e
A_Cl2 = 9.21*10.0**(-14)
B_Cl2 = 0
C_Cl2 = 12.9*(e/k_b)
def give_k_2(T_e):
    return A_Cl2 * ((T_e/(e/k_b)) ** B_Cl2) * np.exp((-1 * C_Cl2) / (T_e))
# Cl + e -> Cl(+) + 2e
A_Cl = 1.0/(3.6*10.0**(6.0))
B_Cl = 0.5
C_Cl = 12.96*(e/k_b)
def give0_k_3(T_e):
    T_ev = T_e/(e/k_b)
    x = np.log(T_ev / 12.96)
    return A_Cl * (T_ev ** B_Cl) * np.exp((-1 * C_Cl) / (T_e)) * (1.419*(10.0**(-7.0)) - 1.864 * (10.0**(-8)) * x
                                                                 - 5.439 * (10.0**(-8)) * x**2
                                                                 + 3.306 * (10.0**(-8)) * x**3
                                                                 - 3.540 * (10.0**(-9)) * x**4
                                                                 - 2.915 * (10.0**(-8)) * x**5)

def give_k_3(T_e):
    T_ev = T_e / (e / k_b)
    return 3.00 * 10.00**(-14)* (T_ev**(0.559)) * np.exp((-13.21)/T_ev)

# Cl2 + e -> Cl + Cl + e
A_Cl2_dis = 3.8*10.0**(-14)
B_Cl2_dis = 0
C_Cl2_dis = 3.824*(e/k_b)
def give_k_4(T_e):
    return A_Cl2_dis * ((T_e/(e/k_b)) ** B_Cl2_dis) * np.exp((-1 * C_Cl2_dis) / (T_e))
# Cl2 + e -> Cl + Cl(-)
A_Cl2_min = 3.69*10.0**(-16)
B_Cl2_min = 0
def give_k_5(T_e):
    T_ev = T_e / (e / k_b)
    return A_Cl2_min * np.exp(-(1.68/T_ev)+1.457/(T_ev**2)-0.44/(T_ev**3)+0.0572/(T_ev**4)-0.0026/(T_ev**5))

# Cl2 + e -> Cl(+) + Cl(-) + e
A_Cl_plus_minus = 8.55*10.0**(-16)
B_Cl_plus_minus = 0
C_Cl_plus_minus = 12.65*(e/k_b)
def give_k_13(T_e):
    T_ev = T_e / (e / k_b)
    return A_Cl_plus_minus * ((T_e/(e/k_b)) ** B_Cl_plus_minus) * np.exp((-1 * C_Cl_plus_minus) / (T_e))


def give_k_getero(T_e, m_i, beta_s, gamma_T, d_c, gamma=1):
    return (np.sqrt((k_b*T_e*(1+beta_s))/(m_i*(1+beta_s*gamma_T)))/d_c)*gamma
