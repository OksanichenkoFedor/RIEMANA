import numpy as np

# Si_s -> Si_g
K_sp_cl_sicl0 = 0.0355
E_th_cl_sicl0_sp = 29.79
# SiCl_s -> SiCl_g
K_sp_cl_sicl1 = 0.0795
E_th_cl_sicl1_sp = 19.44
# SiCl2_s -> SiCl2_g
K_sp_cl_sicl2 = 0.1125
E_th_cl_sicl2_sp = 16.21
# SiCl3_s -> SiCl3_g
K_sp_cl_sicl3 = 0.1399
E_th_cl_sicl3_sp = 14.85

sput_data_Cl_plus = np.array([[E_th_cl_sicl0_sp, E_th_cl_sicl1_sp, E_th_cl_sicl2_sp, E_th_cl_sicl3_sp],
                              [K_sp_cl_sicl0, K_sp_cl_sicl1, K_sp_cl_sicl2, K_sp_cl_sicl3]])