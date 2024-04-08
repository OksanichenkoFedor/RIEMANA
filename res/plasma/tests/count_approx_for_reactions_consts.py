import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from res.plasma.consts import k_b, e

from res.plasma.reactions_consts.Ar import give_k_Ar_mom
from res.plasma.reactions_consts.Cl import give_k_Cl_mom
from res.plasma.reactions_consts.Cl2 import give_k_Cl2_mom

from res.plasma.utils.utils import generate_approximation




Ens = np.arange(0.3,10,0.1)*(e/k_b)

Ar_mom = []
Cl_mom = []
Cl2_mom = []
for i in trange(len(Ens)):
    Ar_mom.append(give_k_Ar_mom(Ens[i]))
    Cl_mom.append(give_k_Cl_mom(Ens[i]))
    Cl2_mom.append(give_k_Cl2_mom(Ens[i]))

Ar_mom = np.array(Ar_mom)
Cl_mom = np.array(Cl_mom)
Cl2_mom = np.array(Cl2_mom)

print("Ar:")
w_Ar, f_Ar = generate_approximation(Ens*(k_b/e), Ar_mom, do_print=True)
print("---")
print("Cl:")
w_Cl, f_Cl = generate_approximation(Ens*(k_b/e), Cl_mom, do_print=True)

plt.plot(Ens*(k_b/e), Ar_mom, ".", label="Ar", color = (1,0,0))
plt.plot(Ens*(k_b/e), f_Ar(Ens*(k_b/e)), color = (0.7,0,0.3), label="approx Ar")

plt.plot(Ens*(k_b/e), Cl_mom, ".", label="Cl", color = (0,0,1))
plt.plot(Ens*(k_b/e), f_Cl(Ens*(k_b/e)), color = (0.3,0,0.7), label="approx Cl")


plt.xlabel("$T_e,eV$")
plt.grid()
plt.legend()
plt.show()






