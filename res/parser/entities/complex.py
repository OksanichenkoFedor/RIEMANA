import numpy as np

from matplotlib.patches import Circle as CirclePlot
from matplotlib.patches import Polygon, Arc
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt

from res.parser.entities.ancestors import Curve, Edge, Drawable, Entity, Surface
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.parser.entities.auxiliary import Axis2Placement3D, EdgeCurve
from res.parser.entities.basic import CartesianPoint

import res.config as config


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
        start_angle = give_angle(start_x, start_y, self.R)
        end_angle = give_angle(end_x, end_y, self.R)
        delta = np.array([0, 0, 0])
        delta[0] = self.R * np.linalg.norm(np.cross(self.z, np.array([1.0, 0.0, 0.0])))
        delta[1] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 1.0, 0.0])))
        delta[2] = self.R * np.linalg.norm(np.cross(self.z, np.array([0.0, 0.0, 1.0])))

        coords = self.give_coords(20, start_point.coord, end_point.coord, True)


        def draw_function(axis, color, is_plotting):
            if color is None:
                color = "b"
            if is_plotting:
                pass
                #arc = Arc((0, 0), width=2 * self.R, height=2 * self.R, theta1=start_angle, theta2=end_angle,
                #         color=color)
                #axis.add_patch(arc)
                #pathpatch_2d_to_3d(arc, centre_vector=self.start_coord, normal=self.z)
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
        # print(start_x,start_y,end_x,end_y, self.R)
        if start_angle>end_angle:
            end_angle+=2*np.pi
            #print("Strange angles: ",start_angle/(np.pi), end_angle/(np.pi), orientation)
        num = number_points
        angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0*number_points), dtype=np.float64)
        while angles.shape[0]>number_points:
            num = num-0.1
            angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0 * num),
                               dtype=np.float64)

        while angles.shape[0]<number_points:
            num = num+0.1
            angles = np.arange(start_angle, end_angle, (end_angle - start_angle) / (1.0 * num),
                               dtype=np.float64)


        Xs = (self.start_coord[0] + self.R*self.x[0] * np.cos(angles) + self.R*self.y[0] * np.sin(angles)).reshape((1, number_points))
        Ys = (self.start_coord[1] + self.R*self.x[1] * np.cos(angles) + self.R*self.y[1] * np.sin(angles)).reshape((1, number_points))
        Zs = (self.start_coord[2] + self.R*self.x[2] * np.cos(angles) + self.R*self.y[2] * np.sin(angles)).reshape((1, number_points))
        coords = np.concatenate((Xs, Ys, Zs), axis=0)
        #print("give_coords, circle: ", number_points, coords.shape)
        if bool(orientation)==False:
            print("FFFFFFFFFFFFFF", coords.shape)
            coords = coords[:,::-1]
        return coords


def give_angle(x, y, r):
    cos = x / r
    sin = y / r
    cos = cos / np.sqrt(cos * cos + sin * sin)
    sin = sin / np.sqrt(cos * cos + sin * sin)

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

        #print(self.knots[0],self.knots[-1])
        self.knots = (np.array(self.knots) - self.knots[0]) / (self.knots[-1] - self.knots[0])
        #self.knots = self.knots*(1.0*self.N-3.0)/(1.0*self.N-1.0)+1.0/(self.N-1.0)
        #self.knots = np.array([0] + list(self.knots) + [1])

    def check_data(self):
        if len(self.knot_multiplicities) != self.N - 2:
            raise ValueError('Incorrect shape of knot_multiplicities, expected ', self.N - 2, " got ",
                             len(self.knot_multiplicities))
        if len(self.knots) != self.N-2:
            raise ValueError('Incorrect shape of knots, expected ', self.N - 2, " got ",
                             len(self.knots))

        if self.end_of_line != "3,.UNSPECIFIED.,.F.,.F.,.UNSPECIFIED.":
            raise ValueError('Unexpected extra parameters: ', self.end_of_line)

        for i in range(self.N):
            if type(self.points[i]) != CartesianPoint:
                raise ValueError('Expected CartesianPoint, got ', type(self.points[i]))

    def draw(self, axis, color, is_plotting):
        if self.knots[-1] != 1.0:
            color = (self.knots[-1], 0, 0)
        else:
            color = "b"
        coords = np.array(self.coords)
        color_start = np.array([1, 0, 0])
        color_end = np.array([0, 0, 0])
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

        # self.coords = coords

        def draw_function(axis, color, is_plotting):
            if color is None:
                if self.knots[-1] != 1.0:
                    color = "k"
                else:
                    color = "r"
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
        for gamma in gammas:
            ind = np.searchsorted(self.knots, gamma)
            start_coord = np.array(self.coords[ind - 1])
            end_coord = np.array(self.coords[ind])
            start_dist = np.abs(gamma - self.knots[ind - 1])
            end_dist = np.abs(self.knots[ind] - gamma)
            coord = (end_dist * start_coord + start_dist * end_coord) / (start_dist + end_dist)
            res_coords.append(coord)
        return np.array(res_coords).T

    def generate_gammas(self, start_coord, end_coord, orientation, number_points=None):
        print("Ориентация кусочнолинейной необработана")
        coords = np.array(self.coords[:-2])
        C = coords - start_coord
        C = np.sum(C * C, axis=1)
        start_second, start_first = np.argsort(C)[-2:]
        start_first_dist, start_second_dist = np.sort(np.sqrt(C))[:2]
        start_second1, start_first1 = np.max((start_second, start_first)), np.min((start_second, start_first))
        start_first, start_second = start_first1, start_second1
        if start_first1 != start_first:
            start_first_dist, start_second_dist = start_second_dist, start_first_dist
        if np.abs(start_first - start_second) > 1:
            raise ValueError('Not near points in OrientedEdge, id: ', self.id)
        C = coords - end_coord
        C = np.sum(C * C, axis=1)
        end_second, end_first = np.argsort(C)[-2:]
        end_first_dist, end_second_dist = np.sort(np.sqrt(C))[:2]
        end_second1, end_first1 = np.max((end_second, end_first)), np.min((end_second, end_first))
        end_first, end_second = end_first1, end_second1
        start_gamma = (start_second_dist * self.knots[start_first] + start_first_dist * self.knots[start_second]) / (
                start_first_dist + start_second_dist)

        end_gamma = (end_second_dist * self.knots[end_first] + end_first_dist * self.knots[end_second]) / (
                end_first_dist + end_second_dist)
        if number_points is None:
            if start_gamma < end_gamma:
                gammas = [start_gamma] + list(self.knots[start_first:end_first]) + [end_gamma]
                return np.array(gammas)
            else:
                gammas = [end_gamma] + list(self.knots[end_first:start_first]) + [start_gamma]
                return np.array(gammas[::-1])

        return np.arange(start_gamma, end_gamma, (end_gamma - start_gamma) / number_points)

    def give_coords(self, number_points, start_coord, end_coord, orientation):
        gammas = self.generate_gammas(start_coord, end_coord, orientation, number_points)
        coords = self.gamma_points(gammas)
        #print("give_coords, BSplineCurveWithKnots: ",number_points, coords.shape)
        #return None
        if bool(orientation)==False:
            print("FFFFFFFFFFFFFF", coords.shape)
            coords = coords[:,::-1]
        return coords


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
            print("fdfdfdfdfdfdf")
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
        print(bool(self.orientation))
        return self.edge.give_coords(number_points, bool(self.orientation))


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
            color = "r"

        if is_plotting and type(self.coords)==type(np.array([])):
            xyz = self.coords.T
            xyz = xyz.reshape(-1, 1, 3)
            segments = np.hstack([xyz[:-1], xyz[1:]])
            colors = np.arange(0, 1, 1 / xyz.shape[0])
            coll = Line3DCollection(segments, cmap=plt.cm.plasma)
            coll.set_array(colors)
            axis.add_collection(coll)
            return (np.min(self.coords, axis=1)).reshape((3, 1)), (np.max(self.coords, axis=1)).reshape((3, 1))
        return np.array([0,0,0]).reshape((3,1)), np.array([0,0,0]).reshape((3,1))
        # if color is None:
        #    color = self.color
        # min_coord = np.array([0, 0, 0]).reshape(3, 1)
        # max_coord = np.array([0, 0, 0]).reshape(3, 1)
        # for edge in self.oriented_edges:
        #    curr_min, curr_max = edge.draw(axis, color, is_plotting)
        #    new_min = np.concatenate((min_coord, curr_min), axis=1)
        #    min_coord = np.min(new_min, axis=1).reshape((3, 1))
        #    new_max = np.concatenate((max_coord, curr_max), axis=1)
        #    max_coord = np.max(new_max, axis=1).reshape((3, 1))
        # return min_coord, max_coord

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
        if self.coords is None:
            pass
        else:
            pass
        return self.coords


class FaceBound(Entity):
    def extract_data(self, params, data):
        params = params.split(",")
        self.loop = data[int(params[0])]
        if params[-1][1] == "T":
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        # print("FaceBound: ", bool(self.orientation), len(self.loop.oriented_edges))

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
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        self.surface = data[int(params[1])]
        # print("AdvancedFace: ", list_fb, type(self.surface), bool(self.orientation))

    def check_data(self):
        if not isinstance(self.surface, Surface):
            raise ValueError('Expected Surface, got ', type(self.surface))
        for fb in self.face_bounds:
            if not isinstance(fb, FaceBound):
                raise ValueError('Expected FaceBound, got ', type(fb))
        for fb in self.face_bounds:
            pass
            a = fb.loop.give_coords(config.elem_on_edge, fb.orientation)
