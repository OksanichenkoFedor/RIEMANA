from res.parser.entities.basic import CartesianPoint, Direction
from res.parser.entities.auxiliary import Axis2Placement3D, Plane, Vector, Line
from res.parser.entities.complex import Circle

def entity_factory(type, id, params, data):
    if type == "CARTESIAN_POINT":
        return CartesianPoint(id, params)
    if type == "DIRECTION":
        return Direction(id, params)
    if type == "AXIS2_PLACEMENT_3D":
        return Axis2Placement3D(id, params, data)
    if type == "CIRCLE":
        return Circle(id, params, data)
    if type == "PLANE":
        return Plane(id, params, data)
    if type == "VECTOR":
        return Vector(id, params, data)
    if type == "LINE":
        return Line(id, params, data)

    print("Unknown type: ",type)

