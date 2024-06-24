# %%
import pandas as pd
import numpy as np


def total_VarRad(raw_rad, dia_juliano_ref, latitude, longitude, longitude_ref, isc, horalocal_ref, nome_arquivo):
    dados = pd.DataFrame()

    dados['Hora'] = raw_rad[0]

# RN, Nome_Arquivo, ano, mes, dia_juliano_ref, dia_final, latitude, longitude, temp_min, temp_max, prec_max

# Dados = RAW_RAD, dia_juliano_ref, latitude, longitude_ref, isc, horalocal_ref, nome_arquivo

# %%
     # HORA LOCAL
    dados['Hora Local'] = list(range(1440))*(int((len(raw_rad)/1440)))
# %%




    # DIA JULIANO
    cont = 0
    cont1 = 0
    dia_juliano = np.zeros(len((raw_rad)))
    for i in range(len(raw_rad)):
        if cont1 <= 1439:
            dia_juliano[i] = int(dia_juliano_ref + cont)
            cont1+=1
        else:
            cont +=1
            dia_juliano[i] = int(dia_juliano_ref + cont)
            cont1 = 1
    dados['Dia Juliano'] = dia_juliano


        # MES
    dia_mes = np.zeros(len((raw_rad)))
    for i in range(len(raw_rad)):
        dia_mes[i] = dia_juliano[i] - dia_juliano_ref + 1
    dados['Mês'] = dia_mes
# %%
    dados['Latitude'] = latitude

    dados['Longitude'] = longitude

    dados['Lon red'] = longitude_ref


    # %%
    declinacao = 23.45*(np.sin(((dia_juliano+284)*(360/365))*np.pi/180))
    dados['Declinação'] = declinacao

    # %%
    rad = (2*np.pi*(dia_juliano-1)/365)
    dados['RAD(rad)'] = rad

    # %%
    et = 229.18 * (0.000075 + 0.001868 * np.cos(rad) - 0.032077 * np.sin(rad) - 0.014615 * np.cos(2 * rad) - 0.04089 * np.sin(2 * rad))
    dados['Et'] = et   

    # Horasolar
    horasolar = (horalocal_ref + ((4 * (longitude - longitude_ref)) + et)) / 60
    dados['Hora solar'] = horasolar

    # Omega
    omega = (horasolar - 12) * 15
    dados['Omega'] = omega

    # CosAZS
    cosAZS = (np.sin(latitude * np.pi / 180) * np.sin(declinacao * np.pi / 180)) + (np.cos(latitude * np.pi / 180) * np.cos(declinacao * np.pi / 180) * np.cos(omega * np.pi / 180))
    dados['cosAZS'] = cosAZS
    # AZS
    AZS = np.arccos(cosAZS) * 180 / np.pi
    dados['AZS'] = AZS

    # CosAZS12
    cosAZS12 = np.where(AZS > 90, 0, cosAZS**1.2)
    dados['cosAZS^1,2'] = cosAZS12

    # CosAZS02
    cosAZS02 = np.where(AZS > 90, 0, cosAZS**0.2)
    dados['cosAZS^0,2'] = cosAZS02

    # Alpha
    alpha = np.arcsin(cosAZS) * 180 / np.pi
    dados['Alpha'] = alpha

    # Eo
    Eo = 1.00011 + (0.0334221 * np.cos(rad)) + (0.00128 * np.sin(rad)) + (0.000719 * np.cos(2 * rad)) + (0.000077 * np.sin(2 * rad))
    dados['Eo'] = Eo

    # Ioh
    Ioh = isc * Eo * cosAZS
    dados['Ioh W/m^2'] = Ioh

    # Io
    Io = isc * Eo
    dados['Io W/m^2'] = Io

    Iox = np.where(Io < 0, 0, Io)
    dados['Iox W/m^2'] = Iox     

    return dados

# %%

# %%
