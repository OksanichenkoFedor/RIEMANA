import numpy as np
from numba import njit

@njit()
def process_particles(counter_arr, is_full_arr, params_arr, Ns, xsize, ysize, y0):
    for i in range(len(params_arr)):
        params = params_arr[i]
        unfound = True
        curr_x = params[0]
        curr_y = y0
        is_on_horiz = 1
        curr_angle = params[1]
        is_add = params[2]
        prev_y, prev_x = None, None
        while unfound:
            if (prev_x is None) and (prev_y is None):
                prev_y, prev_x = curr_y, curr_x
            if (curr_angle > 1.5 * np.pi or curr_angle < 0.5 * np.pi) or (not is_on_horiz):
                curr_att_y = int(curr_y)
                prev_att_y = int(prev_y)
            else:
                curr_att_y = int(curr_y) - 1
                prev_att_y = int(prev_y) - 1

            if (curr_angle <= 1.0 * np.pi) or is_on_horiz:
                curr_att_x = int(curr_x)
                prev_att_x = int(prev_x)
                if is_on_horiz:
                    prev_att_x = curr_att_x
            else:
                curr_att_x = int(curr_x) - 1
                prev_att_x = int(prev_x)# - 1

            if is_full_arr[curr_att_x,curr_att_y]==1:
                if is_add:
                    counter_arr[curr_att_x, curr_att_y]+=1
                    #print("Села")
                else:
                    counter_arr[curr_att_x, curr_att_y]-=1
                    #print("Выбила")
                if counter_arr[curr_att_x,curr_att_y]<=0:
                    is_full_arr[curr_att_x, curr_att_y] = 0
                    counter_arr[curr_att_x, curr_att_y] = 0

                elif counter_arr[curr_att_x,curr_att_y]>=2*Ns[0]:
                    is_full_arr[prev_att_x, prev_att_y] = 1
                    counter_arr[curr_att_x, curr_att_y] = Ns[0]
                    counter_arr[prev_att_x, prev_att_y] = Ns[0]
                unfound = False
            elif is_full_arr[curr_att_x, curr_att_y]==2:
                if is_on_horiz:
                    curr_angle = np.pi - curr_angle
                    if curr_angle < 0:
                        curr_angle += 2.0*np.pi
                else:
                    curr_angle = 2.0*np.pi-curr_angle
            else:
                prev_x = curr_x
                prev_y = curr_y
                prev_horiz = is_on_horiz
                prev_angle = curr_angle
                #curr_x1, curr_y1, curr_angle1, is_on_horiz1 = give_next_cell_compl(prev_x, prev_y, prev_angle, prev_horiz)
                curr_x, curr_y, curr_angle, is_on_horiz = give_next_cell(prev_x, prev_y, prev_angle, prev_horiz)
                #if (np.abs(curr_y1-curr_y)>0.1 or np.abs(curr_x1-curr_x)>0.1) or (np.abs(is_on_horiz1-is_on_horiz)>0.1 or np.abs(curr_angle1-curr_angle)>0.1):
                #    print("Ахтунг!!!")
                #    print(curr_y1, curr_y)
                #    print(curr_x1, curr_x)
                #    print(is_on_horiz1, is_on_horiz)
                #    print(curr_angle1, curr_angle)
                #    print("---")
                #plt.plot(curr_x-0.5,curr_y-0.5,"o",color="g")
                #plt.plot(curr_x1 - 0.5, curr_y1 - 0.5, ".", color="r")
                if (curr_x>=xsize or curr_x<0) or (curr_y>=ysize or curr_y<0):
                    unfound = False
                elif int(curr_y)<=1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                    unfound = False


@njit()
def give_next_cell_compl(x_coord, y_coord, angle, is_on_horiz):
    if angle > 1.5 * np.pi or angle < 0.5 * np.pi:
        if angle <= 1.0 * np.pi:
            # летим вправо-вниз
            if is_on_horiz:
                delta_x = np.tan(angle) + x_coord - int(x_coord)
                if delta_x > 1.0:
                    # правая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = 1 + int(x_coord)
                else:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord += np.tan(angle)
                    y_coord += 1
            else:
                delta_y = 1.0 / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = 1 + int(y_coord)
                else:
                    # правая грань
                    is_on_horiz = 0
                    y_coord += 1.0 / np.tan(angle)
                    x_coord += 1
        else:
            # летим влево-вниз
            if is_on_horiz:
                delta_x = np.tan(angle) + x_coord - int(x_coord)
                if delta_x < 0:
                    # левая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = int(x_coord)
                else:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord += np.tan(angle)
                    y_coord += 1
            else:
                delta_y = (-1.0) / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = 1 + int(y_coord)
                else:
                    # левая грань
                    is_on_horiz = 0
                    y_coord -= 1.0 / np.tan(angle)
                    x_coord -= 1
    else:
        if angle <= 1.0 * np.pi:
            # летим вправо-вверх
            if is_on_horiz:
                delta_x = (-1.0) * np.tan(angle) + x_coord - int(x_coord)
                if delta_x > 1.0:
                    print("Err? ",x_coord)
                    # правая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = 1 + int(x_coord)
                else:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord -= np.tan(angle)
                    y_coord -= 1
            else:
                delta_y = 1.0 / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (int(y_coord) - y_coord) / np.tan(angle)
                    y_coord = int(y_coord)
                else:
                    # правая грань
                    is_on_horiz = 0
                    y_coord += 1.0 / np.tan(angle)
                    x_coord += 1
        else:
            # летим влево-вверх
            if is_on_horiz:
                delta_x = (-1.0) * np.tan(angle) + x_coord - int(x_coord)
                if delta_x < 0:
                    # левая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = int(x_coord)
                else:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord -= np.tan(angle)
                    y_coord -= 1
            else:
                delta_y = (-1.0) / np.tan(angle) + y_coord - int(y_coord)
                if delta_y < 0.0:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = int(y_coord)
                else:
                    # левая грань
                    is_on_horiz = 0
                    y_coord -= 1.0 / np.tan(angle)
                    x_coord -= 1

    return 1.0*x_coord, 1.0*y_coord, angle, is_on_horiz

@njit()
def give_next_cell(x_coord, y_coord, angle, is_on_horiz):
    if angle > 1.5 * np.pi or angle < 0.5 * np.pi:
        x_mult = 1.0
    else:
        x_mult = -1.0
    if angle <= 1.0 * np.pi:
        y_mult = 1.0
    else:
        y_mult = -1.0

    if is_on_horiz:
        delta_x = x_mult*np.tan(angle) + x_coord - int(x_coord)
        if delta_x > 1.0:
            is_on_horiz = 0
            y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
            x_coord = 1 + int(x_coord)
        elif delta_x < 0:
            # левая грань
            is_on_horiz = 0
            y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
            x_coord = int(x_coord)
        else:
            is_on_horiz = 1
            x_coord += x_mult*np.tan(angle)
            y_coord += x_mult*1
    else:
        delta_y = y_mult / np.tan(angle) + y_coord - int(y_coord)
        if delta_y > 1.0:
            is_on_horiz = 1
            x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
            y_coord = 1 + int(y_coord)
        elif delta_y < 0.0:
            is_on_horiz = 1
            x_coord = x_coord + (int(y_coord) - y_coord) * np.tan(angle)
            y_coord = int(y_coord)
        else:
            is_on_horiz = 0
            y_coord += y_mult*1.0 / np.tan(angle)
            x_coord += y_mult*1

    return 1.0*x_coord, 1.0*y_coord, angle, is_on_horiz