import numpy as np
import matplotlib.pyplot as plt
from res.counting.wafer_reactions import process_particles
import time
Ns = [1,10]
border = 500
xsize = 2000
ysize = 1800
left_area = 900
right_area = 1100
mask_height = 100
y0 = 0#ysize-1
is_full = np.fromfunction(lambda i, j: j>=border, (xsize, ysize), dtype=int).astype(int)
counter_arr = is_full.copy()*Ns[0]
#---
mask = np.ones((xsize, ysize))
mask[:,:border] = mask[:,:border]*0
mask[:,border+mask_height:border+mask_height+800] = mask[:,border+mask_height:border+mask_height+800]*0
mask[left_area:right_area,:border+mask_height+800] = mask[left_area:right_area,:border+mask_height+800]*0
is_full=mask+is_full
#print(is_full)





def plot_cells(arr_is_full, axis):

    axis.imshow(1.0-is_full.T, cmap="inferno")
    axis.set_ylim([ysize-0.5,-0.5])
    axis.set_xlim([-0.5,xsize-0.5])
    axis.set_yticks(np.arange(0, ysize, 1)-0.5, minor=True)
    axis.set_xticks(np.arange(0, xsize, 1)-0.5, minor=True)
    axis.set_yticks(np.arange(0, ysize, 100)-0.5)
    axis.set_xticks(np.arange(0, xsize, 100)-0.5)
    #axis.grid(which='minor', alpha=0.2)
    axis.grid(which='major', alpha=0.5)



def generate_particles(num):
    x = np.random.random((num,1))*xsize
    angle = np.random.random((num,1))*np.pi - np.pi*0.5
    angle = np.where(angle<0,angle+2*np.pi,angle)
    #angle = np.random.random() * np.pi + np.pi * 0.5
    #angle = np.random.random() * np.pi*2.0
    is_add = (np.random.random((num,1))>0.99).astype(float)
    return np.concatenate((x,angle,is_add),axis=1)#[x, angle, is_add]

print(generate_particles(2))

def plot_particle(params, axis, alpha=1.0):
    color = "r"
    if params[2]:
        color = "g"
    print(10*np.sin(params[1]),10*np.cos(params[1]))
    axis.arrow(params[0]-0.5, y0-0.5, 2*np.sin(params[1]), 2*np.cos(params[1]),color=color,linewidth=2, alpha = alpha)

old_p = None
for i in range(100):
    #fig = plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(1, 1, 1)
    params = []
    #plot_cells(is_full, ax)
    if old_p is None:
        pass
    else:
        pass
        #plot_particle(new_p, ax, alpha=0.5)
    t1 = time.time()
    params = generate_particles(1000000)
    t2 = time.time()
    process_particles(counter_arr, is_full, params, Ns, xsize, ysize, y0)
    t3 = time.time()
    print(t3-t2)
    #plt.show()







