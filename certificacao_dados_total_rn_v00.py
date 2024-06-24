from total_dados_entrada import total_dados_entrada
from total_VarRad import total_VarRad
import pandas as pd

longitude_ref = -45
isc = 1367
horalocal_ref = 0

raw_rad = pd.read_excel('data/RN01-2024-05.xlsx', skiprows=1444, header=None)


RN, nome_arquivo, ano, mes, dia_juliano_ref, dia_final, latitude, longitude, temp_min, temp_max, prec_max = total_dados_entrada('RN01-2024-05.xlsx')

dados = total_VarRad(raw_rad, dia_juliano_ref, latitude, longitude, longitude_ref, isc, horalocal_ref, nome_arquivo)



print(dados)