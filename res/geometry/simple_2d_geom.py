import numpy as np

import matplotlib.pyplot as plt

from res.geometry.geometry2d import Reactor
from res.geometry.proc_functions import give_points_field2d

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111)
reactor = Reactor()
gl_min,gl_max = reactor.draw(ax)

coords = give_points_field2d(gl_min, gl_max, 100)
ans = reactor.is_points_inside(coords)

for i in range(len(ans)):
    if ans[i]:
        ax.plot(coords[0, i], coords[1, i], ".",color="g")
    else:
        ax.plot(coords[0, i], coords[1, i], ".",color="r")

ax.grid()


plt.show()

