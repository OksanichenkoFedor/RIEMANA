import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import trange

from res.geometry.geometry2d import Reactor, TestReactor
from res.geometry.proc_functions import give_points_field2d
from res.counting.gas_dynamics import initgrid, step_custom_njit
from res.const.modeling_params import DELTA_T


koeff = 0.8
N = 40

reactor = TestReactor()
Nx = N
Ny = int(koeff * N)
gl_min, gl_max = reactor.give_axis_bounds()
coords, delta_x, delta_y = give_points_field2d(gl_min, gl_max, Nx=Nx, Ny=Ny, rand=0)

ans, is_inlet, is_outlet, is_boundary = reactor.is_points_inside(coords, delta_x, delta_y)
is_x_walls, is_y_walls = is_boundary

#fig = plt.figure(figsize=(12, 8))
#ax = fig.add_subplot(111)
#reactor.draw(ax)
#plt.show()

grid = initgrid(Nx, Ny, ans.reshape((Nx, Ny)))
Times = []
Q_outs = []
Q_ins = []
for i in trange(200000):
    start_counting = time.time()
    newgrid = step_custom_njit(grid, ans.reshape((Nx, Ny)).astype(int), is_inlet.reshape((Nx, Ny)).astype(int),
                               is_outlet.reshape((Nx, Ny)).astype(int), is_x_walls.reshape((Nx, Ny)).astype(int),
                               is_y_walls.reshape((Nx, Ny)).astype(int),
                               np.zeros((Nx, Ny)), delta_x, delta_y, DELTA_T)
    delta_rho = np.abs(grid[2] - newgrid[2]).sum() / (Nx * Ny * 0.00001)
    delta_u = np.abs(grid[0] - newgrid[0]).sum() / (Nx * Ny * 0.00001)
    delta_v = np.abs(grid[1] - newgrid[1]).sum() / (Nx * Ny * 0.00001)
    r0 = (grid[2].reshape((Nx * Ny,)) * (ans).astype(int)).sum()
    grid = newgrid
    q_out = -(newgrid[0].reshape((Nx * Ny,)) * newgrid[2].reshape((Nx * Ny,)) * (is_outlet).astype(int)).sum()
    q_in = -(newgrid[0].reshape((Nx * Ny,)) * newgrid[2].reshape((Nx * Ny,)) * (is_inlet).astype(int)).sum()

    r = (newgrid[2].reshape((Nx * Ny,)) * (ans).astype(int)).sum()

    alpha = (r0)/(r)

    #newgrid[2] = newgrid[2]*alpha

    if i % 1000== 0:

        print("Iteration ", i, ": ", round(delta_rho, 7), round(delta_u, 7), round(delta_v, 7))
        #print(r0, r)
        #print(alpha)
        print("Q_out: ",q_out)
        Q_outs.append(q_out)
        Q_ins.append(q_in)
        print("Q_in: ", q_in)
        print("Rho: ",r)
    end_counting = time.time()
    Times.append(end_counting - start_counting)
    if i>0 and i%1000==0:
        pass
        #fig = plt.figure(figsize=(12, 8))
        #ax = fig.add_subplot(111)
        #reactor.draw(ax, grid[0].reshape((Nx * Ny,)), grid[1].reshape((Nx * Ny,)))
        #reactor.draw(ax, grid[2].reshape((Nx * Ny,)))
        #plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.semilogy(Q_outs, label="Q_out")
ax.semilogy(Q_ins, label="Q_ins")
ax.grid()
ax.legend()
#reactor.draw(ax, grid[0].reshape((Nx * Ny,)), grid[1].reshape((Nx * Ny,)))
plt.show()