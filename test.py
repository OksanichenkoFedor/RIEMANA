
from res.plasma.reactions_consts.Ar import give_Ar_mom_trans

import numpy as np
import matplotlib.pyplot as plt
k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)
T = np.arange(0,8,0.1)*(e / k_b)
#print(A)
Ks = []
for i in range(len(T)):
    Ks.append(give_Ar_mom_trans(T[i]))

plt.plot(T/(e / k_b),Ks,".")
plt.grid()
plt.show()






