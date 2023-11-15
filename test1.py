import numpy as np
a = np.array([1,2,3])
b = np.array([4,5,6])
c = np.array([7,8,9])
print(np.concatenate((a.reshape((3,1)),b.reshape((3,1)),c.reshape((3,1))),axis=1).T)
#print(a[4])