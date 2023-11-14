import numpy as np

from res.parser.entities.ancestors import Surface, Drawable
from res.parser.entities.auxiliary import Axis2Placement3D
from res.const.plot_config import NUMBER_OF_CON_SURFACE_POINTS, NUMBER_OF_CYL_SURFACE_POINTS, \
    NUMBER_OF_TOR_SURFACE_POINTS


class ConicalSurface(Surface, Drawable):

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


class CylindricalSurface(Surface, Drawable):

    def extract_data(self, line, data):
        pass
        params = line.split(",")
        self.placement = data[int(params[0])]

        self.radius = float(params[1])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)
        # print("CylSurf: ", int(params[0]), self.radius)

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

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


class ToroidalSurface(Surface, Drawable):

    def extract_data(self, line, data):
        pass
        params = line.split(",")
        self.placement = data[int(params[0])]

        self.major_radius = float(params[1])
        self.minor_radius = float(params[2])
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)
        #print("TorSurf: ", int(params[0]), self.major_radius, self.minor_radius, self.start_coord)

    def check_data(self):
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))

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
