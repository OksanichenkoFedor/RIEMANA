#HSU Cl2 plasma model (http://iopscience.iop.org/0022-3727/39/15/009)

# k = A*(T_e**B)*np.exp((-1*C)/(T_e))

# Ar + e -> Ar(+) + 2e
A_Ar = 1.235*10.0**(-13)
B_Ar = 0
C_Ar = 18.69
k_Ar = A*(T_e**B_Ar)*np.exp((-1*C_Ar)/(T_e))
# Cl2 + e -> Cl2(+) + 2e
A_Cl2 = 9.21*10.0**(-14)
B_Cl2 = 0
C_Cl2 = 12.9
# Cl + e -> Cl(+) + 2e
A_Cl = 1.0/(3.6*10.0**(6.0))
B_Cl = 0.5
C_Cl = 0
# Cl2 + e -> Cl + Cl + 2e
A_Cl2_dis = 0
B_Cl2_dis = 0
C_Cl2_dis = 0
# Cl2 + e -> Cl + Cl(-)
A_Cl2_min = 0
B_Cl2_min = 0
C_Cl2_min = 0