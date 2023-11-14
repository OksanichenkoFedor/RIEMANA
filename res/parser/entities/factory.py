from res.parser.entities.basic import CartesianPoint, Direction
from res.parser.entities.auxiliary import Axis2Placement3D, Plane, Vector, Line, VertexPoint, EdgeCurve
from res.parser.entities.complex import Circle, BSplineCurveWithKnots, OrientedEdge, EdgeLoop
from res.parser.entities.surfaces import ConicalSurface, CylindricalSurface, ToroidalSurface

def entity_factory(type, id, params, data):
    if type == "CARTESIAN_POINT":
        return CartesianPoint(id, params, data)
    if type == "DIRECTION":
        return Direction(id, params, data)
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
    if type == "B_SPLINE_CURVE_WITH_KNOTS":
        return BSplineCurveWithKnots(id, params, data)
    if type == "CONICAL_SURFACE":
        return ConicalSurface(id, params, data)
    if type == "CYLINDRICAL_SURFACE":
        return CylindricalSurface(id, params, data)
    if type == "TOROIDAL_SURFACE":
        return ToroidalSurface(id, params, data)
    if type == "EDGE_CURVE":
        return EdgeCurve(id, params, data)
    if type == "ORIENTED_EDGE":
        return OrientedEdge(id, params, data)
    if type =="EDGE_LOOP":
        return EdgeLoop(id, params, data)


    print("Unknown type: ", type)

