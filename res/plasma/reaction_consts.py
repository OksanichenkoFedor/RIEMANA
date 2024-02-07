#HSU Cl2 plasma model (http://iopscience.iop.org/0022-3727/39/15/009)

# k = A*(T_e**B)*np.exp((-1*C)/(T_e))



k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)

# Ar + e -> Ar(+) + 2e
A_Ar = 1.235*10.0**(-13)
B_Ar = 0
C_Ar = 18.69*(e/k_b)

# Cl2 + e -> Cl2(+) + 2e
A_Cl2 = 9.21*10.0**(-14)
B_Cl2 = 0
C_Cl2 = 12.9*(e/k_b)

# Cl + e -> Cl(+) + 2e
A_Cl = 1.0/(3.6*10.0**(6.0))
B_Cl = 0.5
C_Cl = 12.6*(e/k_b)

# Cl2 + e -> Cl + Cl + 2e
A_Cl2_dis = 3.8*10.0**(-14)
B_Cl2_dis = 0
C_Cl2_dis = 3.824*(e/k_b)

# Cl2 + e -> Cl + Cl(-)
A_Cl2_min = 8.55*10.0**(-16)
B_Cl2_min = 0
C_Cl2_min = 12.65*(e/k_b)