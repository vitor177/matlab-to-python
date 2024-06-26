# %%
from total_dados_entrada import total_dados_entrada
from total_VarRad import total_VarRad
import pandas as pd

longitude_ref = 0
isc = 1367
horalocal_ref = 0

raw_rad = pd.read_excel('data/RN01-2024-05.xlsx', skiprows=3)
print(raw_rad.head())

#df1 = raw_rad[raw_rad.isnull().any(axis=1)]
# %%,
print(raw_rad.isnull().sum().sum())
# %%
print(raw_rad.columns[2:])
# %%
cols_para_verificar = raw_rad.columns[2:]  # Seleciona todas as colunas exceto a primeira
print(raw_rad[raw_rad.duplicated(subset=cols_para_verificar)])
# %%