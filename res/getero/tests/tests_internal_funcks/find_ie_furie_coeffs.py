from res.getero.reactions.reaction_consts.angular_dependences import ion_enh_etch_an_dep
import numpy as np
import matplotlib.pyplot as plt

def generate_approximation(Thetas,Coeffs, do_print=False):

    x_train = (np.array(Thetas)).reshape((-1, 1))
    y_train = np.array(Coeffs)

    def model_predict(x, w):
        x = x.reshape((-1, 1))
        X = np.ones(x.shape)
        X = np.concatenate([X, np.pow(np.cos(x), 1)], axis=1)
        X = np.concatenate([X, np.pow(np.cos(x), 2)], axis=1)
        X = np.concatenate([X, np.pow(np.cos(x), 3)], axis=1)
        X = np.concatenate([X, np.pow(np.cos(x), 4)], axis=1)
        X = np.concatenate([X, np.pow(np.cos(x), 5)], axis=1)
        X = np.concatenate([X, np.pow(np.cos(x), 6)], axis=1)

        return X @ w

    X = np.ones(x_train.shape)
    X = np.concatenate([X, np.pow(np.cos(x_train), 1)], axis=1)
    X = np.concatenate([X, np.pow(np.cos(x_train), 2)], axis=1)
    X = np.concatenate([X, np.pow(np.cos(x_train), 3)], axis=1)
    X = np.concatenate([X, np.pow(np.cos(x_train), 4)], axis=1)
    X = np.concatenate([X, np.pow(np.cos(x_train), 5)], axis=1)
    X = np.concatenate([X, np.pow(np.cos(x_train), 6)], axis=1)

    w_res = np.linalg.pinv(X) @ y_train

    def res_fun(x):
        return model_predict(x, w_res)

    if do_print:
        print("g(phi) = A+B*cos(phi)+C*$cos(phi)^2$+D*$cos(phi)^3$+E*$cos(phi)^4$+F*$cos(phi)^5$+G*$cos(phi)^6$")
        print("A:", w_res[0])
        print("B:", w_res[1])
        print("C:", w_res[2])
        print("D:", w_res[3])
        print("E:", w_res[4])
        print("F:", w_res[5])

    return w_res, res_fun, model_predict

Theta = np.arange(0,1,0.01)*np.pi*0.5
res = []
for i in range(len(Theta)):
    res.append(ion_enh_etch_an_dep(Theta[i]))
def count_norm(fun, thetas):
    res = fun(thetas)
    return res
w_res, res_fun, mp = generate_approximation(Theta,res)
w = np.array([0.00134, 1.5803, -0.26805, -0.94336, 1.22596, -0.1855625, -0.413133])
def res_fun_1(x):
    return mp(x, w)
plt.plot(Theta, res, label="old fun")
plt.plot(Theta,count_norm(res_fun,Theta),label="furie approx")
plt.plot(Theta,count_norm(res_fun_1,Theta),label="furie approx 1")
plt.grid()
plt.legend()
print(w_res)
plt.show()