import numpy as np
from res.const.geom_const import *
from res.geometry.count_functions import pnt2line
import matplotlib.path as mplPath


class Reactor:
    def __init__(self):
        delta_r = R_CON_DOWN - R_CON_UP * 1.0
        r_cent = R_LOC_INLET - R_CON_UP
        l = np.sqrt(delta_r ** 2 + H_CON ** 2)
        alpha = np.arctan((1.0 * H_CON) / delta_r)
        l1 = l - r_cent / np.cos(alpha) - R_INLET
        l2 = l - r_cent / np.cos(alpha) + R_INLET
        self.x1 = R_CON_DOWN - l1 * np.cos(alpha)
        self.x2 = R_CON_DOWN - l2 * np.cos(alpha)
        self.y1 = H_REACTOR + l1 * np.sin(alpha)
        self.y2 = H_REACTOR + l2 * np.sin(alpha)
        self.make_lines()

    def make_lines(self):

        self.lines = []
        # self.bounds = []
        self.boundsx = []
        self.boundsy = []
        self.boundsn = []
        self.outlet = Line([R_DN0, R_REACTOR], [0, 0])
        self.lines.append(self.outlet)

        self.lines.append(Line([R_REACTOR, R_REACTOR], [0, H_REACTOR]))
        self.boundsy.append(Line([R_REACTOR, R_REACTOR], [0, H_REACTOR]))

        self.lines.append(Line([R_REACTOR, R_CON_DOWN], [H_REACTOR, H_REACTOR]))
        self.boundsx.append(Line([R_REACTOR, R_CON_DOWN], [H_REACTOR, H_REACTOR]))

        self.lines.append(Line([R_CON_DOWN, self.x1], [H_REACTOR, self.y1]))
        self.boundsn.append(Line([R_CON_DOWN, self.x1], [H_REACTOR, self.y1]))

        self.lines.append(Line([self.x1, self.x2], [self.y1, self.y2]))
        self.inlet = Line([self.x1, self.x2], [self.y1, self.y2])

        self.lines.append(Line([self.x2, R_CON_UP], [self.y2, H_REACTOR + H_CON]))
        self.boundsn.append(Line([self.x2, R_CON_UP], [self.y2, H_REACTOR + H_CON]))

        self.lines.append(Line([R_CON_UP, 0], [H_REACTOR + H_CON, H_REACTOR + H_CON]))
        self.boundsx.append(Line([R_CON_UP, 0], [H_REACTOR + H_CON, H_REACTOR + H_CON]))

        self.lines.append(Line([0, 0], [H_REACTOR + H_CON, H_DNO + H_WAFER]))
        self.boundsy.append(Line([0, 0], [H_REACTOR + H_CON, H_DNO + H_WAFER]))

        self.lines.append(Line([0, R_WAFER], [H_DNO + H_WAFER, H_DNO + H_WAFER]))
        self.boundsx.append(Line([0, R_WAFER], [H_DNO + H_WAFER, H_DNO + H_WAFER]))

        self.lines.append(Line([R_WAFER, R_WAFER], [H_DNO + H_WAFER, H_DNO]))
        self.boundsy.append(Line([R_WAFER, R_WAFER], [H_DNO + H_WAFER, H_DNO]))

        self.lines.append(Line([R_WAFER, R_DN0], [H_DNO, H_DNO]))
        self.boundsx.append(Line([R_WAFER, R_DN0], [H_DNO, H_DNO]))

        self.lines.append(Line([R_DN0, R_DN0], [H_DNO, 0]))
        self.boundsy.append(Line([R_DN0, R_DN0], [H_DNO, 0]))

        points = []
        for line in self.lines:
            points.append([line.x1, line.y1])
        points = np.array(points)
        self.path = mplPath.Path(points)

    def generate_points(self):
        pass

    def give_axis_bounds(self):
        gl_min, gl_max = np.array([0, 0]).reshape(2, 1), np.array([R_REACTOR, H_REACTOR + H_CON]).reshape(2, 1)
        mid_coord = 0.5 * (gl_max + gl_min)
        delta = 0.51 * (gl_max - gl_min)
        min_coord = mid_coord - delta
        max_coord = mid_coord + delta
        return min_coord, max_coord

    def draw(self, axis, colors=None):
        for bound in self.boundsx:
            bound.draw(axis, "k")
        for bound in self.boundsy:
            bound.draw(axis, "k")
        for bound in self.boundsn:
            bound.draw(axis, "k")
        self.inlet.draw(axis, "r")
        self.outlet.draw(axis, "b")
        if colors is None:
            for i in range(len(self.is_inside)):
                if self.is_inlet[i]:
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color="r")
                elif self.is_outlet[i]:
                    pass
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color="b")
                elif self.is_x_walls[i]:
                    pass
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color=(0.3, 0.7, 0.5))
                elif self.is_y_walls[i]:
                    pass
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color=(0.7, 0.3, 0.5))
                elif self.is_inl_walls[i]:
                    pass
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color=(0.3, 0.3, 0.3))
                elif self.is_inside[i]:
                    pass
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color="g")
        else:
            max_color = np.max(colors)
            min_color = np.max(colors)
            print(max_color)
            print(min_color)
            for i in range(len(self.is_inside)):
                alpha = (colors[i]-min_color)/(max_color-min_color)
                if self.is_inside[i]:
                    axis.plot(self.coords[0, i], self.coords[1, i], ".", color=(alpha, 1.0-alpha, 0))



        min_coord, max_coord = self.give_axis_bounds()
        axis.set_xlim(min_coord[0, 0], max_coord[0, 0])
        axis.set_ylim(min_coord[1, 0], max_coord[1, 0])

    def is_points_inside(self, coords, delta_x, delta_y):
        ans = self.path.contains_points(coords.T)
        is_inlet = self.inlet.is_boundary(coords, delta_x, delta_y, is_inlet=True)
        is_inlet = (is_inlet.astype(int) * ans.astype(int)).astype(bool)
        is_outlet = self.outlet.is_boundary(coords, delta_x, delta_y)
        is_outlet = (is_outlet.astype(int) * ans.astype(int)).astype(bool)
        is_boundary_x = None
        for line in self.boundsx:
            curr_bounds = line.is_boundary(coords, delta_x, delta_y)
            if is_boundary_x is None:
                is_boundary_x = curr_bounds
            else:
                is_boundary_x = is_boundary_x + curr_bounds
        is_boundary_x = (is_boundary_x.astype(int) * ans.astype(int)).astype(bool)

        is_boundary_y = None
        for line in self.boundsy:
            curr_bounds = line.is_boundary(coords, delta_x, delta_y)
            if is_boundary_y is None:
                is_boundary_y = curr_bounds
            else:
                is_boundary_y = is_boundary_y + curr_bounds
        is_boundary_y = (is_boundary_y.astype(int) * ans.astype(int)).astype(bool)

        is_boundary_n = None
        for line in self.boundsn:
            curr_bounds = line.is_boundary(coords, delta_x, delta_y, is_inlet=True)
            if is_boundary_n is None:
                is_boundary_n = curr_bounds
            else:
                is_boundary_n = is_boundary_n + curr_bounds
        is_boundary_n = (is_boundary_n.astype(int) * ans.astype(int)).astype(bool)
        is_boundary_x = (is_boundary_x.astype(int) - is_boundary_x.astype(int) * is_boundary_n.astype(int)).astype(bool)
        is_outlet = (is_outlet.astype(int) - is_outlet.astype(int) * is_boundary_y.astype(int)).astype(bool)

        self.is_inside = ans
        self.is_inlet = is_inlet
        self.is_outlet = is_outlet
        self.is_x_walls = is_boundary_x
        self.is_y_walls = is_boundary_y
        self.is_inl_walls = is_boundary_n
        self.coords = coords
        return ans, is_inlet, is_outlet, (is_boundary_x, is_boundary_y, is_boundary_n)

class TestReactor:
    def __init__(self):
        self.make_lines()

    def make_lines(self):
        self.lines = []
        self.boundsx = []
        self.boundsy = []

        self.lines.append(Line([0, 0], [0, (0.5 - 0.5 * ALPHA_OUT) * TEST_H]))
        self.boundsy.append(Line([0, 0], [0, (0.5 - 0.5 * ALPHA_OUT) * TEST_H]))

        self.outlet = Line([0, 0], [(0.5 - 0.5 * ALPHA_OUT) * TEST_H, (0.5 + 0.5 * ALPHA_OUT) * TEST_H])
        self.lines.append(self.outlet)

        self.lines.append(Line([0, 0], [(0.5 + 0.5 * ALPHA_OUT) * TEST_H, TEST_H]))
        self.boundsy.append(Line([0, 0], [(0.5 + 0.5 * ALPHA_OUT) * TEST_H, TEST_H]))

        self.lines.append(Line([0, TEST_W], [TEST_H, TEST_H]))
        self.boundsx.append(Line([0, TEST_W], [TEST_H, TEST_H]))

        self.lines.append(Line([TEST_W, TEST_W], [TEST_H, (0.5 + 0.5 * ALPHA_IN) * TEST_H]))
        self.boundsy.append(Line([TEST_W, TEST_W], [TEST_H, (0.5 + 0.5 * ALPHA_IN) * TEST_H]))

        self.inlet = Line([TEST_W, TEST_W], [(0.5 - 0.5 * ALPHA_IN) * TEST_H, (0.5 + 0.5 * ALPHA_IN) * TEST_H])
        self.lines.append(self.inlet)

        self.lines.append(Line([TEST_W, TEST_W], [(0.5 - 0.5 * ALPHA_IN) * TEST_H, 0]))
        self.boundsy.append(Line([TEST_W, TEST_W], [(0.5 - 0.5 * ALPHA_IN) * TEST_H, 0]))

        self.lines.append(Line([TEST_W, 0], [0, 0]))
        self.boundsx.append(Line([TEST_W, 0], [0, 0]))

        points = []
        for line in self.lines:
            points.append([line.x1, line.y1])
        points = np.array(points)
        self.path = mplPath.Path(points)

    def give_axis_bounds(self):
        gl_min, gl_max = np.array([0, 0]).reshape(2, 1), np.array([TEST_W, TEST_H]).reshape(2, 1)
        mid_coord = 0.5 * (gl_max + gl_min)
        delta = 0.51 * (gl_max - gl_min)
        min_coord = mid_coord - delta
        max_coord = mid_coord + delta
        return min_coord, max_coord

    def draw(self, axis, vx, vy=None):
        for bound in self.boundsx:
            bound.draw(axis, "k")
        for bound in self.boundsy:
            bound.draw(axis, "k")
        self.inlet.draw(axis, "r")
        self.outlet.draw(axis, "b")
        if vy is None:
            print("dfdfdfdfdf")
            color = vx
            max_col = np.max(color)
            min_col = np.min(color)
            print(max_col,min_col)
            for i in range(len(self.is_inside)):
                #alpha = 1-np.log(1+(np.e-1)*(color[i]-min_col)/(max_col-min_col))
                alpha = 1-(color[i] - min_col) / (max_col - min_col)
                if self.is_inside[i]:
                    axis.plot(self.coords[0, i], self.coords[1, i], ".",color=(alpha,alpha, alpha))
        else:
            max_vx = np.max(np.abs(vx))
            max_vy = np.max(np.abs(vy))
            print(max_vx,max_vy)
            if max_vx==0:
                max_vx = 1
                if max_vy == 0:
                    max_vy = 1
                    max_div = 1
                else:
                    max_div = max_vy
            else:
                if max_vy == 0:
                    max_vy = 1
                    max_div = max_vx
                else:
                    max_div = np.sqrt(max_vy**2+max_vx**2)


            for i in range(len(self.is_inside)):
                alpha = 1 - np.sqrt((vx[i]**2+vy[i]**2)/(max_div**2))
                if self.is_inside[i]:
                    axis.arrow(self.coords[0, i], self.coords[1, i],0.01*vx[i]/max_vx,0.01*vy[i]/max_vy, color=(alpha, alpha, alpha))
                    #axis.plot(self.coords[0, i], self.coords[1, i], ".", color=(alpha, alpha, alpha))

    def is_points_inside(self, coords, delta_x, delta_y):
        ans = self.path.contains_points(coords.T)
        is_inlet = self.inlet.is_boundary(coords, delta_x, delta_y, is_inlet=False)
        is_inlet = (is_inlet.astype(int) * ans.astype(int)).astype(bool)
        is_outlet = self.outlet.is_boundary(coords, delta_x, delta_y)
        is_outlet = (is_outlet.astype(int) * ans.astype(int)).astype(bool)
        is_boundary_x = None
        for line in self.boundsx:
            curr_bounds = line.is_boundary(coords, delta_x, delta_y)
            if is_boundary_x is None:
                is_boundary_x = curr_bounds
            else:
                is_boundary_x = is_boundary_x + curr_bounds
        is_boundary_x = (is_boundary_x.astype(int) * ans.astype(int)).astype(bool)

        is_boundary_y = None
        for line in self.boundsy:
            curr_bounds = line.is_boundary(coords, delta_x, delta_y)
            if is_boundary_y is None:
                is_boundary_y = curr_bounds
            else:
                is_boundary_y = is_boundary_y + curr_bounds
        is_boundary_y = (is_boundary_y.astype(int) * ans.astype(int)).astype(bool)

        is_outlet = (is_outlet.astype(int) - is_outlet.astype(int) * is_boundary_y.astype(int)).astype(bool)
        is_inlet = (is_inlet.astype(int) - is_inlet.astype(int) * is_boundary_y.astype(int)).astype(bool)

        self.is_inside = ans
        self.is_inlet = is_inlet
        self.is_outlet = is_outlet
        self.is_x_walls = is_boundary_x
        self.is_y_walls = is_boundary_y
        self.coords = coords
        return ans, is_inlet, is_outlet, (is_boundary_x, is_boundary_y)


class Line:
    def __init__(self, x, y):
        self.x1 = x[0]
        self.x2 = x[1]
        # print(x,y)
        self.y1 = y[0]
        self.y2 = y[1]

    def draw(self, axis, color):
        axis.plot([self.x1, self.x2], [self.y1, self.y2], color=color)

    def is_boundary(self, coords, delta_x, delta_y, is_inlet=False):
        if is_inlet:
            def func(x, y):
                new_x = (x - self.x1) * np.cos(ALPHA) - (y - self.y1) * np.sin(ALPHA)
                new_y = (y - self.y1) * np.cos(ALPHA) + (x - self.x1) * np.sin(ALPHA)
                new_x2 = (self.x2 - self.x1) * np.cos(ALPHA) - (self.y2 - self.y1) * np.sin(ALPHA)
                if (new_x * (new_x2 - new_x) > 0):
                    if new_y ** 2 < (delta_x * np.sin(ALPHA)) ** 2:
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            def func(x, y):
                dist, nearest = pnt2line((x, y), (self.x1, self.y1), (self.x2, self.y2))
                dx = np.abs(nearest[0] - x)
                dy = np.abs(nearest[1] - y)
                if (dist ** 2 > 1 * (delta_x ** 2 + delta_y ** 2)):
                    return False
                else:
                    if dx <= 1 * delta_x and dy <= 1 * delta_y:
                        return True
                    else:
                        return False

        f = np.vectorize(func)
        return f(coords[0], coords[1])
