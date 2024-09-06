import pandas as pd 
import numpy as np
from total_dados_entrada import total_dados_entrada
from flag_plot import flag_plot
from testes import plot_boxplot

def total_qualidade_met(raw_met, dados, fp_min, fp_max, mes, dia_final, anox, fig, nome_arquivo):


    temp_min = fp_min
    temp_max = fp_max
    fig = 10

    dia_mes = dados.iloc[:, 2]
    # ======= Informações dos dados brutos =======
    vel_avg = raw_met.iloc[:, 3].to_numpy()
    vel_max = raw_met.iloc[:, 4].to_numpy()
    vel_min = raw_met.iloc[:, 5].to_numpy()
    vel_std = raw_met.iloc[:, 6].to_numpy()

    temp_avg = raw_met.iloc[:, 7].to_numpy()
    temp_max = raw_met.iloc[:, 8].to_numpy()
    temp_min = raw_met.iloc[:, 9].to_numpy()
    temp_std = raw_met.iloc[:, 10].to_numpy()

    ur_avg = raw_met.iloc[:, 11].to_numpy()
    ur_max = raw_met.iloc[:, 12].to_numpy()
    ur_min = raw_met.iloc[:, 13].to_numpy()
    ur_std = raw_met.iloc[:, 14].to_numpy()

    n, m = raw_met.shape
    dia_anterior = 1440                 
    data = raw_met.iloc[dia_anterior:, 0].to_numpy()

    # %%
    # ======= Criação das Flags =======
    flag6 = 60000
    flag5 = 50000
    flag4 = 40000
    flag3 = 30000
    flag2 = 20000
    flag1 = 10000

    #==========================================================================
    #                             Temperatura    
    #==========================================================================
    # ======= Desvio padrão =======
    temp_desv = np.full(n - dia_anterior, np.nan)

    temp_desv_flag6 = 0
    temp_desv_flag3 = 0
    temp_desv_flag1 = 0

    for i in range(n - dia_anterior):
        if temp_avg[dia_anterior + i] == flag6:
            temp_desv[i] = flag6
            temp_desv_flag6 += 1
        elif temp_std[dia_anterior + i] == 0:
            temp_desv[i] = flag3
            temp_desv_flag3 += 1
        else:
            temp_desv[i] = flag1
            temp_desv_flag1 += 1

    # ======= Deriva Temp =======
    deriva_temp = np.full(n - dia_anterior, np.nan)

    deriva_temp_flag6 = 0
    deriva_temp_flag5 = 0
    deriva_temp_flag4 = 0
    deriva_temp_flag3 = 0
    deriva_temp_flag1 = 0

    for i in range(n - dia_anterior):
        if temp_desv[i] == flag6:
            deriva_temp[i] = flag6
            deriva_temp_flag6 += 1
        elif temp_desv[i] == flag5:
            deriva_temp[i] = flag5
            deriva_temp_flag5 += 1
        elif temp_desv[i] in [flag4, flag3]:
            deriva_temp[i] = flag4
            deriva_temp_flag4 += 1
        else:
            if temp_avg[i + dia_anterior] >= temp_min[i + dia_anterior] and temp_avg[i + dia_anterior] <= temp_max[i + dia_anterior]:
                deriva_temp[i] = flag1
                deriva_temp_flag1 += 1
            else:
                deriva_temp[i] = flag3
                deriva_temp_flag3 += 1

    # %%
    # ======= Fisicamente possível =======
    temp_fp_min = fp_min
    temp_fp_max = fp_max

    # ======= Fisicamente possível -> Validação =======
    temp_valid_fp = np.full(n - dia_anterior, np.nan)

    temp_valid_flag6 = 0
    temp_valid_flag4 = 0
    temp_valid_flag3 = 0
    temp_valid_flag1 = 0

    for i in range(n - dia_anterior):
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

    # %%
    # ======= Extremamente Raro =======
    temp_er = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        temp_er[i] = abs(np.max(temp_avg[dia_anterior + i - 61:dia_anterior + i]) - np.min(temp_avg[dia_anterior + i - 61:dia_anterior + i]))
        if temp_er[i] >= flag5:
            temp_er[i] = flag5

    # ======= Extremamente Raro -> Validação =======
    temp_valid_er = np.full(n - dia_anterior, np.nan)

    temp_valid_er_flag6 = 0
    temp_valid_er_flag5 = 0
    temp_valid_er_flag4 = 0
    temp_valid_er_flag2 = 0
    temp_valid_er_flag1 = 0

    for i in range(n - dia_anterior):
        if temp_valid_fp[i] == flag6:
            temp_valid_er[i] = flag6
            temp_valid_er_flag6 += 1
        elif temp_er[i] == flag5:
            temp_valid_er[i] = flag5
            temp_valid_er_flag5 += 1
        elif temp_valid_fp[i] == flag3:
            temp_valid_er[i] = flag4
            temp_valid_er_flag4 += 1
        elif temp_er[i] < 5:
            temp_valid_er[i] = flag1
            temp_valid_er_flag1 += 1
        else:
            temp_valid_er[i] = flag2
            temp_valid_er_flag2 += 1

    # %%
    # ======= ET =======
    temp_et = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        temp_et[i] = abs(np.max(temp_avg[i:dia_anterior + i]) - np.min(temp_avg[i:dia_anterior + i]))
        if temp_et[i] >= flag5:
            temp_et[i] = flag5

    # ======= ET -> Validação =======
    temp_valid_et = np.full(n - dia_anterior, np.nan)

    temp_valid_et_flag6 = 0
    temp_valid_et_flag5 = 0
    temp_valid_et_flag4 = 0
    temp_valid_et_flag3 = 0
    temp_valid_et_flag2 = 0
    temp_valid_et_flag1 = 0

    for i in range(n - dia_anterior):
        if temp_valid_er[i] == flag6:
            temp_valid_et[i] = flag6
            temp_valid_et_flag6 += 1
        elif temp_et[i] == flag5:
            temp_valid_et[i] = flag5
            temp_valid_et_flag5 += 1
        elif temp_valid_er[i] == flag4:
            temp_valid_et[i] = flag4
            temp_valid_et_flag4 += 1
        elif temp_valid_er[i] == flag2:
            temp_valid_et[i] = flag2
            temp_valid_et_flag2 += 1
        elif temp_et[i] > 0.5:
            temp_valid_et[i] = flag1
            temp_valid_et_flag1 += 1
        else:
            temp_valid_et[i] = flag3
            temp_valid_et_flag3 += 1

    # ======= Resultado =======
    temp_resultado = np.full(n - dia_anterior, np.nan)

    temp_resultado_flag6 = 0
    temp_resultado_flag3 = 0
    temp_resultado_flag2 = 0
    temp_resultado_flag1 = 0

    for i in range(n - dia_anterior):
        if temp_valid_et[i] == flag6:
            temp_resultado[i] = flag6
            temp_resultado_flag6 += 1
        elif temp_valid_et[i] in [flag4, flag3]:
            temp_resultado[i] = flag3
            temp_resultado_flag3 += 1
        elif temp_valid_et[i] == flag2:
            temp_resultado[i] = flag2
            temp_resultado_flag2 += 1
        else:
            temp_resultado[i] = flag1
            temp_resultado_flag1 += 1

    # %%
    # ==========================================================================
    #                            Umidade Relativa do Ar    
    # ==========================================================================

    # ======= Validação =======
    ur_valid = np.full(n - dia_anterior, np.nan)

    ur_valid_flag6 = 0
    ur_valid_flag3 = 0
    ur_valid_flag1 = 0

    for i in range(n - dia_anterior):
        if ur_avg[i + dia_anterior] == flag6:
            ur_valid[i] = flag6
            ur_valid_flag6 += 1
        elif ur_avg[i + dia_anterior] < 0 or ur_avg[i + dia_anterior] > 100:
            ur_valid[i] = flag3
            ur_valid_flag3 += 1
        else:
            ur_valid[i] = flag1
            ur_valid_flag1 += 1

    # ======= Desvio Padrão =======
    ur_desv = np.full(n - dia_anterior, np.nan)

    ur_desv_flag6 = 0
    ur_desv_flag3 = 0
    ur_desv_flag1 = 0

    for i in range(n - dia_anterior):
        if ur_valid[i] == flag6:
            ur_desv[i] = flag6
            ur_desv_flag6 += 1
        elif ur_valid[i] == flag3:
            ur_desv[i] = flag3
            ur_desv_flag3 += 1
        elif ur_valid[i] == flag1 and ur_std[i + dia_anterior] == 0 and ur_avg[i + dia_anterior] != 100:
            ur_desv[i] = flag3
            ur_desv_flag3 += 1
        else:
            ur_desv[i] = flag1
            ur_desv_flag1 += 1

    # ======= Deriva UR =======
    deriva_ur = np.full(n - dia_anterior, np.nan)

    deriva_ur_flag6 = 0
    deriva_ur_flag5 = 0
    deriva_ur_flag4 = 0
    deriva_ur_flag3 = 0
    deriva_ur_flag1 = 0

    for i in range(n - dia_anterior):
        if ur_desv[i] == flag6:
            deriva_ur[i] = flag6
            deriva_ur_flag6 += 1
        elif ur_desv[i] == flag5:
            deriva_ur[i] = flag5
            deriva_ur_flag5 += 1
        elif ur_desv[i] == flag4:
            deriva_ur[i] = flag4
            deriva_ur_flag4 += 1
        elif ur_desv[i] == flag3:
            deriva_ur[i] = flag4
            deriva_ur_flag4 += 1
        else:
            if ur_avg[i + dia_anterior] >= ur_min[i + dia_anterior] and ur_avg[i + dia_anterior] <= ur_max[i + dia_anterior]:
                deriva_ur[i] = flag1
                deriva_ur_flag1 += 1
            else:
                deriva_ur[i] = flag3
                deriva_ur_flag3 += 1

    # ======= Resultado =======
    ur_resultado = np.full(n - dia_anterior, np.nan)

    ur_resultado_flag6 = 0
    ur_resultado_flag3 = 0
    ur_resultado_flag1 = 0

    for i in range(n - dia_anterior):
        if deriva_ur[i] == flag6:
            ur_resultado[i] = flag6
            ur_resultado_flag6 += 1
        elif deriva_ur[i] == flag3:
            ur_resultado[i] = flag3
            ur_resultado_flag3 += 1
        elif deriva_ur[i] == flag4:
            ur_resultado[i] = flag3
            ur_resultado_flag3 += 1
        else:
            ur_resultado[i] = flag1
            ur_resultado_flag1 += 1


    # ==========================================================================
    #                           Velocidade do Vento    
    # ==========================================================================

    # ======= Desvio Padrão =======
    vel_desv = np.full(n - dia_anterior, np.nan)

    vel_desv_flag6 = 0
    vel_desv_flag3 = 0
    vel_desv_flag1 = 0

    for i in range(n - dia_anterior):
        if vel_avg[i + dia_anterior] == flag6:
            vel_desv[i] = flag6
            vel_desv_flag6 += 1
        else:
            if vel_avg[i + dia_anterior] > 0:
                if vel_std[i + dia_anterior] == 0:
                    vel_desv[i] = flag3
                    vel_desv_flag3 += 1
                else:
                    vel_desv[i] = flag1
                    vel_desv_flag1 += 1
            else:
                vel_desv[i] = flag1
                vel_desv_flag1 += 1

    # ======= Deriva Vel =======
    deriva_vel = np.full(n - dia_anterior, np.nan)

    deriva_vel_flag6 = 0
    deriva_vel_flag5 = 0
    deriva_vel_flag4 = 0
    deriva_vel_flag3 = 0
    deriva_vel_flag1 = 0

    for i in range(n - dia_anterior):
        if vel_desv[i] == flag6:
            deriva_vel[i] = flag6
            deriva_vel_flag6 += 1
        elif vel_desv[i] == flag5:
            deriva_vel[i] = flag5
            deriva_vel_flag5 += 1
        elif vel_desv[i] in [flag4, flag3]:
            deriva_vel[i] = flag4
            deriva_vel_flag4 += 1
        elif vel_avg[i + dia_anterior] == 0 and vel_std[i + dia_anterior] == 0:
            deriva_vel[i] = flag1
            deriva_vel_flag1 += 1
        else:
            if vel_avg[i + dia_anterior] > vel_min[i + dia_anterior] and vel_avg[i + dia_anterior] < vel_max[i + dia_anterior]:
                deriva_vel[i] = flag1
                deriva_vel_flag1 += 1
            else:
                deriva_vel[i] = flag3
                deriva_vel_flag3 += 1

    # ======= Fisicamente Possível -> Validação =======
    vel_valid_fp = np.full(n - dia_anterior, np.nan)

    vel_valid_fp_flag6 = 0
    vel_valid_fp_flag4 = 0
    vel_valid_fp_flag3 = 0
    vel_valid_fp_flag1 = 0

    for i in range(n - dia_anterior):
        if deriva_vel[i] == flag6:
            vel_valid_fp[i] = flag6
            vel_valid_fp_flag6 += 1
        elif deriva_vel[i] in [flag3, flag4]:
            vel_valid_fp[i] = flag4
            vel_valid_fp_flag4 += 1
        elif deriva_vel[i] == flag1 and vel_avg[i + dia_anterior] < 0:
            vel_valid_fp[i] = flag3
            vel_valid_fp_flag3 += 1
        elif deriva_vel[i] == flag1 and vel_avg[i + dia_anterior] > 25:
            vel_valid_fp[i] = flag3
            vel_valid_fp_flag3 += 1
        else:
            vel_valid_fp[i] = flag1
            vel_valid_fp_flag1 += 1

    # ======= Extremamente Raro =======
    vel_er = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        vel_er[i] = abs(max(vel_avg[dia_anterior - 180 + i - 1 : dia_anterior + i - 1]) - min(vel_avg[dia_anterior - 180 + i - 1 : dia_anterior + i - 1]))
        if vel_er[i] >= flag5:
            vel_er[i] = flag5

    # ======= Extremamente Raro -> Validação =======
    vel_valid_er = np.full(n - dia_anterior, np.nan)

    vel_valid_er_flag6 = 0
    vel_valid_er_flag5 = 0
    vel_valid_er_flag4 = 0
    vel_valid_er_flag2 = 0
    vel_valid_er_flag1 = 0

    for i in range(n - dia_anterior):
        if vel_valid_fp[i] == flag6:
            vel_valid_er[i] = flag6
            vel_valid_er_flag6 += 1
        else:
            if vel_er[i] == flag5:
                vel_valid_er[i] = flag5
                vel_valid_er_flag5 += 1
            elif vel_valid_fp[i] in [flag4, flag3]:
                vel_valid_er[i] = flag4
                vel_valid_er_flag4 += 1
            elif vel_valid_fp[i] == flag1 and vel_er[i] < 0.1:
                vel_valid_er[i] = flag2
                vel_valid_er_flag2 += 1
            else:
                vel_valid_er[i] = flag1
                vel_valid_er_flag1 += 1

    # %%

    # ======= ET =======
    vel_et = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        vel_et[i] = abs(max(vel_avg[i:dia_anterior + i]) - min(vel_avg[i:dia_anterior + i]))
        if vel_et[i] >= flag5:
            vel_et[i] = flag5

    # ======= ET -> Validação =======
    vel_valid_et = np.full(n - dia_anterior, np.nan)

    vel_valid_et_flag6 = 0
    vel_valid_et_flag5 = 0
    vel_valid_et_flag4 = 0
    vel_valid_et_flag3 = 0
    vel_valid_et_flag2 = 0
    vel_valid_et_flag1 = 0

    for i in range(n - dia_anterior):
        if vel_valid_er[i] == flag6:
            vel_valid_et[i] = flag6
            vel_valid_et_flag6 += 1
        elif vel_valid_er[i] == flag5:
            vel_valid_et[i] = flag5
            vel_valid_et_flag5 += 1
        elif vel_valid_er[i] in [flag4, flag3]:
            vel_valid_et[i] = flag4
            vel_valid_et_flag4 += 1
        elif vel_valid_er[i] == flag2:
            vel_valid_et[i] = flag2
            vel_valid_et_flag2 += 1
        elif vel_valid_er[i] == flag1 and vel_et[i] < 0.5:
            vel_valid_et[i] = flag3
            vel_valid_et_flag3 += 1
        else:
            vel_valid_et[i] = flag1
            vel_valid_et_flag1 += 1

    # ======= Resultado =======
    vel_resultado = np.full(n - dia_anterior, np.nan)

    vel_resultado_flag6 = 0
    vel_resultado_flag3 = 0
    vel_resultado_flag2 = 0
    vel_resultado_flag1 = 0

    for i in range(n - dia_anterior):
        if vel_valid_et[i] == flag6:
            vel_resultado[i] = flag6
            vel_resultado_flag6 += 1
        elif vel_valid_et[i] in [flag3, flag4]:
            vel_resultado[i] = flag3
            vel_resultado_flag3 += 1
        elif vel_valid_et[i] == flag2:
            vel_resultado[i] = flag2
            vel_resultado_flag2 += 1
        else:
            vel_resultado[i] = flag1
            vel_resultado_flag1 += 1

    # %%
    # ======= Temperatura =======
    temperatura = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if temp_resultado[i] not in [flag6, flag3]:
            temperatura[i] = temp_avg[dia_anterior + i]

    temperaturax = np.copy(temperatura)
    temperaturay = np.copy(temperatura)

    for i in range(len(temperatura)):
        if temperatura[i] > 1000:
            temperaturax[i] = 0
            temperaturay[i] = np.nan

    quar_quartil_temp = np.nanquantile(temperaturay, 0.75)
    max_temp = np.nanmax(temperaturax)
    mediana_temp = np.nanmedian(temperaturay)
    media_temp = np.nanmean(temperaturay)
    min_temp = np.nanmin(temperaturay)
    prim_quartil_temp = np.nanquantile(temperaturay, 0.25)
    std_temp = np.nanstd(temperaturay)

    # ======= Umidade Relativa =======
    umidade = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if ur_resultado[i] not in [flag6, flag3]:
            umidade[i] = ur_avg[dia_anterior + i]

    umidadex = np.copy(umidade)
    umidadey = np.copy(umidade)

    for i in range(len(umidade)):
        if umidade[i] > 1000:
            umidadex[i] = 0
            umidadey[i] = np.nan

    quar_quartil_ur = np.nanquantile(umidadey, 0.75)
    max_ur = np.nanmax(umidadex)
    mediana_ur = np.nanmedian(umidadey)
    media_ur = np.nanmean(umidadey)
    min_ur = np.nanmin(umidadey)
    prim_quartil_ur = np.nanquantile(umidadey, 0.25)
    std_ur = np.nanstd(umidadey)

    # ======= Velocidade =======
    velocidade = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if vel_resultado[i] not in [flag6, flag3]:
            velocidade[i] = vel_avg[dia_anterior + i]

    velocidadex = np.copy(velocidade)
    velocidadey = np.copy(velocidade)

    for i in range(len(velocidade)):
        if velocidade[i] > 1000:
            velocidadex[i] = 0
            velocidadey[i] = np.nan

    quar_quartil_vel = np.nanquantile(velocidadey, 0.75)
    max_vel = np.nanmax(velocidadex)
    mediana_vel = np.nanmedian(velocidadey)
    media_vel = np.nanmean(velocidadey)
    min_vel = np.nanmin(velocidadey)
    prim_quartil_vel = np.nanquantile(velocidadey, 0.25)
    std_vel = np.nanstd(velocidadey)


    # ======= Hora =======
    max_dia = np.max(dia_mes)
    n1 = max_dia * 24
    horaX = np.full(n1, np.nan)

    cont = 0
    for i in range(n1):
        horaX[i] = cont
        cont = (cont + 1) % 24

    # ======= Temp avg min =======
    temp_avg_min = np.full(n - dia_anterior, np.nan)
    temp_max_min = np.full(n - dia_anterior, np.nan)
    temp_min_min = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if temp_resultado[i] not in [flag6, flag3] or temp_resultado[i] <= 20000:
            if temp_avg[i + dia_anterior] <= flag2:
                temp_avg_min[i] = temp_avg[i + dia_anterior]
                temp_max_min[i] = temp_max[i + dia_anterior]
                temp_min_min[i] = temp_min[i + dia_anterior]

    # ======= Temp avg Hora =======
    temp_avg_hora = np.zeros(n1)
    temp_max_hora = np.zeros(n1)
    temp_min_hora = np.zeros(n1)
    aux = 0
    auxx = 60

    for i in range(n1):
        if auxx < n1:
            temp_avg_hora[i] = np.nanmean(temp_avg_min[aux:auxx])
            temp_max_hora[i] = np.nanmean(temp_max_min[aux:auxx])
            temp_min_hora[i] = np.nanmean(temp_min_min[aux:auxx])
            aux = auxx
            auxx += 60

    # ======= Vel min =======
    vel_avg_min = np.full(n - dia_anterior, np.nan)
    vel_max_min = np.full(n - dia_anterior, np.nan)
    vel_min_min = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if vel_resultado[i] not in [flag6, flag3]:
            if vel_avg[i + dia_anterior] <= flag2:
                vel_avg_min[i] = vel_avg[i + dia_anterior]
                vel_max_min[i] = vel_max[i + dia_anterior]
                vel_min_min[i] = vel_min[i + dia_anterior]

    # ======= Vel Hora =======
    vel_avg_hora = np.zeros(n1)
    vel_max_hora = np.zeros(n1)
    vel_min_hora = np.zeros(n1)
    aux = 0
    auxx = 60

    for i in range(n1):
        if auxx < n1:
            vel_avg_hora[i] = np.nanmean(vel_avg_min[aux:auxx])
            vel_max_hora[i] = np.nanmean(vel_max_min[aux:auxx])
            vel_min_hora[i] = np.nanmean(vel_min_min[aux:auxx])
            aux = auxx
            auxx += 60

    # ======= Umidade relativa - min =======
    ur_avg_min = np.full(n - dia_anterior, np.nan)
    ur_max_min = np.full(n - dia_anterior, np.nan)
    ur_min_min = np.full(n - dia_anterior, np.nan)

    for i in range(n - dia_anterior):
        if ur_resultado[i] not in [flag6, flag3]:
            if ur_avg[i + dia_anterior] <= flag2:
                ur_avg_min[i] = ur_avg[i + dia_anterior]
                ur_max_min[i] = ur_max[i + dia_anterior]
                ur_min_min[i] = ur_min[i + dia_anterior]

    # ======= Umidade relativa - Hora =======
    ur_avg_hora = np.zeros(n1)
    ur_max_hora = np.zeros(n1)
    ur_min_hora = np.zeros(n1)
    aux = 0
    auxx = 60

    for i in range(n1):
        if auxx < n1:
            ur_avg_hora[i] = np.nanmean(ur_avg_min[aux:auxx])
            ur_max_hora[i] = np.nanmean(ur_max_min[aux:auxx])
            ur_min_hora[i] = np.nanmean(ur_min_min[aux:auxx])
            aux = auxx
            auxx += 60

    # %%

    # =============== Integração - hora ======================
    horax = np.arange(24)

    # ======= Matriz auxiliar =======
    matx_dia = np.zeros((24, 24))
    matxx_dia = np.full((max_dia * 24, 24), np.nan)

    for i in range(24):
        matx_dia[i, i] = 1

    aux = 0
    for i in range(max_dia):
        matxx_dia[aux:aux + 24, :] = matx_dia
        aux += 24

    # ======= Temp avg hora =======
    temp_med_horax = temp_avg_hora[:, np.newaxis] * matxx_dia
    temp_med = np.nanmean(temp_med_horax, axis=0)

    # ======= Vel avg hora =======
    vel_med_horax = vel_avg_hora[:, np.newaxis] * matxx_dia
    vel_med = np.nanmean(vel_med_horax, axis=0)

    # ======= UR avg hora =======
    ur_med_horax = ur_avg_hora[:, np.newaxis] * matxx_dia
    ur_med = np.nanmean(ur_med_horax, axis=0)

    # ======= Matrizes com os dados =======
    M = np.full((n - dia_anterior, 37), np.nan)

    M[:, 0] = temp_desv
    M[:, 1] = deriva_temp
    M[:, 2] = temp_fp_min
    M[:, 3] = temp_fp_max
    M[:, 4] = temp_valid_fp
    M[:, 5] = temp_er
    M[:, 6] = temp_valid_er
    M[:, 7] = temp_et
    M[:, 8] = temp_valid_et
    M[:, 9] = temp_resultado

    M[:, 10] = ur_valid
    M[:, 11] = ur_desv
    M[:, 12] = deriva_ur
    M[:, 13] = ur_resultado

    M[:, 14] = vel_desv
    M[:, 15] = deriva_vel
    M[:, 16] = vel_valid_fp
    M[:, 17] = vel_er
    M[:, 18] = vel_valid_er
    M[:, 19] = vel_et
    M[:, 20] = vel_valid_et
    M[:, 21] = vel_resultado

    M[:24, 22] = horax

    M[:n1, 23] = temp_avg_hora
    M[:n1, 24] = temp_max_hora
    M[:n1, 25] = temp_min_hora

    M[:n1, 26] = vel_avg_hora
    M[:n1, 27] = vel_max_hora
    M[:n1, 28] = vel_min_hora

    M[:n1, 29] = ur_avg_hora
    M[:n1, 30] = ur_max_hora
    M[:n1, 31] = ur_min_hora

    M[:24, 33] = horax
    M[:24, 34] = temp_med
    M[:24, 35] = vel_med
    M[:24, 36] = ur_med

    # ======= Matrizes com as Flags =======
    N = np.zeros((6, 16))

    N[0, 0] = temp_desv_flag1
    N[2, 0] = temp_desv_flag3
    N[5, 0] = temp_desv_flag6

    N[0, 1] = deriva_temp_flag1
    N[2, 1] = deriva_temp_flag3
    N[3, 1] = deriva_temp_flag4
    N[4, 1] = deriva_temp_flag5
    N[5, 1] = deriva_temp_flag6

    N[0, 2] = temp_valid_flag1
    N[2, 2] = temp_valid_flag3
    N[3, 2] = temp_valid_flag4
    N[5, 2] = temp_valid_flag6

    N[0, 3] = temp_valid_er_flag1
    N[1, 3] = temp_valid_er_flag2
    N[3, 3] = temp_valid_er_flag4
    N[4, 3] = temp_valid_er_flag5
    N[5, 3] = temp_valid_er_flag6

    N[0, 4] = temp_valid_et_flag1
    N[1, 4] = temp_valid_et_flag2
    N[2, 4] = temp_valid_et_flag3
    N[3, 4] = temp_valid_et_flag4
    N[4, 4] = temp_valid_et_flag5
    N[5, 4] = temp_valid_et_flag6

    N[0, 5] = temp_resultado_flag1
    N[1, 5] = temp_resultado_flag2
    N[2, 5] = temp_resultado_flag3
    N[5, 5] = temp_resultado_flag6

    N[0, 6] = ur_valid_flag1
    N[2, 6] = ur_valid_flag3
    N[5, 6] = ur_valid_flag6

    N[0, 7] = ur_desv_flag1
    N[2, 7] = ur_desv_flag3
    N[5, 7] = ur_desv_flag6

    N[0, 8] = deriva_ur_flag1
    N[2, 8] = deriva_ur_flag3
    N[3, 8] = deriva_ur_flag4
    N[4, 8] = deriva_ur_flag5
    N[5, 8] = deriva_ur_flag6

    N[0, 9] = ur_resultado_flag1
    N[2, 9] = ur_resultado_flag3
    N[5, 9] = ur_resultado_flag6

    N[0, 10] = vel_desv_flag1
    N[2, 10] = vel_desv_flag3
    N[5, 10] = vel_desv_flag6

    N[0, 11] = deriva_vel_flag1
    N[2, 11] = deriva_vel_flag3
    N[3, 11] = deriva_vel_flag4
    N[4, 11] = deriva_vel_flag5
    N[5, 11] = deriva_vel_flag6

    N[0, 12] = vel_valid_fp_flag1
    N[2, 12] = vel_valid_fp_flag3
    N[3, 12] = vel_valid_fp_flag4
    N[5, 12] = vel_valid_fp_flag6

    N[0, 13] = vel_valid_er_flag1
    N[1, 13] = vel_valid_er_flag2
    N[3, 13] = vel_valid_er_flag4
    N[4, 13] = vel_valid_er_flag5
    N[5, 13] = vel_valid_er_flag6

    N[0, 14] = vel_valid_et_flag1
    N[1, 14] = vel_valid_et_flag2
    N[2, 14] = vel_valid_et_flag3
    N[3, 14] = vel_valid_et_flag4
    N[4, 14] = vel_valid_et_flag5
    N[5, 14] = vel_valid_et_flag6

    N[0, 15] = vel_resultado_flag1
    N[1, 15] = vel_resultado_flag2
    N[2, 15] = vel_resultado_flag3
    N[5, 15] = vel_resultado_flag6

    # ======= Box Plot =======
    O = np.full((7, 3), np.nan)

    O[0, 0] = quar_quartil_vel
    O[1, 0] = max_vel
    O[2, 0] = mediana_vel
    O[3, 0] = media_vel
    O[4, 0] = min_vel
    O[5, 0] = prim_quartil_vel
    O[6, 0] = std_vel

    O[0, 1] = quar_quartil_temp
    O[1, 1] = max_temp
    O[2, 1] = mediana_temp
    O[3, 1] = media_temp
    O[4, 1] = min_temp
    O[5, 1] = prim_quartil_temp
    O[6, 1] = std_temp

    O[0, 2] = quar_quartil_ur
    O[1, 2] = max_ur
    O[2, 2] = mediana_ur
    O[3, 2] = media_ur
    O[4, 2] = min_ur
    O[5, 2] = prim_quartil_ur
    O[6, 2] = std_ur

        # Estatísticas dos boxplots
    bxpstats = [
        {'whishi': max_vel, 'whislo': min_vel, 'fliers': [], 'q1': prim_quartil_vel, 'med': media_vel, 'q3': quar_quartil_vel},
        {'whishi': max_temp, 'whislo': min_temp, 'fliers': [], 'q1': prim_quartil_temp, 'med': media_temp, 'q3': quar_quartil_temp},
        {'whishi': max_ur, 'whislo': min_ur, 'fliers': [], 'q1': prim_quartil_ur, 'med': media_ur, 'q3': quar_quartil_ur}
    ]

    plot_boxplot(bxpstats)

    # ======= Matriz com as Flags por variável =======
    contra_n = np.full((6, 16), np.nan)
    contra_n[5, :] = N[0, :]
    contra_n[4, :] = N[1, :]
    contra_n[3, :] = N[2, :]
    contra_n[2, :] = N[3, :]
    contra_n[1, :] = N[4, :]
    contra_n[0, :] = N[5, :]


    # %%
    flag_mapping = {
        flag1: 'Flag1',
        flag2: 'Flag2',
        flag3: 'Flag3',
        flag4: 'Flag4',
        flag5: 'Flag5',
        flag6: 'Flag6'
    }

    # ======= matriz com os dados para exportação =======
    aux = pd.DataFrame(M)

    # Substituir os valores das flags com os nomes correspondentes
    for flag_value, flag_name in flag_mapping.items():
        aux.replace(flag_value, flag_name, inplace=True)

    # Construa o dataframe final
    data = pd.DataFrame(data)  # Supondo que 'data' é um array ou lista de dados
    aux = pd.concat([data, aux], axis=1)

    # Nomes das colunas
    column_names = ['data', 'temp desv padrão', 'max,avg,min - temp', 'temp fp min', 'temp fp max', 'temp validação',
                    'temp er', 'temp validação', 'temp et', 'temp validação', 'resultado', 'ur validação',
                    'ur desv padrão', 'max,avg,min - ur', 'resultado', 'vel desv padrão', 'max,avg,min - vel',
                    'vel validação', 'vel er', 'vel validação', 'vel et', 'vel validação', 'resultado', 'hora',
                    'temp_avg_hora', 'temp_max_hora', 'temp_min_hora', 'vel_avg_hora', 'vel_max_hora',
                    'vel_min_hora', 'ur_avg_hora', 'ur_max_hora', 'ur_min_hora', '', 'hora', 'temperatura',
                    'velocidade', 'umidade relativa']
    aux.columns = column_names


    # Exportar para excel
    nome = f"{nome_arquivo}_CQD_METP"
    aux.to_excel(f"{nome}.xlsx", index=False)

    M = aux.copy()


    # %%
    n = np.array(N)  # Converte 'n' para uma matriz numpy se ainda não for

    # Cria uma lista de listas com os valores das flags
    aux = pd.DataFrame(n)

    # Mapeia as flags para os nomes correspondentes
    flag_mapping = {
        flag1: 'Flag 1',
        flag2: 'Flag 2',
        flag3: 'Flag 3',
        flag4: 'Flag 4',
        flag5: 'Flag 5',
        flag6: 'Flag 6'
    }

    # Substitui os valores das flags com os nomes correspondentes
    for flag_value, flag_name in flag_mapping.items():
        aux.replace(flag_value, flag_name, inplace=True)


    # Define os cabeçalhos das colunas
    header_flags = ['Flag 1', 'Flag 2', 'Flag 3', 'Flag 4', 'Flag 5', 'Flag 6']
    header_columns = [
        'temp desv padrão', 'max,avg,min - temp', 'temp validação fp', 'temp validação er', 'temp validação et',
        'temp resultado', 'ur validação', 'ur desv padrão', 'max,avg,min - ur', 'ur resultado', 'vel desv padrão',
        'max,avg,min - vel', 'vel validação fp', 'vel validação er', 'vel validação et', 'vel resultado'
    ]

    # Cria um DataFrame com os cabeçalhos e os dados
    df_flags = pd.DataFrame(aux.values, columns=header_columns)

    header_df = pd.DataFrame(header_flags, columns=['FLAGS'])
    df_flags_expanded = pd.concat([header_df, df_flags], axis=1)

    nome_flags = f"{nome_arquivo}_Flags_MET"
    df_flags_expanded.to_excel(f"{nome_flags}.xlsx", index=False)

    #N = df_flags_expanded.copy()

    # ======= matriz com o potencial para exportação =======
    o = np.array(O)  
    aux_potential = pd.DataFrame(o)

    # Adiciona os cabeçalhos
    header_potential = ['Q3', 'Max', 'Mediana', 'Média', 'Min', 'Q1', 'Std']

    header_df = pd.DataFrame(header_potential)
    df_flags_expanded = pd.concat([header_df, aux_potential], axis=1)
    column_names_potential = ['', 'Vel', 'Temp', 'UR']
    df_flags_expanded.columns = column_names_potential






    nome_potential = f"{nome_arquivo}_BoxPlot"

    df_flags_expanded.to_excel(f"{nome_potential}.xlsx", index=False)

    O = df_flags_expanded.copy()

    ####### PLOTAGEM
    temp_avg = temp_avg[dia_anterior:]  
    temp_min = temp_min[dia_anterior:]
    temp_max = temp_max[dia_anterior:]
    from flag_plot import flag_plot

    # Função flag_plot é chamada aqui
    flag = flag_plot(temp_avg, temp_resultado)

    # Verifica o tamanho da temp_avg
    n = len(temp_avg)

    # Loop para modificar os valores acima de 60
    for i in range(n):
        if temp_avg[i] > 60:
            temp_avg[i] = 0
            temp_max[i] = 0
            temp_min[i] = 0

    # %%
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from total_xplot3x import xplot3x
    xplot3x(
        variavel1=temp_avg,
        variavel2=flag[:, 1],
        variavel3=flag[:, 2],
        data=data,
        num_figura=fig,
        titulo='Air temperature',
        titulo_var='Temp',
        dia_final=dia_final,
        mes=mes,
        ano=anox,
        lim_sy=40,
        lim_iy=0,
        und_y='[°C]',
        tam_font=10,
        cor1='b',
        cor2=[1, 0.75, 0.035],
        cor3='red',
        nome_arquivo=nome_arquivo
    )
    from total_xplot3cx import total_xplot3cx

    # Exemplo de chamada para a função TOTAL_Xplot3Cx
    total_xplot3cx(
        variavel1=temp_max,
        variavel2=temp_min,
        variavel3=temp_avg,
        data=data,
        num_figura=fig + 1,
        titulo='Air temperature  ',
        dia_final=dia_final,
        mes=mes,
        ano=anox,
        lim_sy=40,
        lim_iy=0,
        und_y='[°C]',
        tam_font=10,
        var1='Temp max',
        var2='Temp min',
        var3='Temp avg',
        nome_arquivo=nome_arquivo
    )

    vel_avg = vel_avg[dia_anterior:]
    vel_min = vel_min[dia_anterior:]
    vel_max = vel_max[dia_anterior:]

    flag = flag_plot(vel_avg, vel_resultado)

    vel_avg[vel_avg > 10] = 0
    vel_max[vel_max > 10] = 0
    vel_min[vel_min > 10] = 0

    from total_xplot3 import total_xplot3


    total_xplot3(variavel1=vel_avg,
                variavel2= flag[:, 1],
                variavel3= flag[:, 2],
                data=data,
                    numfigura=fig + 2,
                    titulo= 'Wind speed ',
                    titulo_var= 'Wind',
                    diafinal= dia_final,
                        mes= mes,
                        ano= anox,
                        limsy= 20,
                        limiy= 0,
                            undy= '[m/s]',
                            tamfont= 10,
                            cor1= 'b',
                            cor2= [1, 0.75, 0.035],
                                cor3= 'red',
                                nome_arquivo= nome_arquivo)

    from total_xplot3c import total_xplot3c

    total_xplot3c(variavel1=vel_max,
                variavel2=vel_min,
                variavel3=vel_avg,
                data=data,
                num_figura=fig+3,
                titulo='Wind speed',
                diafinal=dia_final,
                mes=mes,
                ano=anox,
                lim_sy=20,
                lim_iy=0,
                und_y='[m/s]',
                tam_font=10,
                var1='Wind max',
                var2='Wind min',
                var3='Wind avg',
                nome_arquivo=nome_arquivo)
    
    # ======= UR_AVG =======
    ur_avg = ur_avg[dia_anterior:]
    ur_min = ur_min[dia_anterior:]
    ur_max = ur_max[dia_anterior:]
    flag = flag_plot(ur_avg, ur_resultado)


    ur_avg[(ur_avg > 100) | (ur_avg < 0)] = 0

    xplot3x(variavel1=ur_avg,
            variavel2=flag[:, 1],
            variavel3=flag[:, 2],
            data=data,
            num_figura=fig+4,
            titulo='Relative Humidity',
            titulo_var='RH',
            dia_final=dia_final,
            mes = mes,
            ano= anox,
            lim_sy= 100,
            lim_iy= 0,
            und_y='[%]',
            tam_font= 10,
            cor1='b',
            cor2=[1, 0.75, 0.035],
            cor3='red',
            nome_arquivo= nome_arquivo)
    total_xplot3cx(
        variavel1=ur_max,
        variavel2=ur_min,
        variavel3=ur_avg,
        data=data,
        num_figura=fig+5,
        titulo='Relative Humidity',
        dia_final=dia_final,
        mes=mes,
        ano=anox,
        lim_sy=100,
        lim_iy=0,
        und_y= '[%]',
        tam_font= 10,
        var1='RH max',
        var2='RH min',
        var3='RH avg',
        nome_arquivo= nome_arquivo)
    return M, N, O