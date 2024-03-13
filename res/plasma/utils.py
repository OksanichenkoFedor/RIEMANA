import numpy as np
do_print = False

def good_form(num):
    if num == 0.0:
        return "0.0"
    elif str(num) == "inf":
        return "inf"
    # print(num)
    integ = int(np.log(num) / np.log(10))
    ost = num / (10.0 ** (integ))
    return str(round(ost, 5)) + "*10^" + str(integ)

#def iprint(*args):
#    if do_print:
#        print(args)