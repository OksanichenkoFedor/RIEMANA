import numpy as np
from res.const.geom_const import *

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
        self.bounds = []
        self.outlet = Line([R_DN0, R_REACTOR], [0, 0])
        self.lines.append(self.outlet)

        self.lines.append(Line([R_REACTOR, R_REACTOR], [0, H_REACTOR]))
        self.bounds.append(Line([R_REACTOR, R_REACTOR], [0, H_REACTOR]))

        self.lines.append(Line([R_REACTOR, R_CON_DOWN], [H_REACTOR, H_REACTOR]))
        self.bounds.append(Line([R_REACTOR, R_CON_DOWN], [H_REACTOR, H_REACTOR]))

        self.lines.append(Line([R_CON_DOWN,self.x1],[H_REACTOR,self.y1]))
        self.bounds.append(Line([R_CON_DOWN,self.x1],[H_REACTOR,self.y1]))

        self.lines.append(Line([self.x1, self.x2], [self.y1, self.y2]))
        self.inlet = Line([self.x1, self.x2], [self.y1, self.y2])

        self.lines.append(Line([self.x2, R_CON_UP], [self.y2, H_REACTOR+H_CON]))
        self.bounds.append(Line([self.x2, R_CON_UP], [self.y2, H_REACTOR+H_CON]))

        self.lines.append(Line([R_CON_UP,0],[H_REACTOR+H_CON,H_REACTOR+H_CON]))
        self.bounds.append(Line([R_CON_UP,0],[H_REACTOR+H_CON,H_REACTOR+H_CON]))

        self.lines.append(Line([0, 0], [H_REACTOR+H_CON, H_DNO+H_WAFER]))
        self.bounds.append(Line([0, 0], [H_REACTOR+H_CON, H_DNO+H_WAFER]))

        self.lines.append(Line([0,R_WAFER],[H_DNO+H_WAFER,H_DNO+H_WAFER]))
        self.bounds.append(Line([0,R_WAFER],[H_DNO+H_WAFER,H_DNO+H_WAFER]))

        self.lines.append(Line([R_WAFER,R_WAFER],[H_DNO+H_WAFER,H_DNO]))
        self.bounds.append(Line([R_WAFER,R_WAFER],[H_DNO+H_WAFER,H_DNO]))

        self.lines.append(Line([R_WAFER,R_DN0],[H_DNO, H_DNO]))
        self.bounds.append(Line([R_WAFER,R_DN0],[H_DNO, H_DNO]))

        self.lines.append(Line([R_DN0, R_DN0], [H_DNO, 0]))
        self.bounds.append(Line([R_DN0, R_DN0], [H_DNO, 0]))

        points = []
        for line in self.lines:
            points.append([line.x1,line.y1])
        points = np.array(points)
        print(points.shape)
        self.path = mplPath.Path(points)






    def generate_points(self):
        pass

    def draw(self, axis):
        for bound in self.bounds:
            bound.draw(axis,"k")
        self.inlet.draw(axis,"r")
        self.outlet.draw(axis,"b")
        gl_min, gl_max = np.array([0, 0]).reshape(2, 1), np.array([R_REACTOR, H_REACTOR + H_CON]).reshape(2, 1)
        mid_coord = 0.5 * (gl_max + gl_min)
        delta = 0.55 * np.max(gl_max - gl_min)
        min_coord = mid_coord - delta
        max_coord = mid_coord + delta
        axis.set_xlim(min_coord[0, 0], max_coord[0, 0])
        axis.set_ylim(min_coord[1, 0], max_coord[1, 0])
        return min_coord, max_coord
        #return gl_min,gl_max

    def is_points_inside(self, coords, include_bounds=True):
        return self.path.contains_points(coords.T)

class Line:
    def __init__(self,x,y):
        self.x1 = x[0]
        self.x2 = x[1]
        self.y1 = y[0]
        self.y2 = y[1]

    def draw(self,axis,color):
        axis.plot([self.x1,self.x2],[self.y1,self.y2],color=color)

