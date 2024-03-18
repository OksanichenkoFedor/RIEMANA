import numpy as np

from res.step.parser.entities.ancestors import Entity, Edge, Drawable, Curve
from res.step.parser.entities.auxiliary import VertexPoint

from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt

import res.config.step as config


class EdgeCurve(Edge):

    def extract_data(self, params, data):
        params = params.split(",")
        # print("EgdeCurve: ",params)
        self.start = data[int(params[0])]
        self.end = data[int(params[1])]
        self.curve = data[int(params[2])]
        if params[-1][1] == "T":
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', type(self.start))

    def check_data(self):
        if type(self.start) != VertexPoint:
            raise ValueError('Expected VertexPoint, got ', type(self.start))
        if type(self.end) != VertexPoint:
            raise ValueError('Expected VertexPoint, got ', type(self.end))
        if not isinstance(self.curve, Curve):
            raise ValueError('Expected Curve, got ', type(self.curve))
        self.start_coord = self.start.coord
        self.end_coord = self.end.coord

    def generate_draw_function(self, start_point=None, end_point=None):
        if start_point is None:
            start_point = self.start
        if end_point is None:
            end_point = self.end
        return self.curve.generate_draw_function(start_point, end_point)

    def give_coords(self, number_points, orientation):
        return self.curve.give_coords(number_points, self.start_coord, self.end_coord, orientation)


class OrientedEdge(Edge, Drawable):

    def __init__(self, id, params, data):
        super(OrientedEdge, self).__init__(id, params, data)
        self.generate_draw_function()

    def extract_data(self, params, data):
        params = params.split(",")
        self.edge = data[int(params[2])]
        if params[0] != "*" or params[1] != "*":
            raise ValueError('Strange OrientedEdge ', self.id)
        if params[-1][1] == "T":
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        # print("OrientedEdge: ", params)

    def check_data(self):
        if not isinstance(self.edge, EdgeCurve):
            raise ValueError('Expected EdgeCurve, got ', type(self.edge))
        self.start_coord = self.edge.start_coord
        self.end_coord = self.edge.end_coord

    def generate_draw_function(self):
        self.draw = self.edge.generate_draw_function()

    def draw(self, axis, color, is_plotting):
        pass

    def give_coords(self, number_points, orientation=None):
        return self.edge.give_coords(number_points, bool(self.orientation))


class EdgeLoop(Entity, Drawable):

    def extract_data(self, params, data):
        params = np.array(params[1:-1].split(",")).astype("int")
        self.oriented_edges = []
        for i in range(len(params)):
            new_edge = data[params[i]]
            self.oriented_edges.append(new_edge)
        self.color = tuple(np.random.random(3))
        self.give_coords(config.elem_on_edge, True)

    def check_data(self):
        for edge in self.oriented_edges:
            if not isinstance(edge, OrientedEdge):
                raise ValueError('Expected OrientedEdge, got ', type(edge))

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "r"
        if is_plotting:
            axis.add_collection(self.coll)
        return self.min, self.max

    def give_coords(self, num_points, orientation):
        self.coords = None
        for i in range(len(self.oriented_edges)):
            curr_coords = self.oriented_edges[i].give_coords(num_points, orientation)
            if curr_coords is None:
                pass
            else:
                if self.coords is None:
                    self.coords = curr_coords
                else:
                    pass
                    self.coords = np.concatenate((self.coords, curr_coords), axis=1)
        xyz = self.coords.T
        xyz = xyz.reshape(-1, 1, 3)
        segments = np.hstack([xyz[:-1], xyz[1:]])
        colors = np.arange(0, 1, 1 / xyz.shape[0])
        self.coll = Line3DCollection(segments, cmap=plt.cm.plasma)
        self.coll.set_array(colors)
        self.min = (np.min(self.coords, axis=1)).reshape((3, 1))
        self.max = (np.max(self.coords, axis=1)).reshape((3, 1))
        return self.coords
