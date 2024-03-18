import numpy as np
import matplotlib.pyplot as plt
contur = np.array([[0,1,1,0],[1,1,0,0]]).T
print(contur.shape)
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(len(contur)):
    ax.plot([contur[i,0],contur[(i+1)%len(contur),0]],
             [contur[i,1],contur[(i+1)%len(contur),1]],color="k")
ax.grid()
ax.set_xlim([-1,2])
ax.set_ylim([-1,2])
plt.show()