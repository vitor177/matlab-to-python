# %%
from total_xplot_dia import total_xplot_dia
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from total_xplot2 import total_xplot2
from total_xplot_over import total_xplot_over
#function [P] = TOTAL_over_irradiance(RAW,DADOS,header,col,fig,dia_final,mes,ano,Arquivo,Nome_Arquivo)

def total_over_irradiance(raw, dados, header, col, fig, dia_final, mes, ano, arquivo, nome_arquivo):

    # =================================================================
    #                    Detecção de eventos de sobreirradiancia     
    # =================================================================

    # ======= Informações dos dados brutos =======

    #raw_met = pd.read_excel(arquivo, skiprows=3)
    #dados = pd.read_excel('RN01-2024-05_VarRAD.xlsx')
    # %%
    col = 15

    data = raw.iloc[:, 0]
    data1 = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')

    ghi_avg = pd.to_numeric(raw.iloc[:, col])
    ghi_max = pd.to_numeric(raw.iloc[:, col])  # GHI 1 max

    vel_avg = pd.to_numeric(raw.iloc[:, 3])
    temp_avg = pd.to_numeric(raw.iloc[:, 7])
    ur_avg = pd.to_numeric(raw.iloc[:, 11])
    prec_avg = pd.to_numeric(raw.iloc[:, 3])
    dir_avg = pd.to_numeric(raw.iloc[:, 3])
    press_avg = pd.to_numeric(raw.iloc[:, 3])  # retirar depois

    clear_sky = pd.to_numeric(raw.iloc[:, 21])
    n, m = raw.shape

    for i in range(n):
        if ghi_avg[i] > 2000:
            ghi_avg[i] = 0
        if ghi_max[i] > 2000:
            ghi_max[i] = 0

    # ======= Informações da VarRad =======
    horalocal = dados.iloc[:, 1]
    dia_mes = dados.iloc[:, 2]
    cosazs = dados.iloc[:, 13]
    cosazs12 = dados.iloc[:, 15]
    alpha = dados.iloc[:, 17]
    ioh = pd.to_numeric(dados.iloc[:, 19])
    iox = pd.to_numeric(dados.iloc[:, 21])

    ioh[ioh < 0] = 0

    ghi_avg1 = ghi_max.copy()

    over_irradiance = np.full(n, np.nan)
    over_irradiance_plot = np.full(n, np.nan)
    over_irradiance_aux = np.zeros(n)
    cont_over_irradiance = 0
    temp_over = np.full(n, np.nan)
    temp = 0
    k = 1

    aux_vel_avg = np.full(n, np.nan)
    aux_temp_avg = np.full(n, np.nan)
    aux_ur_avg = np.full(n, np.nan)
    aux_dir_avg = np.full(n, np.nan)
    aux_prec_avg = np.full(n, np.nan)
    aux_press_avg = np.full(n, np.nan)

    for i in range(n):
        if ghi_max[i] >= ioh[i]:
            over_irradiance[i] = ghi_max[i]
            over_irradiance_aux[i] = 1
            aux_vel_avg[i] = vel_avg[i]
            aux_temp_avg[i] = temp_avg[i]
            aux_ur_avg[i] = ur_avg[i]
            aux_dir_avg[i] = dir_avg[i]
            aux_prec_avg[i] = prec_avg[i]
            aux_press_avg[i] = press_avg[i]
            cont_over_irradiance += 1
            temp += 1
        if i > 1 and over_irradiance_aux[i-1] == 1 and over_irradiance_aux[i] == 0:
            temp_over[k-1] = temp
            temp = 0
            k += 1
        if ghi_max[i] >= ioh[i] and ghi_max[i] >= 1000:
            over_irradiance_plot[i] = ghi_max[i]


    # %%
    # %%

    k = 0
    for i in range(n):
        if temp_over[i] > 0:
            k += 1
    quantidade_eventos = k

    # %%

    ###########################################################################
    # OVER IRRADIANCE > 1000


    over_irradiance_1000 = np.full(n, np.nan)
    over_irradiance_1000_aux = np.zeros(n)
    temp_over_1000 = np.zeros(n)
    posicao_over_1000 = np.full(n, np.nan)
    hora_over_1000 = [np.nan] * n
    temp_over_1000_aux = np.full(n, np.nan)
    temp_over_1000_auxx = np.full(n, np.nan)

    cont_over_irradiance_1000 = 0
    temp_1000 = 0

    k = 1

    # %%
    over_irradiance
    # %%

    for i in range(n):
        if over_irradiance[i] >= 1000 and over_irradiance[i] < 1367:
            over_irradiance_1000[i] = over_irradiance[i]
            over_irradiance_1000_aux[i] = 1
            cont_over_irradiance_1000 += 1
            temp_1000 += 1
            temp_over_1000_aux[i] = temp_1000

        if i > 1 and over_irradiance_1000_aux[i-1] == 1 and over_irradiance_1000_aux[i] == 0:
            temp_over_1000[k-1] = temp_1000
            temp_over_1000_auxx[i] = temp_1000
            #print(data[i-temp_1000])
            hora_over_1000[k-1] = data[i-temp_1000]
            temp_1000 = 0
            posicao_over_1000[k-1] = i
            k += 1

    # %%
    #############################################

    k = 0
    for i in range(n):
        if temp_over_1000[i] > 0:
            k += 1
    quantidade_eventos_1000 = k

    maior_temp_1000 = np.max(temp_over_1000)
    data_maior_1000 = 1
    maior_evento_1000 = np.full(int(maior_temp_1000), np.nan)

    for i in range(n):
        if temp_over_1000_aux[i] == maior_temp_1000:
            aux = i
            data_maior_1000 = i
            for k in range(int(maior_temp_1000)):
                maior_evento_1000[k] = ghi_max[aux-k]

    # media da irradiancia do evento de maior duração
    medio_maior_evento_1000 = np.nanmean(maior_evento_1000)

    # !
    max_maior_evento_1000 = np.nanmax(maior_evento_1000) if np.nanmax(maior_evento_1000) > 0 else 0

    valor_1000_1 = np.full(n, np.nan)
    valor_1000_2 = np.full(n, np.nan)
    valor_1000_3 = np.full(n, np.nan)
    valor_1000_4 = np.full(n, np.nan)
    valor_1000_5 = np.full(n, np.nan)

    cont_1000_1 = 0
    cont_1000_2 = 0
    cont_1000_3 = 0
    cont_1000_4 = 0
    cont_1000_5 = 0

    resumo_evento_1000 = np.full((1000, 5), np.nan)
    resumo_evento_data_1000 = [np.nan] * 1000

    evento_auxxx = np.full(n, np.nan)
    energia_clear_sky_1000 = np.full(n, np.nan)
    j = 1

    # %%
    over_irradiance_1000
    # %%
    for i in range(n):
        if 0 < temp_over_1000_auxx[i] <= 1:
            cont_1000_1 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_1[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
                energia_clear_sky_1000[k-1] = clear_sky[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
            resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
            #evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
            j += 1
        if 1 < temp_over_1000_auxx[i] <= 2:
            cont_1000_2 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_2[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
                energia_clear_sky_1000[k-1] = clear_sky[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
            resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
            evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
            j += 1
        if 2 < temp_over_1000_auxx[i] <= 3:
            cont_1000_3 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_3[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
                energia_clear_sky_1000[k-1] = clear_sky[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
            resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
            evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
            j += 1
        if 3 < temp_over_1000_auxx[i] <= 4:
            cont_1000_4 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_4[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
                energia_clear_sky_1000[k-1] = clear_sky[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
            resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
            evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
            j += 1
        if 4 < temp_over_1000_auxx[i]:
            cont_1000_5 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_5[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
                energia_clear_sky_1000[k-1] = clear_sky[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
            resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
            evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
            j += 1

    data_resumo_evento = {
        'mean_irradiance': resumo_evento_1000[:, 0],
        'max_irradiance': resumo_evento_1000[:, 1],
        'duration': resumo_evento_1000[:, 2],
        'mean_energy': resumo_evento_1000[:, 3],
        'mean_energy_clear_sky': resumo_evento_1000[:, 4]
    }

    resumo_evento_df = pd.DataFrame(data_resumo_evento)
    resumo_evento_data_1000 = np.array(resumo_evento_data_1000)


    # Converter resumo_evento_data_1000 para DataFrame
    resumo_evento_data_1000_df = pd.DataFrame(resumo_evento_data_1000, columns=['Data'])

    # Concatenar os DataFrames
    aux_1000 = pd.concat([resumo_evento_data_1000_df, resumo_evento_df], axis=1)

    # Definir nomes das colunas
    aux_1000.columns = ['Data', 'Valor médio do evento > 1000 W/m²', 'Valor máximo do evento > 1000 W/m²',
                                    'Duração > 1000 W/m²', 'Energia do evento > 1000 (Wh/m²)', 'Energia de céu claro']

    energia_1000 = aux_1000[['Data', 'Energia do evento > 1000 (Wh/m²)']].copy()
    # %%
    resumo_evento_data_1000.shape


    # %%
    #print(np.where(~np.isnan(aux_1000['Valor máximo do evento > 1000 W/m²'])))
    # %%
    #aux_1000.to_excel(nome, index=False)
    # %%

    std_1000_1 = np.nanmean(valor_1000_1)
    std_1000_2 = np.nanmean(valor_1000_2)
    std_1000_3 = np.nanmean(valor_1000_3)
    std_1000_4 = np.nanmean(valor_1000_4)
    std_1000_5 = np.nanmean(valor_1000_5)

    max_1000_1 = np.max(valor_1000_1)
    max_1000_2 = np.max(valor_1000_2)
    max_1000_3 = np.max(valor_1000_3)
    max_1000_4 = np.max(valor_1000_4)
    max_1000_5 = np.max(valor_1000_5)


    # %%

    # OVER IRRADIANCE > 1367

    over_irradiance_1367 = np.full(n, np.nan)
    over_irradiance_1367_aux = np.zeros(n)
    temp_over_1367 = np.zeros(n)
    posicao_over_1367 = np.full(n, np.nan)
    hora_over_1367 = [np.nan] * n
    temp_over_1367_aux = np.full(n, np.nan)
    temp_over_1367_aux_x = np.full(n, np.nan)

    cont_over_irradiance_1367 = 0
    temp_1367 = 0
    k = 1

    for i in range(n):
        if over_irradiance[i] >= 1367:
            over_irradiance_1367[i] = over_irradiance[i]
            over_irradiance_1367_aux[i] = 1
            cont_over_irradiance_1367 += 1
            temp_1367 += 1
            temp_over_1367_aux[i] = temp_1367
        if i > 1 and over_irradiance_1367_aux[i-1] == 1 and over_irradiance_1367_aux[i] == 0:
            temp_over_1367[k-1] = temp_1367
            temp_over_1367_aux_x[i] = temp_1367
            hora_over_1367[k-1] = data[i-temp_1367]
            temp_1367 = 0
            posicao_over_1367[k-1] = i
            k += 1

    # %%

    k = 0

    for i in range(n):
        if temp_over_1367[i] > 0:
            k += 1

    quantidade_eventos_1367 = k

    maior_temp_1367 = np.max(temp_over_1367)  # maior tempo de um evento

    data_maior_1367 = 1
    maior_evento_1367 = np.full(int(maior_temp_1367), np.nan)  # Cria o vetor com o maior evento

    # %%

    for i in range(n):
        if temp_over_1367_aux[i] == maior_temp_1367:
            aux = i
            data_maior_1367 = i
            for k in range(int(maior_temp_1367)):
                maior_evento_1367[k] = ghi_max[aux-k]

    # Erro matlab to python
    if maior_evento_1367.size > 0:
        medio_maior_evento_1367 = np.nanmean(maior_evento_1367)
    else:
        medio_maior_evento_1367 = np.nan

    if maior_evento_1367.size > 0 and np.nanmax(maior_evento_1367) > 0:
        max_maior_evento_1367 = np.nanmax(maior_evento_1367)
    else:
        max_maior_evento_1367 = 0


    # %%
    # TEMPO EVENTOS > 1367

    valor_1367_1 = np.full(n, np.nan)  # Armazena os eventos maiores que 1367 com até 1 min
    valor_1367_2 = np.full(n, np.nan)  # Armazena os eventos maiores que 1367 com até 2 min
    valor_1367_3 = np.full(n, np.nan)  # Armazena os eventos maiores que 1367 com até 3 min
    valor_1367_4 = np.full(n, np.nan)  # Armazena os eventos maiores que 1367 com até 4 min
    valor_1367_5 = np.full(n, np.nan)  # Armazena os eventos maiores que 1367 com 5 ou mais min

    cont_1367_1 = 0
    cont_1367_2 = 0
    cont_1367_3 = 0
    cont_1367_4 = 0
    cont_1367_5 = 0

    resumo_evento_1367 = np.full((1000, 5), np.nan)
    resumo_evento_data_1367 = [np.nan] * 1000
    evento_auxxx = np.full(n, np.nan)
    energia_clear_sky_1367 = np.full(n, np.nan)
    j = 0

    for i in range(n):
        if 0 < temp_over_1367_aux_x[i] <= 1:
            cont_1367_1 += 1
            for k in range(1, int(temp_over_1367_aux_x[i])+1):
                valor_1367_1[i-k] = over_irradiance_1367[i-k]
                evento_auxxx[k-1] = over_irradiance_1367[i-k]
                energia_clear_sky_1367[k-1] = clear_sky[i-k]
            resumo_evento_data_1367[j] = data[i]
            resumo_evento_1367[j, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j, 2] = temp_over_1367_aux_x[i]
            resumo_evento_1367[j, 3] = (np.nanmean(evento_auxxx) * temp_over_1367_aux_x[i]) / 60
            resumo_evento_1367[j, 4] = (np.nanmean(energia_clear_sky_1367) * temp_over_1367_aux_x[i]) / 60
            evento_auxxx[:int(temp_over_1367_aux_x[i])] = np.nan
            j += 1
        elif 1 < temp_over_1367_aux_x[i] <= 2:
            cont_1367_2 += 1
            for k in range(1, int(temp_over_1367_aux_x[i])+1):
                valor_1367_2[i-k] = over_irradiance_1367[i-k]
                evento_auxxx[k-1] = over_irradiance_1367[i-k]
                energia_clear_sky_1367[k-1] = clear_sky[i-k]
            resumo_evento_data_1367[j] = data[i]
            resumo_evento_1367[j, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j, 2] = temp_over_1367_aux_x[i]
            resumo_evento_1367[j, 3] = (np.nanmean(evento_auxxx) * temp_over_1367_aux_x[i]) / 60
            resumo_evento_1367[j, 4] = (np.nanmean(energia_clear_sky_1367) * temp_over_1367_aux_x[i]) / 60
            evento_auxxx[:int(temp_over_1367_aux_x[i])] = np.nan
            j += 1
        elif 2 < temp_over_1367_aux_x[i] <= 3:
            cont_1367_3 += 1
            for k in range(1, int(temp_over_1367_aux_x[i])+1):
                valor_1367_3[i-k] = over_irradiance_1367[i-k]
                evento_auxxx[k-1] = over_irradiance_1367[i-k]
                energia_clear_sky_1367[k-1] = clear_sky[i-k]
            resumo_evento_data_1367[j] = data[i]
            resumo_evento_1367[j, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j, 2] = temp_over_1367_aux_x[i]
            resumo_evento_1367[j, 3] = (np.nanmean(evento_auxxx) * temp_over_1367_aux_x[i]) / 60
            resumo_evento_1367[j, 4] = (np.nanmean(energia_clear_sky_1367) * temp_over_1367_aux_x[i]) / 60
            evento_auxxx[:int(temp_over_1367_aux_x[i])] = np.nan
            j += 1
        elif 3 < temp_over_1367_aux_x[i] <= 4:
            cont_1367_4 += 1
            for k in range(1, int(temp_over_1367_aux_x[i])+1):
                valor_1367_4[i-k] = over_irradiance_1367[i-k]
                evento_auxxx[k-1] = over_irradiance_1367[i-k]
                energia_clear_sky_1367[k-1] = clear_sky[i-k]
            resumo_evento_data_1367[j] = data[i]
            resumo_evento_1367[j, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j, 2] = temp_over_1367_aux_x[i]
            resumo_evento_1367[j, 3] = (np.nanmean(evento_auxxx) * temp_over_1367_aux_x[i]) / 60
            resumo_evento_1367[j, 4] = (np.nanmean(energia_clear_sky_1367) * temp_over_1367_aux_x[i]) / 60
            evento_auxxx[:int(temp_over_1367_aux_x[i])] = np.nan
            j += 1
        elif temp_over_1367_aux_x[i] > 4:
            cont_1367_5 += 1
            for k in range(1, int(temp_over_1367_aux_x[i])+1):
                valor_1367_5[i-k] = over_irradiance_1367[i-k]
                evento_auxxx[k-1] = over_irradiance_1367[i-k]
                energia_clear_sky_1367[k-1] = clear_sky[i-k]
            resumo_evento_data_1367[j] = data[i]
            resumo_evento_1367[j, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j, 2] = temp_over_1367_aux_x[i]
            resumo_evento_1367[j, 3] = (np.nanmean(evento_auxxx) * temp_over_1367_aux_x[i]) / 60
            resumo_evento_1367[j, 4] = (np.nanmean(energia_clear_sky_1367) * temp_over_1367_aux_x[i]) / 60
            evento_auxxx[:int(temp_over_1367_aux_x[i])] = np.nan
            j += 1

    #energia_1367 = list(zip(resumo_evento_data_1367, resumo_evento_1367[:, 3]))

    data_resumo_evento_1367 = {
        'mean_irradiance': resumo_evento_1367[:, 0],
        'max_irradiance': resumo_evento_1367[:, 1],
        'duration': resumo_evento_1367[:, 2],
        'mean_energy': resumo_evento_1367[:, 3],
        'mean_energy_clear_sky': resumo_evento_1367[:, 4]
    }

    resumo_evento_df = pd.DataFrame(data_resumo_evento_1367)
    resumo_evento_data_1367 = np.array(resumo_evento_data_1367)

    # Converter resumo_evento_data_1000 para DataFrame
    resumo_evento_data_1367_df = pd.DataFrame(resumo_evento_data_1367, columns=['Data'])

    # Concatenar os DataFrames
    aux_1367 = pd.concat([resumo_evento_data_1367_df, resumo_evento_df], axis=1)
    aux_1367.columns = ['Data 1367', 'Valor médio do evento > 1367 W/m²', 'Valor máximo do evento > 1367 W/m²', 'Duração > 1367 W/m²', 'Energia do evento > 1367 (Wh/m²)', 'Energia de ceu claro (Wh/m²) > 1367']

    energia_1367 = aux_1367[['Data 1367', 'Energia do evento > 1367 (Wh/m²)']].copy()


    # %%

    # Concatenando aux_1000 com aux_1367
    
    aux_final = pd.concat([aux_1000,aux_1367], axis=1)
    
    nome = f"{nome_arquivo}-{arquivo} - Eventos_duracao.xlsx"
    pd.DataFrame(aux_final).to_excel(nome, index=False)

    # Cálculo de médias e máximos
    std_1367_1 = np.nanmean(valor_1367_1)
    std_1367_2 = np.nanmean(valor_1367_2)
    std_1367_3 = np.nanmean(valor_1367_3)
    std_1367_4 = np.nanmean(valor_1367_4)
    std_1367_5 = np.nanmean(valor_1367_5)

    max_1367_1 = np.nanmax(valor_1367_1)
    max_1367_2 = np.nanmax(valor_1367_2)
    max_1367_3 = np.nanmax(valor_1367_3)
    max_1367_4 = np.nanmax(valor_1367_4)
    max_1367_5 = np.nanmax(valor_1367_5)


    # %%
    std_1367_1

    # %%

    # INFORMAÇÕES DE MÁXIMOS
    ############# VER COM ALAN
    n_eventos_x = quantidade_eventos_1000 + cont_over_irradiance_1367

    max_over = np.nanmax(ghi_max)
    hora_max = None

    for i in range(n):
        if ghi_max[i] == max_over:
            hora_max = data[i]
            break

    energia1 = energia_1000.copy()
    energia2 = energia_1367.copy()

    energia1.columns = ['hora', 'energia']
    energia2.columns = ['hora', 'energia']
    #energia1 = pd.DataFrame(energia_1000, columns=['hora', 'energia'])
    #energia2 = pd.DataFrame(energia_1367, columns=['hora', 'energia'])

    energia = pd.concat([energia1, energia2], axis=0, ignore_index=True)
    # %%


    # %%
    max_energia_1000 = energia_1000.iloc[:, 1].max()
    max_energia_1367 = energia_1367.iloc[:, 1].max()
    # %%
    # Encontrar o máximo global entre os dois valores
    max_energia = max(max_energia_1000, max_energia_1367)
    max_energia
    # %%
    hora_energia_max = '99'
    # %%
    for index, row in energia.iterrows():
        if row.iloc[1] == max_energia:
            hora_energia_max = row.iloc[0]
            break
    hora_energia_max
    # %%

    if maior_temp_1000 > maior_temp_1367:
        hora_duracao = data[data_maior_1000]
    else:
        hora_duracao = data[data_maior_1367]
    # %%
    energia.shape

    # %%
    if n_eventos_x > 0:
        dia_maior_evento = int(str(hora_max)[8:10])
        dia_maior_duracao = int(str(hora_duracao)[8:10])
        dia_maior_energia = int(str(hora_energia_max)[8:10])
    # %%

    # %%

    ###################################### PLOTAGENS
    ############## TOTAL XPLOT2

    total_xplot2(variavel1=over_irradiance_plot, variavel2=ioh, data=data, num_figura=fig, 
                titulo='Overirradiance Events - GHI ', dia_final=dia_final, mes=mes, ano=ano,
                lim_sy=1800, lim_iy=0, und_y='W/m²', tam_font=10, cor1='blue', cor2='k', 
                nome_arquivo=nome_arquivo)

    # %%

    #########################################################
    # TOTAL XPLOT OVER


    # %%

    #TOTAL_Xplot_over(Ioh,clear_sky,GHI_avg,data,fig+1,'Measured GHI, 
    #Clear Sky and Extraterrestrial ',dia_final,mes,ano,1800,0,'W/m²',10,'Ioh',
    #'Clear','GHI',Nome_Arquivo)

    total_xplot_over(variavel1=ioh, variavel2=clear_sky, variavel3=ghi_avg, data=data, num_figura=fig+1,
                    titulo='Measured GHI Clear Sky and Extraterrestrial ', dia_final=dia_final, mes=mes, ano=ano,
                lim_sy=1800, lim_iy=0, und_y='W/m²', tam_font=10, var1='Ioh', var2='Clear',var3='GHI',
                nome_arquivo=nome_arquivo)


    # %%

    if n_eventos_x > 0:
        total_xplot_dia(variavel1=ioh, variavel2=clear_sky, variavel3=ghi_avg, 
                        data=data, num_figura=fig+2, titulo='Day of the most intense event ', 
                        dia=dia_maior_evento, lim_sy=1800, lim_iy=0, und_y='W/m²', 
                        tam_font=15, var1='Ioh', var2='Clear', var3='GHI', nome_arquivo=nome_arquivo)
        
        total_xplot_dia(variavel1=ioh, variavel2=clear_sky, variavel3=ghi_avg, 
                        data=data, num_figura=fig+3, titulo='Day the most lasting event ', 
                        dia=dia_maior_duracao, lim_sy=1800, lim_iy=0, und_y='W/m²', 
                        tam_font=15, var1='Ioh', var2='Clear', var3='GHI', nome_arquivo=nome_arquivo)
        
        total_xplot_dia(variavel1=ioh, variavel2=clear_sky, variavel3=ghi_avg, 
                        data=data, num_figura=fig+4, titulo='Day of the event with the highest energy ', 
                        dia=dia_maior_energia, lim_sy=1800, lim_iy=0, und_y='W/m²', 
                        tam_font=15, var1='Ioh', var2='Clear', var3='GHI', nome_arquivo=nome_arquivo)


    # %%

# Assumindo que as variáveis estão previamente definidas

# Total de eventos
    cont_tot = quantidade_eventos_1367 + quantidade_eventos_1000

    # Contagens por intervalo de tempo
    cont_tot_1 = cont_1000_1 + cont_1367_1
    cont_tot_2 = cont_1000_2 + cont_1367_2
    cont_tot_3 = cont_1000_3 + cont_1367_3
    cont_tot_4 = cont_1000_4 + cont_1367_4
    cont_tot_5 = cont_1000_5 + cont_1367_5

    cont_1000_1p = cont_1000_1 / cont_tot_1 if cont_tot_1 != 0 else np.nan
    cont_1000_2p = cont_1000_2 / cont_tot_2 if cont_tot_2 != 0 else np.nan
    cont_1000_3p = cont_1000_3 / cont_tot_3 if cont_tot_3 != 0 else np.nan
    cont_1000_4p = cont_1000_4 / cont_tot_4 if cont_tot_4 != 0 else np.nan
    cont_1000_5p = cont_1000_5 / cont_tot_5 if cont_tot_5 != 0 else np.nan
    cont_tot_1000_p = quantidade_eventos_1000 / cont_tot if cont_tot != 0 else np.nan

    cont_1367_1p = cont_1367_1 / cont_tot_1 if cont_tot_1 != 0 else np.nan
    cont_1367_2p = cont_1367_2 / cont_tot_2 if cont_tot_2 != 0 else np.nan
    cont_1367_3p = cont_1367_3 / cont_tot_3 if cont_tot_3 != 0 else np.nan
    cont_1367_4p = cont_1367_4 / cont_tot_4 if cont_tot_4 != 0 else np.nan
    cont_1367_5p = cont_1367_5 / cont_tot_5 if cont_tot_5 != 0 else np.nan
    cont_tot_1367_p = quantidade_eventos_1367 / cont_tot if cont_tot != 0 else np.nan


    # Matriz de informações (6x17) inicializada com NaNs
    p = np.full((1000, 1000), np.nan, dtype=object)

    # Populando a matriz p
    p[0, 0] = cont_tot_1
    p[1, 0] = cont_tot_2
    p[2, 0] = cont_tot_3
    p[3, 0] = cont_tot_4
    p[4, 0] = cont_tot_5
    p[5, 0] = cont_tot

    p[0, 1] = cont_1000_1
    p[1, 1] = cont_1000_2
    p[2, 1] = cont_1000_3
    p[3, 1] = cont_1000_4
    p[4, 1] = cont_1000_5
    p[5, 1] = quantidade_eventos_1000

    p[0, 2] = cont_1000_1p
    p[1, 2] = cont_1000_2p
    p[2, 2] = cont_1000_3p
    p[3, 2] = cont_1000_4p
    p[4, 2] = cont_1000_5p
    p[5, 2] = cont_tot_1000_p

    p[0, 3] = cont_1367_1
    p[1, 3] = cont_1367_2
    p[2, 3] = cont_1367_3
    p[3, 3] = cont_1367_4
    p[4, 3] = cont_1367_5
    p[5, 3] = quantidade_eventos_1367

    p[0, 4] = cont_1367_1p
    p[1, 4] = cont_1367_2p
    p[2, 4] = cont_1367_3p
    p[3, 4] = cont_1367_4p
    p[4, 4] = cont_1367_5p
    p[5, 4] = cont_tot_1367_p

    p[0, 5] = std_1000_1
    p[1, 5] = std_1000_2
    p[2, 5] = std_1000_3
    p[3, 5] = std_1000_4
    p[4, 5] = std_1000_5

    p[0, 6] = max_1000_1
    p[1, 6] = max_1000_2
    p[2, 6] = max_1000_3
    p[3, 6] = max_1000_4
    p[4, 6] = max_1000_5

    p[0, 7] = std_1367_1
    p[1, 7] = std_1367_2
    p[2, 7] = std_1367_3
    p[3, 7] = std_1367_4
    p[4, 7] = std_1367_5

    p[0, 8] = max_1367_1
    p[1, 8] = max_1367_2
    p[2, 8] = max_1367_3
    p[3, 8] = max_1367_4
    p[4, 8] = max_1367_5

    if maior_temp_1000 > maior_temp_1367:
        p[1, 11] = maior_temp_1000
        p[2, 11] = medio_maior_evento_1000
        p[3, 11] = max_maior_evento_1000
    else:
        p[1, 11] = maior_temp_1367
        p[2, 11] = medio_maior_evento_1367
        p[3, 11] = max_maior_evento_1367

    p[1, 12] = maior_temp_1000
    p[2, 12] = medio_maior_evento_1000
    p[3, 12] = max_maior_evento_1000

    p[1, 13] = maior_temp_1367
    p[2, 13] = medio_maior_evento_1367
    p[3, 13] = max_maior_evento_1367

    p[0, 16] = max_over
    p[0, 18] = max_energia

    # %%

    # %%

    p[0][12] = np.datetime64(data[data_maior_1000])
    p[0][13] = np.datetime64(data[data_maior_1367])
    p[0][15] = np.datetime64(hora_max)
    p[0][17] = np.datetime64(hora_energia_max)

    if maior_temp_1000 > maior_temp_1367:
        p[0][11] = np.datetime64(data[data_maior_1000])
    else:
        p[0][11] = np.datetime64(data[data_maior_1367])

    p[0][10] = 'Evento de maior duração'
    p[1][10] = 'Tempo do evento de maior duração (min)'
    p[2][10] = 'Valor médio da GHI do evento de maior duração (W/m²)'
    p[3][10] = 'Valor máximo da GHI do evento de maior duração (W/m²)'


    # %%


    # %%
    # AUXX e AUX
    auxx = [['Qt. eventos -  < 1 minuto'], ['Qt. eventos -  2 minutos'], ['Qt. eventos -  3 minutos'],
            ['Qt. eventos - 4 minutos'], ['Qt. eventos -  > 5 minutos'], ['Total']]
    auxx = [auxx[i] + [p[i][j] for j in range(len(p[0]))] for i in range(len(auxx))]

    aux = [['Tempo', 'Total de eventos', 'Quant de eventos >= 1000 e < 1367 W/m²', 'Quant de eventos >= 1000 e < 1367 (%)',
            'Qt. de eventos  > 1367  W/m²', 'Qt. de eventos  > 1367  (%)', 'Valor médio da GHI dos eventos >1000 e <1367 (W/m²)',
            'Valor máximo da GHI dos eventos >1000 e <1367 (W/m²)', 'Valor médio da GHI dos eventos >1367(W/m²)',
            'Valor máximo da GHI dos eventos >1367 (W/m²)', '', '', 'Maior duração de evento',
            'Maior duração de evento >1000 e <1367', 'Maior duração de evento >1367', '', 'Hora/Dia do maior evento',
            'Valor do maior evento em W/m²', 'Hora/Dia do evento de maior energia', 'Valor da energia do maior evento Wh/m²']]
    aux.extend(auxx)

    # Salvando no Excel
    #nome = f"{nome_arquivo}-{arquivo} - Eventos_info.xlsx"
    df = pd.DataFrame(aux)
    #df.to_excel(nome, index=False, header=False)
    
    nome = f"{nome_arquivo}-{arquivo} - Eventos_info.xlsx"
    pd.DataFrame(df).to_excel(nome, index=False)

