import numpy as np



A = np.array([0,1,2,3,0])

print(np.where(A>0,A+3,0))
