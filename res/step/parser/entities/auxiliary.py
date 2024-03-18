from res.step.parser.entities.ancestors import Entity
from res.step.parser.entities.basic import CartesianPoint, Direction


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


class Vector(Entity):

    def extract_data(self, params, data):
        params = params.split(",")
        self.direction = data[int(params[0])]
        self.length = float(params[1])

    def check_data(self):
        if type(self.direction) != Direction:
            raise ValueError('Expected Direction, got ', type(self.direction))
        self.vec_coord = self.direction.vector


class VertexPoint(Entity):

    def extract_data(self, params, data):
        self.point = data[int(params)]

    def check_data(self):
        if type(self.point) != CartesianPoint:
            raise ValueError('Expected CartesianPoint, got ', type(self.point))
        self.coord = self.point.coord



