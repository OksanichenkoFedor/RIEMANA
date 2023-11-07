import numpy as np
from matplotlib.patches import Circle as CirclePlot
from matplotlib.patches import Polygon

from res.parser.entities.entity import Entity
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.parser.entities.auxiliary import Axis2Placement3D, VertexPoint, Curve, Edge
from res.parser.entities.basic import CartesianPoint


class Circle(Curve):
    def __init__(self, id, params, data):
        super(Circle, self).__init__(id)
        params = params.split(",")
        self.placement = data[int(params[0])]
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))
        self.R = float(params[1])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)

    def draw(self, axis):
        self.circ = CirclePlot((0, 0), self.R)
        axis.add_patch(self.circ)
        pathpatch_2d_to_3d(self.circ, centre_vector=self.start_coord, normal=self.z)
        delta = np.array([0, 0, 0])
        delta[0] = self.R * np.linalg.norm(np.cross(self.z, np.array([1.0, 0.0, 0.0])))
        delta[1] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 1.0, 0.0])))
        delta[2] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 0.0, 1.0])))
        return (self.start_coord - delta).reshape((3, 1)), (self.start_coord + delta).reshape((3, 1))


class EntityEdge(Edge):

    def __init__(self, id, params, data):
        super(EntityEdge, self).__init__(id)
        params = params.split(",")
        self.start = data[int(params[0])]
        self.end = data[int(params[1])]
        self.curve = data[int(params[2])]
        if params[-1][1] == "T":
            self.orientation = 1
        elif params[-1][1] == "F":
            self.orientation = -1
        else:
            raise ValueError('Incorrect orientation: ', type(self.start))
        if type(self.start) != VertexPoint:
            raise ValueError('Expected VertexPoint, got ', type(self.start))
        if type(self.end) != VertexPoint:
            raise ValueError('Expected VertexPoint, got ', type(self.end))
        if issubclass(Curve, type(self.curve)):
            raise ValueError('Expected Curve, got ', type(self.curve))
        self.start_coord = self.start.coord
        self.end_coord = self.end.coord


class BSplineCurveWithKnots(Curve):
    def __init__(self, id, params, data):
        super(BSplineCurveWithKnots, self).__init__(id)
        self.extract_data(params, data)
        self.check_data()

    def extract_data(self, line, data):
        ind1 = line.find("(")
        ind2 = line.find(")")
        self.control_points_list = list(np.array(line[ind1 + 1:ind2].split(",")).astype("int"))
        line = line[:ind1 - 1] + line[ind2 + 1:]

        ind1 = line.find("(")
        ind2 = line.find(")")
        self.knot_multiplicities = list(np.array(line[ind1 + 1:ind2].split(",")).astype("int"))
        line = line[:ind1 - 1] + line[ind2 + 1:]

        ind1 = line.find("(")
        ind2 = line.find(")")
        self.knots = list(np.array(line[ind1 + 1:ind2].split(",")).astype("float"))
        line = (line[:ind1 - 1] + line[ind2 + 1:]).replace(" ", "")

        self.end_of_line = line

        self.N = len(self.control_points_list)

        self.points = []
        self.coords = []
        for i in range(self.N):
            self.points.append(data[self.control_points_list[i]])
            self.coords.append(self.points[-1].coord)
        print(self.control_points_list)
        print(self.knots)
        print(self.knot_multiplicities)
        coords = np.array(self.coords)
        print(coords.shape)
        print(np.min(coords, axis=0).shape)
        print("---")

    def check_data(self):
        if len(self.knot_multiplicities) != self.N - 2:
            raise ValueError('Incorrect shape of knot_multiplicities, expected ', self.N - 2, " got ",
                             len(self.knot_multiplicities))
        if len(self.knots) != self.N - 2:
            raise ValueError('Incorrect shape of knots, expected ', self.N - 2, " got ",
                             len(self.knots))

        if self.end_of_line != "3,.UNSPECIFIED.,.F.,.F.,.UNSPECIFIED.":
            raise ValueError('Unexpected extra parameters: ', self.end_of_line)

        for i in range(self.N):
            if type(self.points[i]) != CartesianPoint:
                raise ValueError('Expected CartesianPoint, got ', type(self.points[i]))

    def draw(self, axis):
        coords = np.array(self.coords)
        print(coords[:-1, 0])
        axis.plot(list(coords[:-1, 0]) + list(coords[1:, 0]),
                  list(coords[:-1, 1]) + list(coords[1:, 1]),
                  list(coords[:-1, 2]) + list(coords[1:, 2]),
                  color="r")
        return (np.min(coords, axis=0)).reshape((3, 1)), (np.max(coords, axis=0)).reshape((3, 1))
