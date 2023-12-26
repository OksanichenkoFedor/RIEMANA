import numpy as np
from res.const.modeling_params import RHO, MU, V0
from res.const.geom_const import COS_ALPHA, SIN_ALPHA
from numba import njit


@njit()
def initgrid(gridx, gridy, is_inside):
    grid = np.zeros((3, gridx, gridy))
    grid[0] = np.ones((gridx, gridy)) * 0.0  # u
    grid[1] = np.ones((gridx, gridy)) * 0.0  # v
    grid[2] = RHO * np.ones((gridx, gridy))  # pho

    return grid


@njit()
def step_custom_njit(grid, is_inside, is_inlet, is_outlet, is_x_walls, is_y_walls, is_inl_walls, dx, dy, dt):
    newgrid = grid.copy()
    u = grid[0]
    v = grid[1]
    rho = grid[2]
    for x in range(1, newgrid.shape[1] - 1):
        for y in range(1, newgrid.shape[2] - 1):
            # rho (1.3.1.2-1.3.1.4)
            delta_pho_x = rho[x + 1, y] * u[x, y] + u[x + 1, y] * rho[x, y] - 2 * u[x, y] * rho[x, y]  # 1.3.1.3
            delta_pho_y = rho[x, y + 1] * u[x, y] + u[x, y + 1] * rho[x, y] - 2 * u[x, y] * rho[x, y]  # 1.3.1.4
            new_rho = rho[x, y] - ((dt) / (dx)) * (delta_pho_x) - ((dt) / (dy)) * (delta_pho_y)  # 1.3.1.2

            # u (1.3.2.6-1.3.2.10)
            delta_u_xx = u[x - 1, y] + u[x + 1, y] - 2 * u[x, y]  # 1.3.2.8
            delta_v_xy = v[x + 1, y + 1] + v[x, y] - v[x + 1, y] - v[x, y + 1]  # 1.3.2.9
            delta_u_yy = u[x, y - 1] + u[x, y + 1] - 2 * u[x, y]  # 1.3.2.10
            #delta_mu_x = (MU / (3.0 * rho[x, y])) * (
            #        4.0 * (dt / (dx * dx)) * delta_u_xx +
            #        1.0 * (dt / (dx * dy)) * delta_v_xy +
            #        3.0 * (dt / (dy * dy)) * delta_u_yy)  # 1.3.2.7
            delta_mu_x = (MU / (3.0 * 1.0)) * (
                    4.0 * (dt / (dx * dx)) * delta_u_xx +
                    1.0 * (dt / (dx * dy)) * delta_v_xy +
                    3.0 * (dt / (dy * dy)) * delta_u_yy)  # 1.3.2.7
            new_u = u[x, y] - (dt / dx) * u[x, y] * (u[x + 1, y] - u[x, y]) - \
                    (dt / dy) * v[x, y] * (u[x, y + 1] - u[x, y]) + delta_mu_x  # 1.3.2.6

            # v (1.3.3.6-1.3.3.10)
            delta_v_yy = v[x, y - 1] + v[x, y + 1] - 2 * v[x, y]  # 1.3.3.8
            delta_u_xy = u[x + 1, y + 1] + u[x, y] - u[x + 1, y] - u[x, y + 1]  # 1.3.3.9
            delta_v_xx = v[x - 1, y] + v[x + 1, y] - 2 * v[x, y]  # 1.3.3.10
            #delta_mu_y = (MU / (3.0 * rho[x, y])) * (
            #        4.0 * (dt / (dy * dy)) * delta_v_yy +
            #        1.0 * (dt / (dx * dy)) * delta_u_xy +
            #        3.0 * (dt / (dx * dx)) * delta_v_xx)  # 1.3.3.7
            delta_mu_y = (MU / (3.0 * 1.0)) * (
                    4.0 * (dt / (dy * dy)) * delta_v_yy +
                    1.0 * (dt / (dx * dy)) * delta_u_xy +
                    3.0 * (dt / (dx * dx)) * delta_v_xx)  # 1.3.3.7
            new_v = v[x, y] - (dt / dx) * u[x, y] * (v[x + 1, y] - v[x, y]) - \
                    (dt / dy) * v[x, y] * (v[x, y + 1] - v[x, y]) + delta_mu_y  # 1.3.2.6

            newgrid[0, x, y] = new_u * is_inside[x, y]
            newgrid[1, x, y] = new_v * is_inside[x, y]
            newgrid[2, x, y] = new_rho# * is_inside[x, y]

    return boundary_step_njit(newgrid, is_inlet, is_outlet, is_x_walls, is_y_walls, is_inl_walls)


@njit()
def boundary_step_njit(grid, is_inlet, is_outlet, is_x_walls, is_y_walls, is_inl_walls):
    newgrid = grid.copy()
    u = grid[0]
    v = grid[1]
    rho = grid[2]
    for x in range(0, newgrid.shape[1] - 0):
        for y in range(0, newgrid.shape[2] - 0):
            newgrid[2, x, y] = rho[x, y]

            # vertic and horiz walls
            newgrid[0, x, y] = u[x, y] * (1.0 - is_y_walls[x, y] - is_outlet[x, y])
            newgrid[1, x, y] = v[x, y] * (1.0 - is_x_walls[x, y])

            # inlet
            #newgrid[0, x, y] = newgrid[0, x, y] * (1.0 - is_inlet[x, y]) - is_inlet[x, y] * SIN_ALPHA * V0
            #newgrid[1, x, y] = newgrid[1, x, y] * (1.0 - is_inlet[x, y]) - is_inlet[x, y] * COS_ALPHA * V0
            newgrid[0, x, y] = newgrid[0, x, y] * (1.0 - is_inlet[x, y]) - is_inlet[x, y] * 1 * V0
            newgrid[1, x, y] = newgrid[1, x, y] * (1.0 - is_inlet[x, y]) - is_inlet[x, y] * 0 * V0

            # inl walls
            PSP = newgrid[0, x, y] * COS_ALPHA + newgrid[1, x, y] * SIN_ALPHA
            newgrid[0, x, y] = newgrid[0, x, y] * (1.0 - is_inl_walls[x, y]) - is_inl_walls[x, y] * COS_ALPHA * PSP
            newgrid[1, x, y] = newgrid[1, x, y] * (1.0 - is_inl_walls[x, y]) + is_inl_walls[x, y] * SIN_ALPHA * PSP

    return newgrid