import numpy as np

def plot_cells(axis, arr_is_full, ysize, xsize):

    axis.imshow(1.0-arr_is_full.T, cmap="inferno")
    axis.set_ylim([ysize-0.5,-0.5])
    axis.set_xlim([-0.5,xsize-0.5])
    axis.set_yticks(np.arange(0, ysize, 1)-0.5, minor=True)
    axis.set_xticks(np.arange(0, xsize, 1)-0.5, minor=True)
    axis.set_yticks(np.arange(0, ysize, 100)-0.5)
    axis.set_xticks(np.arange(0, xsize, 100)-0.5)
    #axis.grid(which='minor', alpha=0.2)
    axis.grid(which='major', alpha=0.5)


def plot_particle(params, axis, y0, alpha=1.0):
    color = "r"
    if params[2]:
        color = "g"
    print(10*np.sin(params[1]),10*np.cos(params[1]))
    axis.arrow(params[0]-0.5, y0-0.5, 2*np.sin(params[1]), 2*np.cos(params[1]),color=color,linewidth=2, alpha = alpha)