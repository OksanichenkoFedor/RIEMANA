import numpy as np

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
        id_1 = start_point.id
        id_2 = end_point.id
        x = [start_point.coord[0], end_point.coord[0]]
        y = [start_point.coord[1], end_point.coord[1]]
        z = [start_point.coord[2], end_point.coord[2]]
        def draw_function(axis, color, is_plotting):
            if color is None:
                color="g"
            if is_plotting:
                axis.plot(x, y, z, color=color)
            return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), np.array(
                [np.max(x), np.max(y), np.max(z)]).reshape((3, 1))
        return draw_function


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
            self.orientation = 1
        elif params[-1][1] == "F":
            self.orientation = -1
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


