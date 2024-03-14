import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


from res.plasma.start_params import T_gas, R, L, gamma_cl, W
from res.plasma.models.consist_model_aclr import run_consist_model
from res.plasma.consts import e, k_b


res = run_consist_model(p_0=10*0.13333, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.2, W=600, plot_error=True)