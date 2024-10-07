from res.global_entities.etcher import Etcher

def run_Ar(y_ar, N, U):

    params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": y_ar,
            "W": 600,
            "U_i": U,
            "time": 120.0,
            "do_half": False,
            "rt_type": "bvh",
            "num_one_side_points": 10
            }

    etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=int(N))

    etch.init()
    etch.run(params, start_filename="../")
#run_Ar(0.5, 80, 40)

run_Ar(0.5, 10, 40)

run_Ar(0.5, 60, 40)
run_Ar(0.5, 30, 40)
run_Ar(0.5, 20, 40)
run_Ar(0.5, 15, 40)
run_Ar(0.5, 10, 40)
run_Ar(0.5, 5, 40)
#run_Ar(0.5, 6, 40)
#run_Ar(0.5, 12, 40)



#run_Ar(0.5, 6, 100)
#run_Ar(0.5, 6, 300)


#run_Ar(0.5, 6, 200)
#run_Ar(0.0, 6, 200)
#run_Ar(0.1, 6, 200)
#run_Ar(0.2, 6, 200)
#run_Ar(0.3, 6, 200)
#run_Ar(0.4, 6, 200)
#run_Ar(0.6, 6, 200)
#run_Ar(0.7, 6, 200)
#run_Ar(0.8, 6, 200)
#run_Ar(0.9, 6, 200)