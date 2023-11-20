import numpy as np
a = np.array([[1,2,3],[1,2,3]])
b = np.array([[4,5,6],[4,5,6]])
print(a.shape)
c= np.array([1,2,3])
d= np.array([4,5,6])
print(np.cross(a.T,b.T,axis=0).shape)
print(np.cross(c,d))