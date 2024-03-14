from numba import jit
import numpy as np
import time

k_b = 1.388*10.0**(-23)
e = 1.602*10.0**(-19)

x = np.arange(100).reshape(10, 10)
A_Ar = 1.235*10.0**(-13)
B_Ar = 0
C_Ar = 18.69
@jit(nopython=True)
def f1(T_e):
    return A_Ar * ((T_e) ** B_Ar) * np.exp((-1 * C_Ar) / (T_e))

@jit(nopython=True)
def f2(T_e):
    return 1.235*10.0**(-13) * ((T_e) ** 0) * np.exp((-1 * 18.69) / (T_e))
# DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
start = time.perf_counter()
f1(2)
end = time.perf_counter()
print("Elapsed (with compilation) = {}s".format((end - start)))
# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
start = time.perf_counter()
f1(2)
end = time.perf_counter()
print("Elapsed (after compilation) = {}s".format((end - start)))


start = time.perf_counter()
f2(2)
end = time.perf_counter()
print("Elapsed (with compilation) = {}s".format((end - start)))
# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
start = time.perf_counter()
f2(2)
end = time.perf_counter()
print("Elapsed (after compilation) = {}s".format((end - start)))
