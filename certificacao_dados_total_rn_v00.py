# %%
from total_dados_entrada import total_dados_entrada
from total_VarRad import total_VarRad
from total_qualidade_ghi import total_qualidade_ghi
import pandas as pd
from total_over_irradiance import total_over_irradiance
from limpeza import limpar_e_mover_arquivos
import warnings
from total_qualidade_met import total_qualidade_met
warnings.filterwarnings("ignore")
from flags import flags
from ywrite import ywrite
longitude_ref = -45
isc = 1367
horalocal_ref = 0
arquivo = 'data/RN01-2024-05.xlsx'

header = pd.read_excel(arquivo)
raw_rad = header.iloc[1443:].reset_index(drop=True)
raw_met = header.iloc[3:].reset_index(drop=True)

# Parâmetros de entrada
rn, nome_arquivo, ano, mes, dia_juliano_ref, dia_final, latitude, longitude, temp_min, temp_max, prec_max = total_dados_entrada(arquivo.split('/')[1])

# Variáveis Radiométricas
dados = total_VarRad(raw_rad, dia_juliano_ref, latitude, longitude, longitude_ref, isc, horalocal_ref, nome_arquivo)

##############################Controle de qualidade de dados Radiométricos################################

## ____> DELE [M1,N1,O1,P1] = TOTAL_Qualidade_GHI(RAW_RAD,RAW_MET,DADOS,header,'Global Horizontal Irradiance ','GHI',16,mes,dia_final,ano,1,Nome_Arquivo);
m1, n1, o1, p1 = total_qualidade_ghi(raw_rad, raw_met, dados, header, 'Global Horizontal Irradiance', 'GHI', 16, mes, dia_final, ano, 1, nome_arquivo)

total_over_irradiance(raw=raw_rad,dados=dados,header=header,col=16,fig=5,dia_final=dia_final,mes=mes,ano=ano,arquivo='Overirradiance Events - GHI',nome_arquivo=nome_arquivo)

#################################### Controle de qualidade de dados Meterorólogicos#################################
# Não precisa de P
m, n, o = total_qualidade_met(raw_met,dados,temp_min,temp_max,mes,dia_final,ano,10,nome_arquivo) # OK

ywrite(raw_met,n1,n,nome_arquivo)
#ywrite

flag_output = flags(raw_rad, m, m1,nome_arquivo)

# iec67724

limpar_e_mover_arquivos('.', nome_arquivo)
# %%