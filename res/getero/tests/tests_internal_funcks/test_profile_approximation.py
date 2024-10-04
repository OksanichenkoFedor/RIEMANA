from res.getero.algorithm.dynamic_profile import give_line_arrays
from res.getero.algorithm.ray_tracing.bvh import bvh_count_collision_point, build_BVH
from res.getero.algorithm.ray_tracing.utils import check_angle_collision
from res.getero.algorithm.utils import straight_reflection
from res.getero.tests.tests_internal_funcks.help_test_funks import create_test_wafer
from res.global_entities.plotter import generate_figure
from res.global_entities.wafer import Wafer, prepare_segment_for_intersection_checking
from res.getero.algorithm.monte_carlo import generate_particles
from res.getero.algorithm.ray_tracing.profile_approximation import count_norm_angle

import res.utils.config as config

from tqdm import trange
import time
import matplotlib.pyplot as plt
import numpy as np

params = config.plasma_params

n_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

y_ar_plus = params["j_ar_plus"]/n_full
y_cl = params["j_cl"]/n_full
y_cl_plus = params["j_cl_plus"]/n_full
cell_size = params["cell_size"]
T_i = params["T_i"]
U_i = params["U_i"]

def plot_wafer(c_wafer, ax=None):
    X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
    X, Y = prepare_segment_for_intersection_checking(X,Y, None, None, False, 10)
    X, Y = np.array(X)+0.5, np.array(Y)+0.5
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.set_aspect(1)
        ax.set_ylim([Y.max(), Y.min()])
        x_ticks = np.arange(0, 2*c_wafer.xsize, 1)
        y_ticks = np.arange(0, c_wafer.ysize, 1)
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.grid()
    #m = 260
    #n = 267
    m = 0
    n = len(X)
    #print(X[m:n], Y[m:n])
    ax.plot(X[m:n], Y[m:n])
    #ax.plot(X[m:n], Y[m:n], ".")
    #ax.set_ylim([Y[m:n].max(), Y[m:n].min()])
    #ax.plot(X, Y, "o")
    return ax
    #ax.plot(arr_x,arr_y,color="r")

def test_prof_approx(curr_wafer, num_particles, num_one_side_points):

    params = generate_particles(num_particles, curr_wafer.xsize, y_ar_plus=y_ar_plus, y_cl=y_cl, y_cl_plus=y_cl_plus,
                                T_i=T_i, T_e=U_i, y0=curr_wafer.y0)
    ax = None
    na = []
    As = []
    Bs = []
    ax = plot_wafer(curr_wafer, ax)
    for i in trange(len(params)):
        err_x, err_y = [], []
        partile = params[i]
        #partile = [91.43574696,1.,1.,0.12,1.14797243,0.,91.,1.]
        #particle = [1.32206804e+02,1.00000000e+00,1.00000000e+00,1.20000000e-01,9.59745319e-01,0.00000000e+00,1.32000000e+02,1.00000000e+00]
        #print(partile)
        curr_vec = np.zeros(2)
        curr_vec[0] = partile[0]
        curr_vec[1] = partile[1]
        start_segment = np.ones((2, 2)) * (-1.0)
        curr_en = partile[3]
        curr_angle = partile[4]
        curr_type = partile[5]
        ax.plot([curr_vec[0], curr_vec[0] + 5 * np.sin(curr_angle)],
                [curr_vec[1], curr_vec[1] + 5 * np.cos(curr_angle)], color=(0, 0, 1, 0.5))
        NodeList = build_BVH(curr_wafer.border_arr, curr_wafer.is_half)
        is_collide, coll_vec, norm_angle, start_segment, _ = bvh_count_collision_point(NodeList, curr_vec, curr_angle,
                                                                                   start_segment)
        num = 0
        while is_collide and num<50:
            num+=1
            err_x.append(coll_vec[0])
            err_y.append(coll_vec[1])
            #print("--- ", coll_vec)
            n_angle, deb, bX, bY, A, B, reach_left_side = count_norm_angle(curr_wafer.border_arr, coll_vec, start_segment,
                                                          curr_wafer.is_half, num_one_side_points=num_one_side_points)



            #alpha = 2.0 / (max(np.abs(A), np.abs(B)))
            #x = alpha * np.arange(-1, 1, 0.1) * B + coll_vec[0]
            #y = alpha * np.arange(-1, 1, 0.1) * (-1.0 * A) + coll_vec[1]
            #ax.plot(x, y, color="g")
            if deb == -1:
                color = "b"
            elif deb == -2:
                color = "g"
            elif deb == 1:
                color = "r"
                #print(bX, bY)
                #ax.plot(bX, bY, color=(0.5,0.5,0))
            elif deb == 2:
                color = "k"


            new_angle = straight_reflection(curr_angle,n_angle)

            is_oob, left_angle, right_angle, res_angle= check_angle_collision(curr_angle, new_angle, start_segment, coll_vec)

            if res_angle is None:
                ax.plot([curr_vec[0], curr_vec[0] - 5 * np.sin(curr_angle)],
                        [curr_vec[1], curr_vec[1] - 5 * np.cos(curr_angle)], color=(0, 0, 1, 0.5))
                color = "r"
                #ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(res_angle)],
                #        [coll_vec[1], coll_vec[1] + 2 * np.cos(res_angle)], color=(1, 0.5, 0))
                ax.plot([coll_vec[0], coll_vec[0] + 5 * np.sin(new_angle)],
                        [coll_vec[1], coll_vec[1] + 5 * np.cos(new_angle)], color=color)

                ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(left_angle)],
                        [coll_vec[1], coll_vec[1] + 2 * np.cos(left_angle)], color=(1, 1, 0.5))
                ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(right_angle)],
                        [coll_vec[1], coll_vec[1] + 2 * np.cos(right_angle)], color=(1, 1, 0.5))
                color = "k"
                ax.plot([coll_vec[0], coll_vec[0] + 5 * np.sin(n_angle)],
                       [coll_vec[1], coll_vec[1] + 5 * np.cos(n_angle)], color=color)
                plt.show()
            if len(err_x)%5==0 and False:
                ax = None
                ax.plot(bX, bY, ".")
                ax = plot_wafer(curr_wafer, ax)
                for i in range(len(err_x)-1):
                    ax.plot([err_x[i], err_x[i+1]], [err_y[i], err_y[i+1]], color=(0, 0, 1, 0.5))
                ax.set_xlim([min(err_x) - 5, max(err_x) + 5])
                ax.set_ylim([max(err_y) + 5, min(err_y) - 5])
                plt.show()

            color = "g"
            #ax.plot(bX, bY, ".")
            #ax.plot([curr_vec[0], coll_vec[0]], [curr_vec[1], coll_vec[1]], color=(0, 0, 1, 0.5))

            color = "k"
            ax.plot([coll_vec[0], coll_vec[0] + 5 * np.sin(n_angle)],
                    [coll_vec[1], coll_vec[1] + 5 * np.cos(n_angle)], color=color)

            if reach_left_side and False:
                color = "g"
                ax.plot(bX, bY, ".")
                ax.plot([curr_vec[0], coll_vec[0]], [curr_vec[1], coll_vec[1]], color=(0, 0, 1, 0.5))

                color = "k"
                ax.plot([coll_vec[0], coll_vec[0] + 5 * np.sin(n_angle)],
                        [coll_vec[1], coll_vec[1] + 5 * np.cos(n_angle)], color=color)
                plt.show()
                ax = None
                ax = plot_wafer(curr_wafer, ax)

            if is_oob and False:


                color = "r"
                ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(res_angle)],
                        [coll_vec[1], coll_vec[1] + 2 * np.cos(res_angle)], color=(1,0.5,0))
                ax.plot([coll_vec[0], coll_vec[0] + 5 * np.sin(new_angle)],
                    [coll_vec[1], coll_vec[1] + 5 * np.cos(new_angle)], color=color)

                ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(left_angle)],
                    [coll_vec[1], coll_vec[1] + 2 * np.cos(left_angle)], color=(1,1,0.5))
                ax.plot([coll_vec[0], coll_vec[0] + 2 * np.sin(right_angle)],
                    [coll_vec[1], coll_vec[1] + 2 * np.cos(right_angle)], color=(1,1,0.5))
            curr_vec = coll_vec
            curr_angle = res_angle
            is_collide, coll_vec, norm_angle, start_segment, _ = bvh_count_collision_point(NodeList, curr_vec, curr_angle,
                                                                                        start_segment)
            #plt.show()
        #print("end")
        if num>=900:
            print(partile)



    plt.show()

end_wafer = Wafer()
#end_wafer.load("../files/wafer_2000.zip")
import os
print(os.listdir("../../"))
end_wafer.load("../../../data/wafer_U40_Ar0.5_SiNum7.zip")

#end_wafer = create_test_wafer(num_del=200)
#end_wafer.save("../files/test_wafer_500del.zip")
#end_wafer.load("../files/test_wafer_15000del.zip")
end_wafer.check_self_intersection()
#end_wafer.make_half()
#end_wafer.return_half()
#f = generate_figure(end_wafer, wafer_curr_type="is_cell", do_plot_line=True)
#plt.show()
test_prof_approx(end_wafer, 600, 30)
