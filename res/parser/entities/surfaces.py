import numpy as np

from res.parser.entities.ancestors import Surface
from res.parser.entities.auxiliary import Axis2Placement3D
from res.frontend.step.draw_2d import give_angle
from res.const.plot_config import NUMBER_OF_CON_SURFACE_POINTS, NUMBER_OF_CYL_SURFACE_POINTS, \
    NUMBER_OF_TOR_SURFACE_POINTS


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
        self.T = np.concatenate((self.x.reshape((3, 1)), self.y.reshape((3, 1)), self.z.reshape((3, 1))), axis=1).T

    def coordinates_transposition(self, coords):
        # print("Начали переводить на плоскость")
        delta = (coords - self.start_coord.reshape((3, 1)).repeat(coords.shape[1], axis=1))
        inside_coord = self.T @ delta
        return inside_coord[:-1, :].T, "pln"

    def give_3d_meshgrid(self, boundary_coords):
        meshgrid_2d = self.give_2d_meshgrid(boundary_coords)
        if meshgrid_2d is None:
            print("Возврат сетки не реализован - плоскость")
            return None
        u, v, path = meshgrid_2d
        x = self.start_coord[0] + u * self.x[0] + v * self.y[0]
        y = self.start_coord[1] + u * self.x[1] + v * self.y[1]
        z = self.start_coord[2] + u * self.x[2] + v * self.y[2]
        # print(x.shape,y.shape,z.shape)
        return (x, y, z, path)


class ConicalSurface(Surface):

    def extract_data(self, line, data):
        pass
        params = line.split(",")
        self.placement = data[int(params[0])]

        self.radius = float(params[1])
        if self.radius > 10000:
            self.incorr = True
        else:
            self.incorr = False
        self.angle = float(params[2])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)
        # print("ConSurf: ",int(params[0]), self.radius, self.angle, self.start_coord)

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

    def coordinates_transposition(self, coords):
        # print("Перевод координат не реализован - конус")
        new_coords = coords - self.start_coord.reshape((3, 1))
        v = new_coords * np.repeat(self.z.reshape((3, 1)), coords.shape[1], axis=1)
        v = v.sum(axis=0).reshape(1, coords.shape[1])
        cos = ((new_coords - v * self.z.reshape((3, 1))) / (self.radius + v * np.tan(self.angle))) * \
              np.repeat(self.x.reshape((3, 1)), coords.shape[1], axis=1)
        cos = cos.sum(axis=0)
        sin = ((new_coords - v * self.z.reshape((3, 1))) / (self.radius + v * np.tan(self.angle))) * \
              np.repeat(self.y.reshape((3, 1)), coords.shape[1], axis=1)
        sin = sin.sum(axis=0)
        u = []
        for i in range(len(sin)):
            u.append(give_angle(cos[i], sin[i], 1))
        u = np.array(u).reshape(1, coords.shape[1])

        return np.concatenate((u, v), axis=0).T, "con"

    def give_3d_meshgrid(self, boundary_coords):
        meshgrid_2d = self.give_2d_meshgrid(boundary_coords)
        if meshgrid_2d is None:
            print("Возврат сетки не реализован - конус")
            return None
        u, v, path = meshgrid_2d
        x = self.start_coord[0] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + v * \
            self.z[0]
        y = self.start_coord[1] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + v * \
            self.z[1]
        z = self.start_coord[2] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + v * \
            self.z[2]
        return (x, y, z, path)

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "g"
        u, v = np.mgrid[0:NUMBER_OF_CON_SURFACE_POINTS, 0:NUMBER_OF_CON_SURFACE_POINTS] * (
                1.0 / NUMBER_OF_CON_SURFACE_POINTS)
        u = u * 2 * (np.pi * (NUMBER_OF_CON_SURFACE_POINTS + 2) / NUMBER_OF_CON_SURFACE_POINTS)
        v = (v - 0.5) * 200
        x = self.start_coord[0] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + v * \
            self.z[0]
        y = self.start_coord[1] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + v * \
            self.z[1]
        z = self.start_coord[2] + (self.radius + v * np.tan(self.angle)) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + v * \
            self.z[2]
        if not self.incorr:
            if is_plotting:
                axis.plot_surface(x, y, z, rstride=1, cstride=1, color=color)
            return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), \
                   np.array([np.max(x), np.max(y), np.max(z)]).reshape((3, 1))
        else:
            return np.array([0, 0, 0]).reshape((3, 1)), np.array([0, 0, 0]).reshape((3, 1))


class CylindricalSurface(Surface):

    def extract_data(self, line, data):
        pass
        params = line.split(",")
        self.placement = data[int(params[0])]

        self.radius = float(params[1])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

    def coordinates_transposition(self, coords):
        # print("---")
        # print("Перевод координат не реализован - цилиндр")
        new_coords = coords - self.start_coord.reshape((3, 1))
        v = new_coords * np.repeat(self.z.reshape((3, 1)), coords.shape[1], axis=1)
        v = v.sum(axis=0).reshape(1, coords.shape[1])
        cos = (new_coords * np.repeat(self.x.reshape((3, 1)), coords.shape[1], axis=1)) / self.radius
        cos = cos.sum(axis=0).reshape(1, coords.shape[1])
        sin = (new_coords * np.repeat(self.y.reshape((3, 1)), coords.shape[1], axis=1)) / self.radius
        sin = sin.sum(axis=0).reshape(1, coords.shape[1])
        u = []
        for i in range(len(sin[0])):
            u.append(give_angle(cos[0, i], sin[0, i], 1))
        u = np.array(u).reshape(1, coords.shape[1])
        return np.concatenate((u, v), axis=0).T, "cyl"

    def give_3d_meshgrid(self, boundary_coords):
        meshgrid_2d = self.give_2d_meshgrid(boundary_coords)
        if meshgrid_2d is None:
            print("Возврат сетки не реализован - цилиндр")
            return None
        u, v, path = meshgrid_2d
        x = self.start_coord[0] + (self.radius) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + v * \
            self.z[0]
        y = self.start_coord[1] + (self.radius) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + v * \
            self.z[1]
        z = self.start_coord[2] + (self.radius) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + v * \
            self.z[2]
        return (x, y, z, path)

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "g"
        u, v = np.mgrid[0:NUMBER_OF_CYL_SURFACE_POINTS, 0:NUMBER_OF_CYL_SURFACE_POINTS] * (
                1.0 / NUMBER_OF_CYL_SURFACE_POINTS)
        u = u * 2 * (np.pi * (NUMBER_OF_CYL_SURFACE_POINTS + 2) / NUMBER_OF_CYL_SURFACE_POINTS)
        v = (v - 0.5) * 200
        x = self.start_coord[0] + (self.radius) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + v * \
            self.z[0]
        y = self.start_coord[1] + (self.radius) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + v * \
            self.z[1]
        z = self.start_coord[2] + (self.radius) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + v * \
            self.z[2]
        if is_plotting:
            axis.plot_surface(x, y, z, rstride=1, cstride=1, color=color)

        return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), \
               np.array([np.max(x), np.max(y), np.max(z)]).reshape((3, 1))


class ToroidalSurface(Surface):

    def extract_data(self, line, data):
        params = line.split(",")
        self.placement = data[int(params[0])]

        self.major_radius = float(params[1])
        self.minor_radius = float(params[2])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)
        # print("TorSurf: ", int(params[0]), self.major_radius, self.minor_radius, self.start_coord)

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

    def coordinates_transposition(self, coords):
        #print("Перевод координат не реализован - тор")
        new_coords = coords - self.start_coord.reshape((3, 1))
        #print(new_coords.shape)
        sin_v = ((new_coords * np.repeat(self.z.reshape((3, 1)),
                                        coords.shape[1], axis=1)).sum(axis=0)).reshape(1, coords.shape[1])/self.minor_radius

        cos_v1 = ((new_coords * np.repeat(self.x.reshape((3, 1)),
                                        coords.shape[1], axis=1)).sum(axis=0)).reshape(1, coords.shape[1])
        cos_v2 = ((new_coords * np.repeat(self.y.reshape((3, 1)),
                                          coords.shape[1], axis=1)).sum(axis=0)).reshape(1, coords.shape[1])
        cos_v = np.sqrt(cos_v1*cos_v1+cos_v2*cos_v2)
        cos_v = ((cos_v.sum(axis=0) - self.major_radius) / self.minor_radius).reshape(1, coords.shape[1])
        v = []
        #print(cos_v)
        for i in range(len(sin_v[0])):
            #print(i, sin_v[0,i], cos_v[0,i])
            v.append(give_angle(cos_v[0, i], sin_v[0, i], 1))
        v = np.array(v).reshape(1, coords.shape[1])
        cos_u = new_coords * np.repeat(self.x.reshape((3, 1)), coords.shape[1], axis=1) / (
                    self.major_radius + self.minor_radius * cos_v)
        cos_u = cos_u.sum(axis=0).reshape(1, coords.shape[1])
        #print(cos_u.shape)
        sin_u = new_coords * np.repeat(self.y.reshape((3, 1)), coords.shape[1], axis=1) / (
                    self.major_radius + self.minor_radius * cos_v)
        sin_u = sin_u.sum(axis=0).reshape(1, coords.shape[1])
        #print(sin_u.shape)
        u = []
        for i in range(len(sin_u[0])):
            u.append(give_angle(cos_u[0, i], sin_u[0, i], 1))
        u = np.array(u).reshape(1, coords.shape[1])
        return np.concatenate((u, v), axis=0).T, "tor"

    def give_3d_meshgrid(self, boundary_coords):
        meshgrid_2d = self.give_2d_meshgrid(boundary_coords)
        if meshgrid_2d is None:
            print("Возврат сетки не реализован - тор")
            return None
        u, v, path = meshgrid_2d
        x = self.start_coord[0] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + self.minor_radius * self.z[0] * np.sin(v)
        y = self.start_coord[1] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + self.minor_radius * self.z[1] * np.sin(v)
        z = self.start_coord[2] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + self.minor_radius * self.z[2] * np.sin(v)
        return (x, y, z, path)

    def draw(self, axis, color, is_plotting):
        if color is None:
            color = "g"
        u, v = np.mgrid[0:NUMBER_OF_TOR_SURFACE_POINTS,
               0: NUMBER_OF_TOR_SURFACE_POINTS] * (1.0 / NUMBER_OF_TOR_SURFACE_POINTS)
        u = u * 2 * (np.pi * (NUMBER_OF_TOR_SURFACE_POINTS + 2) / NUMBER_OF_TOR_SURFACE_POINTS)
        v = v * 2 * (np.pi * (NUMBER_OF_TOR_SURFACE_POINTS + 2) / NUMBER_OF_TOR_SURFACE_POINTS)
        x = self.start_coord[0] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[0] + np.sin(u) * self.y[0]) + self.minor_radius * self.z[0] * np.sin(v)
        y = self.start_coord[1] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[1] + np.sin(u) * self.y[1]) + self.minor_radius * self.z[1] * np.sin(v)
        z = self.start_coord[2] + (self.major_radius + self.minor_radius * np.cos(v)) * (
                np.cos(u) * self.x[2] + np.sin(u) * self.y[2]) + self.minor_radius * self.z[2] * np.sin(v)
        if is_plotting:
            axis.plot_surface(x, y, z, rstride=1, cstride=1)
        return np.array([np.min(x), np.min(y), np.min(z)]).reshape((3, 1)), \
               np.array([np.max(x), np.max(y), np.max(z)]).reshape((3, 1))
