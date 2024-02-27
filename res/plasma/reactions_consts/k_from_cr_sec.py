import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import CubicSpline
from scipy.special import gamma
from res.plasma.consts import m_e, e, k_b


def give_sigma(filename):
    f = open(filename)
    A = f.readlines()
    f.close()
    Engs = []
    Sigmas = []
    for line in A:
        line = np.array(line.split()).astype(float)
        Engs.append(line[0])
        Sigmas.append(line[1]*0.0001)
    spl = CubicSpline(Engs, Sigmas)
    return spl


def Maxvell_EEDF(energy,T_e):
    return (T_e**(-1.5))*np.sqrt((gamma(2.5)**3)/(gamma(1.5)**5))*np.exp((-energy*gamma(2.5))/(T_e*gamma(1.5)))


def give_reaction_const(filename, up=10):
    spl = give_sigma(filename)

    def int_fun(en, T_e):
        return np.sqrt((2*e)/m_e)*spl(en)*en*Maxvell_EEDF(en,T_e)

    def give_k(T_e):
        T_ev = T_e / (e / k_b)
        result = integrate.quad(lambda x: int_fun(x, T_ev), 0, up)
        return result[0]

    return give_k