import numpy as np

from matplotlib.patches import Circle as CirclePlot
from matplotlib.patches import Polygon, Arc

from res.parser.entities.ancestors import Curve, Edge, Drawable, Entity, Surface
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.parser.entities.auxiliary import Axis2Placement3D, EdgeCurve
from res.parser.entities.basic import CartesianPoint


class Circle(Curve, Drawable):

    def extract_data(self, params, data):
        params = params.split(",")
        self.placement = data[int(params[0])]
        self.R = float(params[1])

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "g"
        if is_plotting:
            self.circ = CirclePlot((0, 0), self.R, color=color, fill=True)
            axis.add_patch(self.circ)
            pathpatch_2d_to_3d(self.circ, centre_vector=self.start_coord, normal=self.z)
        delta = np.array([0, 0, 0])
        delta[0] = self.R * np.linalg.norm(np.cross(self.z, np.array([1.0, 0.0, 0.0])))
        delta[1] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 1.0, 0.0])))
        delta[2] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 0.0, 1.0])))
        return (self.start_coord - delta).reshape((3, 1)), (self.start_coord + delta).reshape((3, 1))

    def generate_draw_function(self, start_point, end_point):
        start_coord = start_point.coord - self.start_coord
        end_coord = end_point.coord - self.start_coord
        start_x, start_y, start_z = np.dot(start_coord, self.x), np.dot(start_coord, self.y), np.dot(start_coord,
                                                                                                     self.z)
        end_x, end_y, end_z = np.dot(end_coord, self.x), np.dot(end_coord, self.y), np.dot(end_coord, self.z)
        if np.abs(start_z) > 0.01:
            raise ValueError('Point out of circle, id: ', type(start_point.id))
        if np.abs(end_z) > 0.01:
            raise ValueError('Point out of circle, id: ', type(end_point.id))
        start_angle = give_angle(start_x, start_y, self.R)
        end_angle = give_angle(end_x, end_y, self.R)
        delta = np.array([0, 0, 0])
        delta[0] = self.R * np.linalg.norm(np.cross(self.z, np.array([1.0, 0.0, 0.0])))
        delta[1] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 1.0, 0.0])))
        delta[2] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 0.0, 1.0])))

        def draw_function(axis, color, is_plotting):
            if color is None:
                color = "b"
            if is_plotting:
                arc = Arc((0, 0), width=2 * self.R, height=2 * self.R, theta1=start_angle, theta2=end_angle,
                          color=color)
                axis.add_patch(arc)
                pathpatch_2d_to_3d(arc, centre_vector=self.start_coord, normal=self.z)
            return (self.start_coord - delta).reshape((3, 1)), (self.start_coord + delta).reshape((3, 1))

        return draw_function


def give_angle(x, y, r):
    cos = x / r
    sin = y / r

    if cos >= 0 and sin >= 0:
        return np.arcsin(sin)
    elif cos >= 0 and sin < 0:
        return 2 * np.pi - np.arcsin((-1) * sin)
    elif cos < 0 and sin >= 0:
        return np.pi - np.arcsin(sin)
    elif cos < 0 and sin < 0:
        return np.pi + np.arcsin((-1) * sin)
    else:
        print("Aхтунг!!!")


class BSplineCurveWithKnots(Curve, Drawable):

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

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "r"
        coords = np.array(self.coords)
        if is_plotting:
            axis.plot(list(coords[:-1, 0]) + list(coords[1:, 0]),
                      list(coords[:-1, 1]) + list(coords[1:, 1]),
                      list(coords[:-1, 2]) + list(coords[1:, 2]),
                      color=color)
        return (np.min(coords, axis=0)).reshape((3, 1)), (np.max(coords, axis=0)).reshape((3, 1))

    def generate_draw_function(self, start_point, end_point):
        coords = np.array(self.coords)
        C = coords - start_point.coord
        C = np.sum(C * C, axis=1)
        start_second, start_first = np.argsort(C)[-2:]
        start_second, start_first = np.max((start_second, start_first)), np.min((start_second, start_first))
        if np.abs(start_first - start_second) > 1:
            raise ValueError('Not near points in OrientedEdge, id: ', start_point.id)
        C = coords - end_point.coord
        C = np.sum(C * C, axis=1)
        end_second, end_first = np.argsort(C)[-2:]
        end_second, end_first = np.max((end_second, end_first)), np.min((end_second, end_first))
        if np.abs(end_first - end_second) > 1:
            raise ValueError('Not near points in OrientedEdge, id: ', end_point.id)
        if end_first > start_second:
            coords = coords[start_first:end_second, :]
            coords[0] = start_point.coord
            coords[-1] = end_point.coord

            def draw_function(axis, color, is_plotting):
                if color is None:
                    color = (0.3, 0, 0.7)
                if is_plotting:
                    axis.plot(list(coords[:-1, 0]) + list(coords[1:, 0]),
                              list(coords[:-1, 1]) + list(coords[1:, 1]),
                              list(coords[:-1, 2]) + list(coords[1:, 2]),
                              color=color)
                return (np.min(coords, axis=0)).reshape((3, 1)), (np.max(coords, axis=0)).reshape((3, 1))

            return draw_function

        else:
            coords = coords[end_first:start_second, :]
            coords[0] = end_point.coord
            coords[-1] = start_point.coord
            coords = coords[::-1, :]

            def draw_function(axis, color, is_plotting):
                if color is None:
                    color = (0.7, 0, 0.3)
                if is_plotting:
                    axis.plot(list(coords[:-1, 0]) + list(coords[1:, 0]),
                              list(coords[:-1, 1]) + list(coords[1:, 1]),
                              list(coords[:-1, 2]) + list(coords[1:, 2]),
                              color=color)
                return np.array([0, 0, 0]).reshape(3, 1), np.array([0, 0, 0]).reshape(3, 1)

            return draw_function


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
            self.orientation = 1
        elif params[-1][1] == "F":
            self.orientation = -1
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


class EdgeLoop(Entity, Drawable):

    def extract_data(self, params, data):
        params = np.array(params[1:-1].split(",")).astype("int")
        self.oriented_edges = []
        for i in range(len(params)):
            new_edge = data[params[i]]
            self.oriented_edges.append(new_edge)
        self.color = tuple(np.random.random(3))

    def check_data(self):
        for edge in self.oriented_edges:
            if not isinstance(edge, OrientedEdge):
                raise ValueError('Expected OrientedEdge, got ', type(edge))

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = self.color
        min_coord = np.array([0, 0, 0]).reshape(3, 1)
        max_coord = np.array([0, 0, 0]).reshape(3, 1)
        for edge in self.oriented_edges:
            curr_min, curr_max = edge.draw(axis, color, is_plotting)
            new_min = np.concatenate((min_coord, curr_min), axis=1)
            min_coord = np.min(new_min, axis=1).reshape((3, 1))
            new_max = np.concatenate((max_coord, curr_max), axis=1)
            max_coord = np.max(new_max, axis=1).reshape((3, 1))
        return min_coord, max_coord


class FaceBound(Entity):
    def extract_data(self, params, data):
        params = params.split(",")
        self.loop = data[int(params[0])]
        if params[-1][1] == "T":
            self.orientation = 1
        elif params[-1][1] == "F":
            self.orientation = -1
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        #print("FaceBound: ", bool(self.orientation), len(self.loop.oriented_edges))

    def check_data(self):
        if not isinstance(self.loop, EdgeLoop):
            raise ValueError('Expected EdgeLoop, got ', type(self.loop))


class AdvancedFace(Entity):
    def extract_data(self, params, data):
        params = params[1:].split(")")
        list_fb = np.array(params[0].split(",")).astype(int)
        self.face_bounds = []
        for i in range(len(list_fb)):
            self.face_bounds.append(data[list_fb[i]])
        params = params[1].split(",")
        if params[-1][1] == "T":
            self.orientation = 1
        elif params[-1][1] == "F":
            self.orientation = -1
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        self.surface = data[int(params[1])]
        print("AdvancedFace: ", list_fb, type(self.surface), bool(self.orientation))

    def check_data(self):
        if not isinstance(self.surface, Surface):
            raise ValueError('Expected Surface, got ', type(self.surface))
        for fb in self.face_bounds:
            if not isinstance(fb, FaceBound):
                raise ValueError('Expected FaceBound, got ', type(fb))
