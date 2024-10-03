from res.getero.algorithm.monte_carlo import generate_particles
import numpy as np
import matplotlib.pyplot as plt

from res.getero.tests.tests_internal_funcks.help_test_funks import create_test_wafer
from res.global_entities.plotter import generate_figure

wafer = create_test_wafer(num_del=100)
wafer.make_half()

A = generate_particles(1000000, wafer.xsize, 0.5, 0.1, 0.3, 1/23.6, 40, 0)
print(A.shape, A[:,0].min(), A[:,0].max())
#print(A[])

plt.hist(A[:,0],bins=200)
#plt.hist(np.random.random(100000), bins=200)
plt.show()

f = generate_figure(wafer, wafer_curr_type="is_cell", do_plot_line=True)
plt.show()

#print("-------------------")
#print(np.random.choice(4,10,p=[0.1,0.3,0.2,0.4]))
