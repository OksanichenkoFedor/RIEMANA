import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from res.plasma.algorithm.beta_s import count_min_beta

gammas = np.arange(0,1000,0.1)

B = []

for i in range(len(gammas)):
    B.append(count_min_beta(gammas[i]))

plt.plot(gammas,B)
plt.show()

