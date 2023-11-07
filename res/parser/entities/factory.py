from res.parser.entities.basic import CartesianPoint, Direction
from res.parser.entities.auxiliary import Axis2Placement3D, Plane, Vector, Line, VertexPoint
from res.parser.entities.complex import Circle, EntityEdge, BSplineCurveWithKnots

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
    if type == "VERTEX_POINT":
        return VertexPoint(id, params, data)
    if type == "EDGE_CURVE":
        return EntityEdge(id, params, data)
    if type == "B_SPLINE_CURVE_WITH_KNOTS":
        return BSplineCurveWithKnots(id, params, data)

    print("Unknown type: ", type)

