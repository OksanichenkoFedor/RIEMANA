import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


from res.plasma.start_params import T_gas, R, L, gamma_cl, W
from res.plasma.old_models.consist_model import run_consist_model
from res.plasma.consts import e, k_b


res = run_consist_model(5*0.13333, T_gas, R, L, gamma_cl, 0, W, plot_error=True)