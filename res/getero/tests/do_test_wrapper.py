import numpy as np

import time
from res.utils.wrapper import clever_njit


@clever_njit(do_njit=False)
def count_sum(A):
    s = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            s+=A[i,j]
    return s

@clever_njit(do_njit=True, parallel=True)
def count_sum1(A):
    s = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            s+=A[i,j]
    return s



#nc = wr(count_sum)

count_sum1(np.array([[1,2,3,4,5,6]]))
A = np.random.random((2000,2000))
start = time.time()
count_sum(A)
end = time.time()
print(end-start)
#A = np.random.random((2000,2000))
start = time.time()
count_sum1(A)
end = time.time()
print(end-start)

