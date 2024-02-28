import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


from res.plasma.start_params import T_gas, R, L, gamma_cl, W
from res.plasma.old_models.consist_model import run_consist_model
from res.plasma.consts import e, k_b





N_e = []
T_e = []

#y_ar = np.arange(0,1,0.01)
Ps = np.arange(1.1,2,0.01)*0.13333

for i in trange(len(Ps)):
    curr_y_ar = 0
    curr_p = Ps[i]
    res = run_consist_model(curr_p, T_gas, R, L, gamma_cl, curr_y_ar, W)
    N_e.append(res["n_e"])
    T_e.append(res["T_e"])


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(Ps/0.13333, N_e, ".", label="n_e")
ax1.set_xlabel("p,mtorr")
ax1.set_ylabel("n_e,$m^3 c^{-1}$")
ax1.grid()
ax1.legend()

ax2.plot(Ps/0.13333,np.array(T_e)/(e/k_b), ".", label="T_e")
ax2.set_xlabel("p,mtorr")
ax2.set_ylabel("T_e,eV")
ax2.grid()
ax2.legend()
plt.show()