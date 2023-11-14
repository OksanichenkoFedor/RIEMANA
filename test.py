VecStart_x = [0,1,3,5]
VecStart_y = [2,2,5,5]
VecStart_z = [0,1,1,5]
VecEnd_x = [1,2,-1,6]
VecEnd_y = [3,1,-2,7]
VecEnd_z  =[1,0,4,9]

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.plot(VecStart_x + VecEnd_x, VecStart_y + VecEnd_y, VecStart_z +VecEnd_z)
plt.show()
