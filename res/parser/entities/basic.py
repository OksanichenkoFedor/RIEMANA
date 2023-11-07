import numpy as np
from res.parser.entities.entity import Entity

class CartesianPoint(Entity):
    def __init__(self, id, params):
        super(CartesianPoint, self).__init__(id)
        coord = params[1:-1].split(",")
        self.coord = np.array([float(coord[0]), float(coord[1]), float(coord[2])])


class Direction(Entity):
    def __init__(self, id, params):
        super(Direction, self).__init__(id)
        coord = params[1:-1].split(",")
        self.vector = np.array([float(coord[0]), float(coord[1]), float(coord[2])])