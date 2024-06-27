# %%
import numpy as np
import pandas as pd


arquivo = 'data/RN01-2024-05.xlsx'
raw_rad = pd.read_excel(arquivo, skiprows=1444, header=None)

raw_met = pd.read_excel(arquivo, skiprows=3)

dados = pd.read_excel('RN01-2024-05_VarRAD.xlsx')
# %%
var = 16
ghi_avg = raw_rad.iloc[:,var-1]
ghi_max = raw_rad.iloc[:,var]
ghi_min = raw_rad.iloc[:,var+1]
ghi_std = raw_rad.iloc[:,var+2]

ghi_avg_p = raw_rad[var+5]


# vou voltar aqui mais tarde, provavelmente previous pegar 20 amostras antes até o final
#ghi_avg_p
# %%
n, m = raw_rad.shape
print(n,m)
# %%
print(len(dados.columns))

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


m = pd.DataFrame()

kt = np.divide(ghi_avg,ioh)

print(type(kt))
for i in range(n):
    if ioh[i] == flag6:
        kt[i] = np.nan
    else:
        if kt[i] > 10:
            kt[i] = 0
        if kt[i] < 0:
            kt[i] = 0

m['Data'] = raw_rad.iloc[:, 0]
m['GHI AVG'] = ghi_avg
m['Ioh'] = ioh
m['Kt'] = kt

m.to_excel('_CQD_GHI.xlsx', engine='xlsxwriter', index=False)  




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
m['Kt Céu'] = kt_ceu
# %%

ioh = np.maximum(ioh, 0)

over_irradiance = np.nan(n)
cont_over_irradiance = 0
for i in range(n):
    if ioh[i] == flag6:
        over_irradiance[i] = flag6
    else:
        if ghi_max[i] > ioh[i]:
            over_irradiance[i] = ghi_avg[i]
            cont_over_irradiance+=1
            
over_irradiance_1000 = np.nan(n)

