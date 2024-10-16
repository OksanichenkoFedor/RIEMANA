from res.global_entities.wafer import Wafer
#from res.global_entities.plotter import generate_figure
import matplotlib.pyplot as plt
from res.getero.frontend.grafic_funcs import plot_cells, plot_line, plot_animation
import time
import numpy as np
import os
from tqdm import trange


def generate_figure(wafer, wafer_curr_type, do_plot_line=True, axis=None, x_cut=80, y_start=50, y_end=250):
    if axis is None:
        f = plt.figure(figsize=(9, 7), dpi=100, tight_layout=True)
        axis = f.add_subplot(1, 1, 1)
    start = time.time()
    axis.clear()
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    # curr_type = config.wafer_plot_types[config.wafer_plot_num]
    #print(y_start)
    plot_cells(axis, wafer, wafer_curr_type, do_cut=True, cut_x=[x_cut, wafer.xsize-x_cut], cut_y=[y_start, wafer.ysize-y_end])
    X, Y = wafer.profiles[-1]
    if do_plot_line:
        plot_line(axis, X, Y, wafer.start_x, wafer.start_y, 0, 0,
                  do_points=False)
    x_major_ticks = np.arange(0, wafer.xsize, 10) + 0.5
    x_minor_ticks = np.arange(0, wafer.xsize, 1) + 0.5
    y_major_ticks = np.arange(0, wafer.ysize, 10) + 0.5
    y_minor_ticks = np.arange(0, wafer.ysize, 1) + 0.5
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)

    end = time.time()
    print("Plot time: ", round(end - start, 3))
    if axis is None:
        return f


def count_delta_xy(wafer):
    w_if = wafer.is_full[:, int(wafer.border+wafer.mask_height):].copy()
    w_if = np.where(w_if == 0, 1, 0)
    delta_x = int(((w_if.sum(axis=1).astype(bool)).astype(int).sum()+wafer.left_area-wafer.right_area)*0.5)
    delta_y = (w_if.sum(axis=0).astype(bool)).astype(int).sum()
    return delta_x, delta_y


def parce_wafer(filename, axis, x_cut=80, y_start=50, y_end=250):
    W = Wafer()
    W.load(filename)
    delta_x, delta_y = count_delta_xy(W)
    delta_x, delta_y = delta_x*25, delta_y*25
    time = 60
    print(delta_x,delta_y)
    fig = generate_figure(W, "is_cell", do_plot_line=False, axis=axis, x_cut=x_cut, y_start=y_start, y_end=y_end)
    return fig, delta_x, delta_y


