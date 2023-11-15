import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt

from res.parser.entities.ancestors import Entity, Curve, Edge, Surface
from res.parser.entities.basic import CartesianPoint, Direction


class Axis2Placement3D(Entity):

    def extract_data(self, params, data):
        params = params.split(",")
        self.point = data[int(params[0])]
        self.axis1 = data[int(params[1])]
        self.axis2 = data[int(params[2])]

    def check_data(self):
        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        if type(self.axis1) != Direction:
            raise ValueError('Expected Direction, got ', type(self.axis1))
        if type(self.axis2) != Direction:
            raise ValueError('Expected Direction, got ', type(self.axis2))

    def check_orthgonality(self):
        dot = self.axis1.x * self.axis2.x + self.axis1.y * self.axis2.y + self.axis1.z * self.axis2.z
        if dot > 0.01:
            print("Not orthogonal: ", dot)


class Plane(Surface):

    def extract_data(self, params, data):
        self.placement = data[int(params)]

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)


class Vector(Entity):

    def extract_data(self, params, data):
        params = params.split(",")
        self.direction = data[int(params[0])]
        self.length = float(params[1])

    def check_data(self):
        if type(self.direction) != Direction:
            raise ValueError('Expected Direction, got ', type(self.direction))
        self.vec_coord = self.direction.vector


class Line(Curve):

    def extract_data(self, params, data):
        params = params.split(",")
        self.point = data[int(params[0])]
        self.vector = data[int(params[1])]

    def check_data(self):
        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        if type(self.vector) != Vector:
            raise ValueError('Expected Direction, got ', type(self.vector))
        self.start_coord = self.point.coord
        self.vec_coord = self.vector.vec_coord

    def generate_draw_function(self, start_point, end_point):
        #id_1 = start_point.id
        #id_2 = end_point.id
        x = [start_point.coord[0], end_point.coord[0]]
        y = [start_point.coord[1], end_point.coord[1]]
        z = [start_point.coord[2], end_point.coord[2]]
        coords = self.give_coords(10, start_point.coord, end_point.coord, True)
        #print(coords.T)

        def draw_function(axis, color, is_plotting):
            if color is None:
                color = "g"
            if is_plotting:
                axis.plot(x, y, z, color=color)

            if is_plotting:
                pass
                #for i in range(coords.shape[1] - 1):
                #    axis.plot([coords[0, i], coords[0, i + 1]],
                #              [coords[1, i], coords[1, i + 1]],
                #              [coords[2, i], coords[2, i + 1]], color="k")
                #xyz = coords.T
                #xyz = xyz.reshape(-1, 1, 3)
                #segments = np.hstack([xyz[:-1], xyz[1:]])
                #colors = np.arange(0, 1, 1 / xyz.shape[0])
                #coll = Line3DCollection(segments, cmap=plt.cm.plasma)
                #coll.set_array(colors)
                #axis.add_collection(coll)


            return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), np.array(
                [np.max(x), np.max(y), np.max(z)]).reshape((3, 1))



        return draw_function

    def give_coords(self, number_points, start_coord, end_coord, orientation):
        print("Ориентация необработана у прямой")
        if np.max(np.abs(np.cross(start_coord-self.start_coord, self.vec_coord)))>0.001:
            print("Ахтунг!!!")
        if np.max(np.abs(np.cross(end_coord-self.start_coord, self.vec_coord)))>0.001:
            print("Ахтунг!!!")
        start_coord = start_coord.reshape((3, 1)).repeat(number_points, axis=1)
        end_coord = end_coord.reshape((3, 1)).repeat(number_points, axis=1)
        mult = np.arange(0, 1, 1 / number_points).reshape((1, number_points)).repeat(3, axis=0)
        #print("give_coords, line: ", number_points, start_coord.shape, end_coord.shape, mult.shape)
        coords = start_coord + (end_coord - start_coord) * mult
        if bool(orientation)==False:
            print("FFFFFFFFFFFFFF", coords.shape)
            coords = coords[:,::-1]
        return coords


class VertexPoint(Entity):

    def extract_data(self, params, data):
        self.point = data[int(params)]

    def check_data(self):
        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        self.coord = self.point.coord


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
