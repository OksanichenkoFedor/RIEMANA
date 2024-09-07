import numpy as np
import matplotlib.pyplot as plt

from res.getero.reaction_consts.angular_dependences import sput_an_dep, ion_enh_etch_an_dep

Theta = np.arange(0, 1, 0.001) * np.pi * 0.5

# print(np.power(Theta, 2))

#G_phy = 0.4 * (18.7 * np.cos(Theta) - 64.7 * np.power(np.cos(Theta), 2) + 145.2 * np.power(np.cos(Theta), 3) -
#               206 * np.power(np.cos(Theta), 4) + 147.3 * np.power(np.cos(Theta), 5) - 39.9 * np.power(np.cos(Theta),
#                                                                                                       6))

#G_phy1 = -141.3 * np.power(np.cos(Theta), 6) + 641.1 * np.power(np.cos(Theta), 5) - 1111.3 * np.power(np.cos(Theta),
#                                                                                                      4) + \
#         944.6 * np.power(np.cos(Theta), 3) - 422.0 * np.power(np.cos(Theta), 2) + 95.31 * np.power(np.cos(Theta),
#                                                                                                  1) - 5.460 # http://dx.doi.org/10.1116/1.3231450

#G_phy2 = -81.70 * np.power(np.cos(Theta), 5) + 224.03 * np.power(np.cos(Theta), 4) - \
#         208.19 * np.power(np.cos(Theta), 3) + 67.569 * np.power(np.cos(Theta), 2) - \
#         0.711 * np.power(np.cos(Theta), 1) - 0.0242

#G_chem = 0.9 * (1.1 - 0.31 * Theta + 1.61 * np.power(Theta, 2) - 2.13 * np.power(Theta, 3) + 0.6 * np.power(Theta, 4))


#def give_chem(phi):
#    phi = (180.0 / np.pi) * phi
#    if phi < 25:
#        return 1.0
#    else:
#        return (90.0 - phi) / 65.0 - ((phi - 25) * (phi - 90)) / 5000


G_chem1 = np.zeros(Theta.shape)
for i in range(len(G_chem1)):
    G_chem1[i] = ion_enh_etch_an_dep(Theta[i])
G_phy1 = np.zeros(Theta.shape)
for i in range(len(G_phy1)):
    G_phy1[i] = sput_an_dep(Theta[i])

fig, (ax11, ax22) = plt.subplots(1, 2, figsize=(18, 7))

#ax11.plot(Theta * (180 / np.pi), G_phy/G_phy[0], label="2015")
ax11.plot(Theta * (180 / np.pi), G_phy1/G_phy1[0], label="2009")
#ax11.plot(Theta * (180 / np.pi), G_phy2/G_phy2[0], label="2009_2")
ax11.set_title("Физическое распыление", size=20)
ax11.set_ylabel("$g_{phys}$", size=15)
ax11.set_xlabel(r"$\theta$", size=20)
ax11.set_title("(a)", y=-0.15, loc='left', size=20)
ax11.grid()
#ax11.legend()

#ax22.plot(Theta * (180 / np.pi), G_chem, label="2015")
ax22.plot(Theta * (180 / np.pi), G_chem1, label="2009")
ax22.set_title("Ионно-стимулированное травление", size=20)
ax22.grid()
ax22.set_ylabel("$g_{chem}$", size=15)
ax22.set_xlabel(r"$\theta$", size=20)
ax22.set_title("(b)", y=-0.15, loc='left', size=20)
#ax22.legend()
plt.show()
