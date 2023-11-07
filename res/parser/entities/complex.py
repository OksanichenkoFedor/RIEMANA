import numpy as np
from matplotlib.patches import Circle as CirclePlot

from res.parser.entities.entity import Entity
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.parser.entities.auxiliary import Axis2Placement3D


class Circle(Entity):
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
        return (self.start_coord-delta).reshape((3,1)),(self.start_coord+delta).reshape((3,1))
