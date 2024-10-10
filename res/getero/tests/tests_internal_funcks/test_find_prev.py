from res.getero.algorithm.ray_tracing.cell_by_cell.space_orientation import give_next_cell, find_next
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np





def generate_point(axis):
    start_x = 0
    start_y = 0

    is_on_horiz = np.random.randint(0, 2)
    if is_on_horiz:
        add_x = np.random.random()
        add_y = np.random.randint(0, 2)
        if add_y == 0:
            angle = np.random.random() * np.pi * 2
            while angle > 0.5*np.pi and angle < 1.5*np.pi:
                angle = np.random.random() * np.pi * 2
        elif add_y == 1:
            angle = np.random.random() * np.pi * 2
            while angle < 0.5 * np.pi or angle > 1.5 * np.pi:
                angle = np.random.random() * np.pi * 2
    else:
        add_y = np.random.random()
        add_x = np.random.randint(0, 2)
        if add_x == 0:
            angle = np.random.random() * np.pi * 2
            while angle > np.pi:
                angle = np.random.random() * np.pi * 2
        elif add_x == 1:
            angle = np.random.random() * np.pi * 2
            while angle < np.pi:
                angle = np.random.random() * np.pi * 2

    x = start_x + add_x
    y = start_y + add_y
    #print("---")
    #print(x, y, is_on_horiz)
    new_x, new_y, new_is_on_horiz = give_next_cell(x, y, angle, is_on_horiz)
    #print(angle/np.pi)
    #print(new_x, new_y)
    next_att_x, next_att_y = find_next(new_x, new_y, x, y, start_x, start_y, False)

    rect = Rectangle((start_x, start_y), 1, 1, alpha=0.5, color="b")
    axis.add_patch(rect)
    rect = Rectangle((next_att_x, next_att_y), 1, 1, alpha=0.5, color="r")
    axis.add_patch(rect)
    axis.plot(x, y, "o", color="b")
    axis.plot(new_x, new_y, ".", color="r")
    axis.arrow(x, y, 0.5 * np.sin(angle), 0.5 * np.cos(angle), color="g", linewidth=1)


y_size = 3
x_size = 3
fig, axes = plt.subplots(y_size, x_size, figsize=(4 * x_size, 4 * y_size))

for i in range(x_size):
    for j in range(y_size):
        x_major_ticks = np.arange(-3, 3, 1)
        y_major_ticks = np.arange(-3, 3, 1)
        axes[i, j].set_xticks(x_major_ticks)
        axes[i, j].set_yticks(y_major_ticks)
        axes[i, j].set_aspect(1)
        axes[i, j].grid(which='major', alpha=0.8)
        axes[i, j].set(xlim=[-3, 3], ylim=[3, -3])
        generate_point(axes[i, j])
plt.show()

print((2.0 - int(2.0)) == 0)
