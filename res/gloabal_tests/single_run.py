from res.global_entities.etcher import Etcher

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=84)

etch.init()
etch.run(params, start_filename="../")


#-----------------------------------------------------------


params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 30
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=42)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 20
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=28)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60.0/6.0
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=14)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60.0/7.0
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=12)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60.0/12.0
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=7)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60.0/21.0
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=4)

etch.init()
etch.run(params, start_filename="../")

#-----------------------------------------------------------

params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 200,
            "time": 60.0/28.0
        }

etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=3)

etch.init()
etch.run(params, start_filename="../")