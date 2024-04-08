import pandas as pd
import numpy as np

from res.plasma.reactions.consts import e, k_b


def give_numbed_data(pre_react_data):
    max_len = 0
    max_key = 0
    res = []
    for key in pre_react_data.keys():
        max_len = max(max_len, len(pre_react_data[key]))
        max_key = max(max_key, key)
    connector = np.zeros(max_key + 1)
    keys = list(pre_react_data.keys())
    for i in range(len(keys)):
        res.append(pre_react_data[keys[i]])
        connector[keys[i]] = i

    for i in range(len(res)):
        while len(res[i]) < max_len:
            res[i].append(0)

    return np.array(res), np.array(connector).astype(int)


def generate_dict(Nums, const_arr):
    res = {}
    for i in range(len(Nums)):
        res[Nums[i]] = const_arr[i]
    return res


def give_consts(filename, do_rand=True):
    data = pd.read_csv(filename)
    for column in data.columns:
        data = data.rename(columns={column: column.replace(" ", "")})
    Nums = np.array(data["Num"]).astype(int)
    A_num = np.array(data["A_num"]).astype(float)
    A_pow = np.array(data["A_pow"]).astype(float)
    B = np.array(data["B"]).astype(float)
    Err = np.array(data["err"]).astype(float)
    if do_rand:
        A_num = A_num * (1.0+Err*0.01*(2*np.random.random(Err.shape)-1))
    Type = np.array(data["type"])
    for i in range(len(Type)):
        Type[i] = Type[i].replace(" ", "")

    A = A_num * np.power(10, A_pow) * np.power(k_b / e, B)

    C = np.array(data["C"]).astype(float) * np.power(e / k_b, 1)
    D = np.array(data["D"]).astype(float) * np.power(e / k_b, 2)
    E = np.array(data["E"]).astype(float) * np.power(e / k_b, 3)
    F = np.array(data["F"]).astype(float) * np.power(e / k_b, 4)
    G = np.array(data["G"]).astype(float) * np.power(e / k_b, 5)
    En = np.array(data["En"]).astype(float) * e

    is_inel = np.array(data["is_inel"]).astype(int)
    is_el = np.array(data["is_el"]).astype(int)
    is_ch = np.array(data["is_ch"]).astype(int)
    for_chem = np.concatenate(
        (A[is_ch != 0].reshape((-1, 1)), B[is_ch != 0].reshape((-1, 1)), C[is_ch != 0].reshape((-1, 1)),
         D[is_ch != 0].reshape((-1, 1)), E[is_ch != 0].reshape((-1, 1)), F[is_ch != 0].reshape((-1, 1)),
         G[is_ch != 0].reshape((-1, 1))), axis=1)
    Nums_chem = Nums[is_ch != 0]

    for_inel = np.concatenate(
        (A[is_inel != 0].reshape((-1, 1)), B[is_inel != 0].reshape((-1, 1)), C[is_inel != 0].reshape((-1, 1)),
         D[is_inel != 0].reshape((-1, 1)), E[is_inel != 0].reshape((-1, 1)), F[is_inel != 0].reshape((-1, 1)),
         G[is_inel != 0].reshape((-1, 1)), En[is_inel != 0].reshape((-1, 1))), axis=1)
    Nums_inel = Nums[is_inel != 0]

    for_el = np.concatenate(
        (A[is_el != 0].reshape((-1, 1)), B[is_el != 0].reshape((-1, 1)), C[is_el != 0].reshape((-1, 1)),
         D[is_el != 0].reshape((-1, 1)), E[is_el != 0].reshape((-1, 1)), F[is_el != 0].reshape((-1, 1)),
         G[is_el != 0].reshape((-1, 1))), axis=1)
    Nums_el = Nums[is_el != 0]

    chem_data, chem_connector = give_numbed_data(generate_dict(Nums_chem, for_chem))
    inel_data, inel_connector = give_numbed_data(generate_dict(Nums_inel, for_inel))
    el_data, el_connector = give_numbed_data(generate_dict(Nums_el, for_el))

    ar_vec = Nums[(Type == "Ar") * (is_inel == 1)]
    cl2_vec = Nums[(Type == "Cl2")*(is_inel == 1)]
    cl_vec = Nums[(Type == "Cl") * (is_inel == 1)]
    #print("Ar: ",ar_vec)
    #print("Cl: ", cl_vec)
    #print("Cl2: ", cl2_vec)

    return chem_data, chem_connector, inel_data, inel_connector, el_data, el_connector, ar_vec, cl2_vec, cl_vec
