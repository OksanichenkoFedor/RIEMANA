import numpy as np
from numba import jit

@jit(nopython=True)
def give_k(params, T_e):
    return params[0]*(T_e**params[1])*np.exp(params[2]/T_e + params[3]/(T_e**2) + params[4]/(T_e**3) +
                                             params[5]/(T_e**4) + params[6]/(T_e**5))

@jit(nopython=True)
def count_inel_power(T_e, curr_ens_data):
    inel_power = 0
    for i in range(len(curr_ens_data)):
        inel_power += give_k(curr_ens_data[i][:-1], T_e) * curr_ens_data[i][-1]
    return inel_power