from res.step.parser.entities.basic import CartesianPoint, Direction
from res.step.parser.entities.auxiliary import Axis2Placement3D, Vector, VertexPoint
from res.step.parser.entities.faces import FaceBound, AdvancedFace
from res.step.parser.entities.surfaces import Plane, ConicalSurface, CylindricalSurface, ToroidalSurface
from res.step.parser.entities.curves import Circle, BSplineCurveWithKnots, Line
from res.step.parser.entities.edges import OrientedEdge, EdgeLoop, EdgeCurve
from res.step.parser.entities.shells import ClosedShell

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
    if type == "EDGE_LOOP":
        return EdgeLoop(id, params, data)
    if type == "FACE_BOUND":
        return FaceBound(id, params, data)
    if type == "ADVANCED_FACE":
        return AdvancedFace(id, params, data)
    if type == "CLOSED_SHELL":
        return ClosedShell(id, params, data)



    print("Unknown type: ", type)

