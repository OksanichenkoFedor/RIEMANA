import numpy as np

from res.parser.entities.entity import Entity
from res.parser.entities.basic import CartesianPoint, Direction


class Axis2Placement3D(Entity):
    def __init__(self, id, params, data):
        super(Axis2Placement3D, self).__init__(id)
        params = params.split(",")
        self.point = data[int(params[0])]
        self.axis1 = data[int(params[1])]
        self.axis2 = data[int(params[2])]

        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        if type(self.axis1) != Direction:
            raise ValueError('Expected Direction, got ', type(self.axis1))
        if type(self.axis2) != Direction:
            raise ValueError('Expected Direction, got ', type(self.axis2))


    def check_orthgonality(self):
        dot = self.axis1.x*self.axis2.x+self.axis1.y*self.axis2.y+self.axis1.z*self.axis2.z
        if dot>0.01:
            print("Not orthogonal: ",dot)

class Plane(Entity):
    def __init__(self, id, params, data):
        super(Plane, self).__init__(id)
        self.placement = data[int(params)]
        if type(self.placement) != Axis2Placement3D:
            raise ValueError('Expected Axis2Placement3D point, got ', type(self.placement))
        self.start_coord = self.placement.point.coord
        self.z = self.placement.axis1.vector
        self.x = self.placement.axis2.vector
        self.y = np.cross(self.z, self.x)


class Vector(Entity):
    def __init__(self, id, params, data):
        super(Vector, self).__init__(id)
        params = params.split(",")
        self.direction = data[int(params[0])]
        self.length = float(params[1])

        if type(self.direction) != Direction:
            raise ValueError('Expected Direction, got ', type(self.direction))
        self.vec_coord = self.direction.vector

class Line(Entity):
    def __init__(self, id, params, data):
        super(Line, self).__init__(id)
        print("Line: ", params)
        params = params.split(",")
        self.point = data[int(params[0])]
        self.vector = data[int(params[1])]
        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        if type(self.vector) != Vector:
            raise ValueError('Expected Direction, got ', type(self.vector))
        self.start_coord = self.point.coord
        self.vec_coord = self.vector.vec_coord
        print("Line: ", self.start_coord, self.vec_coord)
