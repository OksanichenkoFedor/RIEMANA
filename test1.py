import numpy as np
import matplotlib.pyplot as plt
from res.plasma.reactions_consts.k_from_cr_sec import give_reaction_const
from res.plasma.reactions_consts.Ar import give_Ar_mom_trans
from res.plasma.consts import m_e, e, k_b

give_Ar_mom1 = give_reaction_const("res/plasma/reactions_consts/Ar_mom1.txt",up=200)
give_Ar_mom2 = give_reaction_const("res/plasma/reactions_consts/Ar_mom2.txt",up=200)
give_Cl_mom = give_reaction_const("res/plasma/reactions_consts/Cl_mom.txt",up=200)

engs = np.arange(0.1, 10, 0.02)
K1 = []
K2 = []
K3 = []
K4 = []

for i in range(len(engs)):
    K1.append(give_Ar_mom1(engs[i]*(e / k_b)))
    K2.append(give_Ar_mom2(engs[i]*(e / k_b)))
    K3.append(give_Cl_mom(engs[i]*(e / k_b)) )
    K4.append(give_Ar_mom_trans(engs[i]*(e / k_b)))
plt.plot(engs,K1,label="Ar1")
plt.plot(engs,K2,label="Ar2")
plt.plot(engs,K3,label="Cl")
#plt.plot(engs,K4,label="Ar_b")
plt.xlabel("Энергия,эВ")
plt.ylabel("k,$m^3$/c")
plt.legend()
plt.grid()
plt.show()

