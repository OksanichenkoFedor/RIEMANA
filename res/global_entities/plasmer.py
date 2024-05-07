from res.plasma.models.consist_model_aclr import run_consist_model
from res.plasma.reactions.const_functions import give_consts

class Plasmer:
    def __init__(self, consts_filename):
        self.data = {}
        self.consts_filename = consts_filename

    def count_plasma(self, params):
        consts = give_consts(self.consts_filename, do_rand=False)
        self.data = run_consist_model(p_0=params["p_0"], T_gas=params["T_gas"], R=params["R"], L=params["L"],
                                      gamma_cl=params["gamma_cl"], y_ar=params["y_ar"], W=params["W"], consts=consts)
        res_params = {
            "j_cl": self.data["j_cl"],
            "j_ar_plus": self.data["j_ar_plus"],
            "j_cl_plus": self.data["j_cl_plus"],
            "j_cl2_plus": self.data["j_cl2_plus"],
            "T_i": self.data["T_i"]
        }
        return res_params