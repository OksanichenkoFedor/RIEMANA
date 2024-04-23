import numpy as np

# Si_s -> Si_g
K_sp_ar_sicl0 = 0.0352
E_th_ar_sicl0_sp = 31.86
# SiCl_s -> SiCl_g
K_sp_ar_sicl1 = 0.08
E_th_ar_sicl1_sp = 20.57
# SiCl2_s -> SiCl2_g
K_sp_ar_sicl2 = 0.1142
E_th_ar_sicl2_sp = 16.93
# SiCl3_s -> SiCl3_g
K_sp_ar_sicl3 = 0.1424
E_th_ar_sicl3_sp = 15.29

sput_data_Ar_plus = np.array([[E_th_ar_sicl0_sp, E_th_ar_sicl1_sp, E_th_ar_sicl2_sp, E_th_ar_sicl3_sp],
                              [K_sp_ar_sicl0, K_sp_ar_sicl1, K_sp_ar_sicl2, K_sp_ar_sicl3]])