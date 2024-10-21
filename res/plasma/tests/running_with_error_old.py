import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import time

from res.plasma.models.consist_model_aclr import run_consist_model
from res.plasma.reactions.consts import e, k_b
from res.plasma.reactions.const_functions import give_consts

y_ar = np.arange(0.0, 0.95, 0.01)

N_rep = 100

N_e = np.zeros((N_rep, y_ar.shape[0]))
N_cl = np.zeros((N_rep, y_ar.shape[0]))
N_cl_plus = np.zeros((N_rep, y_ar.shape[0]))
N_cl_minus = np.zeros((N_rep, y_ar.shape[0]))
N_cl2 = np.zeros((N_rep, y_ar.shape[0]))
N_cl2_plus = np.zeros((N_rep, y_ar.shape[0]))
N_ar = np.zeros((N_rep, y_ar.shape[0]))
N_ar_plus = np.zeros((N_rep, y_ar.shape[0]))
Beta = np.zeros((N_rep, y_ar.shape[0]))
T_e = np.zeros((N_rep, y_ar.shape[0]))
J_cl = np.zeros((N_rep, y_ar.shape[0]))
J_ar_plus = np.zeros((N_rep, y_ar.shape[0]))
J_cl_plus = np.zeros((N_rep, y_ar.shape[0]))
J_cl2_plus = np.zeros((N_rep, y_ar.shape[0]))
Times = np.zeros((N_rep, y_ar.shape[0]))
plot_arrays = {
    "W_el_Ar": np.zeros((N_rep, y_ar.shape[0])),
    "W_el_Cl2": np.zeros((N_rep, y_ar.shape[0])),
    "W_el_Cl": np.zeros((N_rep, y_ar.shape[0])),
    "W_inel_Ar": np.zeros((N_rep, y_ar.shape[0])),
    "W_inel_Cl2": np.zeros((N_rep, y_ar.shape[0])),
    "W_inel_Cl": np.zeros((N_rep, y_ar.shape[0])),
}
consts = give_consts("../../data/plasma_cl2_ar_data.csv", do_rand=False)
run = run_consist_model(p_0=10 * 0.13333, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.5, W=600, consts=consts)
def print_j(cres,y_ar):
    print("---")
    print("J_cl(y_ar=" + str(y_ar) + "): ", cres["j_cl"])
    print("J_ar_plus(y_ar=" + str(y_ar) + "): ", cres["j_ar_plus"])
    print("J_cl_plus(y_ar=" + str(y_ar) + "): ", cres["j_cl_plus"])
    print("J_cl2_plus(y_ar=" + str(y_ar) + "): ", cres["j_cl2_plus"])

res = run_consist_model(p_0=10 * 0.13333, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.5, W=600, consts=consts)
print_j(res,0.5)
res = run_consist_model(p_0=10 * 0.13333, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.1, W=600, consts=consts)
print_j(res,0.1)
res = run_consist_model(p_0=10 * 0.13333, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.9, W=600, consts=consts)
print_j(res,0.9)
for i in trange(N_rep):
    consts = give_consts("../../data/plasma_cl2_ar_data.csv", do_rand=True)
    for j in range(len(y_ar)):
        curr_y_ar = y_ar[j]
        # print("dfdf: ",curr_y_ar)
        curr_p = 10 * 0.13333  # Ps[i]
        # print(Ps[i])
        start = time.time()
        res = run_consist_model(p_0=curr_p, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=curr_y_ar, W=600,
                                consts=consts)
        end = time.time()
        Times[i, j] = end - start
        N_e[i, j] = res["n_e"]
        N_cl[i, j] = res["n_cl"]
        N_cl_plus[i, j] = res["n_cl_plus"]
        N_cl_minus[i, j] = res["n_cl_minus"]
        N_cl2[i, j] = res["n_cl2"]
        N_cl2_plus[i, j] = res["n_cl2_plus"]
        N_ar[i, j] = res["n_ar"]
        N_ar_plus[i, j] = res["n_ar_plus"]
        T_e[i, j] = res["T_e"]
        Beta[i, j] = res["n_cl_minus"] / res["n_e"]
        J_cl[i, j] = res["j_cl"]
        J_ar_plus[i, j] = res["j_ar_plus"]
        J_cl_plus[i, j] = res["j_cl_plus"]
        J_cl2_plus[i, j] = res["j_cl2_plus"]
        for key in plot_arrays.keys():
            plot_arrays[key][i, j] = res[key]


def plot_dov_int(axis, x, y, label, color="b"):
    mean = y.mean(axis=0)
    std = y.std(axis=0)
    axis.plot(x, mean, label=label, color=color)
    axis.fill_between(x, (mean - std), (mean + std), color=color, alpha=0.1)


print("Avg time (ms): ", round(1000 * Times.mean(), 2), "+-", round(1000 * Times.std(), 2))

fig, ([ax11, ax12], [ax21, ax22]) = plt.subplots(2, 2, figsize=(13, 11))

# fig.suptitle("en_loss first")

plot_dov_int(ax11, y_ar, N_e / (10.0 ** 17), "N_e", "b")
ax11.set_xlabel("доля аргона", size=10)
ax11.set_ylabel("$n_e, 10^{17} m^{-3}$", size=15)
ax11.set_title("Концентрация электронов")
ax11.grid()

plot_dov_int(ax12, y_ar, T_e / (e / k_b), "T_e", "b")
ax12.set_xlabel("доля аргона", size=10)
ax12.set_ylabel("T_e,eV", size=15)
ax12.set_title("Температура электронов")
ax12.grid()

plot_dov_int(ax21, y_ar, N_cl / (10.0 ** 20), "N_Cl", "b")
ax21.set_xlabel("доля аргона", size=10)
ax21.set_ylabel("$n_{Cl}, 10^{20} m^{-3}$", size=15)
ax21.set_title("Концентрация молекул $Cl$")
ax21.grid()

plot_dov_int(ax22, y_ar, J_cl2_plus, "J_Cl2_plus", "r")
plot_dov_int(ax22, y_ar, J_cl_plus, "J_Cl_plus", "g")
plot_dov_int(ax22, y_ar, J_ar_plus, "J_Ar_plus", "b")
plot_dov_int(ax22, y_ar, J_cl, "J_Cl", "k")
ax22.set_xlabel("доля аргона", size=10)
ax22.set_ylabel("$j, m^{-2}/s$", size=15)
ax22.set_title("Концентрация ионов")
ax22.legend()
ax22.grid()

plt.show()

fig, (ax11, ax22) = plt.subplots(1, 2, figsize=(18, 5))

plot_dov_int(ax22, y_ar, np.array(plot_arrays["W_el_Ar"]) * np.array(N_e), "Ar", "b")
plot_dov_int(ax22, y_ar, np.array(plot_arrays["W_el_Cl2"]) * np.array(N_e), "Cl2", (1,0.647,0))
plot_dov_int(ax22, y_ar, np.array(plot_arrays["W_el_Cl"]) * np.array(N_e), "Cl", "g")
ax22.set_title("(b)", y=-0.15, loc='left', size=20)
ax22.set_xlabel("доля аргона", size=10)
ax22.set_ylabel("W,Вт", size=15)
ax22.grid()
ax22.legend()

plot_dov_int(ax11, y_ar, np.array(plot_arrays["W_inel_Ar"]) * np.array(N_e), "Ar", "b")
plot_dov_int(ax11, y_ar, np.array(plot_arrays["W_inel_Cl2"]) * np.array(N_e), "Cl2", (1,0.647,0))
plot_dov_int(ax11, y_ar, np.array(plot_arrays["W_inel_Cl"]) * np.array(N_e), "Cl", "g")
ax11.set_xlabel("доля аргона", size=10)
ax11.set_ylabel("W,Вт", size=15)
ax11.set_title("(a)", y=-0.15, loc='left', size=20)
ax11.grid()
ax11.legend()

plt.show()