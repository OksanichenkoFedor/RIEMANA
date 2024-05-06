import numpy as np

from res.getero.algorithm.wafer_generator import generate_pure_wafer
from res.getero.algorithm.dynamic_profile import delete_point, create_point


class Wafer:
    def __init__(self, multiplier, Si_num):
        generate_pure_wafer(self, multiplier, Si_num)

    def process_file(self, filename, verbose=0):
        f = open(filename)
        A = f.readlines()
        f.close()
        for line in A[:]:
            line = line.split()
            if len(line) == 3:
                x = int(line[1])
                y = int(line[2])
                self.counter_arr[:, x, y] = np.array([0, 0, 0, 0])
                self.is_full[x, y] = 0
                delete_point(self.border_arr, x, y)
                # time.sleep(0.05)
                if verbose:
                    print("Delete: ", x, y)
                # self.replot()
            elif len(line) == 6:
                prev_x = int(line[1])
                prev_y = int(line[2])
                curr_x = int(line[4])
                curr_y = int(line[5])
                self.counter_arr[:, prev_x, prev_y] = np.array([0, 0, 0, 1])
                self.is_full[prev_x, prev_y] = 1
                create_point(self.border_arr, prev_x, prev_y, curr_x, curr_y)
                if verbose:
                    print("Create: ", prev_x, prev_y, " from: ", curr_x, curr_y)


    def give_part_of_border(self, target_x, target_y, num_one_side_points):
        # ищем начало
        X, Y = np.zeros(2 * num_one_side_points + 1), np.zeros(2 * num_one_side_points + 1)
        X[num_one_side_points] = target_x
        Y[num_one_side_points] = target_y
        start_x, start_y = target_x, target_y
        for i in range(num_one_side_points):
            new_x, new_y = self.border_arr[start_x, start_y, 1], self.border_arr[start_x, start_y, 2]
            if new_x != -1 and new_y != -1:
                start_x, start_y = new_x, new_y
            X[num_one_side_points - (i+1)] = start_x
            Y[num_one_side_points - (i+1)] = start_y

        end_x, end_y = target_x, target_y
        for i in range(num_one_side_points):
            new_x, new_y = self.border_arr[end_x, end_y, 3], self.border_arr[end_x, end_y, 4]
            if new_x != -1 and new_y != -1:
                end_x, end_y = new_x, new_y
            X[num_one_side_points + (i + 1)] = end_x
            Y[num_one_side_points + (i + 1)] = end_y

        return X, Y, num_one_side_points

    def give_el_border(self, target_num):
        curr_x, curr_y = self.start_x, self.start_y
        num = 0
        while num<target_num and (curr_x!=self.end_x or curr_y!=self.end_y):
            curr_x, curr_y = self.border_arr[curr_x, curr_y, 3],  self.border_arr[curr_x, curr_y, 4]
            num+=1
        return curr_x, curr_y


    def save(self, filename):
        pass

    def load(self, filename):
        pass
