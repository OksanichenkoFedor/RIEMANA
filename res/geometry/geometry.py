import numpy as np


class Cylinder:
    def __init__(self, x, y, z, start_coord, radius, height):
        self.x = np.array(x)
        self.x = np.array(x) / np.linalg.norm(x)
        self.y = np.array(y)
        self.y = np.array(y) / np.linalg.norm(y)
        self.z = np.array(z)
        self.z = np.array(z) / np.linalg.norm(z)
        self.start_coord = np.array(start_coord)
        self.radius = radius
        self.height = height

    def generate_points(self, Nz=10, N_phi=10, N_r=10, uniq=False):

        if uniq:
            uniq = 0.0
        else:
            uniq = 1.0

        u = np.repeat((np.arange(0, 1, 1.0 / N_phi) * 2 * np.pi).reshape((N_phi, 1)), Nz, axis=1)
        v = np.repeat((np.arange(0, Nz, 1.0) * (self.height / (Nz - 1.0))).reshape((1, Nz)), N_phi, axis=0)
        x = self.start_coord[0] + self.radius * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + self.z[0] * v
        y = self.start_coord[1] + self.radius * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + self.z[1] * v
        z = self.start_coord[2] + self.radius * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + self.z[2] * v
        self.bounds = np.concatenate((x.reshape((1, N_phi, Nz)),
                                      y.reshape((1, N_phi, Nz)),
                                      z.reshape((1, N_phi, Nz))), axis=0).reshape((3, -1))

        r = np.repeat((np.arange(0, N_r, 1.0) * (self.radius / (N_r - uniq))).reshape((1, N_r)), N_phi, axis=0)
        u = np.repeat((np.arange(0, 1, 1.0 / N_phi) * 2 * np.pi).reshape((N_phi, 1)), N_r, axis=1)

        x = self.start_coord[0] + r * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + self.z[0] * 0
        y = self.start_coord[1] + r * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + self.z[1] * 0
        z = self.start_coord[2] + r * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + self.z[2] * 0
        x = x.reshape((1, N_r * N_phi))
        y = y.reshape((1, N_r * N_phi))
        z = z.reshape((1, N_r * N_phi))
        self.down = np.concatenate((x, y, z), axis=0)

        x = self.start_coord[0] + r * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + self.z[0] * self.height
        y = self.start_coord[1] + r * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + self.z[1] * self.height
        z = self.start_coord[2] + r * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + self.z[2] * self.height
        x = x.reshape((1, N_r * N_phi))
        y = y.reshape((1, N_r * N_phi))
        z = z.reshape((1, N_r * N_phi))
        self.up = np.concatenate((x, y, z), axis=0)

        self.coords = np.concatenate((self.down, self.bounds, self.up), axis=1)

        self.phi = np.arange(0, N_phi * 1.0, 1.0) * 2 * (np.pi / (N_phi - uniq))
        x = self.start_coord[0] + self.radius * (self.x[0] * np.cos(self.phi) + self.y[0] * np.sin(self.phi)) + self.z[
            0] * 0
        y = self.start_coord[1] + self.radius * (self.x[1] * np.cos(self.phi) + self.y[1] * np.sin(self.phi)) + self.z[
            1] * 0
        z = self.start_coord[2] + self.radius * (self.x[2] * np.cos(self.phi) + self.y[2] * np.sin(self.phi)) + self.z[
            2] * 0
        self.down_arc = np.concatenate((x.reshape((1, N_phi)), y.reshape((1, N_phi)), z.reshape((1, N_phi))), axis=0)
        x = self.start_coord[0] + self.radius * (self.x[0] * np.cos(self.phi) + self.y[0] * np.sin(self.phi)) + self.z[
            0] * self.height
        y = self.start_coord[1] + self.radius * (self.x[1] * np.cos(self.phi) + self.y[1] * np.sin(self.phi)) + self.z[
            1] * self.height
        z = self.start_coord[2] + self.radius * (self.x[2] * np.cos(self.phi) + self.y[2] * np.sin(self.phi)) + self.z[
            2] * self.height
        self.up_arc = np.concatenate((x.reshape((1, N_phi)), y.reshape((1, N_phi)), z.reshape((1, N_phi))), axis=0)
        self.N_phi = N_phi
        self.lines = np.array(
            [(self.x * self.radius) + self.start_coord, (self.y * self.radius) + self.start_coord,
             ((-1) * self.x * self.radius) + self.start_coord,
             ((-1) * self.y * self.radius) + self.start_coord]).reshape(
            (4, 3, 1))
        self.lines = np.repeat(self.lines, 2, axis=2)
        add = np.repeat(np.array(self.z).reshape(1, 3), 4, axis=0)
        self.lines[:, :, 1] = self.lines[:, :, 1] + add * self.height

    def draw(self, axis):
        color1 = np.random.random(3)
        color2 = color1 * 0.5
        #for i in range(self.coords.shape[1]):
        #    axis.plot(self.coords[0][i], self.coords[1][i], self.coords[2][i], ".", color=color1)

        for i in range(4):
            axis.plot([self.lines[i, 0, 0], self.lines[i, 0, 1]],
                      [self.lines[i, 1, 0], self.lines[i, 1, 1]],
                      [self.lines[i, 2, 0], self.lines[i, 2, 1]], color=color2)

        for i in range(self.N_phi):
            axis.plot([self.up_arc[0, i], self.up_arc[0, (i + 1) % self.N_phi]],
                      [self.up_arc[1, i], self.up_arc[1, (i + 1) % self.N_phi]],
                      [self.up_arc[2, i], self.up_arc[2, (i + 1) % self.N_phi]], color=color2)

        for i in range(self.down_arc.shape[1]):
            axis.plot([self.down_arc[0, i], self.down_arc[0, (i + 1) % self.N_phi]],
                      [self.down_arc[1, i], self.down_arc[1, (i + 1) % self.N_phi]],
                      [self.down_arc[2, i], self.down_arc[2, (i + 1) % self.N_phi]], color=color2)

        return np.min(self.coords, axis=1), np.max(self.coords, axis=1)

    def is_points_inside(self, coords, include_bounds=True, include_down=True):
        new_coords = coords - self.start_coord.reshape((3, 1))
        v = new_coords * np.repeat(self.z.reshape((3, 1)), coords.shape[1], axis=1)
        v = v.sum(axis=0).reshape(1, coords.shape[1])
        cos = (new_coords * np.repeat(self.x.reshape((3, 1)), coords.shape[1], axis=1)) / self.radius
        cos = cos.sum(axis=0).reshape(1, coords.shape[1])
        sin = (new_coords * np.repeat(self.y.reshape((3, 1)), coords.shape[1], axis=1)) / self.radius
        sin = sin.sum(axis=0).reshape(1, coords.shape[1])
        r = cos * cos + sin * sin
        if include_bounds:
            r = ((r >= 0).astype(int) * (r <= 1.0).astype(int)).astype(bool)
            v = ((v >= 0).astype(int) * (v <= self.height).astype(int)).astype(bool)
        else:
            r = ((r >= 0).astype(int) * (r < 1.0).astype(int)).astype(bool)
            if include_down:
                v = ((v >= 0).astype(int) * (v < self.height).astype(int)).astype(bool)
            else:
                v = ((v > 0).astype(int) * (v < self.height).astype(int)).astype(bool)

        ans = ((r.astype(int)) * (v.astype(int))).astype(bool)
        return ans.reshape((ans.shape[1],))

    def get_around_points(self, mult):
        new_start = self.start_coord+0.5*(1.0-mult)*self.z*self.height
        new_cyl = Cylinder(self.x,self.y,self.z,new_start,self.radius*mult,self.height*mult)
        return new_cyl


class Conus:
    def __init__(self, x, y, z, start_coord, up_radius, down_radius, height):
        self.x = np.array(x)
        self.x = np.array(x) / np.linalg.norm(x)
        self.y = np.array(y)
        self.y = np.array(y) / np.linalg.norm(y)
        self.z = np.array(z)
        self.z = np.array(z) / np.linalg.norm(z)
        self.start_coord = np.array(start_coord)
        self.up_radius = up_radius
        self.down_radius = down_radius
        self.height = height

    def generate_points(self, Nz=10, N_phi=10, N_r_down=10, N_r_up=10, uniq=False):
        if uniq:
            uniq = 0.0
        else:
            uniq = 1.0

        u = np.repeat((np.arange(0, 1, 1.0 / N_phi) * 2 * np.pi).reshape((N_phi, 1)), Nz, axis=1)
        v = np.repeat((np.arange(0, Nz, 1.0) * (self.height / (Nz - 1.0))).reshape((1, Nz)), N_phi, axis=0)
        self.tan = (self.up_radius - self.down_radius) / self.height
        x = self.start_coord[0] + (self.down_radius + v * self.tan) * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + \
            self.z[0] * v
        y = self.start_coord[1] + (self.down_radius + v * self.tan) * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + \
            self.z[1] * v
        z = self.start_coord[2] + (self.down_radius + v * self.tan) * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + \
            self.z[2] * v
        self.bounds = np.concatenate((x.reshape((1, N_phi, Nz)),
                                      y.reshape((1, N_phi, Nz)),
                                      z.reshape((1, N_phi, Nz))), axis=0).reshape((3, -1))

        r = np.repeat((np.arange(0, N_r_down, 1.0) * (self.down_radius / (N_r_down - uniq))).reshape((1, N_r_down)),
                      N_phi, axis=0)
        u = np.repeat((np.arange(0, 1, 1.0 / N_phi) * 2 * np.pi).reshape((N_phi, 1)), N_r_down, axis=1)

        x = self.start_coord[0] + r * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + self.z[0] * 0
        y = self.start_coord[1] + r * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + self.z[1] * 0
        z = self.start_coord[2] + r * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + self.z[2] * 0
        x = x.reshape((1, N_r_down * N_phi))
        y = y.reshape((1, N_r_down * N_phi))
        z = z.reshape((1, N_r_down * N_phi))
        self.down = np.concatenate((x, y, z), axis=0)

        r = np.repeat((np.arange(0, N_r_up, 1.0) * (self.up_radius / (N_r_up - uniq))).reshape((1, N_r_up)), N_phi,
                      axis=0)
        u = np.repeat((np.arange(0, 1, 1.0 / N_phi) * 2 * np.pi).reshape((N_phi, 1)), N_r_up, axis=1)
        x = self.start_coord[0] + r * (self.x[0] * np.cos(u) + self.y[0] * np.sin(u)) + self.z[0] * self.height
        y = self.start_coord[1] + r * (self.x[1] * np.cos(u) + self.y[1] * np.sin(u)) + self.z[1] * self.height
        z = self.start_coord[2] + r * (self.x[2] * np.cos(u) + self.y[2] * np.sin(u)) + self.z[2] * self.height
        x = x.reshape((1, N_r_up * N_phi))
        y = y.reshape((1, N_r_up * N_phi))
        z = z.reshape((1, N_r_up * N_phi))
        self.up = np.concatenate((x, y, z), axis=0)

        self.coords = np.concatenate((self.down, self.bounds, self.up), axis=1)

        self.phi = np.arange(0, N_phi * 1.0, 1.0) * 2 * (np.pi / (N_phi - 1.0))
        x = self.start_coord[0] + self.down_radius * (self.x[0] * np.cos(self.phi) + self.y[0] * np.sin(self.phi)) + \
            self.z[
                0] * 0
        y = self.start_coord[1] + self.down_radius * (self.x[1] * np.cos(self.phi) + self.y[1] * np.sin(self.phi)) + \
            self.z[
                1] * 0
        z = self.start_coord[2] + self.down_radius * (self.x[2] * np.cos(self.phi) + self.y[2] * np.sin(self.phi)) + \
            self.z[
                2] * 0
        self.down_arc = np.concatenate((x.reshape((1, N_phi)), y.reshape((1, N_phi)), z.reshape((1, N_phi))), axis=0)
        x = self.start_coord[0] + self.up_radius * (self.x[0] * np.cos(self.phi) + self.y[0] * np.sin(self.phi)) + \
            self.z[
                0] * self.height
        y = self.start_coord[1] + self.up_radius * (self.x[1] * np.cos(self.phi) + self.y[1] * np.sin(self.phi)) + \
            self.z[
                1] * self.height
        z = self.start_coord[2] + self.up_radius * (self.x[2] * np.cos(self.phi) + self.y[2] * np.sin(self.phi)) + \
            self.z[
                2] * self.height
        self.up_arc = np.concatenate((x.reshape((1, N_phi)), y.reshape((1, N_phi)), z.reshape((1, N_phi))), axis=0)
        self.N_phi = N_phi

        lines1 = np.array(
            [(self.x * self.down_radius) + self.start_coord,
             (self.y * self.down_radius) + self.start_coord,
             ((-1) * self.x * self.down_radius) + self.start_coord,
             ((-1) * self.y * self.down_radius) + self.start_coord]).reshape(
            (4, 3, 1))

        lines2 = np.array(
            [(self.x * self.up_radius) + self.start_coord,
             (self.y * self.up_radius) + self.start_coord,
             ((-1) * self.x * self.up_radius) + self.start_coord,
             ((-1) * self.y * self.up_radius) + self.start_coord]).reshape(
            (4, 3, 1))

        self.lines = np.concatenate((lines1, lines2), axis=2)
        add = np.repeat(np.array(self.z).reshape(1, 3), 4, axis=0)
        self.lines[:, :, 1] = self.lines[:, :, 1] + add * self.height

    def draw(self, axis):
        color1 = np.random.random(3)
        color2 = color1 * 0.5

        #for i in range(self.coords.shape[1]):
        #    axis.plot(self.coords[0][i], self.coords[1][i], self.coords[2][i], ".", color=color1)

        for i in range(4):
            axis.plot([self.lines[i, 0, 0], self.lines[i, 0, 1]],
                      [self.lines[i, 1, 0], self.lines[i, 1, 1]],
                      [self.lines[i, 2, 0], self.lines[i, 2, 1]], color=color2)

        for i in range(self.N_phi):
            axis.plot([self.up_arc[0, i], self.up_arc[0, (i + 1) % self.N_phi]],
                      [self.up_arc[1, i], self.up_arc[1, (i + 1) % self.N_phi]],
                      [self.up_arc[2, i], self.up_arc[2, (i + 1) % self.N_phi]], color=color2)

        for i in range(self.down_arc.shape[1]):
            axis.plot([self.down_arc[0, i], self.down_arc[0, (i + 1) % self.N_phi]],
                      [self.down_arc[1, i], self.down_arc[1, (i + 1) % self.N_phi]],
                      [self.down_arc[2, i], self.down_arc[2, (i + 1) % self.N_phi]], color=color2)

        return np.min(self.coords, axis=1), np.max(self.coords, axis=1)

    def is_points_inside(self, coords, include_bounds=True):
        new_coords = coords - self.start_coord.reshape((3, 1))
        v = new_coords * np.repeat(self.z.reshape((3, 1)), coords.shape[1], axis=1)
        v = v.sum(axis=0).reshape(1, coords.shape[1])
        cos = (new_coords * np.repeat(self.x.reshape((3, 1)), coords.shape[1], axis=1))
        cos = cos.sum(axis=0).reshape(1, coords.shape[1])
        sin = (new_coords * np.repeat(self.y.reshape((3, 1)), coords.shape[1], axis=1))
        sin = sin.sum(axis=0).reshape(1, coords.shape[1])
        r = np.sqrt(cos * cos + sin * sin)
        if include_bounds:
            r = ((r >= 0).astype(int) * (r - v * self.tan <= self.down_radius).astype(int)).astype(bool)
            v = ((v >= 0).astype(int) * (v <= self.height).astype(int)).astype(bool)
        else:
            r = ((r >= 0).astype(int) * (r - v * self.tan < self.down_radius).astype(int)).astype(bool)
            v = ((v > 0).astype(int) * (v < self.height).astype(int)).astype(bool)

        ans = ((r.astype(int)) * (v.astype(int))).astype(bool)
        return ans.reshape((ans.shape[1],))

    def get_around_points(self, mult):
        new_start = self.start_coord+0.5*(1.0-mult)*self.z*self.height
        new_con = Conus(self.x,self.y,self.z,new_start,self.up_radius*mult,self.down_radius*mult,self.height*mult)
        return new_con






