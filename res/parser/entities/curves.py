import numpy as np

from res.parser.entities.ancestors import Curve, Drawable
from res.parser.entities.auxiliary import Axis2Placement3D, Vector
from res.parser.entities.basic import CartesianPoint
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.frontend.draw_2d import give_angle

from matplotlib.patches import Circle as CirclePlot
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt


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
        x = [start_point.coord[0], end_point.coord[0]]
        y = [start_point.coord[1], end_point.coord[1]]
        z = [start_point.coord[2], end_point.coord[2]]


        def draw_function(axis, color, is_plotting):
            if color is None:
                color = "g"
            if is_plotting:
                axis.plot(x, y, z, color=color)

            return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), np.array(
                [np.max(x), np.max(y), np.max(z)]).reshape((3, 1))

        return draw_function

    def give_coords(self, number_points, start_coord, end_coord, orientation):
        if np.max(np.abs(np.cross(start_coord - self.start_coord, self.vec_coord))) > 0.001:
            print("Ахтунг!!!")
        if np.max(np.abs(np.cross(end_coord - self.start_coord, self.vec_coord))) > 0.001:
            print("Ахтунг!!!")
        start_coord = start_coord.reshape((3, 1)).repeat(number_points, axis=1)
        end_coord = end_coord.reshape((3, 1)).repeat(number_points, axis=1)
        mult = np.arange(0, 1, 1 / number_points).reshape((1, number_points)).repeat(3, axis=0)
        coords = start_coord + (end_coord - start_coord) * mult
        if not bool(orientation):
            coords = coords[:, ::-1]
        return coords


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
        self.virgin_coords = self.coords
        self.virgin_knots = self.knots
        #print(len(self.knots), self.knots)
        #print(len(self.knot_multiplicities), self.knot_multiplicities)
        #print(len(self.coords), self.coords)
        #print("---")
        self.knots = (np.array(self.knots) - self.knots[0]) / (self.knots[-1] - self.knots[0])

        self.knots = np.array([0] + list(1.0/(self.N-1.0)+self.knots*((self.N-3.0)/(self.N-1.0))) + [1])

    def check_data(self):
        if len(self.knot_multiplicities) != self.N - 2:
            raise ValueError('Incorrect shape of knot_multiplicities, expected ', self.N - 2, " got ",
                             len(self.knot_multiplicities))
        if len(self.virgin_knots) != self.N - 2:
            raise ValueError('Incorrect shape of knots, expected ', self.N - 2, " got ",
                             len(self.knots))

        if self.end_of_line != "3,.UNSPECIFIED.,.F.,.F.,.UNSPECIFIED.":
            raise ValueError('Unexpected extra parameters: ', self.end_of_line)

        for i in range(self.N):
            if type(self.points[i]) != CartesianPoint:
                raise ValueError('Expected CartesianPoint, got ', type(self.points[i]))

    def draw(self, axis, color, is_plotting):
        coords = np.array(self.coords)
        if is_plotting:
            xyz = coords
            xyz = xyz.reshape(-1, 1, 3)
            segments = np.hstack([xyz[:-1], xyz[1:]])
            colors = np.arange(0, 1, 1 / xyz.shape[0])
            coll = Line3DCollection(segments, cmap=plt.cm.plasma)
            coll.set_array(colors)
            axis.add_collection(coll)
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
            coords[0, :] = start_point.coord
            coords[-1, :] = end_point.coord
        else:
            coords = coords[end_first:start_second, :]
            coords[0, :] = end_point.coord
            coords[-1, :] = start_point.coord
            coords = coords[::-1, :]
        coords[0], coords[-1] = coords[-1], coords[0]

        def draw_function(axis, color, is_plotting):
            if is_plotting:
                xyz = coords
                xyz = xyz.reshape(-1, 1, 3)
                segments = np.hstack([xyz[:-1], xyz[1:]])
                colors = np.arange(0, 1, 1 / xyz.shape[0])
                coll = Line3DCollection(segments, cmap=plt.cm.plasma)
                coll.set_array(colors)
                axis.add_collection(coll)
            return (np.min(coords, axis=0)).reshape((3, 1)), (np.max(coords, axis=0)).reshape((3, 1))

        return draw_function

    def gamma_points(self, gammas):
        res_coords = []
        #print(self.coords[-1])
        #print(self.coords[0])
        for gamma in gammas:

            ind = np.searchsorted(self.knots, gamma)
            start_coord = np.array(self.coords[ind - 1])
            end_coord = np.array(self.coords[ind])
            start_dist = np.abs(gamma - self.knots[ind - 1])
            end_dist = np.abs(self.knots[ind] - gamma)
            coord = (end_dist * start_coord + start_dist * end_coord) / (start_dist + end_dist)
            res_coords.append(coord)
            if np.abs(gamma-0)<0.0001:
                pass
                #print("g=0: ",gamma,coord,start_dist,end_dist, ind)
                #print(self.knots)
            if np.abs(gamma-1.0)<0.0001:
                pass
                #print("g=1: ", gamma,coord,start_dist,end_dist, ind)
                #print(self.knots)
        return np.array(res_coords).T

    def generate_gammas(self, start_coord, end_coord, number_points=None):

        #coords = np.array(self.coords[1:-1])
        coords = np.array(self.coords)
        C = coords - start_coord
        C = np.sum(C * C, axis=1)
        start_second, start_first = np.argsort(C)[-2:]
        start_first_dist, start_second_dist = np.sort(np.sqrt(C))[:2]
        start_second1, start_first1 = np.max((start_second, start_first)), np.min((start_second, start_first))
        #print("---")
        #print(self.knots)
        if start_first1 != start_first:
            #print(type(start_first1),type(start_first))
            #print(start_first1, start_first)
            start_first_dist, start_second_dist = start_second_dist, start_first_dist
        start_first, start_second = start_first1, start_second1

        if np.abs(start_first - start_second) > 1:
            raise ValueError('Not near points in OrientedEdge, id: ', self.id)
        C = coords - end_coord
        C = np.sum(C * C, axis=1)
        end_second, end_first = np.argsort(C)[-2:]
        end_first_dist, end_second_dist = np.sort(np.sqrt(C))[:2]
        end_second1, end_first1 = np.max((end_second, end_first)), np.min((end_second, end_first))
        if end_first1 != end_first:
            #print(type(end_first1), type(end_first))
            #print(end_first1, end_first)
            end_first_dist, end_second_dist = end_second_dist, end_first_dist
        end_first, end_second = end_first1, end_second1
        start_gamma = (start_second_dist * self.knots[start_first] + start_first_dist * self.knots[start_second]) / (
                start_first_dist + start_second_dist)

        end_gamma = (end_second_dist * self.knots[end_first] + end_first_dist * self.knots[end_second]) / (
                end_first_dist + end_second_dist)
        if start_gamma < end_gamma:
            pass
            #print("a:",round(start_gamma,4),round(end_gamma,4),start_first,end_second,len(self.knots),round(start_first_dist/start_second_dist))
        else:
            pass
            #print("b:",round(start_gamma,4),round(end_gamma,4),end_first, start_second, len(self.knots),round(end_first_dist/end_second_dist))
        if number_points is None:
            if start_gamma < end_gamma:
                gammas = [start_gamma] + list(self.knots[start_first:end_first]) + [end_gamma]
                #print(gammas)
                return np.array(gammas)
            else:
                gammas = [end_gamma] + list(self.knots[end_first:start_first]) + [start_gamma]
                #print(gammas[::-1])
                return np.array(gammas[::-1])
        gammas = np.array(list(np.arange(start_gamma, end_gamma, (end_gamma - start_gamma) / (number_points-1)))+[end_gamma])
        #print(gammas)
        return gammas

    def give_coords(self, number_points, start_coord, end_coord, orientation):
        gammas = self.generate_gammas(start_coord, end_coord, number_points)
        coords = self.gamma_points(gammas)
        if not bool(orientation):
            coords = coords[:, ::-1]
        return coords


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
            raise ValueError('Point out of circle, id: ', self.id)
        if np.abs(end_z) > 0.01:
            raise ValueError('Point out of circle, id: ', self.id)
        delta = np.array([0, 0, 0])
        delta[0] = self.R * np.linalg.norm(np.cross(self.z, np.array([1.0, 0.0, 0.0])))
        delta[1] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 1.0, 0.0])))
        delta[2] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 0.0, 1.0])))

        coords = self.give_coords(20, start_point.coord, end_point.coord, True)

        def draw_function(axis, color, is_plotting):
            if color is None:
                color = "b"
            if is_plotting:
                xyz = coords.T
                xyz = xyz.reshape(-1, 1, 3)
                segments = np.hstack([xyz[:-1], xyz[1:]])
                colors = np.arange(0, 1, 1 / xyz.shape[0])
                coll = Line3DCollection(segments, cmap=plt.cm.plasma)
                coll.set_array(colors)
                axis.add_collection(coll)

            return (self.start_coord - delta).reshape((3, 1)), (self.start_coord + delta).reshape((3, 1))

        return draw_function

    def give_coords(self, number_points, start_coord, end_coord, orientation):
        start_coord = start_coord - self.start_coord
        end_coord = end_coord - self.start_coord
        start_x, start_y, start_z = np.dot(start_coord, self.x), np.dot(start_coord, self.y), np.dot(start_coord,
                                                                                                     self.z)
        end_x, end_y, end_z = np.dot(end_coord, self.x), np.dot(end_coord, self.y), np.dot(end_coord, self.z)
        if np.abs(start_z) > 0.01:
            raise ValueError('Point out of circle, id: ', self.id)
        if np.abs(end_z) > 0.01:
            raise ValueError('Point out of circle, id: ', self.id)
        start_angle = give_angle(start_x, start_y, self.R)
        end_angle = give_angle(end_x, end_y, self.R)
        if start_angle > end_angle:
            end_angle += 2 * np.pi
        num = number_points
        angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0 * number_points), dtype=np.float64)
        while angles.shape[0] > number_points:
            num = num - 0.1
            angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0 * num),
                               dtype=np.float64)

        while angles.shape[0] < number_points:
            num = num + 0.1
            angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0 * num),
                               dtype=np.float64)

        Xs = (self.start_coord[0] + self.R * self.x[0] * np.cos(angles) + self.R * self.y[0] * np.sin(angles)).reshape(
            (1, number_points))
        Ys = (self.start_coord[1] + self.R * self.x[1] * np.cos(angles) + self.R * self.y[1] * np.sin(angles)).reshape(
            (1, number_points))
        Zs = (self.start_coord[2] + self.R * self.x[2] * np.cos(angles) + self.R * self.y[2] * np.sin(angles)).reshape(
            (1, number_points))
        coords = np.concatenate((Xs, Ys, Zs), axis=0)
        if not bool(orientation):
            coords = coords[:, ::-1]
        return coords



