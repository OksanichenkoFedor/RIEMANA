import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from res.getero.algorithm.silicon_reactions.cell_retraction import retract_cell

def test_one(axis=None, size=10):
    count_arr = np.zeros((4,3,3))
    is_f_arr = np.zeros((3,3))
    count_arr[:, 1, 1] = [100,100,100,100]
    is_f_arr[1,1] = 1
    is_f_arr[1, 0], is_f_arr[1, 2], is_f_arr[0, 1], is_f_arr[2, 1] = 1, 1, 1, 1
    is_third = np.random.random()>0.5
    angle = np.random.random()*np.pi*2

    quarter = int((((angle/np.pi)*4.0+5.0)%8.0)*0.5)


    if quarter==0:
        x0, y0 = 1, 2
        x30, y30, x31, y31 = 0, 1, 2, 1
    elif quarter==1:
        x0, y0 = 2, 1
        x30, y30, x31, y31 = 1, 0, 1, 2
    elif quarter==2:
        x0, y0 = 1, 0
        x30, y30, x31, y31 = 0, 1, 2, 1
    elif quarter==3:
        x0, y0 = 0, 1
        x30, y30, x31, y31 = 1, 0, 1, 2

    is_f_arr[x0, y0] = 0
    if is_third:
        if np.random.random() > 0.5:
            is_f_arr[x30, y30] = 0
        else:
            is_f_arr[x31, y31] = 0

    retract_cell(1, 1, count_arr, is_f_arr, angle, True)

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