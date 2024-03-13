import numpy as np

def good_form(num):
    if num == 0.0:
        return "0.0"
    elif str(num) == "inf":
        return "inf"
    # print(num)
    integ = int(np.log(num) / np.log(10))
    ost = num / (10.0 ** (integ))
    return str(round(ost, 5)) + "*10^" + str(integ)

def generate_approximation(Energies,Konstants, do_print=False):

    x_train = (Energies).reshape((-1, 1))
    y_train = np.log(Konstants)

    def model_predict(x, w):
        x = x.reshape((-1, 1))
        X = np.ones(x.shape)
        X = np.concatenate([X, np.log(x)], axis=1)
        X = np.concatenate([X, 1 / x], axis=1)
        X = np.concatenate([X, 1 / (x ** 2)], axis=1)
        X = np.concatenate([X, 1 / (x ** 3)], axis=1)
        X = np.concatenate([X, 1 / (x ** 4)], axis=1)

        return X @ w

    X = np.ones(x_train.shape)
    X = np.concatenate([X, np.log(x_train)], axis=1)
    X = np.concatenate([X, 1 / x_train], axis=1)
    X = np.concatenate([X, 1 / (x_train ** 2)], axis=1)
    X = np.concatenate([X, 1 / (x_train ** 3)], axis=1)
    X = np.concatenate([X, 1 / (x_train ** 4)], axis=1)

    w_res = np.linalg.pinv(X) @ y_train

    def res_fun(x):
        return np.exp(model_predict(x, w_res))

    #w_res[0] = np.exp(w_res[0])

    if do_print:
        print("k(T) = A*T^(B)*exp($C_1$/$T$ + $C_2$/$T^2$ + $C_3$/$T^3$ + $C_4$/$T^4$)")
        print("A:", good_form(np.exp(w_res[0])))
        print("B:", w_res[1])
        print("$C_1$:", w_res[2])
        print("$C_2$:", w_res[3])
        print("$C_3$:", w_res[4])
        print("$C_4$:", w_res[5])

    return w_res, res_fun
