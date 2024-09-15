from res.getero.algorithm.ray_tracing.collision_functions import count_curr_prev_att
from res.getero.algorithm.dynamic_profile import give_coords_from_num
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt

def plot_one(axis):
    print("-------------")
    axis.set_xlim([-1, 4])
    axis.set_ylim([4, -1])
    axis.set_aspect(1)
    x_ticks = np.arange(-1, 4, 1)
    y_ticks = np.arange(-1, 4, 1)
    axis.set_xticks(x_ticks)
    axis.set_yticks(y_ticks)
    axis.grid()

    start_x, start_y = 1.5, 1.5
    end_num = np.random.randint(0,9)
    end_x, end_y = give_coords_from_num(end_num, start_x, start_y)
    rect = Rectangle((start_x-0.5,start_y-0.5), 1, 1, color=(0,0,1,0.3))
    axis.add_patch(rect)
    rect = Rectangle((end_x-0.5, end_y-0.5), 1, 1, color=(0, 0, 1, 0.3))
    axis.add_patch(rect)

    part = np.random.random()
    x_coll = start_x + part * (end_x - start_x)
    y_coll = start_y + part * (end_y - start_y)
    axis.plot([start_x, x_coll, end_x], [start_y, y_coll, end_y], color="r")

    angle = np.random.random()*2*np.pi
    prev_x, prev_y = x_coll-np.sin(angle), y_coll-np.cos(angle)
    axis.plot([prev_x, x_coll], [prev_y, y_coll], color="g")

    curr_segment = np.zeros((2,2))
    curr_segment[0, 0], curr_segment[0, 1] = start_x, start_y
    curr_segment[1, 0], curr_segment[1, 1] = end_x, end_y
    cross_vec = np.array([x_coll, y_coll])

    test_border_arr = np.zeros((4,4,1))
    test_border_arr[int(start_x), int(start_y),0]=1
    test_border_arr[int(end_x), int(end_y), 0] = 1
    print(curr_segment)
    curr_att_x, curr_att_y, prev_att_x, prev_att_y, num = count_curr_prev_att(cross_vec, curr_segment, angle, test_border_arr)

    rect = Rectangle((curr_att_x + 0.25, curr_att_y + 0.25), 0.5, 0.5, color=(1, 0, 0, 1))
    axis.add_patch(rect)

    rect = Rectangle((prev_att_x + 0.25, prev_att_y + 0.25), 0.5, 0.5, color=(0.5, 0.5, 0, 1))
    axis.add_patch(rect)

    axis.plot([start_x], [start_y], ".", color="k")
    axis.plot([end_x], [end_y], ".", color=(1, 1, 0))

    return num




x_size, y_size = 5, 3

fig, axes = plt.subplots(y_size, x_size, figsize=(2*x_size, 2*y_size))

for i in range(y_size):
    for j in range(x_size):
        num = plot_one(axes[i,j])
        print(i, j, ": ", num)
plt.show()