from res.geometry import Cylinder, Conus
from res.const.geom_const import *
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_box_aspect((1, 1, 1))

drawable = []
reactor = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, 0], R_REACTOR, H_REACTOR)
reactor.generate_points(20, 40, 10)
drawable.append(reactor)

dno = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, 0], R_DN0, H_DNO)
dno.generate_points(10, 25, 8)
drawable.append(dno)

wafer = Cylinder(X_NORM, Y_NORM, Z_NORM, [0, 0, H_DNO], R_WAFER, H_WAFER)
wafer.generate_points(10, 25, 8)
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
    #drawable.append(curr_inlet)

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

N = 10
print(min_coord.shape,min_coord)
print(max_coord.shape,max_coord)
x = min_coord[0,0]+np.arange(0,N,1.0)*((max_coord[0,0]-min_coord[0,0])/(1.0*N-1.0))
print("x: ",x)
x = np.repeat(np.repeat(x.reshape(N,1,1),N,axis=1),N,axis=2).reshape(N,N,N,1)
#print("X: ",x)
y = min_coord[1,0]+np.arange(0,N,1.0)*((max_coord[1,0]-min_coord[1,0])/(1.0*N-1.0))
print("y: ",y)
y = np.repeat(np.repeat(y.reshape(1,N,1),N,axis=0),N,axis=2).reshape(N,N,N,1)
#print("Y: ",y)
z = min_coord[2,0]+np.arange(0,N,1.0)*((max_coord[2,0]-min_coord[2,0])/(1.0*N-1.0))
print("z: ",z)
z = np.repeat(np.repeat(z.reshape(1,1,N),N,axis=1),N,axis=0).reshape(N,N,N,1)
#print("Z: ",z)
coords = np.concatenate((x,y,z),axis=3)
coords = coords+(np.random.random(coords.shape)-0.5)*0.05
coords = coords.reshape(N*N*N,-1).T
ans_r = reactor.is_points_inside(coords)
ans_c = con.is_points_inside(coords)
ans_d = dno.is_points_inside(coords)
ans_w = wafer.is_points_inside(coords)
ans = ((ans_r.astype(int)+ans_c.astype(int))*(1-ans_d.astype(int))*(1-ans_w.astype(int))).astype(bool)
for i in range(len(ans)):
    if ans[i]:
        color="g"
        ax.plot(coords[0, i], coords[1, i], coords[2, i], ".", color=color)
    else:
        color="r"
        #ax.plot(coords[0, i], coords[1, i], coords[2, i], ".", color=color)





plt.show()
