from res.getero.algorithm.monte_carlo import generate_particles
import numpy as np
import matplotlib.pyplot as plt

A = generate_particles(100000, 1000, 0.5, 0.1, 0.3, 1/23.6, 40, 0)
print(A.shape)

plt.hist(A[:,4],bins=200)
#plt.hist(np.random.random(100000), bins=200)
plt.show()
#print("-------------------")
#print(np.random.choice(4,10,p=[0.1,0.3,0.2,0.4]))
