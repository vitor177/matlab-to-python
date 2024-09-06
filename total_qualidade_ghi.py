# %%
import numpy as np
import pandas as pd
from total_over_irradiancex import total_over_irradiancex

# return M1, N1, O1, P1
def total_qualidade_ghi(raw_rad, raw_met, dados, header, titulo, nome_var, var, mes, dia_final, anox, fig, nome_arquivo):


    # arquivo = 'data/RN06-2024-06.xlsx'

    # header = pd.read_excel(arquivo)
    # raw_rad = header.iloc[1443:].reset_index(drop=True)
    # raw_met = header.iloc[3:].reset_index(drop=True)


    # dados = pd.read_excel('RN06-2024-06_VarRAD.xlsx')
    # %%
    #var = 16

    data = raw_rad.iloc[:, 0].to_numpy()
    ghi_avg = raw_rad.iloc[:,var-1].copy() # 44640

    data.shape

    # %%
    ghi_avg[ghi_avg > 1500]

    # %%
    ghi_max = raw_rad.iloc[:,var] # 44640
    ghi_min = raw_rad.iloc[:,var+1] # 44640
    ghi_std = raw_rad.iloc[:,var+2] # 44640
    ghi_mcc_clear = raw_rad.iloc[:, var+5] # 44640

    start_row = 1440-20
    ghi_avg_p = raw_met.iloc[start_row:,var-1]

    # %%


    # vou voltar aqui mais tarde, provavelmente previous pegar 20 amostras antes até o final
    #ghi_avg_p
    # %%
    n, m = raw_rad.shape

    horalocal = dados.iloc[:,1]
    dia_mes = dados.iloc[:,2]
    cosAZS = dados.iloc[:,13]
    cosAZS12 = dados.iloc[:,15]
    alpha = dados.iloc[:,17]
    ioh = dados.iloc[:,19]
    iox = dados.iloc[:,21]

    # %%
    flag6 = 60000
    flag5 = 50000
    flag4 = 40000
    flag3 = 30000
    flag2 = 20000
    flag1 = 10000

    # %%
    import numpy as np
    #m = pd.DataFrame()

    kt = np.divide(ghi_avg,ioh)

    for i in range(n):
        if ioh[i] == flag6:
            kt[i] = np.nan
        else:
            if kt[i] > 10:
                kt[i] = 0
            elif kt[i] < 0:
                kt[i] = 0

    # m['Data'] = raw_rad.iloc[:, 0]
    # m['Kt'] = kt
    # %%
    kt_ceu = np.zeros(n)

    for i in range(n):
        if kt[i] >= 0.7:
            kt_ceu[i] = 1
        elif 0.3 < kt[i] < 0.7:
            kt_ceu[i] = 2
        elif 0.0 < kt[i] <= 0.3:
            kt_ceu[i] = 3
        else:
            kt_ceu[i] = np.nan
    # m['Kt Céu'] = kt_ceu

    # m['GHI avg'] = ghi_avg 
    # m['GHI max'] = ghi_max
    # m['GHI min'] = ghi_min
    # m['GHI Sd'] = ghi_std
    # m['GHI mcclear'] = ghi_avg_p

    # %%
    ioh = np.maximum(ioh, 0)
    over_irradiance = np.full(n, np.nan)
    cont_over_irradiance = 0

    # %%
    for i in range(n):
        if ioh[i] == flag6:
            over_irradiance[i] = flag6
        else:
            if ghi_max[i] > ioh[i]:
                over_irradiance[i] = ghi_avg[i]
                cont_over_irradiance+=1
    #m['Over irradiance GHI'] = over_irradiance

    # %%
    # Verificar 12:40
    over_irradiance_1000 = np.full(n, np.nan)
    cont_over_irradiance_1000 = 0
    for i in range(n):
        if over_irradiance[i] > 1000 and over_irradiance[i] < flag6:
            over_irradiance_1000[i] = ghi_avg[i]
            cont_over_irradiance_1000+=1
    #m['Over irradiance GHI > 1000'] = over_irradiance_1000

    # %%
    # LF GHI

    lf_ghi = np.full(n, np.nan)
    lf_ghi_flag6 = 0
    lf_ghi_flag3 = 0
    lf_ghi_flag1 = 0

    for i in range(n):
        if ghi_avg[i] == flag6:
            lf_ghi[i] = flag6
            lf_ghi_flag6 +=1

        else:
            if ghi_avg[i] < -5 and ghi_avg[i] > 200:
                lf_ghi[i] = flag3
                lf_ghi_flag3+=1

            else:
                lf_ghi[i] = flag1
                lf_ghi_flag1+=1
    #m["LF GHI1 -5 a 2000 W/m²"] = lf_ghi
    # %%
    elevacao7 = np.full(n, np.nan)
    elevacao7_flag6 = elevacao7_flag5 = elevacao7_flag4 = elevacao7_flag1 = 0
    for i in range(n):
        if lf_ghi[i] == flag6:
            elevacao7[i] = flag6
            elevacao7_flag6+=1
        elif lf_ghi[i] == flag3:
            elevacao7[i] = flag4
            elevacao7_flag4+=1
        else:
            if lf_ghi[i] == flag1 and alpha[i] > 7:
                elevacao7[i] = flag1
                elevacao7_flag1+=1
            else:
                elevacao7[i] = flag5
                elevacao7_flag5+=1
    #m['Elevação >7° GHI'] = elevacao7

    # Desvio padrão diferente de 0
    desv_pad_0 = np.full(n, np.nan)

    desv_pad_0_flag6 = desv_pad_0_flag5 = desv_pad_0_flag4 = desv_pad_0_flag3 = desv_pad_0_flag2 = desv_pad_0_flag1 = 0

    for i in range(n):
        if ghi_std[i] == flag6:
            desv_pad_0[i] = flag6
            desv_pad_0_flag6+=1
        else:
            if elevacao7[i] == flag5:
                desv_pad_0[i] = flag5
                desv_pad_0_flag5+=1
            elif elevacao7[i] == flag4:
                desv_pad_0[i] = flag4
                desv_pad_0_flag4+=1
            
            else:
                if elevacao7[i] == flag1 and ghi_std[i] == 0:
                    desv_pad_0[i] = flag3
                    desv_pad_0_flag3+=1
                else:
                    desv_pad_0[i] = flag1
                    desv_pad_0_flag1+=1

    #m['Desvio Padrão ?0'] = desv_pad_0
    # %%
    # Inicializando variáveis
    deriva_ghi = np.full(n, np.nan)

    deriva_ghi_flag6 = 0
    deriva_ghi_flag5 = 0
    deriva_ghi_flag4 = 0
    deriva_ghi_flag3 = 0
    deriva_ghi_flag1 = 0

    for i in range(n):
        if desv_pad_0[i] == flag6:
            deriva_ghi[i] = flag6
            deriva_ghi_flag6 += 1
        elif desv_pad_0[i] == flag5:
            deriva_ghi[i] = flag5
            deriva_ghi_flag5 += 1
        elif desv_pad_0[i] == flag4 or desv_pad_0[i] == flag3:
            deriva_ghi[i] = flag4
            deriva_ghi_flag4 += 1
        else:
            if ghi_avg[i] >= ghi_min[i] and ghi_avg[i] <= ghi_max[i]:
                deriva_ghi[i] = flag1
                deriva_ghi_flag1 += 1
            else:
                deriva_ghi[i] = flag3
                deriva_ghi_flag3 += 1

    #m['GHI_min < GHI_avg < GHI_max'] = deriva_ghi

    # %%
    # Kt GHI
    kt_ghi = np.full(n, np.nan)
    kt_ghi_flag6 = 0
    kt_ghi_flag5 = 0
    kt_ghi_flag4 = 0
    kt_ghi_flag1 = 0

    for i in range(n):
        if deriva_ghi[i] == flag6:
            kt_ghi[i] = flag6
            kt_ghi_flag6 += 1
        elif deriva_ghi[i] == flag5:
            kt_ghi[i] = flag5
            kt_ghi_flag5 += 1
        elif deriva_ghi[i] == flag4 or deriva_ghi[i] == flag3:
            kt_ghi[i] = flag4
            kt_ghi_flag4 += 1
        else:
            if iox[i] == 0:
                kt_ghi[i] = flag5
                kt_ghi_flag5 += 1
            else:
                kt_ghi[i] = ghi_avg[i] / (iox[i] * cosAZS[i])
                kt_ghi_flag1 += 1
    #m['kt GHI'] = kt_ghi
    # %%
    #  0<kt<1,2 GHI
    zero_kt_12 = np.full(n, np.nan)
    zero_kt_12_flag6 = 0
    zero_kt_12_flag5 = 0
    zero_kt_12_flag4 = 0
    zero_kt_12_flag3 = 0
    zero_kt_12_flag1 = 0

    for i in range(n):
        if kt_ghi[i] == flag6:
            zero_kt_12[i] = flag6
            zero_kt_12_flag6 += 1
        elif kt_ghi[i] == flag5:
            zero_kt_12[i] = flag5
            zero_kt_12_flag5 += 1
        elif kt_ghi[i] == flag4:
            zero_kt_12[i] = flag4
            zero_kt_12_flag4 += 1
        else:
            if kt_ghi[i] < 0 or kt_ghi[i] > 1.2:
                zero_kt_12[i] = flag3
                zero_kt_12_flag3 += 1
            else:
                zero_kt_12[i] = flag1
                zero_kt_12_flag1 += 1

    #m['0<kt<1,2 GHI'] = zero_kt_12
    # Note que em Python, o operador lógico para "ou" é "or", e para "e" é "and"

    # %%
    # FP min

    fpmin = -4
    fpmax = (1.5 * iox * cosAZS12) + 100

    fp_ghi = pd.Series(np.full(n, np.nan))
    fp_ghi_flag6 = 0
    fp_ghi_flag5 = 0
    fp_ghi_flag4 = 0
    fp_ghi_flag3 = 0
    fp_ghi_flag1 = 0

    for i in range(n):
        if zero_kt_12[i] == flag6:
            fp_ghi[i] = flag6
            fp_ghi_flag6 += 1
        elif zero_kt_12[i] == flag5:
            fp_ghi[i] = flag5
            fp_ghi_flag5 += 1
        elif zero_kt_12[i] == flag4 or zero_kt_12[i] == flag3:
            fp_ghi[i] = flag4
            fp_ghi_flag4 += 1
        else:
            if ghi_avg[i] < fpmin:
                fp_ghi[i] = flag3
                fp_ghi_flag3 += 1
            else:
                if ghi_avg[i] < fpmax[i]:
                    fp_ghi[i] = flag1
                    fp_ghi_flag1 += 1
                else:
                    fp_ghi[i] = flag3
                    fp_ghi_flag3 += 1

    # m['GHI FP min'] = fpmin
    # m['GHI FPmax'] = fpmax
    # m['FP GHI'] = fp_ghi
    # %%
    # Extremamente Raro
    er_min = -2
    er_max = (1.2 * iox * cosAZS12) + 50

    er_ghi = pd.Series(np.full(n, np.nan))
    er_ghi_flag6 = 0
    er_ghi_flag5 = 0
    er_ghi_flag4 = 0
    er_ghi_flag3 = 0
    er_ghi_flag2 = 0
    er_ghi_flag1 = 0

    for i in range(n):
        if fp_ghi[i] == flag6:
            er_ghi[i] = flag6
            er_ghi_flag6 += 1
        elif fp_ghi[i] == flag5:
            er_ghi[i] = flag5
            er_ghi_flag5 += 1
        elif fp_ghi[i] == flag3 or fp_ghi[i] == flag4:
            er_ghi[i] = flag4
            er_ghi_flag4 += 1
        else:
            if ghi_avg[i] < fpmin:
                er_ghi[i] = flag3
                er_ghi_flag3 += 1
            else:
                if ghi_avg[i] < er_min:
                    er_ghi[i] = flag2
                    er_ghi_flag2 += 1
                else:
                    if ghi_avg[i] < er_max[i]:
                        er_ghi[i] = flag1
                        er_ghi_flag1 += 1
                    elif ghi_avg[i] > er_max[i]:
                        er_ghi[i] = flag2
                        er_ghi_flag2 += 1
                    else:
                        er_ghi[i] = flag3
                        er_ghi_flag3 += 1
    # m['GHI ERmin'] = er_min
    # m['GHI ERmax'] = er_max
    # m['GHI ER'] = er_ghi

    # %%
    # 14 GHI CLEAR SKY
    ghi_mcc_clear_x_13 = ghi_mcc_clear*1.3

    #m['1,3 GHI Clear Sky'] = ghi_mcc_clear_x_13
    # %%
    # GHI CLEAR SKY

    ghi_clear_sky = pd.Series(np.full(n, np.nan))

    ghi_clear_sky_flag6 = 0
    ghi_clear_sky_flag5 = 0
    ghi_clear_sky_flag4 = 0
    ghi_clear_sky_flag2 = 0
    ghi_clear_sky_flag1 = 0

    for i in range(n):
        if er_ghi[i] == flag6:
            ghi_clear_sky[i] = flag6
            ghi_clear_sky_flag6 += 1
        elif er_ghi[i] == flag5:
            ghi_clear_sky[i] = flag5
            ghi_clear_sky_flag5 += 1
        elif er_ghi[i] == flag4 or er_ghi[i] == flag3:
            ghi_clear_sky[i] = flag4
            ghi_clear_sky_flag4 += 1
        elif er_ghi[i] == flag2:
            ghi_clear_sky[i] = flag2
            ghi_clear_sky_flag2 += 1
        else:
            if ghi_avg[i] > ghi_mcc_clear_x_13[i]:
                ghi_clear_sky[i] = flag2
                ghi_clear_sky_flag2 += 1
            else:
                ghi_clear_sky[i] = flag1
                ghi_clear_sky_flag1 += 1
    #m['Clear sky GHI'] = ghi_clear_sky
    # %%
    # Consistência Temporal GHI

    cons_temp_ghi = pd.Series(np.full(n, np.nan))

    cons_temp_ghi_flag6 = 0
    cons_temp_ghi_flag5 = 0
    cons_temp_ghi_flag4 = 0
    cons_temp_ghi_flag3 = 0
    cons_temp_ghi_flag2 = 0
    cons_temp_ghi_flag1 = 0

    for i in range(n):
        if ghi_clear_sky[i] == flag6:
            cons_temp_ghi[i] = flag6
            cons_temp_ghi_flag6 += 1
        elif ghi_clear_sky[i] == flag5:
            cons_temp_ghi[i] = flag5
            cons_temp_ghi_flag5 += 1
        elif ghi_clear_sky[i] == flag4 or ghi_clear_sky[i] == flag3:
            cons_temp_ghi[i] = flag4
            cons_temp_ghi_flag4 += 1
        elif ghi_clear_sky[i] == flag2:
            cons_temp_ghi[i] = flag2
            cons_temp_ghi_flag2 += 1
        else:
            if i == n - 1:
                cons_temp_ghi[i] = cons_temp_ghi[i - 1]
            else:
                ghi_diff = abs(ghi_avg[i] - ghi_avg[i + 1])
                if 800 < ghi_diff <= 1000:
                    cons_temp_ghi[i] = flag2
                    cons_temp_ghi_flag2 += 1
                elif ghi_diff > 1000:
                    cons_temp_ghi[i] = flag3
                    cons_temp_ghi_flag3 += 1
                else:
                    cons_temp_ghi[i] = flag1
                    cons_temp_ghi_flag1 += 1

    #m['Consistência temporal GHI'] = cons_temp_ghi
    # %%
    # Persistência GHI
    persistencia_ghi = pd.Series(np.full(n, np.nan))

    persistencia_ghi_flag6 = 0
    persistencia_ghi_flag5 = 0
    persistencia_ghi_flag4 = 0
    persistencia_ghi_flag3 = 0
    persistencia_ghi_flag2 = 0
    persistencia_ghi_flag1 = 0

    for i in range(n):
        if cons_temp_ghi[i] == flag6:
            persistencia_ghi[i] = flag6
            persistencia_ghi_flag6 += 1
        elif cons_temp_ghi[i] == flag5 and elevacao7[i] == flag5:
            persistencia_ghi[i] = flag5
            persistencia_ghi_flag5 += 1
        elif cons_temp_ghi[i] == flag4 or cons_temp_ghi[i] == flag3:
            persistencia_ghi[i] = flag4
            persistencia_ghi_flag4 += 1
        elif cons_temp_ghi[i] == flag2:
            persistencia_ghi[i] = flag2
            persistencia_ghi_flag2 += 1
        else:
            if i + 20 < len(ghi_avg_p):
                if abs(max(ghi_avg_p[i:i+20]) - min(ghi_avg_p[i:i+20])) != 0:
                    persistencia_ghi[i] = flag1
                    persistencia_ghi_flag1 += 1
                else:
                    persistencia_ghi[i] = flag3
                    persistencia_ghi_flag3 += 1
    #m['Persistência GHI'] = persistencia_ghi
    # %%

    # %%
    # Resultado GHI

    resultado_ghi = pd.Series(np.full(n, np.nan))
    resultado_ghi_flag6 = 0
    resultado_ghi_flag5 = 0
    resultado_ghi_flag3 = 0
    resultado_ghi_flag2 = 0
    resultado_ghi_flag1 = 0

    for i in range(n):
        if persistencia_ghi[i] == flag6:
            resultado_ghi[i] = flag6
            resultado_ghi_flag6 += 1
        elif persistencia_ghi[i] == flag5:
            resultado_ghi[i] = flag5
            resultado_ghi_flag5 += 1
        elif persistencia_ghi[i] == flag4 or persistencia_ghi[i] == flag3:
            resultado_ghi[i] = flag3
            resultado_ghi_flag3 += 1
        elif persistencia_ghi[i] == flag2:
            resultado_ghi[i] = flag2
            resultado_ghi_flag2 += 1
        else:
            resultado_ghi[i] = flag1
            resultado_ghi_flag1 += 1

    #m['Resultado GHI'] = resultado_ghi
    # %%
    # %%
    # Cálculo do Potencial
    ghi_avg_min = pd.Series(np.full(n, np.nan))
    for i in range(n):
        if resultado_ghi[i] != flag6 and resultado_ghi[i] != flag3:
            ghi_avg_min[i] = ghi_avg[i]

    # ======= GHI max min =======
    ghi_max_min = pd.Series(np.full(n, np.nan))
    for i in range(n):
        if resultado_ghi[i] != flag6 and resultado_ghi[i] != flag3:
            ghi_max_min[i] = ghi_max[i]

    # ======= GHI min min =======
    ghi_min_min = pd.Series(np.full(n, np.nan))
    for i in range(n):
        if resultado_ghi[i] != flag6 and resultado_ghi[i] != flag3:
            ghi_min_min[i] = ghi_min[i]

    # m['GHI avg min'] = ghi_avg_min
    # m['GHI max min'] = ghi_max_min
    # m['GHI min min'] = ghi_min_min


    # %%

    # CORRIGIR 
    # HORA

    # ======= Dia =======
    max_dia = max(dia_mes)
    n1 = max_dia * 24
    dia = pd.Series(np.full(n, np.nan))
    aux = 0
    cont = 0

    for i in range(n):
        if horalocal[i] == 0:
            if cont < 60:
                dia[aux] = dia_mes[i]
                aux += 1
                cont += 1
        else:
            cont = 0

    # %%
    # ======= Hora =======
    hora = pd.Series(np.full(n, np.nan))
    cont = 0

    for i in range(n1):
        if cont < 60:
            hora[i] = cont
            cont += 1
        else:
            cont = 0
            hora[i] = cont
            cont += 1

    horay = pd.Series(np.full(n, np.nan))
    cont = 0

    for i in range(n1):
        if cont < 24:
            horay[i] = cont
            cont += 1
        else:
            cont = 0
            horay[i] = cont
            cont += 1

    #m['Hora'] = horay
    # %%
    ghi_avg_min_array = ghi_avg_min.to_numpy()
    ghi_avg_min_matrix = ghi_avg_min_array.reshape(-1, 60)
    ghi_avg_hora = pd.Series(np.nanmean(ghi_avg_min_matrix, axis=1))

    #m['GHI avg Hora'] = ghi_avg_hora
    # %%
    ghi_min_min_array = ghi_min_min.to_numpy()
    ghi_min_min_matrix = ghi_min_min_array.reshape(-1, 60)
    ghi_min_hora = pd.Series(np.nanmean(ghi_min_min_matrix, axis=1))

    # %%
    # ======= GHI max Hora =======
    ghi_max_min_array = ghi_max_min.to_numpy()
    ghi_max_min_matrix = ghi_max_min_array.reshape(-1, 60)
    ghi_max_hora = pd.Series(np.nanmean(ghi_max_min_matrix, axis=1))

    #m['GHI max Hora'] = ghi_max_hora
    # Tenho um vetor que tem (24*30=720) elementos, onde cada elemento representa a hora do mes, quero que tu transforme em um vetor
    # de 24 posições, que vai ter a média das 0 horas, 1 hora, 2 horas, assim sucessivamente. Note que o vetor é escrito de forma sequencial
    # por exemplo quero a media da hora 0: entao vou somar o primeiro elemento, com o vigesimo quinto elemento, etc, entendeu? ate formar um vetor que pode ter 30 ou 31 elementos, dependendo do mes
    # %%

    ghi_mcc_clear_array = ghi_mcc_clear.to_numpy()
    ghi_mcc_clear_matrix = ghi_mcc_clear_array.reshape(-1, 60)
    ghi_clear_hora = pd.Series(np.nanmean(ghi_mcc_clear_matrix, axis=1))

    # %%
    # ======= Horax =======
    horax = np.zeros(24)
    for i in range(len(horax)):
        horax[i] = i

    # %%
    ghi_avg_med = np.zeros(24)
    ghi_min_med = np.zeros(24)
    ghi_max_med = np.zeros(24)
    ghi_clear_med = np.zeros(24)

    for hora in range(24):
        indices = [hora + dia * 24 for dia in range(dia_final)]
        ghi_avg_med[hora] = np.nanmean([ghi_avg_hora[indice] for indice in indices])
        ghi_max_med[hora] = np.nanmean([ghi_max_hora[indice] for indice in indices])
        ghi_min_med[hora] = np.nanmean([ghi_min_hora[indice] for indice in indices])
        ghi_clear_med[hora] = np.nanmean([ghi_clear_hora[indice] for indice in indices])
    # %%

    #==========================================================================
    #                           Sobreirradiancia     
    #==========================================================================

    vel_avg = raw_rad.iloc[:,3]
    temp_avg = raw_rad.iloc[:,7]
    ur_avg = raw_rad.iloc[:,11]

    Mx, Xz = total_over_irradiancex(raw_rad,dados,header,'Over_Irradiance',nome_arquivo)


    # %%
    over_irradiance_1000 = Mx[:,0]

    for i in range(n):
        if over_irradiance_1000[i] < 1000:
            over_irradiance_1000[i] = np.nan


    # %%
    #m.to_excel('_CQD_GHI.xlsx', engine='xlsxwriter', index=False)   
        # %%
    # ======= Matriz com os dados =======
    m = np.full((n, 33), np.nan, dtype=object)


    m[:, 0] = kt
    m[:, 1] = kt_ceu
    m[:, 2] = ghi_avg
    m[:, 3] = ghi_max
    m[:, 4] = ghi_min
    m[:, 5] = ghi_std
    m[:, 6] = ghi_mcc_clear
    m[:, 7] = over_irradiance
    m[:, 8] = over_irradiance_1000
    m[:, 9] = lf_ghi
    m[:, 10] = elevacao7
    m[:, 11] = desv_pad_0
    m[:, 12] = deriva_ghi
    m[:, 13] = kt_ghi
    m[:, 14] = zero_kt_12
    m[:, 15] = fpmin
    m[:, 16] = fpmax
    m[:, 17] = fp_ghi
    m[:, 18] = er_min
    m[:, 19] = er_max
    m[:, 20] = er_ghi
    m[:, 21] = ghi_mcc_clear_x_13
    m[:, 22] = ghi_clear_sky
    m[:, 23] = cons_temp_ghi
    m[:, 24] = persistencia_ghi
    m[:, 25] = resultado_ghi
    m[:, 26] = ghi_avg_min
    m[:, 27] = ghi_max_min
    m[:, 28] = ghi_min_min
    m[:, 29] = horay
    m[:24*dia_final, 30] = ghi_avg_hora
    m[:24*dia_final, 31] = ghi_max_hora
    m[:24*dia_final, 32] = ghi_min_hora

    # %%

    # ======= Matriz com as Flags =======
    n = np.zeros((6, 13), dtype=object)

    n[0, 0] = cont_over_irradiance
    n[0, 1] = cont_over_irradiance_1000

    n[0, 1] = lf_ghi_flag1
    n[2, 1] = lf_ghi_flag3
    n[5, 1] = lf_ghi_flag6

    n[0, 2] = elevacao7_flag1
    n[3, 2] = elevacao7_flag4
    n[4, 2] = elevacao7_flag5
    n[5, 2] = elevacao7_flag6

    n[0, 3] = desv_pad_0_flag1
    n[2, 3] = desv_pad_0_flag3
    n[3, 3] = desv_pad_0_flag4
    n[4, 3] = desv_pad_0_flag5
    n[5, 3] = desv_pad_0_flag6


    # %%

    n[0, 4] = deriva_ghi_flag1
    n[2, 4] = deriva_ghi_flag3
    n[3, 4] = deriva_ghi_flag4
    n[4, 4] = deriva_ghi_flag5
    n[5, 4] = deriva_ghi_flag6

    n[0, 5] = kt_ghi_flag1
    n[3, 5] = kt_ghi_flag4
    n[4, 5] = kt_ghi_flag5
    n[5, 5] = kt_ghi_flag6

    n[0, 6] = zero_kt_12_flag1
    n[2, 6] = zero_kt_12_flag3
    n[3, 6] = zero_kt_12_flag4
    n[4, 6] = zero_kt_12_flag5
    n[5, 6] = zero_kt_12_flag6

    n[0, 7] = fp_ghi_flag1
    n[2, 7] = fp_ghi_flag3
    n[3, 7] = fp_ghi_flag4
    n[4, 7] = fp_ghi_flag5
    n[5, 7] = fp_ghi_flag6

    n[0, 8] = er_ghi_flag1
    n[1, 8] = er_ghi_flag2
    n[2, 8] = er_ghi_flag3
    n[3, 8] = er_ghi_flag4
    n[4, 8] = er_ghi_flag5
    n[5, 8] = er_ghi_flag6

    n[0, 9] = ghi_clear_sky_flag1
    n[1, 9] = ghi_clear_sky_flag2
    n[3, 9] = ghi_clear_sky_flag4
    n[4, 9] = ghi_clear_sky_flag5
    n[5, 9] = ghi_clear_sky_flag6

    n[0, 10] = cons_temp_ghi_flag1
    n[1, 10] = cons_temp_ghi_flag2
    n[2, 10] = cons_temp_ghi_flag3
    n[3, 10] = cons_temp_ghi_flag4
    n[4, 10] = cons_temp_ghi_flag5
    n[5, 10] = cons_temp_ghi_flag6

    n[0, 11] = persistencia_ghi_flag1
    n[1, 11] = persistencia_ghi_flag2
    n[2, 11] = persistencia_ghi_flag3
    n[3, 11] = persistencia_ghi_flag4
    n[4, 11] = persistencia_ghi_flag5
    n[5, 11] = persistencia_ghi_flag6

    n[0, 12] = resultado_ghi_flag1
    n[1, 12] = resultado_ghi_flag2
    n[2, 12] = resultado_ghi_flag3
    n[4, 12] = resultado_ghi_flag5
    n[5, 12] = resultado_ghi_flag6

    # ======= Matriz com a média horária =======
    o = np.zeros((24, 5), dtype=object)

    o[:, 0] = horax
    o[:, 1] = ghi_avg_med
    o[:, 2] = ghi_max_med
    o[:, 3] = ghi_min_med
    o[:, 4] = ghi_clear_med

    # %%
    # %%

    # ======= Matriz com a Sobreirradiancia =======
    size = len(over_irradiance_1000)

    p = np.full((size, 4), np.nan)

    p[:, 0] = over_irradiance_1000
    p[:, 1] = ioh
    p[:, 2] = ghi_avg
    p[:, 3] = resultado_ghi

    # %%

    aux = m.copy()
    potx = m.copy()

    popx = m.copy()

    size, m = aux.shape

    # %%
    aux = pd.DataFrame(aux)

    flag_map = {
        flag6: 'Flag6',
        flag5: 'Flag5',
        flag4: 'Flag4',
        flag3: 'Flag3',
        flag2: 'Flag2',
        flag1: 'Flag1'
    }

    aux.replace(flag_map, inplace=True)

    auxx = np.column_stack((data, aux))
    aux_headers = [
        'Data', 'Kt', 'Kt ceu', 'GHI avg', 'GHI max', 'GHI min', 'GHI std', 
        'GHI MCC clear', 'Over irradiance', 'Over irradiance > 1000', 
        'LF GHI', 'Elevação >7° GHI', 'Desvio padrão >0', 
        'Deriva GHI', 'Kt GHI', '0<kt<1,2 GHI', 'FPmin', 'FPmax', 'FP GHI', 
        'ERmin', 'ERmax', 'ER GHI', 'GHI MCC clear x 13', 'Clear sky GHI', 
        'Consistência temporal GHI', 'Persistência GHI', 'Resultado GHI', 
        'GHI avg min', 'GHI max min', 'GHI min min', 'Hora', 
        'GHI_avg_Hora', 'GHI_min_Hora', 'GHI_max_Hora'
    ]

    # %%
    aux = pd.DataFrame(auxx)
    aux.columns = aux_headers
    nome = f"{nome_arquivo}_CQD_{nome_var}"
    aux.to_excel(f'{nome}.xlsx', index=False)
    M = aux.copy()

    # %%
    aux = pd.DataFrame(n)
    aux = aux.iloc[:, 1:]
    new_line = pd.Series(['Flag 1','Flag 2','Flag 3','Flag 4','Flag 5','Flag 6'])
    aux = pd.concat([new_line, aux], axis=1)
    aux.columns = ['FLAGS','LF GHI1''-5 a 2000 W/m²"','Elevação >7° GHI','Desvio Padrão ?0','GHI_min < GHI_avg < GHI_max','kt GHI','0<kt<1,2 GHI','FP GHI','ER GHI','Clear sky GHI','Consistência temporal GHI','Persistência GHI','Resultado GHI']
    nome = f"{nome_arquivo}_Flags_RAD_{nome_var}"
    aux.to_excel(f"{nome}.xlsx", index=False)
    N = aux.copy()
    # %%

    aux = pd.DataFrame(o)
    aux.columns = ['Hora','GHI avg (W/m²)','GHI max (W/m²)','GHI min (W/m²)','GHI de Céu Claro (W/m²)']
    nome = f"{nome_arquivo}_Potencial_{nome_var}"
    aux.to_excel(f"{nome}.xlsx", index=False)
    O = aux

    # %%
    #ghi_avg = raw_rad.iloc[:,var-1] # 44640

    # %%
    # %%
    from total_xplot2 import total_xplot2
    from total_xplot3 import total_xplot3
    from total_xplot3c import total_xplot3c
    from flag_plot import flag_plot


        # total_xplot2(variavel1=over_irradiance_plot, variavel2=ioh, data=data, num_figura=fig, 
        #             titulo='Overirradiance Events - GHI ', dia_final=dia_final, mes=mes, ano=ano,
        #             lim_sy=1800, lim_iy=0, und_y='W/m²', tam_font=10, cor1='blue', cor2='k', 
        #             nome_arquivo=nome_arquivo)
    # %%
    total_xplot2(variavel1=over_irradiance_1000, variavel2=ioh, data=data, num_figura=fig, titulo=f"Overradiance Events -  {nome_var}",
                dia_final=dia_final, mes=mes, ano=anox, lim_sy=1800, lim_iy=0, und_y='W/m²',
                tam_font=10, cor1='blue', cor2='k', nome_arquivo=nome_arquivo) 
    data = pd.DataFrame(data)
    # %%
    flag = flag_plot(ghi_avg, resultado=resultado_ghi)
    # %%
    for i in range(flag.shape[0]):
        if ghi_avg[i] > 2000:
            ghi_avg[i] = 0
            ghi_max[i] = 0
            ghi_min[i] = 0

    P = flag.copy()
    # %%
    from total_xplot3c import total_xplot3c
    data = pd.DataFrame(data)
    total_xplot3c(variavel1=ghi_max,
                variavel2=ghi_min,
                variavel3=ghi_avg,
                data=data,
                num_figura=fig+2,
                titulo=titulo,
                diafinal=dia_final,
                mes=mes,
                ano=anox,
                lim_sy=1800,
                lim_iy=0,
                und_y='[m/s]',
                tam_font=10,
                var1='GHI1 max',
                var2='GHI12 min',
                var3='GHI1 avg',
                nome_arquivo=nome_arquivo)
    # %%
    data = np.array(data)
    total_xplot3(variavel1=ghi_max,
                variavel2= flag[:, 1],
                variavel3= flag[:, 2],
                data=data,
                    numfigura=fig + 1,
                    titulo= titulo,
                    titulo_var= nome_var,
                    diafinal= dia_final,
                        mes= mes,
                        ano= anox,
                        limsy= 1800,
                        limiy= 0,
                            undy= '[m/s]',
                            tamfont= 10,
                            cor1= 'b',
                            cor2= [1, 0.75, 0.035],
                                cor3= 'red',
                                nome_arquivo= nome_arquivo)
    # %%

    # %%
    # Q = TOTAL_energia(POTX,GHI_avg,Flag1,n,fig+3,Nome_Arquivo,titulo);
    n = ghi_avg.shape[0]

    # %%
    ghi_pot = np.full(n, np.nan)

    # Preencher GHI_pot com base no Flag1
    for i in range(n):
        if potx[i, 25] == flag1:
            ghi_pot[i] = ghi_avg[i]
    # Agrupar em faixas
    bins = np.arange(0, 1850, 50)
    cont, _ = np.histogram(ghi_pot[~np.isnan(ghi_pot)], bins=bins)
    soma_cont = np.sum(cont)
    porcentagem = (cont / soma_cont) * 100

    faixa = bins[:-1]
    faixa1 = np.arange(0, 1850, 100)

    contx = np.zeros(5)
    ranges = [(0, 300), (300, 700), (700, 1000), (1000, 1200), (1200, np.inf)]
    for i in range(5):
        contx[i] = np.sum((ghi_pot >= ranges[i][0]) & (ghi_pot < ranges[i][1]))

    soma_contx = np.sum(contx)
    porcen = (contx / soma_contx) * 100
    # %%
    # %%
    # Exportação para Excel
    Q = np.full((36, 7), np.nan, dtype=object)
    Q[:, 0] = faixa
    Q[:, 1] = cont
    Q[:, 2] = porcentagem


    faixa_adicional = [
        'G <= 300',
        '300 < G <= 700',
        '700 < G <= 1000',
        '1000 < G <= 1200',
        'G >= 1200'
    ]
    faixa_adicional_full = faixa_adicional + [''] * (36 - len(faixa_adicional))


    # %%
    # Adiciona dados de faixa adicional
    contx = np.append(contx, [np.nan] * (37 - 5))
    porcen = np.append(porcen, [np.nan] * (37 - 5))
    Q[: , 4] = faixa_adicional_full

    Q[: , 5] = contx[:36]
    Q[: , 6] = porcen[:36]

    headers = ['Faixa', 'Quantidade de dados', 'Porcentagem', '', 'Faixa', 'Quantidade de dados', 'Porcentagem']
    df = pd.DataFrame(Q, columns=headers)

    df.to_excel(f'{nome_arquivo}_Energia.xlsx', index=False)


    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import UnivariateSpline

    faixaNew = np.arange(0, 1801, 5)

    # Interpolação suave usando UnivariateSpline
    spline = UnivariateSpline(faixa, porcentagem, k=3, s=0)
    suave = spline(faixaNew)

    # Configuração da figura
    fig, ax = plt.subplots(figsize=(9.5, 4)) 

    # Plotar os dados
    ax.plot(faixaNew, suave, 'b', linewidth=1.5)

    # Configurações do gráfico
    ax.set_xlabel('Irradiance [W/m²]', fontsize=10)
    ax.set_ylabel('Energy Fraction [%]', fontsize=10)
    ax.set_title('Irradiance Intensity Distribution', fontsize=10)
    ax.grid(True)
    ax.set_xlim([0, 1800])
    ax.set_ylim([0, 20])
    ax.set_xticks(np.arange(0, 1801, 100))
    ax.set_xticklabels([str(i) for i in np.arange(0, 1801, 100)])
    ax.tick_params(axis='both', which='major', labelsize=10)

    fig.savefig(f'{nome_arquivo}_{titulo}_energia.pdf', format='pdf')
    fig.savefig(f'{nome_arquivo}_{titulo}_energia.svg', format='svg')



    return M, N, O, P
