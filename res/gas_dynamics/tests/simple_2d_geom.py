import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import trange

from res.step.geometry.geometry2d import Reactor
from res.step.geometry.proc_functions import give_points_field2d
from res.gas_dynamics.algorithm.gas_dynamics import initgrid, step_custom, step_custom_njit
from res.const.modeling_params import DELTA_T

start = time.time()
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
reactor = Reactor()
gl_min, gl_max = reactor.draw(ax)
koeff = 0.8
N = 500
Nx = N
Ny = int(koeff*N)
coords, delta_x, delta_y = give_points_field2d(gl_min, gl_max, Nx=Nx, Ny=Ny, rand=0)
ans, is_inlet, is_outlet, is_boundary = reactor.is_points_inside(coords, delta_x, delta_y)
is_x_walls, is_y_walls, is_inl_walls = is_boundary
end_ins = time.time()
print("Preprocessing modelling points: ", round(end_ins-start, 1), " seconds")
#print("Boundary")
#print((is_x_walls*is_y_walls).sum())
#print((is_x_walls*is_inl_walls).sum())
#print((is_y_walls*is_inl_walls).sum())
#print("Inlet")
#print((is_x_walls*is_inlet).sum())
#print((is_y_walls*is_inlet).sum())
#print("Outlet")
#print((is_x_walls*is_outlet).sum())
#print((is_y_walls*is_outlet).sum())
#print("BN x Inlet", (is_inl_walls*is_inlet).sum())


grid1 = initgrid(Nx,Ny,ans.reshape((Nx, Ny)))
grid2 = initgrid(Nx,Ny,ans.reshape((Nx, Ny)))
Times_norm = []
Times_njit = []
for i in trange(20):
    start_counting = time.time()
    grid1 = step_custom(grid1, ans.reshape((Nx, Ny)), is_inlet.reshape((Nx, Ny)),is_outlet.reshape((Nx, Ny)),
                         is_x_walls.reshape((Nx, Ny)), is_y_walls.reshape((Nx, Ny)), is_inl_walls.reshape((Nx, Ny)),
                         delta_x, delta_y, DELTA_T)
    end_counting = time.time()
    Times_norm.append(end_counting-start_counting)
    start_counting = time.time()
    grid2 = step_custom_njit(grid2, ans.reshape((Nx, Ny)), is_inlet.reshape((Nx, Ny)), is_outlet.reshape((Nx, Ny)),
                       is_x_walls.reshape((Nx, Ny)), is_y_walls.reshape((Nx, Ny)), is_inl_walls.reshape((Nx, Ny)),
                       delta_x, delta_y, DELTA_T)
    end_counting = time.time()
    Times_njit.append(end_counting - start_counting)
Times_norm = np.array(Times_norm)
Times_njit = np.array(Times_njit)
print("Pure python: ",round(Times_norm.mean(),2)," seconds")
print("Numba: ",round(Times_njit.mean(),3)," seconds")
#print("Counting time: ", round(end_counting-start_counting,1))

for i in range(len(ans)):
    if is_inlet[i]:
        ax.plot(coords[0, i], coords[1, i], ".", color="r")
    elif is_outlet[i]:
        pass
        ax.plot(coords[0, i], coords[1, i], ".", color="b")
    elif is_x_walls[i]:
        pass
        ax.plot(coords[0, i], coords[1, i], ".", color=(0.3,0.7,0.5))
    elif is_y_walls[i]:
        pass
        ax.plot(coords[0, i], coords[1, i], ".", color=(0.7,0.3,0.5))
    elif is_inl_walls[i]:
        pass
        ax.plot(coords[0, i], coords[1, i], ".", color=(0.3,0.3,0.3))
    elif ans[i]:
        pass
        ax.plot(coords[0, i], coords[1, i], ".", color="g")



ax.grid()



end_plot = time.time()
print("Plotting: ", round(end_plot-end_counting, 1), " seconds")
plt.show()


