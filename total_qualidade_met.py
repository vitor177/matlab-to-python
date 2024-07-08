
import numpy as np
import pandas as pd

def total_qualidade_met(raw, dados, fp_min, fp_max, mes, dia_final, anox, fig, nome_arquivo):

    # ==========================================================================
    #                      Controle de Qualidade
    # ==========================================================================
    dia_mes = dados[:, 2]
    vel_avg = pd.to_numeric(raw.iloc[:, 3])
    vel_max = pd.to_numeric(raw.iloc[:, 4])
    vel_min = pd.to_numeric(raw.iloc[:, 5])
    vel_std = pd.to_numeric(raw.iloc[:, 6])

    temp_avg = pd.to_numeric(raw.iloc[:, 7])
    temp_max = pd.to_numeric(raw.iloc[:, 8])
    temp_min = pd.to_numeric(raw.iloc[:, 9])
    temp_std = pd.to_numeric(raw.iloc[:, 10])

    ur_avg = pd.to_numeric(raw.iloc[:, 11])
    ur_max = pd.to_numeric(raw.iloc[:, 12])
    ur_min = pd.to_numeric(raw.iloc[:, 13])
    ur_std = pd.to_numeric(raw.iloc[:, 14])


    n, m = raw.shape
    
    dia_anterior = 1440
    data = raw.iloc[dia_anterior:]
    
    # ======= Criação das Flags =======
    flag6 = 60000
    flag5 = 50000
    flag4 = 40000
    flag3 = 30000
    flag2 = 20000
    flag1 = 10000
    
    # ==========================================================================
    #                             Temperatura
    # ==========================================================================
    # ======= Desvio padrao =======
    temp_desv = np.full((n-dia_anterior,), np.nan)

    temp_desv_flag6 = 0
    temp_desv_flag3 = 0
    temp_desv_flag1 = 0

    for i in range(n-dia_anterior):
        if temp_avg[dia_anterior + i] == flag6:
            temp_desv[i] = flag6
            temp_desv_flag6 += 1
        else:
            if temp_std[dia_anterior + i] == 0:
                temp_desv[i] = flag3
                temp_desv_flag3 += 1
            else:
                temp_desv[i] = flag1
                temp_desv_flag1 += 1

    # ======= deriva Temp =======
    deriva_temp = np.full((n-dia_anterior,), np.nan)

    deriva_temp_flag6 = 0
    deriva_temp_flag5 = 0
    deriva_temp_flag4 = 0
    deriva_temp_flag3 = 0
    deriva_temp_flag1 = 0

    for i in range(n-dia_anterior):
        if temp_desv[i] == flag6:
            deriva_temp[i] = flag6
            deriva_temp_flag6 += 1
        elif temp_desv[i] == flag5:
            deriva_temp[i] = flag5
            deriva_temp_flag5 += 1
        elif temp_desv[i] == flag4 or temp_desv[i] == flag3:
            deriva_temp[i] = flag4
            deriva_temp_flag4 += 1
        else:
            if temp_avg[i+dia_anterior] >= temp_min[i+dia_anterior] and temp_avg[i+dia_anterior] <= temp_max[i+dia_anterior]:
                deriva_temp[i] = flag1
                deriva_temp_flag1 += 1
            else:
                deriva_temp[i] = flag3
                deriva_temp_flag3 += 1

    # ======= Fisicamente possível =======
    temp_fp_min = fp_min
    temp_fp_max = fp_max

    # ======= Fisicamente possível -> Validação =======
    temp_valid_fp = np.full((n-dia_anterior,), np.nan)

    temp_valid_flag6 = 0
    temp_valid_flag4 = 0
    temp_valid_flag3 = 0
    temp_valid_flag1 = 0

    for i in range(n-dia_anterior):
        if deriva_temp[i] == flag6:
            temp_valid_fp[i] = flag6
            temp_valid_flag6 += 1
        elif deriva_temp[i] == flag3:
            temp_valid_fp[i] = flag4
            temp_valid_flag4 += 1
        elif deriva_temp[i] == flag1 and temp_avg[dia_anterior + i] < temp_fp_min:
            temp_valid_fp[i] = flag3
            temp_valid_flag3 += 1
        elif deriva_temp[i] == flag1 and temp_avg[dia_anterior + i] > temp_fp_max:
            temp_valid_fp[i] = flag3
            temp_valid_flag3 += 1
        else:
            temp_valid_fp[i] = flag1
            temp_valid_flag1 += 1

    # ======= Extremamente Raro =======
    temp_er = np.full((n-dia_anterior,), np.nan)

    for i in range(n-dia_anterior):
        temp_er[i] = abs(max(temp_avg[dia_anterior+i-61:dia_anterior+i]) - min(temp_avg[dia_anterior+i-61:dia_anterior+i]))
        if temp_er[i] >= flag5:
            temp_er[i] = flag5

    # ======= Extremamente Raro -> Validação =======
    temp_valid_er = np.full((n-dia_anterior,), np.nan)

    temp_valid_er_flag6 = 0
    temp_valid_er_flag5 = 0
    temp_valid_er_flag4 = 0
    temp_valid_er_flag2 = 0
    temp_valid_er_flag1 = 0

    for i in range(n-dia_anterior):
        if temp_valid_fp[i] == flag6:
          
