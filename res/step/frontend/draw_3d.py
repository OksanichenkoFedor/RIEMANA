import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d

def rotation_matrix(d):
    sin_angle = np.linalg.norm(d)
    if sin_angle == 0:
        return np.identity(3)
    d /= sin_angle
    eye = np.eye(3)
    ddt = np.outer(d, d)
    skew = np.array([[0, d[2], -d[1]],
                     [-d[2], 0, d[0]],
                     [d[1], -d[0], 0]], dtype=np.float64)
    M = ddt + np.sqrt(1 - sin_angle ** 2) * (eye - ddt) + sin_angle * skew
    return M


def pathpatch_2d_to_3d(pathpatch, centre_vector=(0, 0, 0), normal=(0, 0, 1)):
    if type(normal) is str:
        index = "xyz".index(normal)
        normal = np.roll((1.0, 0, 0), index)
    normal /= np.linalg.norm(normal)
    path = pathpatch.get_path()
    trans = pathpatch.get_patch_transform()
    path = trans.transform_path(path)
    pathpatch.__class__ = art3d.PathPatch3D
    pathpatch._code3d = path.codes
    pathpatch._facecolor3d = pathpatch.get_facecolor
    verts = path.vertices
    d = np.cross(normal, (0, 0, 1))
    M = rotation_matrix(d)
    pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + centre_vector for x, y in verts])


def pathpatch_translate(pathpatch, delta):
    pathpatch._segment3d += delta




