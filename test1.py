import numpy as np
import matplotlib.pyplot as plt
from res.geometry.proc_functions import give_points_field2d
from res.geometry.count_functions import pnt2line
coords, delta_x, delta_y = give_points_field2d(np.array([[0.75],[0.75]]),
                             np.array([[2.25],[2.25]]),30,rand=0)
N = 4
a = np.arange(0,3,0.05)
b = np.arange(0,3,0.05)
x1,x2 = 1.1,2
y2,y1 = 1,2
A = np.array([False, True, False, True])
B = np.array([False, False, True, True])
print((A*B))

#ans = f(coords[0],coords[1])
#for i in range(len(ans)):
#    if ans[i]:
#        plt.plot(coords[0, i], coords[1, i], ".",color="g")
#    else:
#        plt.plot(coords[0, i], coords[1, i], ".", color="r")
#plt.plot([x1,x2],[y1,y2])
#plt.show()
