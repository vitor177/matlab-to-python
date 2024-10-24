# %%
import pandas as pd
import numpy as np


def total_VarRad(raw_rad, dia_juliano_ref: int, latitude: float, longitude: float, longitude_ref, isc, horalocal_ref, nome_arquivo):
    dados = pd.DataFrame()

    dados['Hora'] = raw_rad.iloc[:, 0]

# %%
     # HORA LOCAL
    horalocal = list(range(1440))*(int((len(raw_rad)/1440)))

    dados['Hora Local'] = horalocal
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

        # MES
    dia_mes = np.zeros(len((raw_rad)))
    for i in range(len(raw_rad)):
        dia_mes[i] = dia_juliano[i] - dia_juliano_ref + 1

    dados['Mês'] = dia_mes.astype(int)
    dados['Dia Juliano'] = dia_juliano.astype(int)

# %%
    dados['Latitude'] = latitude

    dados['Longitude'] = longitude

    dados['Lon ref'] = longitude_ref

    dados['Isc'] = isc
    # %%
    declinacao = 23.45*(np.sin(((dia_juliano+284)*(360/365))*np.pi/180))
    dados['Declinação'] = declinacao

    # %%
    rad = (2*np.pi*(dia_juliano-1)/365)
    dados['RAD(rad)'] = rad

    # %%
    et = 229.18 * (0.000075 + 0.001868 * np.cos(rad) - 0.032077 * np.sin(rad * (-0.014615) * np.cos(2*rad) - 0.04089 * np.sin(2 * rad)))
    dados['Et'] = et   

    # Horasolar
    horasolar = (horalocal + ((4 * (longitude - longitude_ref)) + et)) / 60
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
    dados['cos(AZS^(1.2))'] = cosAZS12

    # CosAZS02
    cosAZS02 = np.where(AZS > 90, 0, cosAZS**0.2)
    dados['cos(AZS^(0.2))'] = cosAZS02

    # Alpha
    alpha = np.arcsin(cosAZS) * 180 / np.pi
    dados['Alpha'] = alpha

    # Eo
    Eo = 1.00011 + (0.0334221 * np.cos(rad)) + (0.00128 * np.sin(rad)) + (0.000719 * np.cos(2 * rad)) + (0.000077 * np.sin(2 * rad))
    dados['Eo'] = Eo

    # Ioh
    Ioh = isc * Eo * cosAZS
    dados['Ioh W/m²'] = Ioh

    # Io
    Io = isc * Eo
    dados['Io W/m²'] = Io

    # Iox
    Iox = np.where(Io < 0, 0, Io)
    dados['Iox W/m²'] = Iox

    dados.to_excel(nome_arquivo+'_VarRAD.xlsx', engine='xlsxwriter', index=False)     

    return dados