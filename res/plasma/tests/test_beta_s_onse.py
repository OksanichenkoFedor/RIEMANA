import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import time
from res.plasma.algorithm.beta_s import count_min_beta_s, count_min_beta

def count_beta_s(beta, gamma_T, max_iter):
    delta = 1
    num = 0
    # print("beta_max: ", beta_max)
    # print("b: ", b)
    b = 6 * gamma_T - 1 - gamma_T ** 2
    if count_min_beta(gamma_T) < beta:
        beta_min = count_min_beta_s(gamma_T)
        beta_max = 10000
        d = 0
    elif b < 0:
        beta_min = 0
        print(b)
        beta_max = (-b - np.sqrt(b ** 2 - 16 * gamma_T * gamma_T)) / (4 * gamma_T ** 2)
        d = 1
    else:
        beta_min = 0
        beta_max = 10000
        d = 2

    print(beta_min,beta_max)

    plt.axvline(x=beta_max, color="g")
    plt.axvline(x=beta_min, color="g")

    while delta > 10 ** (-5) and num<max_iter:
        beta_s = 0.5 * (beta_min + beta_max)
        # print(beta_s)
        delta = beta_s * np.exp(((1 + beta_s) * (gamma_T - 1)) / (2 * (1 + beta_s * gamma_T))) - beta
        # print(delta)
        num+=1
        if delta > 0:
            beta_max = beta_s
        else:
            beta_min = beta_s
        delta = np.abs(delta / min(beta_s, 1))
        plt.axvline(x=beta_s, color="r")
        if np.log(beta_s)/np.log(10)<-10 and d==1:
            delta = 0
            beta_s = 0
            print("sfdfdddddddddddddddddd")
        print(delta, beta, beta_s, gamma_T, d)


beta = 1.2623814793272614
gamma_T = 37.50913073577249

delta = 1
num = 0

def f(beta_s):
    return beta_s *np.exp(((gamma_T-1)*(1+beta_s))/(2*(1+beta_s*gamma_T)))

#beta_s = np.arange(0,100,0.001)
beta_s = np.exp(np.arange(np.log(0.000000000000000000000001), np.log(100), 0.01))
beta_s_0 = ((gamma_T**2+1-6*gamma_T)+np.sqrt((gamma_T**2+1-6*gamma_T)**2-8*(2*gamma_T**2)))/(4*gamma_T**2)
beta_s_1 = ((gamma_T**2+1-6*gamma_T)-np.sqrt((gamma_T**2+1-6*gamma_T)**2-8*(2*gamma_T**2)))/(4*gamma_T**2)
A = beta_s*0 + beta
res = []
for i in range(len(beta_s)):
    res.append(f(beta_s[i]))

plt.show()
num = 0
while True:

    num+=1
    plt.semilogx(beta_s, res, label="f(beta_s)")
    plt.semilogy(beta_s, A, label="beta")
    plt.grid()
    plt.legend()
    count_beta_s(beta, gamma_T, max_iter=2*num)
    plt.show()