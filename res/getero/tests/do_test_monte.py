from res.getero.algorithm.monte_carlo import generate_particles
import numpy as np

A = generate_particles(10, 10, 0.5, 0.0, 0.5, 1/23.6)
#print(A)
#print("-------------------")
print(np.random.choice(4,10,p=[0.1,0.3,0.2,0.4]))
