import numpy as np

# Si_s -> Si_g
K_sp_cl2_sicl0 = 0.0429
E_th_cl2_sicl0_sp = 44.4
# SiCl_s -> SiCl_g
K_sp_cl2_sicl1 = 0.1007
E_th_cl2_sicl1_sp = 27.78
# SiCl2_s -> SiCl2_g
K_sp_cl2_sicl2 = 0.1467
E_th_cl2_sicl2_sp = 21.94
# SiCl3_s -> SiCl3_g
K_sp_cl2_sicl3 = 0.1856
E_th_cl2_sicl3_sp = 18.93

sput_data_Cl2_plus = np.array([[E_th_cl2_sicl0_sp, E_th_cl2_sicl1_sp, E_th_cl2_sicl2_sp, E_th_cl2_sicl3_sp],
                              [K_sp_cl2_sicl0, K_sp_cl2_sicl1, K_sp_cl2_sicl2, K_sp_cl2_sicl3]])