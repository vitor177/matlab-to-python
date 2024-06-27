from total_dados_entrada import total_dados_entrada
from total_VarRad import total_VarRad
#from total_qualidade_ghi import total_qualidade_ghi
import pandas as pd

longitude_ref = -45
isc = 1367
horalocal_ref = 0
arquivo = 'data/RN01-2024-05.xlsx'


raw_rad = pd.read_excel(arquivo, skiprows=1444, header=None)

# Parâmetros de entrada
RN, nome_arquivo, ano, mes, dia_juliano_ref, dia_final, latitude, longitude, temp_min, temp_max, prec_max = total_dados_entrada(arquivo.split('/')[1])

# Variáveis Radiométricas
dados = total_VarRad(raw_rad, dia_juliano_ref, latitude, longitude, longitude_ref, isc, horalocal_ref, nome_arquivo)

# Controle de qualidade de dados Radiométricos
#m1, n1, o1, p1 = total_qualidade_ghi()



#print(dados)