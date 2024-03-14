import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from res.plasma.consts import e, k_b

from res.plasma.algorithm.for_testing.utils import count_T_i
from res.plasma.algorithm.for_testing.part_solver import solve_part
from res.plasma.algorithm.for_testing.beta_s import pure_count_beta_s


p_0 = 10*0.13333
T_gas = 600
R = 0.15
L=0.14
gamma_cl=0.2
y_ar=0.8
W=600
V = np.pi * R * R * L

param_vector = (p_0, T_gas, R, L, gamma_cl, y_ar, W, V)

n_es = np.arange(1,20,0.5)*(10.0**(16))
T_es = []
Betas = []
Betas_s = []
for i in trange(len(n_es)):
    #print("dfdfdfdfdf")
    n_e_curr = n_es[i]
    #n_e_curr = 2.3299999999999996*(10**(16))
    T_ec, n_vector, A = solve_part(n_e_curr, param_vector)
    #print(len(A))
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e1, n_cl_minus = n_vector
    curr_beta = n_cl_minus/n_e1
    T_i = count_T_i(p_0, T_gas)
    curr_gamma = T_ec/T_i
    #print("dds")
    curr_beta_s, _ = pure_count_beta_s(curr_beta,curr_gamma)
    #print("dds1")
    Betas.append(curr_beta)
    Betas_s.append(curr_beta_s)
    T_es.append(T_ec)
T_es = np.array(T_es)
fig, ([[ax11, ax12],[ax21,ax22]]) = plt.subplots(2, 2, figsize=(15,7))
ax11.plot(n_es/(10.0**16),T_es*(k_b/e),".")
ax11.set_title("T_e от n_e")
ax11.grid()

ax12.plot(n_es/(10.0**16),Betas,".")
ax12.set_title("beta от n_e")
ax12.grid()

ax21.plot(n_es/(10.0**16),Betas_s,".")
ax21.set_title("beta_s от n_e")
ax21.grid()

plt.show()