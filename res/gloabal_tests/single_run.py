from res.global_entities.etcher import Etcher

def run_Ar(N):

    params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.0,
            "W": 600,
            "U_i": 40,
            "time": 60.0/(1.0*N)
            }

    etch = Etcher(0.2, consts_filename="../data/data.csv", Si_num=int(84.0/(1.0*N)))
    etch.init()
    etch.run(params, start_filename="../")
Ns = [1]
for i in range(len(Ns)):
    #print(i*0.05)
    run_Ar(Ns[i])
