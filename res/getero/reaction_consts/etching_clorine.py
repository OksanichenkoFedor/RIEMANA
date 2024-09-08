ver_1 = [0.99,0.2,0.15,0.001]
ver_2 = [0.75, 0.15, 0.11, 0.007]
ver_3 = [0.4, 0.08, 0.06, 0.004]
test_ver = [1,1,1,1]

curr_ver = test_ver
curr_ver = ver_1

gamma_Cl_A = curr_ver[0] # Si_s + Cl_g -> SiCl_s
gamma_Cl_B = curr_ver[1] # SiCl_s + Cl_g -> SiCl2_s
gamma_Cl_C = curr_ver[2] # SiCl2_s + Cl_g -> SiCl3_s
gamma_Cl_D = curr_ver[3] # SiCl3_s + Cl_g -> SiCl4_g
