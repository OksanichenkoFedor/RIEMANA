import numpy as np
from numba import njit
from res.getero.algorithm.dynamic_profile import delete_point, create_point, give_line_arrays, give_start, give_end
from res.getero.algorithm.ray_tracing.bvh import build_BVH
import res.utils.config as config

from omegaconf import OmegaConf
import numpy as np
from zipfile import ZipFile
import os


class Wafer:
    def __init__(self, multiplier=None, Si_num=84):
        if not (multiplier is None):
            self.generate_pure_wafer(multiplier, Si_num)

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
            X[num_one_side_points - (i + 1)] = start_x
            Y[num_one_side_points - (i + 1)] = start_y

        end_x, end_y = target_x, target_y
        for i in range(num_one_side_points):
            new_x, new_y = self.border_arr[end_x, end_y, 3], self.border_arr[end_x, end_y, 4]
            if new_x != -1 and new_y != -1:
                end_x, end_y = new_x, new_y
            X[num_one_side_points + (i + 1)] = end_x
            Y[num_one_side_points + (i + 1)] = end_y

        return X, Y, num_one_side_points

    def give_el_border(self, target_num):
        curr_x, curr_y = give_start(self.border_arr)
        end_x, end_y = give_end(self.border_arr)
        num = 0
        while num < target_num and (curr_x != end_x or curr_y != end_y):
            curr_x, curr_y = self.border_arr[curr_x, curr_y, 3], self.border_arr[curr_x, curr_y, 4]
            num += 1
        return curr_x, curr_y

    def check_correction(self):
        for curr_x in range(self.border_arr.shape[0]):
            for curr_y in range(self.border_arr.shape[1]):
                if self.is_full[curr_x, curr_y] in [1, 2]:
                    if self.is_near_void(curr_x, curr_y) and self.border_arr[curr_x, curr_y, 0] != 1:
                        raise Exception("This cell (" + str(curr_x) + " " + str(
                            curr_y) + ") is located on the border, but is not included in it")
                    if (not self.is_near_void(curr_x, curr_y)) and self.border_arr[curr_x, curr_y, 0] == 1:
                        raise Exception("This cell (" + str(curr_x) + " " + str(
                            curr_y) + ") is inside wafer, but is included in border")
        self.nodelist = build_BVH(self.border_arr)

    def is_near_void(self, curr_x, curr_y):
        x_size, y_size = self.is_full.shape[0], self.is_full.shape[1]
        unfound = True
        if curr_x != 0:
            if self.is_full[curr_x - 1, curr_y] == 0:
                unfound = False
        if curr_x != x_size - 1:
            if self.is_full[curr_x + 1, curr_y] == 0:
                unfound = False
        if curr_y != 0:
            if self.is_full[curr_x, curr_y - 1] == 0:
                unfound = False
        if curr_y != y_size - 1:
            if self.is_full[curr_x, curr_y + 1] == 0:
                unfound = False
        return not unfound

    def save(self, filename):
        # print("Start saveing: ",filename)
        self.check_correction()
        cdict = {
            "multiplier": self.multiplier,
            "Si_num": self.Si_num,
            "border": self.border,
            "xsize": self.xsize,
            "ysize": self.ysize,
            "y0": self.y0,
            "silicon_size": self.silicon_size,
            "is_half": self.is_half,
            "profiles": self.profiles,

        }
        conf = OmegaConf.create(cdict)
        OmegaConf.save(config=conf, f="cdict.yaml")
        np.save("is_full.npy", self.is_full)
        np.save("counter_arr.npy", self.counter_arr)
        np.save("mask.npy", self.mask)
        np.save("border_arr.npy", self.border_arr)
        # np.save("profiles.npy", np.array(self.profiles))

        with ZipFile(filename, 'w') as myzip:
            myzip.write("is_full.npy")
            myzip.write("counter_arr.npy")
            myzip.write("mask.npy")
            myzip.write("border_arr.npy")
            # myzip.write("profiles.npy")
            myzip.write("cdict.yaml")

        os.remove("is_full.npy")
        os.remove("counter_arr.npy")
        os.remove("mask.npy")
        os.remove("border_arr.npy")
        # os.remove("profiles.npy")
        os.remove("cdict.yaml")

        # print("End saveing: ", filename)

    def load(self, filename):
        with ZipFile(filename) as myzip:
            with myzip.open("is_full.npy") as myfile:
                self.is_full = np.load(myfile)
            with myzip.open("counter_arr.npy") as myfile:
                self.counter_arr = np.load(myfile)
            with myzip.open("mask.npy") as myfile:
                self.mask = np.load(myfile)
            with myzip.open("border_arr.npy") as myfile:
                self.border_arr = np.load(myfile)
            with myzip.open("cdict.yaml") as myfile:
                conf = OmegaConf.load(myfile)
        self.multiplier = float(conf.multiplier)
        self.Si_num = int(conf.Si_num)
        self.border = int(conf.border)
        self.xsize = int(conf.xsize)
        self.ysize = int(conf.ysize)
        self.y0 = int(conf.y0)
        self.silicon_size = int(conf.silicon_size)
        self.profiles = list(conf.profiles)
        self.is_half = bool(conf.is_half)
        self.check_correction()
        self.nodelist = build_BVH(self.border_arr)

    def generate_pure_wafer(self, multiplier, Si_num, fill_sicl3=False, params={}):

        for attr in config.pure_wafer_params:
            if attr in params:
                setattr(self, attr, params[attr])
            else:
                setattr(self, attr, config.pure_wafer_params[attr])

        self.old_wif = []
        self.old_wca = []
        self.profiles = []
        self.multiplier = multiplier
        self.Si_num = Si_num
        self.border = int(self.border * self.multiplier)
        self.xsize = int(self.xsize * self.multiplier * 0.5) * 2
        self.ysize = int(self.ysize * self.multiplier)
        self.left_area = int(self.xsize * 0.5 + 1) - int(self.hole_size * self.multiplier)
        self.right_area = int(self.xsize * 0.5 + 1) + int(self.hole_size * self.multiplier)
        self.mask_height = int(self.mask_height * self.multiplier)
        self.y0 = 1#self.border-2
        self.silicon_size = int(self.silicon_size * self.multiplier)
        self.is_half = False
        # print(25*self.silicon_size)
        self.is_full = np.fromfunction(lambda i, j: j >= self.border, (self.xsize+2, self.ysize), dtype=int).astype(
            int)
        self.counter_arr = self.is_full.copy() * self.Si_num
        self.mask = np.ones((self.xsize+2, self.ysize))
        self.mask[:, :self.border] = self.mask[:, :self.border] * 0
        self.mask[:,
        self.border + self.mask_height:self.border + self.mask_height + self.silicon_size] = self.mask[:,
                                                                                             self.border + self.mask_height:self.border +
                                                                                                                            self.mask_height + self.silicon_size] * 0
        self.mask[self.left_area:self.right_area, :self.border + self.mask_height + self.silicon_size] = \
            self.mask[self.left_area:self.right_area, :self.border + self.mask_height + self.silicon_size] * 0
        self.is_full = self.mask + self.is_full
        self.counter_arr = np.repeat(
            self.counter_arr.reshape(1, self.counter_arr.shape[0], self.counter_arr.shape[1]),
            4, axis=0)
        self.counter_arr[1] = self.counter_arr[1] * 0
        self.counter_arr[2] = self.counter_arr[2] * 0
        ind = 3
        if fill_sicl3:
            ind = 0
        self.counter_arr[ind] = self.counter_arr[ind] * 0

        self.counter_arr[0] = self.counter_arr[0] - self.mask * self.Si_num
        self.border_arr = np.ones((self.xsize+2, self.ysize, 5)) * 0.5
        if config.do_walls:
            for i in range(self.xsize):
                j = i + 1
                self.border_arr[j, self.border, 0] = 1.0
                if i == 0:
                    self.border_arr[j, self.border, 1:] = [0, self.border, j + 1, self.border]
                    self.border_arr[0, self.border] = [1, 0, self.border - 1, j, self.border]
                elif i == self.xsize - 1:
                    self.border_arr[j, self.border, 1:] = [j - 1, self.border, j + 1, self.border]
                    self.border_arr[j + 1, self.border] = [1, j, self.border, j + 1, self.border - 1]
                else:
                    self.border_arr[j, self.border, 1:] = [j - 1, self.border, j + 1, self.border]
        else:
            for i in range(self.xsize+2):
                self.border_arr[i, self.border, 0] = 1.0
                if i == 0:
                    self.border_arr[i, self.border, 1:] = [-1, -1, i + 1, self.border]
                elif i == self.xsize + 1:
                    self.border_arr[i, self.border, 1:] = [i - 1, self.border, -1, -1]
                else:
                    self.border_arr[i, self.border, 1:] = [i - 1, self.border, i + 1, self.border]




        self.border_arr[:, :self.border - 0, :] = self.border_arr[:, :self.border - 0, :] * (
            -2.0)
        self.border_arr[:, self.border + 1:, :] = self.border_arr[:, self.border + 1:, :] * (
            0.0)

        self.is_full[0,self.border:] = np.ones((self.ysize-self.border,))*(-1.0)

        if config.do_walls:
            self.is_full[0, :] = np.ones(self.ysize) * (-1.0)
            self.is_full[-1, :] = np.ones(self.ysize) * (-1.0)
            for i in range(self.border):
                if i==0:
                    self.border_arr[0, i]=[1.0, -1, -1, 0, i + 1]
                    self.border_arr[self.xsize + 1, i] = [1.0, self.xsize + 1, i + 1, -1, -1]
                else:
                    self.border_arr[0, i] = [1.0, 0, i - 1, 0, i + 1]
                    self.border_arr[self.xsize + 1, i]= [1.0, self.xsize + 1, i + 1, self.xsize + 1, i - 1]

        self.border_arr = self.border_arr.astype(int)

        self.clear_between_mask()
        X, Y = give_line_arrays(self.border_arr)  # 1.5, 1.5)
        self.profiles.append([X, Y])
        self.nodelist = build_BVH(self.border_arr)

    def clear_between_mask(self):
        for i in range(self.right_area - self.left_area):
            for j in range(self.mask_height):
                delete_point(self.border_arr, i + self.left_area, j + self.border)
                self.counter_arr[:, i + self.left_area, j + self.border] = np.array([0, 0, 0, 0])
                self.is_full[i + self.left_area, j + self.border] = 0

    def make_half(self):
        if self.is_half:
            raise Exception("Не надо из уже половинки делать половинку (((((")
        self.is_half = True
        # print(self.border_arr.shape)
        # print("x,y sizes: ", self.xsize, self.ysize)
        curr_end_x = int(0.5 * (self.xsize))
        if self.xsize % 2 != 0:
            raise Exception("Не делится на 2 по горизонтали")
        unfound_end = True
        for i in range(self.ysize):
            # print(self.border_arr[curr_end_x, i, 0])
            if self.border_arr[curr_end_x, i, 0] == 1:
                if unfound_end:
                    curr_end_y = i
                    unfound_end = False
                else:
                    pass
                    #raise Exception("Два пересечения, очень плохо")
        if unfound_end:
            raise Exception("Не нашли пересечения!!!")
        end_x = curr_end_x
        end_y = curr_end_y
        # print(self.mask.shape)
        self.is_full = self.is_full[:curr_end_x + 1, :]
        self.border_arr = self.border_arr[:curr_end_x + 1, :, :]






        self.counter_arr = self.counter_arr[:, :curr_end_x + 1, :]
        self.mask = self.mask[:curr_end_x + 1, :]
        self.xsize = curr_end_x + 1

        # self.border_arr[end_x, end_y, 3:] = [-1, -1]
        #print(end_x)
        self.add_reflect_wall()
        #self.border_arr[end_x, end_y, 3:] = [end_x, 0]
        #self.border_arr[end_x, 0] = [1, end_x, end_y, -1, -1]

        X, Y = give_line_arrays(self.border_arr)  # 1.5, 1.5)
        self.profiles = [[X, Y]]
        self.check_correction()
        self.nodelist = build_BVH(self.border_arr)

    def return_half(self):
        # убираем конечную точку
        #end_x, _ = give_end(self.border_arr)
        #end_y = self.border_arr[end_x, 0, 2]
        #self.border_arr[end_x, end_y, 3:] = [-1, -1]
        #self.border_arr[end_x, 0] = [-1, -1, -1, -1, -1]
        self.remove_reflect_wall()


        if not self.is_half:
            raise Exception("Это не половинка, что бы её восстанавливать")
        self.is_half = False
        new_xsize = int(2.0 * self.xsize)

        end_x, end_y = give_end(self.border_arr)
        start_x, start_y = give_start(self.border_arr)
        self.is_full = np.concatenate((self.is_full[:-1], self.is_full[:-1][::-1, :]), axis=0)
        self.border_arr = np.concatenate((self.border_arr[:-1], self.border_arr[:-1][::-1, :, :]), axis=0)
        self.counter_arr = np.concatenate((self.counter_arr[:,:-1], self.counter_arr[:,:-1][:, ::-1, :]), axis=1)
        self.mask = np.concatenate((self.mask[:-1], self.mask[:-1][::-1, :]), axis=0)
        self.xsize = new_xsize

        curr_left_x = end_x
        curr_left_y = end_y
        curr_right_x = end_x + 1
        curr_right_y = end_y
        self.border_arr[end_x, end_y, 3:] = [curr_right_x, curr_right_y]
        self.border_arr[curr_right_x, curr_right_y, 1:3] = [end_x, end_y]
        while curr_left_x != start_x:

            next_left_x, next_left_y = self.border_arr[curr_left_x, curr_left_y, 1:3]
            next_right_y = next_left_y

            next_right_x = self.xsize - next_left_x + 1
            self.border_arr[curr_right_x, curr_right_y, 3:] = [next_right_x, next_right_y]
            self.border_arr[next_right_x, next_right_y, 1:3] = [curr_right_x, curr_right_y]
            curr_left_x, curr_left_y = next_left_x, next_left_y
            curr_right_x, curr_right_y = next_right_x, next_right_y
        if config.do_walls:
            self.border_arr[curr_right_x, curr_right_y, 3:] = [curr_right_x, curr_right_y - 1]
            for i in range(end_y - 1):
                if i == 0:
                    self.border_arr[self.xsize + 1, i] = [1.0, self.xsize + 1, i + 1, -1, -1]
                else:
                    self.border_arr[self.xsize + 1, i] = [1.0, self.xsize + 1, i + 1, self.xsize + 1, i - 1]
        else:
            self.border_arr[curr_right_x, curr_right_y, 3:] = [-1, -1]
        X, Y = give_line_arrays(self.border_arr)
        self.profiles = [[X, Y]]

        self.check_correction()

    def add_reflect_wall(self):
        if False:
            end_x, end_y = give_end(self.border_arr)
            #print(end_x)
            self.border_arr[end_x, end_y, 3:] = [end_x, 0]
            self.border_arr[end_x, 0] = [1, end_x, end_y, -1, -1]
        else:
            end_x, end_y = give_end(self.border_arr)
            #print(self.border_arr.shape, self.counter_arr.shape, self.is_full.shape, self.mask.shape)
            self.is_full = np.concatenate((self.is_full, np.ones((1,self.ysize))*(-1.0)), axis=0)
            self.counter_arr = np.concatenate(
                (self.counter_arr, np.zeros((self.counter_arr.shape[0], 1, self.counter_arr.shape[2]))), axis=1)
            self.border_arr = np.concatenate((self.border_arr, np.ones((1, self.ysize, 5)) * (-1.0)), axis=0)
            self.mask = np.concatenate((self.mask, self.mask[-1, :].reshape((1, self.mask.shape[1]))), axis=0)
            # print(self.border_arr.shape, self.counter_arr.shape, self.is_full.shape, self.mask.shape)
            self.border_arr[end_x, end_y, 3:] = [end_x + 1, end_y]
            self.border_arr[end_x + 1, end_y] = [1, end_x, end_y, end_x + 1, 0]
            self.border_arr[end_x + 1, 0] = [1, end_x + 1, end_y, -1, -1]

            self.is_full = self.is_full.astype(int)
            self.counter_arr = self.counter_arr.astype(int)
            self.border_arr = self.border_arr.astype(int)
            self.mask = self.mask.astype(int)

            self.xsize = self.xsize + 1

    def remove_reflect_wall(self):
        if False:
            end_x, _ = give_end(self.border_arr)
            end_y = self.border_arr[end_x, 0, 2]
            self.border_arr[end_x, end_y, 3:] = [-1, -1]
            self.border_arr[end_x, 0] = [-1, -1, -1, -1, -1]
        else:
            end_x = give_end(self.border_arr)[0]
            end_y = self.border_arr[end_x, 0, 2]
            end_x -= 1
            self.border_arr[end_x, end_y, 3:] = [-1, -1]

            self.border_arr = self.border_arr[:-1, :]
            self.counter_arr = self.counter_arr[:, :-1, :]
            self.mask = self.mask[:-1, :]
            self.is_full = self.is_full[:-1, :]

            self.xsize = self.xsize - 1

    def check_self_intersection(self, curr_x=None, curr_y=None, do_cut=False,range_cut=30):
        X, Y = give_line_arrays(self.border_arr)
        X, Y = prepare_segment_for_intersection_checking(X, Y, curr_x, curr_y, do_cut, range_cut)
        X = np.array(X)
        Y = np.array(Y)

        intersect = check_inter(X,Y)

        if intersect:
            print("Intersect!!!")
        return intersect

@njit()
def check_inter(cX, cY):
    intersect = False
    for i in range(len(cX) - 1):
        for j in range(len(cX) - 1):
            first_vec1, first_vec2 = [cX[i], cY[i]], [cX[i + 1], cY[i + 1]]
            second_vec1, second_vec2 = [cX[j], cY[j]], [cX[j + 1], cY[j + 1]]
            o1 = orientation(first_vec1, first_vec2, second_vec1)
            o2 = orientation(first_vec1, first_vec2, second_vec2)
            o3 = orientation(second_vec1, second_vec2, first_vec1)
            o4 = orientation(second_vec1, second_vec2, first_vec2)
            if o1 * o2 * o3 * o4 != 0 and (o1 != o2 and o3 != o4):
                intersect = True
    return intersect

@njit()
def orientation(p1, p2, p3):
    val = (p2[1] - p1[1])*(p3[0] - p2[0]) - (p2[0] - p1[0])*(p3[1] - p2[1])
    return np.sign(val)

def prepare_segment_for_intersection_checking(cX, cY, curr_x, curr_y, do_cut, range_cut):
    ind = 0
    while ind<len(cX)-2:
        p1, p2, p3 = [cX[ind], cY[ind]], [cX[ind + 1], cY[ind + 1]], [cX[ind + 2], cY[ind + 2]]
        dist1 = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        dist2 = np.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2)
        dist3 = np.sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2)
        if np.abs(dist3-(dist1+dist2))<10**(-5):
            cX.pop(ind + 1)
            cY.pop(ind + 1)
            #print("pop: ", ind+1)
        else:
            ind+=1
    return cX, cY
