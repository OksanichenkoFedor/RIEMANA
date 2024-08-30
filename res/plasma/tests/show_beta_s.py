from res.plasma.algorithm.with_aclr.beta_s import pure_count_beta_s
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

gammas = [5,8,10,12,15,20]
colors = ["r","b","g",(1.0,165.0/255.0,0),(1.0,0,1.0),(0,1.0,1.0)]
beta = np.exp(np.arange(np.log(0.75), np.log(2), 0.001))
beta_s = []
for i in range(len(gammas)):
    beta_s.append([])

for i in trange(len(beta)):
    for j in range(len(gammas)):
        beta_s[j].append(pure_count_beta_s(beta[i], gammas[j])[0])

beta_s = np.array(beta_s)
beta = np.array(beta)
print(beta_s.shape)
#print(beta_s[0])
plt.figure(figsize=(10,7))
for i in range(len(gammas)):

    #plt.semilogx(beta,beta_s[i],label="gamma="+str(gammas[i]))
    plt.plot(beta, beta_s[i], label=r"$\gamma_T$=" + str(gammas[i]), color = colors[i])

plt.xlabel(r"$\beta$", size=15)
plt.ylabel(r"$\beta_s$", size=15)
#plt.xticks(np.arange())
plt.legend()
plt.grid()
plt.show()