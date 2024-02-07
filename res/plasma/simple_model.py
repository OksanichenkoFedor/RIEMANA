import numpy as np

p_0 = 1.333
T_0 = 300
T_gas = 600
j = 10
k_ii = 5.0 * 10.0**(-14)
y_ar = 0
T_e = 34582
gamma_cl = 0.8 # вот это надо найти

R = 0.25 # это параметры пхт реактора от НИИТМ
L = 0.325 # это параметры пхт реактора от НИИТМ

m_cl = 35.5*1.673*10.0**(-27)
m_cl2 = 71*1.673*10.0**(-27)
m_ar = 40*1.673*10.0**(-27)

k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)

A = (p_0/(k_b*T_gas))*(1-y_ar)
V_T = np.sqrt(2*k_b*T_gas/m_cl)



def count_el_reaction_const(curr_A,curr_B,curr_C):
    return curr_A*(T_e**curr_B)*np.exp((-1*curr_C)/(T_e))



