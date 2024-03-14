import numpy as np
from numba import jit


@jit(nopython=True)
def count_min_beta_s(gamma_T):
    b = 6 * gamma_T - 1 - gamma_T ** 2
    beta_s = (-b + np.sqrt(b ** 2 - 16 * gamma_T * gamma_T)) / (4 * gamma_T ** 2)
    return beta_s

@jit(nopython=True)
def count_min_beta(gamma_T):
    beta_s = count_min_beta_s(gamma_T)
    beta = beta_s*np.exp(((1+beta_s)*(gamma_T-1))/(2*(1+beta_s*gamma_T)))
    return beta

@jit(nopython=True)
def count_min_gamma_T(beta):
    beta_min = count_min_beta(5.0+np.sqrt(24.0)+0.00001)
    left_gamma = 5 + np.sqrt(24)
    right_gamma = 10000000
    delta = 1
    while np.abs(delta) > 10.0**(-5):
        curr_gamma = 0.5*(left_gamma+right_gamma)
        c_beta = count_min_beta(curr_gamma)
        delta = c_beta-beta
        if delta>0:
            right_gamma = curr_gamma
        else:
            left_gamma = curr_gamma
    return curr_gamma

@jit(nopython=True)
def pure_count_beta_s(beta, gamma_T):
    delta = 1
    num = 0
    b = 6 * gamma_T - 1 - gamma_T ** 2
    if b ** 2 - 16 * gamma_T * gamma_T < 0:
        beta_min = 0
        beta_max = 10000
        d = 2
    elif count_min_beta(gamma_T) < beta:
        beta_min = count_min_beta_s(gamma_T)
        beta_max = 10000
        d = 0
    else:
        beta_min = 0
        beta_max = (-b - np.sqrt(b ** 2 - 16 * gamma_T * gamma_T)) / (4 * gamma_T ** 2)
        d = 1

    num = 0
    while delta > 10**(-5):
        beta_s = 0.5*(beta_min+beta_max)
        delta = beta_s*np.exp(((1+beta_s)*(gamma_T-1))/(2*(1+beta_s*gamma_T))) - beta
        if delta > 0:
            beta_max = beta_s
        else:
            beta_min = beta_s
        delta = np.abs(delta / min(beta_s, 1))
        if np.log(beta_s)/np.log(10)<-10 and d==1:
            delta = 0
            beta_s = 0
        num+=1


    return beta_s, num

@jit(nopython=True)
def count_beta_s(n_e, n_cl_minus, T_e, T_i):
    beta = n_cl_minus / n_e
    gamma_T = T_e / T_i

    beta_s, num = pure_count_beta_s(beta, gamma_T)

    return beta, gamma_T, beta_s
