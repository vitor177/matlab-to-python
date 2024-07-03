# %%
#function [P] = TOTAL_over_irradiance(RAW,DADOS,header,col,fig,dia_final,mes,ano,Arquivo,Nome_Arquivo)

import numpy as np
import pandas as pd
from datetime import datetime

# =================================================================
#                    Detecção de eventos de sobreirradiancia     
# =================================================================

# ======= Informações dos dados brutos =======

arquivo = 'data/RN01-2024-05.xlsx'
raw_rad = pd.read_excel(arquivo, skiprows=1444, header=None)
#raw_met = pd.read_excel(arquivo, skiprows=3)
dados = pd.read_excel('RN01-2024-05_VarRAD.xlsx')
# %%
col = 15

data = raw_rad.iloc[:, 0]
data1 = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')

ghi_avg = pd.to_numeric(raw_rad.iloc[:, col])
ghi_max = pd.to_numeric(raw_rad.iloc[:, col])  # GHI 1 max

vel_avg = pd.to_numeric(raw_rad.iloc[:, 3])
temp_avg = pd.to_numeric(raw_rad.iloc[:, 7])
ur_avg = pd.to_numeric(raw_rad.iloc[:, 11])
prec_avg = pd.to_numeric(raw_rad.iloc[:, 3])
dir_avg = pd.to_numeric(raw_rad.iloc[:, 3])
press_avg = pd.to_numeric(raw_rad.iloc[:, 3])  # retirar depois

clear_sky = pd.to_numeric(raw_rad.iloc[:, 21])
n, m = raw_rad.shape

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
resumo_evento_data_1000 = [np.nan] * n

evento_auxxx = np.full(n, np.nan)
energia_clear_sky_1000 = np.full(n, np.nan)
j = 1

for i in range(n):
    if 0 < temp_over_1000_auxx[i] <= 1:
        cont_1000_1 += 1
        for k in range(int(temp_over_1000_auxx[i])):
            valor_1000_1[i-k] = over_irradiance_1000[i-k]
            evento_auxxx[k] = over_irradiance_1000[i-k]
            energia_clear_sky_1000[k] = clear_sky[i-k]
        resumo_evento_data_1000[j-1] = data[i]
        resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
        resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
        resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
        resumo_evento_1000[j-1, 3] = (np.nanmean(evento_auxxx) * temp_over_1000_auxx[i]) / 60
        resumo_evento_1000[j-1, 4] = (np.nanmean(energia_clear_sky_1000) * temp_over_1000_auxx[i]) / 60
        evento_auxxx[:int(temp_over_1000_auxx[i])] = np.nan
        j += 1
    if 1 < temp_over_1000_auxx[i] <= 2:
        cont_1000_2 += 1
        for k in range(int(temp_over_1000_auxx[i])):
            valor_1000_2[i-k] = over_irradiance_1000[i-k]
            evento_auxxx[k] = over_irradiance_1000[i-k]
            energia_clear_sky_1000[k] = clear_sky[i-k]
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
        for k in range(int(temp_over_1000_auxx[i])):
            valor_1000_3[i-k] = over_irradiance_1000[i-k]
            evento_auxxx[k] = over_irradiance_1000[i-k]
            energia_clear_sky_1000[k] = clear_sky[i-k]
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
        for k in range(int(temp_over_1000_auxx[i])):
            valor_1000_4[i-k] = over_irradiance_1000[i-k]
            evento_auxxx[k] = over_irradiance_1000[i-k]
            energia_clear_sky_1000[k] = clear_sky[i-k]
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
        for k in range(int(temp_over_1000_auxx[i])):
            valor_1000_5[i-k] = over_irradiance_1000[i-k]
            evento_auxxx[k] = over_irradiance_1000[i-k]
            energia_clear_sky_1000[k] = clear_sky[i-k]
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
# Agora você pode usar resultado_concatenado conforme necessário

# %%
#print(np.where(~np.isnan(aux_1000['Valor máximo do evento > 1000 W/m²'])))
print(aux_1000[:15])
# %%

aux_1000.to_excel('Eventos_duracao.xlsx')
# %%

