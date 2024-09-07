from res.global_entities.getero import Getero
from res.global_entities.plasmer import Plasmer
from res.global_entities.wafer import Wafer
class Etcher:
    def __init__(self, multiplier, Si_num=84, consts_filename="data/data.csv"):
        self.const_params = {
            "a_0": ((1839 * 28 * 9.1 * 10 ** (-31)) / 2330) ** (1.0 / 3.0),
            "cell_size": 2.5 * (10.0 ** (-9)),
            "num_iter": 3010
        }
        self.multiplier = multiplier
        self.Si_num = Si_num
        self.consts_filename = consts_filename
        self.init()

    def init(self):
        self.getero = Getero()
        self.wafer = Wafer(self.multiplier, Si_num=self.Si_num)
        self.plasmer = Plasmer(self.consts_filename)

    def run(self, params, start_filename=""):
        if params["do_half"]:
            self.wafer.make_half()
        time = params["time"]
        num_iter = self.const_params["num_iter"]
        plasma_params = self.plasmer.count_plasma(params)
        plasma_params.update(self.const_params)
        plasma_params.update(params)
        self.getero.change_plasma_params(plasma_params)
        self.getero.run(self.wafer, time, num_iter, start_filename=start_filename)
        if params["do_half"]:
            self.wafer.return_half()


