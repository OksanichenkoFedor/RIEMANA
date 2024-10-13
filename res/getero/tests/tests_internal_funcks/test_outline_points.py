import numpy as np
from matplotlib import pyplot as plt

from res.getero.ray_tracing.cell_by_cell.collision_functions import particle_on_wall
from res.getero.ray_tracing.cell_by_cell.space_orientation import give_next_cell
from res.getero.ray_tracing.utils import count_angle
from matplotlib.patches import Rectangle


def fff(x0, y0, x1, y1):
    cX, cY = [], []
    ccx, ccy = [], []
    inc_x, inc_y = np.sign(int(x1)-int(x0)), np.sign(int(y1)-int(y0))
    angle = count_angle(y1-y0, x1-x0)


    cX.append(int(x0))
    cY.append(int(y0))
    ccx.append(x0)
    ccy.append(y0)


    new_vec, curr_att_x, curr_att_y = particle_on_wall(int(x0), int(y0), np.array([x0, y0]), angle)

    curr_x, curr_y = new_vec[0], new_vec[1]
    cX.append(curr_att_x)
    cY.append(curr_att_y)
    ccx.append(curr_x)
    ccy.append(curr_y)
    if int(curr_x) - curr_x == 0:
        is_on_horiz = 0
    else:
        is_on_horiz = 1
    while (int(curr_x)-int(x1)!=0) or (int(curr_y)-int(y1)!=0):
        #print("---")
        curr_x,curr_y, is_on_horiz = give_next_cell(curr_x,curr_y,angle,is_on_horiz)
        ccx.append(curr_x)
        ccy.append(curr_y)
        #print(is_on_horiz)
        if is_on_horiz:
            curr_att_y += inc_y
        else:
            curr_att_x += inc_x
        cX.append(curr_att_x)
        cY.append(curr_att_y)
    return cX, cY, ccx, ccy



def plot_pixels(cX, cY, axis):
    for i in range(len(cX)):
        rect = Rectangle((cX[i], cY[i]), 1, 1, color=(0, 0, 1, 0.3))
        axis.add_patch(rect)


x0, y0 = 119 71 118 70

x0, y0 = np.random.randint(100)+0.5, np.random.randint(100)+0.5

x1, y1 = np.random.randint(100)+0.5, np.random.randint(100)+0.5

X, Y, cx, cy = fff(x0, y0, x1, y1)

fig, ax = plt.subplots()
ax.set_aspect(1)
plot_pixels(X, Y, ax)

ax.plot([x0,x1],[y0,y1], color="r")
ax.plot(cx, cy, ".", color="g")
x_ticks = np.arange(min(X), max(X)+1, 1)
y_ticks = np.arange(min(Y), max(Y)+1, 1)
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)
ax.grid()
ax.set_xlim([min(X), max(X)+1])
ax.set_ylim([max(Y)+1, min(Y)])
plt.show()