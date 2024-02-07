import numpy as np



A = np.array([[0,1],[9,0]])
print(np.repeat(A.reshape(2,2,1),5,axis=2).shape)

