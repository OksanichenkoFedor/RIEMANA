import numpy as np
from res.utils.config import seed
np.random.seed(seed)
import matplotlib
from matplotlib.patches import Circle
from res.getero.algorithm.dynamic_profile import give_line_arrays
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def plot_cells(axis, counter_arr, arr_is_full, ysize, xsize, plot_type, is_chosen_cell=False, ch_x = None, ch_y = None):
    if plot_type=="is_cell":
        axis.imshow(1.0-arr_is_full.T, cmap="inferno")
    elif plot_type=="Si":
        axis.imshow(counter_arr[0].T, cmap='Greens')
    elif plot_type=="SiCl":
        axis.imshow(counter_arr[1].T, cmap='Greens')
    elif plot_type=="SiCl2":
        axis.imshow(counter_arr[2].T, cmap='Greens')
    elif plot_type=="SiCl3":
        axis.imshow(counter_arr[3].T, cmap='Greens')

    axis.set_ylim([ysize - 0.5, -0.5])
    axis.set_xlim([-0.5, xsize - 0.5])
    axis.set_yticks(np.arange(0, ysize, 1) - 0.5, minor=True)
    axis.set_xticks(np.arange(0, xsize, 1) - 0.5, minor=True)
    axis.set_yticks(np.arange(0, ysize, 100) - 0.5)
    axis.set_xticks(np.arange(0, xsize, 100) - 0.5)
    #xis.grid(which='minor', alpha=1)
    axis.grid(which='major', alpha=0.5)
    if is_chosen_cell:
        rect1 = matplotlib.patches.Rectangle((ch_x - 0.5, ch_y - 0.5), 1, 1, fill=False, color=(1.0,0,0))
        axis.add_patch(rect1)



def plot_particle(params, axis, y0, alpha=1.0):
    color = "r"
    if params[2]:
        color = "g"
    print(10*np.sin(params[1]),10*np.cos(params[1]))
    axis.arrow(params[0]-0.5, y0-0.5, 2*np.sin(params[1]), 2*np.cos(params[1]),color=color,linewidth=2, alpha = alpha)

def plot_line(axis, X, Y, prev_x, prev_y, curr_x, curr_y, size=1):
    circ = Circle(((prev_x - curr_x)*size, (prev_y - curr_y)*size), 0.2*size, color="r")
    axis.add_patch(circ)
    axis.plot((np.array(X) - curr_x)*size, (np.array(Y) - curr_y)*size, color="r")
    axis.plot((np.array(X) - curr_x) * size, (np.array(Y) - curr_y) * size, ".", color="r")



def plot_animation(profiles, xsize, ysize, num):
    fig, ax = plt.subplots(figsize=(10,10))
    x_major_ticks = np.arange(0, xsize, 10)
    x_minor_ticks = np.arange(0, xsize, 1)
    y_major_ticks = np.arange(0, ysize, 10)
    y_minor_ticks = np.arange(0, ysize, 1)
    ax.set_xticks(x_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    ax.set_aspect(1)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.8)
    ax.set(xlim=[0, xsize], ylim=[ysize, 0])
    x, y = profiles[0]
    line, = ax.plot(x, y)
    def update(frame):
        # for each frame, update the data stored on each artist.
        x, y = profiles[frame]
        line.set_xdata(x)
        line.set_ydata(y)  # update the data
        return line,


    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(profiles), interval=50)
    ani.save("files/tmp"+str(num)+".gif")

    #plt.show()