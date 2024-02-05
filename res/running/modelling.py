import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import trange

from res.geometry.geometry2d import Reactor
from res.geometry.proc_functions import give_points_field2d
from res.counting.gas_dynamics import initgrid, step_custom_njit
from res.const.modeling_params import DELTA_T

koeff = 0.8
N = 2000

start = time.time()

reactor = Reactor()
gl_min, gl_max = reactor.give_axis_bounds()
Nx = N
Ny = int(koeff * N)
coords, delta_x, delta_y = give_points_field2d(gl_min, gl_max, Nx=Nx, Ny=Ny, rand=0)
ans, is_inlet, is_outlet, is_boundary = reactor.is_points_inside(coords, delta_x, delta_y)
is_x_walls, is_y_walls, is_inl_walls = is_boundary
end_ins = time.time()
print("Preprocessing: ", round(end_ins - start, 1), " seconds")

grid = initgrid(Nx, Ny, ans.reshape((Nx, Ny)))
Times = []
for i in trange(100):
    start_counting = time.time()
    newgrid = step_custom_njit(grid, ans.reshape((Nx, Ny)), is_inlet.reshape((Nx, Ny)), is_outlet.reshape((Nx, Ny)),
                               is_x_walls.reshape((Nx, Ny)), is_y_walls.reshape((Nx, Ny)),
                               is_inl_walls.reshape((Nx, Ny)),
                               delta_x, delta_y, DELTA_T,i)
    delta_rho = np.abs(grid[2] - newgrid[2]).sum() / (Nx * Ny * 0.0001)
    delta_u = np.abs(grid[0] - newgrid[0]).sum() / (Nx * Ny * 0.0001)
    delta_v = np.abs(grid[1] - newgrid[1]).sum() / (Nx * Ny * 0.0001)
    grid = newgrid
    if i % 40 == 0:
        print("Iteration ", i, ": ", round(delta_rho, 7), round(delta_u, 7), round(delta_v, 7))
    end_counting = time.time()
    Times.append(end_counting - start_counting)


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
reactor.draw(ax)
plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
reactor.draw(ax, newgrid[0].reshape((Nx * Ny,)), newgrid[1].reshape((Nx * Ny,)))
plt.show()
