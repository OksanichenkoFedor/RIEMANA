import numpy as np


def good_form(num):
    integ = int(np.log(num)/np.log(10))
    ost = num / (10.0**(integ))
    return str(round(ost,3))+"*10^"+str(integ)

print(good_form(14560000000))

