from res.gloabal_tests.for_diploma.funks import parce_wafer
import os
from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np

fig, axises = plt.subplots(1, 1, figsize=(13, 11))
parce_wafer("../../data/diff_tests/wafer_only_i3.zip", x_cut=80, y_end=150, axis=axises)
plt.show()