import numpy as np
from numba import jit

k_b = 1.388 * 10.0 ** (-23)
e = 1.602 * 10.0 ** (-19)

k_ii = 5.0 * 10.0 ** (-14)


@jit(nopython=True)
def give_k_getero(T_e, m_i, beta_s, gamma_T, d_c, gamma=1):
    return (np.sqrt((k_b * T_e * (1 + beta_s)) / (m_i * (1 + beta_s * gamma_T))) / d_c) * gamma
