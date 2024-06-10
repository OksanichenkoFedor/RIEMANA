from res.global_entities.etcher import Etcher

def run_Ar(y_ar):

    params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": y_ar,
            "W": 600,
            "U_i": 200,
            "time": 60
            }

    etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=84)

    etch.init()
    etch.run(params, start_filename="../")

for i in range(20):
    print(i*0.05)
    run_Ar(i*0.05)
