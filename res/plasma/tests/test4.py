import numpy as np
import matplotlib.pyplot as plt
from res.plasma.reactions_consts.Cl import count_Cl_inel_power, give_k_Cl_mom

def count_min(gamma_T):
    b = 6*gamma_T - 1 - gamma_T**2
    beta_s = (-b+np.sqrt(b**2 - 16*gamma_T))/(4*gamma_T**2)
    beta = beta_s*np.exp(((1+beta_s)*(gamma_T-1))/(2*(1+beta_s*gamma_T)))
    return beta

G = np.arange(10,50,0.1)
B = []
for i in range(len(G)):
    B.append(count_min(G[i]))

#plt.plot(G,B)
#plt.grid()
#plt.show()

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

T = np.arange(1,4,0.1)*(e/k_b)
Ks = []
for i in range(len(T)):
    Ks.append(count_Cl_inel_power(T[i]))

    #Ks.append(give_k_Cl_mom(T[i]))
plt.plot(T,Ks,'.')
plt.grid()
plt.show()