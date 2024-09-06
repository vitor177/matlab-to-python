# %%

import numpy as np
import pandas as pd

def total_over_irradiancex(raw_rad, dados, header, arquivo, nome_arquivo):

    n, m = raw_rad.shape

    col = 16
    colg = 16

    # ======= Informações dos dados brutos =======

    data = raw_rad.iloc[:,0]
    data1 = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')


    ghi_avg = raw_rad.iloc[:,15]
    ghi_max = raw_rad.iloc[:,15]
    vel_avg = raw_rad.iloc[:,3]
    temp_avg = raw_rad.iloc[:,7]
    ur_avg = raw_rad.iloc[:,11]

    n, m = raw_rad.shape

    # ======= Informações da VarRad =======

    horalocal = dados.iloc[:,1]
    dia_mes = dados.iloc[:,2]
    cosazs = dados.iloc[:,13]
    cosazs12 = dados.iloc[:,15]
    alpha = dados.iloc[:,17]
    ioh = dados.iloc[:,19]
    iox = dados.iloc[:, 21]

    ioh[ioh < 0] = 0

    ghi_avg1 = ghi_max.copy()

    ghi_max[ghi_max > 2000] = 0


    # %%


    # ======= Over irradiance =======
    over_irradiance = np.full(n, np.nan)
    over_irradiance_aux = np.zeros(n)
    cont_over_irradiance = 0
    temp_over = np.full(n, np.nan)
    temp = 0
    k = 1

    aux_vel_avg = np.full(n, np.nan)
    aux_temp_avg = np.full(n, np.nan)
    aux_ur_avg = np.full(n, np.nan)

    for i in range(n):
        if ghi_max[i] >= ioh[i]:
            over_irradiance[i] = ghi_max[i]
            over_irradiance_aux[i] = 1
            aux_vel_avg[i] = vel_avg[i]
            aux_temp_avg[i] = temp_avg[i]
            aux_ur_avg[i] = ur_avg[i]
            cont_over_irradiance += 1
            temp += 1
        
        if i > 1:
            if over_irradiance_aux[i-1] == 1 and over_irradiance_aux[i] == 0:
                temp_over[k-1] = temp
                temp = 0
                k += 1

    quantidade_eventos = np.count_nonzero(temp_over > 0)

    # %%


    # % ======= Over irradiance > 1000 =======

    over_irradiance_1000 = np.full(n, np.nan)
    over_irradiance_1000_aux = np.zeros(n)
    temp_over_1000 = np.zeros(n)
    posicao_over_1000 = np.full(n, np.nan)
    hora_over_1000 = np.full(n, np.nan, dtype=object)
    temp_over_1000_aux = np.full(n, np.nan)
    temp_over_1000_auxx = np.full(n, np.nan)

    cont_over_irradiance_1000 = 0
    temp_1000 = 0
    k = 1

    # %%

    for i in range(n):
        if 1000 <= over_irradiance[i] < 1367:
            over_irradiance_1000[i] = over_irradiance[i]
            over_irradiance_1000_aux[i] = 1
            cont_over_irradiance_1000 += 1
            temp_1000 += 1
            temp_over_1000_aux[i] = temp_1000
        
        if i > 1:
            if over_irradiance_1000_aux[i-1] == 1 and over_irradiance_1000_aux[i] == 0:
                temp_over_1000[k-1] = temp_1000
                temp_over_1000_auxx[i] = temp_1000
                hora_over_1000[k-1] = data.iloc[i-temp_1000]
                temp_1000 = 0
                posicao_over_1000[k-1] = i
                k += 1
    # %%

    quantidade_eventos_1000 = np.count_nonzero(temp_over_1000 > 0)

    # %%

    maior_temp_1000 = int(np.nanmax(temp_over_1000))


    # %%

    maior_evento_1000 = np.full(maior_temp_1000, np.nan)

    # %%

    data_maior_1000 = 1

    # %%

    for i in range(n):
        if temp_over_1000_aux[i] == maior_temp_1000:
            aux = i
            data_maior_1000 = i
            for k in range(maior_temp_1000):
                maior_evento_1000[k] = ghi_max.iloc[aux-k]

    medio_maior_evento_1000 = np.nanmean(maior_evento_1000)

    max_maior_evento_1000 = np.nanmax(maior_evento_1000) if np.nanmax(maior_evento_1000) > 0 else 0


    # % ======= Quantidade de Overirradiance > 1000 =======

    # %%
    valor_1000_1 = np.full(n, np.nan)  # Armazena os eventos maiores que 1000 com até 1 min
    valor_1000_2 = np.full(n, np.nan)  # Armazena os eventos maiores que 1000 com até 2 min
    valor_1000_3 = np.full(n, np.nan)  # Armazena os eventos maiores que 1000 com até 3 min
    valor_1000_4 = np.full(n, np.nan)  # Armazena os eventos maiores que 1000 com até 4 min
    valor_1000_5 = np.full(n, np.nan)  # Armazena os eventos maiores que 1000 com 5 ou mais min

    cont_1000_1 = 0
    cont_1000_2 = 0
    cont_1000_3 = 0
    cont_1000_4 = 0
    cont_1000_5 = 0

    resumo_evento_1000 = np.full((1000, 3), np.nan)
    resumo_evento_data_1000 = np.full(1000, np.nan)
    resumo_evento_data_1000 = [np.nan for _ in resumo_evento_data_1000]
    evento_auxxx = np.full(n, np.nan)
    j = 1

    for i in range(n):
        if 0 < temp_over_1000_auxx[i] <= 1:
            cont_1000_1 += 1
            for k in range(1, int(temp_over_1000_auxx[i])+1):
                valor_1000_1[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            for k in range(int(temp_over_1000_auxx[i])):
                evento_auxxx[k] = np.nan
            j += 1

        if 1 < temp_over_1000_auxx[i] <= 2:
            cont_1000_2 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_2[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            for k in range(int(temp_over_1000_auxx[i])):
                evento_auxxx[k] = np.nan
            j += 1

        if 2 < temp_over_1000_auxx[i] <= 3:
            cont_1000_3 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_3[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            for k in range(int(temp_over_1000_auxx[i])):
                evento_auxxx[k] = np.nan
            j += 1

        if 3 < temp_over_1000_auxx[i] <= 4:
            cont_1000_4 += 1
            for k in range(1,int(temp_over_1000_auxx[i])+1):
                valor_1000_4[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            for k in range(int(temp_over_1000_auxx[i])):
                evento_auxxx[k] = np.nan
            j += 1

        if temp_over_1000_auxx[i] > 4:
            cont_1000_5 += 1
            for k in range(1, int(temp_over_1000_auxx[i])+1):
                valor_1000_5[i-k] = over_irradiance_1000[i-k]
                evento_auxxx[k-1] = over_irradiance_1000[i-k]
            resumo_evento_data_1000[j-1] = data[i]
            resumo_evento_1000[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1000[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1000[j-1, 2] = temp_over_1000_auxx[i]
            for k in range(int(temp_over_1000_auxx[i])):
                evento_auxxx[k] = np.nan
            j += 1
    # %%

    resumo_evento_data_1000 = pd.DataFrame(resumo_evento_data_1000, columns=['Data'])
    # %%
    resumo_evento_1000 = pd.DataFrame(resumo_evento_1000)
    # %%

    aux_1000 = pd.concat([resumo_evento_data_1000, resumo_evento_1000], axis=1)

    aux_1000.columns = ['Data', 'valor médio do evento > 1000 W/m²', 'valor máximo do evento > 1000 W/m²', 'duração > 1000 W/m²']




    # %%
    aux_1000

    # %%

    std_1000_1 = np.nanmean(valor_1000_1)
    std_1000_2 = np.nanmean(valor_1000_2)
    std_1000_3 = np.nanmean(valor_1000_3)
    std_1000_4 = np.nanmean(valor_1000_4)
    std_1000_5 = np.nanmean(valor_1000_5)

    max_1000_1 = np.nanmax(valor_1000_1)
    max_1000_2 = np.nanmax(valor_1000_2)
    max_1000_3 = np.nanmax(valor_1000_3)
    max_1000_4 = np.nanmax(valor_1000_4)
    max_1000_5 = np.nanmax(valor_1000_5)


    # ======= Over irradiance > 1367 =======

    over_irradiance_1367 = np.full(n, np.nan)
    over_irradiance_1367_aux = np.zeros(n)
    temp_over_1367 = np.zeros(n)  # Duração do evento
    posicao_over_1367 = np.full(n, np.nan)
    hora_over_1367 = np.full(n, np.nan)  # Hora do evento
    hora_over_1367 = hora_over_1367.tolist()  # Convertendo para lista
    temp_over_1367_aux = np.full(n, np.nan)
    temp_over_1367_auxx = np.full(n, np.nan)

    cont_over_irradiance_1367 = 0
    temp_1367 = 0
    k = 0

    for i in range(n):
        if over_irradiance[i] >= 1367:
            over_irradiance_1367[i] = over_irradiance[i]
            over_irradiance_1367_aux[i] = 1
            cont_over_irradiance_1367 += 1
            temp_1367 += 1
            temp_over_1367_aux[i] = temp_1367

        if i > 0 and over_irradiance_1367_aux[i-1] == 1 and over_irradiance_1367_aux[i] == 0:
            temp_over_1367[k] = temp_1367
            temp_over_1367_auxx[i] = temp_1367
            hora_over_1367[k] = data[i - int(temp_1367)]
            temp_1367 = 0
            posicao_over_1367[k] = i
            k += 1

    # %%

    k = 0

    for i in range(n):
        if temp_over_1367[i] > 0:
            k += 1
    quantidade_eventos_1367 = k

    maior_temp_1367 = np.nanmax(temp_over_1367)  # Maior tempo de um evento

    data_maior_1367 = 1
    maior_evento_1367 = np.full(int(maior_temp_1367), np.nan)  # Cria o vetor com o maior evento

    # %%

    for i in range(n):
        if temp_over_1367_auxx[i] == maior_temp_1367:
            aux = i
            data_maior_1367 = i
            for k in range(int(maior_temp_1367)):
                maior_evento_1367[k] = ghi_max[aux - k]
            break

    # %%


    if maior_evento_1367.size > 0:  # Verifica se o array tem pelo menos um elemento
        medio_maior_evento_1367 = np.nanmean(maior_evento_1367)
    else:
        medio_maior_evento_1367 = np.nan  # Ou defina outro valor padrão adequado

    # Verifique se o array não está vazio antes de calcular o máximo
    if maior_evento_1367.size > 0:  # Verifica se o array tem pelo menos um elemento
        max_maior_evento_1367 = np.nanmax(maior_evento_1367)
    else:
        max_maior_evento_1367 = 0  # Ou defina outro valor padrão adequado


    # %%


    # ======= TEMPO EVENTOS > 1367 =======
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

    resumo_evento_1367 = np.full((1000, 3), np.nan)
    resumo_evento_data_1367 = np.full(1000, np.nan)
    resumo_evento_data_1367 = resumo_evento_data_1367.tolist()
    evento_auxxx = np.full(n, np.nan)
    j = 1

    for i in range(n):
        if 0 < temp_over_1367_auxx[i] <= 1:
            cont_1367_1 += 1
            for k in range(1, int(temp_over_1367_auxx[i])+1):
                valor_1367_1[i - k] = over_irradiance_1367[i - k]
                evento_auxxx[k-1] = over_irradiance_1367[i - k]
            resumo_evento_data_1367[j-1] = data[i]
            resumo_evento_1367[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j-1, 2] = temp_over_1367_auxx[i]
            evento_auxxx[:int(temp_over_1367_auxx[i])] = np.nan
            j += 1

        elif 1 < temp_over_1367_auxx[i] <= 2:
            cont_1367_2 += 1
            for k in range(1,int(temp_over_1367_auxx[i])+1):
                valor_1367_2[i - k] = over_irradiance_1367[i - k]
                evento_auxxx[k-1] = over_irradiance_1367[i - k]
            resumo_evento_data_1367[j-1] = data[i]
            resumo_evento_1367[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j-1, 2] = temp_over_1367_auxx[i]
            evento_auxxx[:int(temp_over_1367_auxx[i])] = np.nan
            j += 1

        elif 2 < temp_over_1367_auxx[i] <= 3:
            cont_1367_3 += 1
            for k in range(1,int(temp_over_1367_auxx[i])+1):
                valor_1367_3[i - k] = over_irradiance_1367[i - k]
                evento_auxxx[k] = over_irradiance_1367[i - k]
            resumo_evento_data_1367[j-1] = data[i]
            resumo_evento_1367[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j-1, 2] = temp_over_1367_auxx[i]
            evento_auxxx[:int(temp_over_1367_auxx[i])] = np.nan
            j += 1

        elif 3 < temp_over_1367_auxx[i] <= 4:
            cont_1367_4 += 1
            for k in range(1,int(temp_over_1367_auxx[i])+1):
                valor_1367_4[i - k] = over_irradiance_1367[i - k]
                evento_auxxx[k] = over_irradiance_1367[i - k]
            resumo_evento_data_1367[j-1] = data[i]
            resumo_evento_1367[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j-1, 2] = temp_over_1367_auxx[i]
            evento_auxxx[:int(temp_over_1367_auxx[i])] = np.nan
            j += 1

        elif temp_over_1367_auxx[i] > 4:
            cont_1367_5 += 1
            for k in range(1,int(temp_over_1367_auxx[i])+1):
                valor_1367_5[i - k] = over_irradiance_1367[i - k]
                evento_auxxx[k] = over_irradiance_1367[i - k]
            resumo_evento_data_1367[j-1] = data[i]
            resumo_evento_1367[j-1, 0] = np.nanmean(evento_auxxx)
            resumo_evento_1367[j-1, 1] = np.nanmax(evento_auxxx)
            resumo_evento_1367[j-1, 2] = temp_over_1367_auxx[i]
            evento_auxxx[:int(temp_over_1367_auxx[i])] = np.nan
            j += 1    



    resumo_evento_data_1367 = pd.DataFrame(resumo_evento_data_1367, columns=['Data'])
    # %%
    resumo_evento_1367 = pd.DataFrame(resumo_evento_1367)
    # %%


    aux_1367 = pd.concat([resumo_evento_data_1367, resumo_evento_1367], axis=1)

    aux_1367.columns = ['Data', 'Valor médio do evento > 1367 W/m²', 'Valor máximo do evento > 1367 W/m²', 'Duração > 1367 W/m²']


    aux_final = pd.concat([aux_1000,aux_1367], axis=1)
    nome = f"{nome_arquivo}-{arquivo} - Eventos_duracao.xlsx"
    pd.DataFrame(aux_final).to_excel(nome, index=False)

    # %%


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

    n_eventosx = quantidade_eventos_1000 + cont_over_irradiance_1367

    max_over = np.max(ghi_max)

    for i in range(n):
        if ghi_max[i] == max_over:
            hora_max = data[i]

    # ========= Exportação para o Excel =========

    # ======= Matriz com os dados =======
    M = np.full((n, 14), np.nan)

    M[:, 0] = over_irradiance
    M[:, 1] = over_irradiance_1000
    M[:, 2] = over_irradiance_1367

    M[0, 3] = quantidade_eventos
    M[0, 4] = quantidade_eventos_1000
    M[3, 4] = quantidade_eventos_1000 / n_eventosx

    M[0, 5] = quantidade_eventos_1367
    M[3, 5] = quantidade_eventos_1367 / n_eventosx
    M[6, 5] = max_over

    M[:, 6] = posicao_over_1000
    M[:, 7] = temp_over_1000
    M[:, 8] = posicao_over_1367
    M[:, 9] = temp_over_1367

    M[:, 11] = aux_vel_avg
    M[:, 12] = aux_temp_avg
    M[:, 13] = aux_ur_avg

    # %%
    M[0,3]
    # %%


    AUX = pd.DataFrame(M)


    AUX.iloc[2, 4] = 'Eventos >1000'
    AUX.iloc[5, 4] = 'Hora do maior valor registrado'
    AUX.iloc[6, 4] = hora_max

    AUX.iloc[2, 5] = 'Eventos >1367'
    AUX.iloc[5, 5] = 'Maior valor registrado [W/m²]'

    hora_over_1000_series = pd.Series(hora_over_1000)
    hora_over_1367_series = pd.Series(hora_over_1367)
    # %%


    AUXX = pd.concat([pd.Series(data), AUX.iloc[:, :6], hora_over_1000_series, AUX.iloc[:, 7], hora_over_1367_series, AUX.iloc[:, 9], AUX.iloc[:, 10:14]], axis=1)

    # %%
    AUX = [
        'Data',
        'Over irradiance GHI [W/m²]',
        'Over irradiance GHI > 1000 [W/m²]',
        'Over irradiance GHI > 1367 [W/m²]',
        'Quantidade de eventos',
        'Quantidade de eventos > 1000 [W/m²]',
        'Quantidade de eventos > 1367 [W/m²]',
        'Hora do evento > 1000',
        'Duração do evento > 1000 [min]',
        'Hora do evento > 1367',
        'Duração do evento > 1367 [mim]',
        '',
        'Vel_avg',
        'Temp_avg',
        'UR_avg'
    ]

    AUXX.columns = AUX

    nome = f'{nome_arquivo}-{arquivo} - Eventos'

    pd.DataFrame(AUX).to_excel(f'{nome}.xlsx', index=False)
    #pd.DataFrame(aux_final).to_excel(nome, index=False)

    # %%

    # Dados adicionais
    O = np.full((31, 10), np.nan)
    O[0, 0] = quantidade_eventos_1000
    O[0, 1] = quantidade_eventos_1367
    O[0, 2] = quantidade_eventos_1367 + quantidade_eventos_1000
    O[0, 3] = cont_1000_1 + cont_1367_1
    O[0, 4] = cont_1000_2 + cont_1367_2
    O[0, 5] = cont_1000_3 + cont_1367_3
    O[0, 6] = cont_1000_4 + cont_1367_4
    O[0, 7] = cont_1000_5 + cont_1367_5
    O[0, 9] = max_over

    O = pd.DataFrame(O)
    O.iloc[0, 8] = hora_max

    # %%

    AUXXX = [
        'Quant de eventos > 1000  W/m²',
        'Qt. de eventos  > 1367  W/m²',
        'Total de eventos',
        'Qt. eventos -  < 1 minuto',
        'Qt. eventos -  2 minutos',
        'Qt. eventos -  3 minutos',
        'Qt. eventos - 4 minutos',
        'Qt. eventos -  > 5 minutos',
        'Hora/Dia do maior evento',
        'Valor do maior evento em W/m²'
    ]
    O.columns = AUXXX
    

    AUX = pd.concat([AUXX, O], axis=1)
    AUX.to_excel(f'{nome_arquivo}-{arquivo} - Eventos.xlsx', index=False)

    pd.DataFrame(AUX).to_excel(nome, index=False, engine='xlsxwriter')




    # %%
    # Matriz de informações para o artigo

    def safe_divide(numerator, denominator):
        return numerator / denominator if denominator != 0 else 0

    cont_tot = quantidade_eventos_1367 + quantidade_eventos_1000
    cont_tot_1 = cont_1000_1 + cont_1367_1
    cont_tot_2 = cont_1000_2 + cont_1367_2
    cont_tot_3 = cont_1000_3 + cont_1367_3
    cont_tot_4 = cont_1000_4 + cont_1367_4
    cont_tot_5 = cont_1000_5 + cont_1367_5

    cont_1000_1p = safe_divide(cont_1000_1, cont_tot_1)
    cont_1000_2p = safe_divide(cont_1000_2, cont_tot_2)
    cont_1000_3p = safe_divide(cont_1000_3, cont_tot_3)
    cont_1000_4p = safe_divide(cont_1000_4, cont_tot_4)
    cont_1000_5p = safe_divide(cont_1000_5, cont_tot_5)
    cont_tot_1000_p = safe_divide(quantidade_eventos_1000, cont_tot)

    cont_1367_1p = safe_divide(cont_1367_1, cont_tot_1)
    cont_1367_2p = safe_divide(cont_1367_2, cont_tot_2)
    cont_1367_3p = safe_divide(cont_1367_3, cont_tot_3)
    cont_1367_4p = safe_divide(cont_1367_4, cont_tot_4)
    cont_1367_5p = safe_divide(cont_1367_5, cont_tot_5)
    cont_tot_1367_p = safe_divide(quantidade_eventos_1367, cont_tot)

    P = np.full((6, 17), np.nan,dtype=object)

    P[0, 0] = cont_tot_1
    P[1, 0] = cont_tot_2
    P[2, 0] = cont_tot_3
    P[3, 0] = cont_tot_4
    P[4, 0] = cont_tot_5
    P[5, 0] = cont_tot

    P[0, 1] = cont_1000_1
    P[1, 1] = cont_1000_2
    P[2, 1] = cont_1000_3
    P[3, 1] = cont_1000_4
    P[4, 1] = cont_1000_5
    P[5, 1] = quantidade_eventos_1000

    P[0, 2] = cont_1000_1p
    P[1, 2] = cont_1000_2p
    P[2, 2] = cont_1000_3p
    P[3, 2] = cont_1000_4p
    P[4, 2] = cont_1000_5p
    P[5, 2] = cont_tot_1000_p

    P[0, 3] = cont_1367_1
    P[1, 3] = cont_1367_2
    P[2, 3] = cont_1367_3
    P[3, 3] = cont_1367_4
    P[4, 3] = cont_1367_5
    P[5, 3] = quantidade_eventos_1367

    P[0, 4] = cont_1367_1p
    P[1, 4] = cont_1367_2p
    P[2, 4] = cont_1367_3p
    P[3, 4] = cont_1367_4p
    P[4, 4] = cont_1367_5p
    P[5, 4] = cont_tot_1367_p

    P[0, 5] = std_1000_1
    P[1, 5] = std_1000_2
    P[2, 5] = std_1000_3
    P[3, 5]  = std_1000_4
    P[4, 5]  = std_1000_5

    P[0,6] = max_1000_1
    P[1,6] = max_1000_2
    P[2,6] = max_1000_3
    P[3,6] = max_1000_4
    P[4,6] = max_1000_5


    P[0,7] = std_1367_1
    P[1,7] = std_1367_2
    P[2,7] = std_1367_3
    P[3,7] = std_1367_4
    P[4,7] = std_1367_5


    P[0,8] = max_1367_1
    P[1,8] = max_1367_2
    P[2,8] = max_1367_3
    P[3,8] = max_1367_4
    P[4,8] = max_1367_5

    if maior_temp_1000 > maior_temp_1367:
        P[1, 11] = maior_temp_1000
        P[2, 11] = medio_maior_evento_1000
        P[3, 11] = max_maior_evento_1000
    else:
        P[1, 11] = maior_temp_1367
        P[2, 11] = medio_maior_evento_1367
        P[3, 11] = max_maior_evento_1367

    P[1, 12] = maior_temp_1000
    P[2, 12] = medio_maior_evento_1000
    P[3, 12] = max_maior_evento_1000

    P[1, 13] = maior_temp_1367
    P[2, 13] = medio_maior_evento_1367
    P[3, 13] = max_maior_evento_1367

    P[0, 16] = max_over

    P[0, 12] = np.datetime64(data[data_maior_1000])
    P[0, 13] = np.datetime64(data[data_maior_1367])
    P[0, 15] = np.datetime64(hora_max)

    if maior_temp_1000 > maior_temp_1367:
        P[0, 11] = np.datetime64(data[data_maior_1000])
    else:
        P[0, 11] = np.datetime64(data[data_maior_1367])


    P[0][10] = 'Evento de maior duração'
    P[1][10] = 'Tempo do evento de maior duração (min)'
    P[2][10] = 'Valor médio da GHI do evento de maior duração (W/m²)'
    P[3][10] = 'Valor máximo da GHI do evento de maior duração (W/m²)'

    auxx = [['Qt. eventos -  < 1 minuto'], ['Qt. eventos -  2 minutos'], ['Qt. eventos -  3 minutos'],
                ['Qt. eventos - 4 minutos'], ['Qt. eventos -  > 5 minutos'], ['Total']]

    auxx = [auxx[i] + [P[i][j] for j in range(len(P[0]))] for i in range(len(auxx))]
    aux = [['Tempo', 'Total de eventos', 'Quant de eventos >= 1000 e < 1367 W/m²', 'Quant de eventos >= 1000 e < 1367 (%)',
            'Qt. de eventos  > 1367  W/m²', 'Qt. de eventos  > 1367  (%)', 'Valor médio da GHI dos eventos >1000 e <1367 (W/m²)',
            'Valor máximo da GHI dos eventos >1000 e <1367 (W/m²)', 'Valor médio da GHI dos eventos >1367(W/m²)',
            'Valor máximo da GHI dos eventos >1367 (W/m²)', '', '', 'Maior duração de evento',
            'Maior duração de evento >1000 e <1367', 'Maior duração de evento >1367', '', 'Hora/Dia do maior evento',
            'Valor do maior evento em W/m²']]
    aux.extend(auxx)

    # %%
    df = pd.DataFrame(aux)
    nome = f"{nome_arquivo}-{arquivo} - Eventos_info.xlsx"
    pd.DataFrame(df).to_excel(nome, index=False)
    # %%



    # Inicializando as matrizes Q e M com NaN
    Q = np.full((n, 13), np.nan)
    M = np.full((n, 3), np.nan)

    # Preenchendo a matriz Q
    Q[:, 0] = ghi_avg
    Q[:, 1] = ghi_max
    Q[:, 2] = ioh
    Q[:, 3] = valor_1000_1
    Q[:, 4] = valor_1000_2
    Q[:, 5] = valor_1000_3
    Q[:, 6] = valor_1000_4
    Q[:, 7] = valor_1000_5
    Q[:, 8] = valor_1367_1
    Q[:, 9] = valor_1367_2
    Q[:, 10] = valor_1367_3
    Q[:, 11] = valor_1367_4
    Q[:, 12] = valor_1367_5

    # Preenchendo a matriz M
    Z = temp_over_1000
    M[:, 0] = over_irradiance
    M[:, 1] = over_irradiance_1000
    M[:, 2] = over_irradiance_1367


    # %%

    # %%
    AUXX = pd.DataFrame(M)

    # %%
    header = header.iloc[1]

    # %%

    AUX = ['Over irradiance GHI [W/m²]', 'Over irradiance GHI > 1000 [W/m²]', 'Over irradiance GHI > 1367 [W/m²]']
    AUX = pd.DataFrame([AUX])
    header = pd.DataFrame([header])

    # %%
    header = header.reset_index(drop=True)
    AUX = AUX.reset_index(drop=True)

    combined_df = pd.concat([header, AUX], axis=1)

    # %%
    raw_rad = raw_rad.reset_index(drop=True)
    AUXX = AUXX.reset_index(drop=True)
    combined_df_2 = pd.concat([raw_rad, AUXX], axis=1)

    # %%
    combined_df = combined_df.reset_index(drop=True)
    combined_df_2 = combined_df_2.reset_index(drop=True)

    # %%
    combined_df.columns = [f'col_{i}' for i in range(combined_df.shape[1])]
    combined_df_2.columns = [f'col_{i}' for i in range(combined_df_2.shape[1])]

    final_combined_df = pd.concat([combined_df, combined_df_2], axis=0, ignore_index=True)

    # %%
    # %%

    # Substituindo valores 60000 por 'NAN' no dataframe final_df
    final_combined_df.replace(60000, 'NAN', inplace=True)

    # Salvando os dados em um arquivo Excel
    nome = f"{nome_arquivo}-{arquivo}-Eventos_tab.xlsx"
    final_combined_df.to_excel(nome, index=False, header=False)

    return M, Z
