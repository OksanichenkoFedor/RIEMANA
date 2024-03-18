import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
from res.getero.algorithm.main_cycle import process_particles
from res.wafer.grafic_funcs import plot_cells
from res.wafer.monte_carlo import generate_particles
import res.config.getero_reactions as config
import time


is_full = np.fromfunction(lambda i, j: j>=config.border, (config.xsize, config.ysize), dtype=int).astype(int)
counter_arr = is_full.copy()*config.Ns[0]
#---
mask = np.ones((config.xsize, config.ysize))
mask[:,:config.border] = mask[:,:config.border]*0
mask[:,config.border+config.mask_height:config.border+config.mask_height+config.silicon_size] = mask[:,config.border+config.mask_height:config.border+config.mask_height+config.silicon_size]*0
mask[config.left_area:config.right_area,:config.border+config.mask_height+config.silicon_size] = mask[config.left_area:config.right_area,:config.border+config.mask_height+config.silicon_size]*0
is_full=mask+is_full





print(generate_particles(2, config.xsize))



old_p = None
Times = []
for i in trange(300):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1)
    params = []
    plot_cells(ax, is_full, config.ysize, config.xsize)
    if old_p is None:
        pass
    else:
        pass
        #plot_particle(new_p, ax, y0, alpha=0.5)
    t1 = time.time()
    params = generate_particles(200000,config.xsize)
    t2 = time.time()
    process_particles(counter_arr, is_full, params, config.Ns, config.xsize, config.ysize, config.y0)
    t3 = time.time()
    #print(t3-t2)
    Times.append(t3-t2)
    plt.show()

Times = np.array(Times[1:])
print(Times.mean())
print(Times.std())







