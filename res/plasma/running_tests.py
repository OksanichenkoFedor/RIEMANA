import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


from res.plasma.start_params import T_gas, R, L, gamma_cl, W
from res.plasma.old_models.consist_model import run_consist_model
from res.plasma.consts import e, k_b





N_e_s = []
T_e_s = []
N_e = []
T_e = []

y_ar = np.arange(0,1,0.02)
Ps = np.arange(0.8,2.0,0.02)*0.13333

for i in trange(len(y_ar)):
    curr_y_ar = y_ar[i]
    curr_p = 18*0.13333#Ps[i]
    print("---")
    #print(Ps[i])
    res1 = run_consist_model(curr_p, T_gas, R, L, gamma_cl, curr_y_ar, W, simple=True)
    N_e_s.append(res1["n_e"])
    T_e_s.append(res1["T_e"])
    res = run_consist_model(curr_p, T_gas, R, L, gamma_cl, curr_y_ar, W, simple=False)
    N_e.append(res["n_e"])
    T_e.append(res["T_e"])


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(y_ar, N_e, ".", label="n_e")
ax1.plot(y_ar, N_e_s, ".", label="n_e_s")
ax1.set_xlabel("p,mtorr")
ax1.set_ylabel("n_e,$m^3 c^{-1}$")
ax1.grid()
ax1.legend()

ax2.plot(y_ar, np.array(T_e)/(e/k_b), ".", label="T_e")
ax2.plot(y_ar, np.array(T_e_s)/(e/k_b), ".", label="T_e_s")
ax2.set_xlabel("доля аргона")
ax2.set_ylabel("T_e,eV")
ax2.grid()
ax2.legend()
plt.show()