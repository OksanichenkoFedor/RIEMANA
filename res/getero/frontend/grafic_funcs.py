import numpy as np

from res.utils.config import seed
np.random.seed(seed)
import matplotlib
from matplotlib.patches import Circle
from res.getero.algorithm.dynamic_profile import give_line_arrays
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def plot_cells(axis, wafer, plot_type, is_chosen_cell=False, ch_x = None, ch_y = None, do_cut=False, cut_x=[0,-1], cut_y=[0,-1]):
    counter_arr = wafer.counter_arr
    arr_is_full = wafer.is_full
    ysize, xsize = wafer.xsize, wafer.ysize


    if cut_x[1]==-1:
        cut_x[1] = xsize
    if cut_y[1]==-1:
        cut_y[1] = ysize
    if do_cut:
        pass
        n_aif = arr_is_full.copy()[cut_x[0]:cut_x[1], cut_y[0]:cut_y[1]]
        n_ca = counter_arr.copy()[:, cut_x[0]:cut_x[1], cut_y[0]:cut_y[1]]
    else:
        n_aif = arr_is_full.copy() + (wafer.is_hard.copy()).astype(float)*(-5.0)
        n_ca = counter_arr.copy()
    if plot_type=="is_cell":
        axis.imshow(1.0-n_aif.T, cmap="inferno")
    elif plot_type=="Si":
        axis.imshow(n_ca[0].T, cmap='Greens')
    elif plot_type=="SiCl":
        axis.imshow(n_ca[1].T, cmap='Greens')
    elif plot_type=="SiCl2":
        axis.imshow(n_ca[2].T, cmap='Greens')
    elif plot_type=="SiCl3":
        axis.imshow(n_ca[3].T, cmap='Greens')
    axis.set_ylim([cut_y[1]-cut_y[0] - 0.5,  - 0.5])
    axis.set_xlim([-0.5, cut_x[1]-cut_x[0] - 0.5])
    axis.set_yticks(np.arange(0, cut_y[1]-cut_y[0], 1) - 0.5, minor=True)
    axis.set_xticks(np.arange(0, cut_x[1]-cut_x[0], 1) - 0.5, minor=True)
    axis.set_yticks(np.arange(0, cut_y[1]-cut_y[0], 100) - 0.5)
    axis.set_xticks(np.arange(0, cut_x[1]-cut_x[0], 100) - 0.5)
    axis.grid(which='minor', alpha=1)
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

def plot_line(axis, X, Y, add_x, add_y, size=1, do_points=True):
    circ = Circle(((X[0] + add_x)*size, (Y[0] + add_y)*size), 0.4*size, color="r")
    axis.add_patch(circ)
    axis.plot((np.array(X) + add_x)*size, (np.array(Y) + add_y)*size, color="r")
    if do_points:
        axis.plot((np.array(X) + add_x) * size, (np.array(Y) + add_y) * size, ".", color="r")



def plot_animation(profiles, xsize, ysize, num, filename=None):
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
    if filename is None:
        ani.save("data/pictures/tmp"+str(num)+".gif", writer='pillow')
    else:
        ani.save(filename+".gif", writer='pillow')

    #plt.show()