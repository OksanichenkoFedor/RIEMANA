import numpy as np

from res.plasma.consts import k_b, m_cl, m_cl2, m_ar, m_e

from res.plasma.utils import good_form

from res.plasma.reactions_consts.Ar import count_Ar_inel_power, give_k_Ar_mom
from res.plasma.reactions_consts.Cl import count_Cl_inel_power, give_k_Cl_mom
from res.plasma.reactions_consts.Cl2 import count_Cl2_inel_power, give_k_Cl2_mom

from res.plasma.algorithm.utils import count_T_i, count_m_eff, count_tau_eff


def count_W_eff(T_e, V, n_ar, n_cl2, n_cl, do_print=False):
    inel_part = V * (
            n_ar * count_Ar_inel_power(T_e) + n_cl2 * count_Cl2_inel_power(T_e) + n_cl * count_Cl_inel_power(T_e))
    k_ar_m = give_k_Ar_mom(T_e)
    k_cl2_m = give_k_Cl2_mom(T_e)
    k_cl_m = give_k_Cl_mom(T_e)

    el_part = 3 * V * T_e * k_b * m_e * (k_ar_m * (n_ar / m_ar) + k_cl2_m * (n_cl2 / m_cl2) + k_cl_m * (n_cl / m_cl))
    if do_print:
        print("inel_part: ", good_form(inel_part))
        print("el_part: ", good_form(el_part))
    return el_part + inel_part


def count_W_ion(T_e, tau_eff, n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, p_0, T_gas, V, do_print=False):
    T_i = count_T_i(p_0, T_gas, do_print=False)
    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, do_print=False)
    eU_f = 0.5 * k_b * T_e * np.log((T_e * m_eff) / (T_i * m_e))
    W_ion = (eU_f + 0.5 * T_e * k_b) * tau_eff * V

    if do_print:
        print("W_ion: ", good_form(W_ion))
    return W_ion


def count_W_e(T_e, tau_eff, V, do_print=False):
    W_e = 2 * T_e * k_b * tau_eff * V
    if do_print:
        print("W_e: ", good_form(W_e))
    return W_e


def count_n_e(T_e, n_vector, param_vector, do_print=False):
    p_0, T_gas, R, L, gamma_cl, y_ar, W, V = param_vector
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    tau_eff = count_tau_eff(T_e, n_vector, param_vector, do_print=False)

    W_ion = count_W_ion(T_e, tau_eff, n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, p_0, T_gas, V, do_print=False)
    W_e = count_W_e(T_e, tau_eff, V, do_print=False)
    W_eff = count_W_eff(T_e, V, n_ar, n_cl2, n_cl, do_print=False)
    n_e = (W - 1 * (W_ion + W_e)) / W_eff
    if do_print:
        print("n_e_new: ", good_form(n_e))
    return n_e
