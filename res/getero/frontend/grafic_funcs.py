import numpy as np

def plot_cells(axis, counter_arr, arr_is_full, ysize, xsize, plot_type):
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
    #axis.grid(which='minor', alpha=0.2)
    axis.grid(which='major', alpha=0.5)


def plot_particle(params, axis, y0, alpha=1.0):
    color = "r"
    if params[2]:
        color = "g"
    print(10*np.sin(params[1]),10*np.cos(params[1]))
    axis.arrow(params[0]-0.5, y0-0.5, 2*np.sin(params[1]), 2*np.cos(params[1]),color=color,linewidth=2, alpha = alpha)