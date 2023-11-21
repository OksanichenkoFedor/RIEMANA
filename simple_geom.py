import numpy as np

from res.geometry.geometry import Cylinder, Conus
from res.const.geom_const import *
from res.geometry.proc_functions import give_points_field, give_inlets_surroundings
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_box_aspect((1, 1, 1))

drawable = []
reactor = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, 0], R_REACTOR, H_REACTOR)
reactor.generate_points(Nz=20, N_phi=40, N_r=10)
drawable.append(reactor)

dno = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, 0], R_DN0, H_DNO)
dno.generate_points(Nz=10, N_phi=32, N_r=8)
drawable.append(dno)

wafer = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, H_DNO], R_WAFER, H_WAFER)
wafer.generate_points(Nz=10, N_phi=32, N_r=8)
drawable.append(wafer)

inlets = []
for i in range(8):
    curr_z = np.array([np.cos(i * DELTA_PHI), np.sin(i * DELTA_PHI), Z_PHI])
    curr_x = np.array([-np.sin(i * DELTA_PHI), np.cos(i * DELTA_PHI), 0])
    curr_y = np.cross(curr_z, curr_x)
    curr_inlet = Cylinder(curr_x, curr_y, curr_z,
                          [R_LOC_INLET * np.cos(i * DELTA_PHI), R_LOC_INLET * np.sin(i * DELTA_PHI), H_LOC_INLET],
                          R_INLET, L_INLET)
    curr_inlet.generate_points(5, 10, 8)
    inlets.append(curr_inlet)
    drawable.append(curr_inlet)




con = Conus(X_NORM,Y_NORM,Z_NORM,[0,0,H_REACTOR],R_CON_UP,R_CON_DOWN,H_CON)
con.generate_points(Nz=10,N_phi=20,N_r_down=10,N_r_up=8)
drawable.append(con)





gl_min, gl_max = np.array([0, 0, 0]).reshape(3,1), np.array([0, 0, 0]).reshape(3,1)
for el in drawable:
    curr_min, curr_max = el.draw(ax)
    gl_min = np.min(np.concatenate((curr_min.reshape(3,1),gl_min),axis=1),axis=1).reshape(3,1)
    gl_max = np.max(np.concatenate((curr_max.reshape(3,1),gl_max),axis=1), axis=1).reshape(3,1)

mid_coord = 0.5 * (gl_max+gl_min)
delta = 0.5 * np.max(gl_max - gl_min)
min_coord = mid_coord - delta
max_coord = mid_coord + delta
ax.set_xlim(min_coord[0, 0], max_coord[0, 0])
ax.set_ylim(min_coord[1, 0], max_coord[1, 0])
ax.set_zlim(min_coord[2, 0], max_coord[2, 0])

con_inl = con.get_around_points(0.9)
con_inl.generate_points(Nz=10,N_phi=20,N_r_down=10,N_r_up=8)

react_2 = reactor.get_around_points(0.9)
react_2.generate_points(Nz=10, N_phi=64, N_r=60)

dno_surr = dno.get_around_points(1.1)
dno_surr.generate_points(Nz=10, N_phi=64, N_r=16)

w_sur = wafer.get_around_points(1.1)
w_sur.generate_points(Nz=10, N_phi=32, N_r=8)

inside_walls = np.concatenate((react_2.bounds,react_2.down,con_inl.bounds, dno_surr.bounds,dno_surr.up, w_sur.up, w_sur.bounds),axis=1)


coords = give_points_field(min_coord, max_coord, 10)

in_surr1 = give_inlets_surroundings(inlets,mult=2,N_phi=16,Nz=30,N_r=8)
in_surr2 = give_inlets_surroundings(inlets,mult=4,N_phi=8,Nz=20,N_r=8)

in_surr2 = give_inlets_surroundings(inlets,mult=10,N_phi=8,Nz=10,N_r=4)

coords = np.concatenate((coords,inside_walls,in_surr1,in_surr2),axis=1)


inlet_anses = []
for i in range(8):
    c_ans = inlets[i].is_points_inside(coords, include_bounds=False)
    inlet_anses.append(c_ans)
ans_r = reactor.is_points_inside(coords)
ans_c = con.is_points_inside(coords)
ans_d = dno.is_points_inside(coords,include_bounds=False)
ans_w = wafer.is_points_inside(coords,include_bounds=False, include_down=True)
ans = (ans_r.astype(int)+ans_c.astype(int))*(1-ans_d.astype(int))*(1-ans_w.astype(int))
for i in range(8):
    ans = ans*(1-c_ans.astype(int))
ans = ans.astype(bool)
new_coords = []
for i in range(len(ans)):
    if ans[i]:
        color="g"
        #ax.plot(coords[0, i], coords[1, i], coords[2, i], ".", color=color)
        new_coords.append([coords[0, i], coords[1, i], coords[2, i]])

new_coords = np.array(new_coords)
print("Используем: ",new_coords.shape," точек.")

for coord in new_coords:
    ax.plot(coord[0], coord[1], coord[2], ".", color=color)





plt.show()
