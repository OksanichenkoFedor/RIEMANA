import numpy as np
import res.utils.config as config
seed = np.random.randint(0, 100)
#seed = 66
seed = 40
print("Numpy random seed: ",seed)
#np.random.seed(seed)
#config.seeder.init_seed(seed)
config.seed = seed
from res.getero.frontend.panel import AppFrame
from tkinter import Tk



root = Tk()
app = AppFrame()
root.mainloop()