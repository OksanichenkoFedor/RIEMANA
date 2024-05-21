from res.global_entities.etcher import Etcher

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.1,
            "W": 600,
            "U_i": 200,
            "time": 0.5
        }

etch = Etcher(0.01, "../data/data.csv")

etch.init()
etch.run(params, start_filename="../")