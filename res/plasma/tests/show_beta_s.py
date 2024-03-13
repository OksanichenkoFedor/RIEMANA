from res.plasma.algorithm.beta_s import pure_count_beta_s
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

gammas = [37.50913073577249]

beta = np.exp(np.arange(np.log(1), np.log(2), 0.001))
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
for i in range(len(gammas)):

    #plt.semilogx(beta,beta_s[i],label="gamma="+str(gammas[i]))
    plt.semilogx(beta, beta_s[i]/beta, label="gamma=" + str(gammas[i]))
plt.xlabel("$a_b$")
plt.ylabel("$a_s/a_b$")
plt.legend()
plt.grid()
plt.show()