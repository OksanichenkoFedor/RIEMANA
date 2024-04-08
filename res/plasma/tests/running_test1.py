import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from res.plasma.models.consist_model_mult_laps import run_consist_model
from res.plasma.reactions.consts import e, k_b





N_e = []
N_cl = []
T_e = []
plot_arrays = {
    "W_el_Ar": [],
    "W_el_Cl2": [],
    "W_el_Cl": [],
    "W_inel_Ar": [],
    "W_inel_Cl2": [],
    "W_inel_Cl": [],
}

y_ar = np.arange(0.0,1.0,0.01)
Ps = np.arange(0.8,2.0,0.02)*0.13333

for i in trange(len(y_ar)):
    curr_y_ar = y_ar[i]
    print("dfdf: ",curr_y_ar)
    curr_p = 10*0.13333#Ps[i]
    print("---")
    #print(Ps[i])
    res = run_consist_model(p_0 = curr_p, T_gas = 600, R=0.15, L=0.14, gamma_cl=0.2, y_ar=curr_y_ar, W=600)
    N_e.append(res["n_e"])
    N_cl.append(res["n_cl"])
    T_e.append(res["T_e"])
    for key in plot_arrays.keys():
        plot_arrays[key].append(res[key])


fig, ([ax11, ax12], [ax21, ax22]) = plt.subplots(2, 2, figsize=(12, 8))

fig.suptitle("T_e first")

ax11.plot(y_ar, N_cl, ".", label="n_cl")
#ax1.plot(y_ar, N_cl_s, ".", label="n_cl_s")
ax11.set_xlabel("доля аргона")
ax11.set_ylabel("n_cl,$m^3 c^{-1}$")
ax11.grid()
ax11.legend()

ax21.plot(y_ar, np.array(T_e)/(e/k_b), ".", label="T_e")
#ax2.plot(y_ar, np.array(T_e_s)/(e/k_b), ".", label="T_e_s")
ax21.set_xlabel("доля аргона")
ax21.set_ylabel("T_e,eV")
ax21.grid()
ax21.legend()


ax12.plot(y_ar, plot_arrays["W_el_Ar"], ".", label="Ar")
ax12.plot(y_ar, plot_arrays["W_el_Cl2"], ".", label="Cl2")
ax12.plot(y_ar, plot_arrays["W_el_Cl"], ".", label="Cl")
ax12.set_title("Потеря энергии на эластичные соударения")
ax12.set_xlabel("доля аргона")
ax12.set_ylabel("W,Вт")
ax12.grid()
ax12.legend()

ax22.plot(y_ar, plot_arrays["W_inel_Ar"], ".", label="Ar")
ax22.plot(y_ar, plot_arrays["W_inel_Cl2"], ".", label="Cl2")
ax22.plot(y_ar, plot_arrays["W_inel_Cl"], ".", label="Cl")
ax22.set_title("Потеря энергии на неупругие соударения")
ax22.set_xlabel("доля аргона")
ax22.set_ylabel("W,Вт")
ax22.grid()
ax22.legend()

plt.show()