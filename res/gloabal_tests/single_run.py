from res.global_entities.etcher import Etcher

def run_Ar(y_ar, N):

    params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": y_ar,
            "W": 600,
            "U_i": 200,
            "time": 240.0/(1.0*N),
            "do_half": True,
            "rt_type": "bvh",

            }

    etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=int(84/N))

    etch.init()
    etch.run(params, start_filename="../")
Ns = [6]
run_Ar(0.5, 6)
for i in range(len(Ns)):
    print(Ns[i])
    run_Ar(0.5, Ns[i])
