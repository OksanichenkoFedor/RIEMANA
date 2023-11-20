import numpy as np

from res.parser.entities.edges import EdgeLoop
from res.frontend.draw_3d import pathpatch_2d_to_3d
from res.parser.entities.ancestors import Edge, Drawable, Entity, Surface

import res.config as config

from matplotlib.patches import PathPatch


class FaceBound(Entity):
    def extract_data(self, params, data):
        params = params.split(",")
        self.loop = data[int(params[0])]
        if params[-1][1] == "T":
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        self.coords = self.loop.give_coords(config.elem_on_edge, self.orientation)

    def check_data(self):
        if not isinstance(self.loop, EdgeLoop):
            raise ValueError('Expected EdgeLoop, got ', type(self.loop))


class AdvancedFace(Entity, Drawable):
    def extract_data(self, params, data):
        params = params[1:].split(")")
        list_fb = np.array(params[0].split(",")).astype(int)
        self.face_bounds = []
        for i in range(len(list_fb)):
            self.face_bounds.append(data[list_fb[i]])
        params = params[1].split(",")
        if params[-1][1] == "T":
            self.orientation = True
        elif params[-1][1] == "F":
            self.orientation = False
        else:
            raise ValueError('Incorrect orientation: ', self.id)
        self.surface = data[int(params[1])]
        # print("AdvancedFace: ", list_fb, type(self.surface), bool(self.orientation))

    def check_data(self):
        self.plot_surfaces = []
        if not isinstance(self.surface, Surface):
            raise ValueError('Expected Surface, got ', type(self.surface))
        for fb in self.face_bounds:
            if not isinstance(fb, FaceBound):
                raise ValueError('Expected FaceBound, got ', type(fb))
            plot_surface = self.surface.give_3d_meshgrid(fb.coords)
            self.plot_surfaces.append(plot_surface)
        self.min, self.max = np.array([0, 0, 0]), np.array([0, 0, 0])
        for ps in self.plot_surfaces:
            if ps != None:
                self.min[0], self.max[0] = np.min((np.min(ps[0]), self.min[0])), np.max((np.max(ps[0]), self.max[0]))
                self.min[1], self.max[1] = np.min((np.min(ps[1]), self.min[1])), np.max((np.max(ps[1]), self.max[1]))
                self.min[2], self.max[2] = np.min((np.min(ps[2]), self.min[2])), np.max((np.max(ps[2]), self.max[2]))

    def draw(self, axis, color, is_plotting):
        for fb in self.face_bounds:
            fb.loop.draw(axis, color, is_plotting)
        for ps in self.plot_surfaces:
            if is_plotting and ps != None:
                print(ps[0].shape, ps[1].shape, ps[2].shape)
                print(ps[0][0], ps[1][0], ps[2][0])
                color = np.random.random(3)
                for i in range(len(ps[0])):
                    axis.plot(ps[0][i], ps[1][i], ps[2][i], ".", color=color)

                # axis.plot_trisurf(list(ps[0] + (np.random.random(ps[0].shape) - 0.5) * 0.000001),
                #                  list(ps[1] + (np.random.random(ps[1].shape) - 0.5) * 0.000001),
                #                  list(ps[2] + (np.random.random(ps[2].shape) - 0.5) * 0.000001), color="g")
                # if ps[3]==None:
                #
                # else:
                # self.patch = PathPatch(ps[3], facecolor='g', lw=2)
                # axis.add_patch(self.patch)
                # pathpatch_2d_to_3d(self.patch, centre_vector=self.surface.start_coord, normal=self.surface.z)
        return self.min.reshape((3, 1)), self.max.reshape((3, 1))
