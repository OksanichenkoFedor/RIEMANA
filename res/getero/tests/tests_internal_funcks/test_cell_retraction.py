import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from res.getero.silicon_reactions.cell_retraction import retract_cell
from res.getero.algorithm.dynamic_profile import give_coords_from_num

def test_one(axis=None, size=10):
    count_arr = np.zeros((4,3,3))
    is_f_arr = np.zeros((3,3))
    is_around = np.random.randint(0,2,8)
    for i in range(8):
        curr_x, curr_y = give_coords_from_num(i, 1, 1)
        if is_around[i]:
            is_f_arr[curr_x, curr_y] = 1
    count_arr[:, 1, 1] = [100,100,100,100]
    #is_f_arr[1,1] = 1
    angle = np.random.random()*np.pi*2

    quarter = int((((angle/np.pi)*4.0+5.0)%8.0)*0.5)
    #print("start is_around: ",is_around)
    koeffs = retract_cell(1, 1, count_arr, is_f_arr, angle, True)



    for i in range(3):
        for j in range(3):
            color = "r"
            if is_f_arr[i,j]==0:
                color=(0,1,0,0.5)
            else:
                color=(1,0,0,0.5)
            rect = Rectangle((i*size, j*size), size, size, color=color)
            axis.add_patch(rect)
            axis.text(size * (0.3 + i) - 0.25 * size, size * (0.45+j) - 0.25 * size,
                      count_arr[0,i,j], size=5.0, color="k")
            axis.text(size * (0.3 + i) + 0.25 * size, size * (0.45 + j) - 0.25 * size,
                      count_arr[1, i, j], size=5.0, color="k")
            axis.text(size * (0.3 + i) + 0.25 * size, size * (0.45 + j) + 0.25 * size,
                      count_arr[2, i, j], size=5.0, color="k")
            axis.text(size * (0.3 + i) - 0.25 * size, size * (0.45 + j) + 0.25 * size,
                      count_arr[3, i, j], size=5.0, color="k")

    for i in range(8):
        curr_x, curr_y = give_coords_from_num(i, 1, 1)
        axis.text(size * curr_x + 0.5 * size, size * curr_y + 0.5 * size,
                  round(koeffs[i],2), size=7.0, color="k")

    axis.axvline(x=size, color="k")
    axis.axvline(x=2 * size, color="k")
    # axis.axvline(x=30, color="b")
    axis.axhline(y=size, color="k")
    axis.axhline(y=2 * size, color="k")
    axis.set_xlim((0, 3 * size))
    axis.set_ylim((3 * size, 0))
    #axis.text(size * 1.5 - 0.3 * size, size * 1.5 - 0.3 * size, str(round(angle / np.pi, 3)), color="k")
    #axis.text(size * 1.5 - 0.3 * size, size * 1.5 + 0.3 * size, quarter, color="k")
    axis.plot([size*1.5, size*1.5-size*1.5*np.sin(angle)], [size*1.5, size*1.5-size*1.5*np.cos(angle)], color="b")



x_size = 4
y_size = 4
fig, axes = plt.subplots(x_size, y_size, figsize=(2.5*y_size, 2.5*x_size))
#print(axes.shape)
for i in range(x_size):
    for j in range(y_size):
        test_one(axes[i,j])
plt.show()