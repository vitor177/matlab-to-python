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
ghi_mcc_clear = raw_rad.iloc[:, var+5]

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
m['Kt'] = kt
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

m['GHI avg'] = ghi_avg 
m['GHI max'] = ghi_max
m['GHI min'] = ghi_min
m['GHI Sd'] = ghi_std
m['GHI mcclear'] = ghi_avg_p

# %%
ioh = np.maximum(ioh, 0)
over_irradiance = np.full(n, np.nan)
cont_over_irradiance = 0

print(over_irradiance)
# %%
for i in range(n):
    if ioh[i] == flag6:
        over_irradiance[i] = flag6
    else:
        if ghi_max[i] > ioh[i]:
            over_irradiance[i] = ghi_avg[i]
            cont_over_irradiance+=1
m['Over irradiance GHI'] = over_irradiance

# %%
# Verificar 12:40
over_irradiance_1000 = np.full(n, np.nan)
cont_over_irradiance_1000 = 0
for i in range(n):
    if over_irradiance[i] > 1000 and over_irradiance[i] < flag6:
        over_irradiance_1000[i] = ghi_avg[i]
        cont_over_irradiance_1000+=1
m['Over irradiance GHI > 1000'] = over_irradiance_1000



# %%
# LF GHI

lf_ghi = np.full(n, np.nan)
lf_ghi_flag6 = 0
lf_ghi_flag3 = 0
lf_ghi_flag1 = 0

for i in range(n):
    if ghi_avg[i] == flag6:
        lf_ghi[i] = flag6
        lf_ghi_flag6 +=1

    else:
        if ghi_avg[i] < -5 and ghi_avg[i] > 200:
            lf_ghi[i] = flag3
            lf_ghi_flag3+=1

        else:
            lf_ghi[i] = flag1
            lf_ghi_flag1+=1
m["LF GHI1 -5 a 2000 W/m²"] = lf_ghi
# %%
elevacao7 = np.full(n, np.nan)
elevacao7_flag6 = elevacao7_flag5 = elevacao7_flag4 = elevacao7_flag1 = 0
for i in range(n):
    if lf_ghi[i] == flag6:
        elevacao7[i] = flag6
        elevacao7_flag6+=1
    elif lf_ghi[i] == flag3:
        elevacao7[i] = flag4
        elevacao7_flag4+=1
    else:
        if lf_ghi[i] == flag1 and alpha[i] > 7:
            elevacao7[i] = flag1
            elevacao7_flag1+=1
        else:
            elevacao7[i] = flag5
            elevacao7_flag5+=1
m['Elevação >7° GHI'] = elevacao7
# %%
# Desvio padrão diferente de 0
desv_pad_0 = np.full(n, np.nan)

desv_pad_0_flag6 = desv_pad_0_flag5 = desv_pad_0_flag4 = desv_pad_0_flag3 = desv_pad_0_flag2 = desv_pad_0_flag1 = 0

for i in range(n):
    if ghi_std[i] == flag6:
        desv_pad_0_flag6+=1
    else:
        if elevacao7[i] == flag5:
            desv_pad_0[i] = flag5
            desv_pad_0_flag5+=1
        elif elevacao7[i] == flag4:
            desv_pad_0[i] = flag4
            desv_pad_0_flag4+=1
        
        else:
            if elevacao7[i] == flag1 and ghi_std[i] == 0:
                desv_pad_0[i] = flag3
                desv_pad_0_flag3+=1
            else:
                desv_pad_0[i] = flag1
                desv_pad_0_flag1+=1

m['Desvio Padrão ?0'] = desv_pad_0
# %%
# Inicializando variáveis
deriva_ghi = np.full(n, np.nan)

deriva_ghi_flag6 = 0
deriva_ghu_flag5 = 0
deriva_ghi_flag4 = 0
deriva_ghi_flag3 = 0
deriva_ghi_flag1 = 0

for i in range(n):
    if desv_pad_0[i] == flag6:
        deriva_ghi[i] = flag6
        deriva_ghi_flag6 += 1
    elif desv_pad_0[i] == flag5:
        deriva_ghi[i] = flag5
        deriva_ghu_flag5 += 1
    elif desv_pad_0[i] == flag4 or desv_pad_0[i] == flag3:
        deriva_ghi[i] = flag4
        deriva_ghi_flag4 += 1
    else:
        if ghi_avg[i] >= ghi_min[i] and ghi_avg[i] <= ghi_max[i]:
            deriva_ghi[i] = flag1
            deriva_ghi_flag1 += 1
        else:
            deriva_ghi[i] = flag3
            deriva_ghi_flag3 += 1

m['GHI_min < GHI_avg < GHI_max'] = deriva_ghi

# %%
# Kt GHI
kt_ghi = np.full(n, np.nan)
kt_ghi_flag6 = 0
kt_ghi_flag5 = 0
kt_ghi_flag4 = 0
kt_ghi_flag1 = 0

for i in range(n):
    if deriva_ghi[i] == flag6:
        kt_ghi[i] = flag6
        kt_ghi_flag6 += 1
    elif deriva_ghi[i] == flag5:
        kt_ghi[i] = flag5
        kt_ghi_flag5 += 1
    elif deriva_ghi[i] == flag4 or deriva_ghi[i] == flag3:
        kt_ghi[i] = flag4
        kt_ghi_flag4 += 1
    else:
        if iox[i] == 0:
            kt_ghi[i] = flag5
            kt_ghi_flag5 += 1
        else:
            kt_ghi[i] = ghi_avg[i] / (iox[i] * cosAZS[i])
            kt_ghi_flag1 += 1
m['kt GHI'] = kt_ghi
# %%
#  0<kt<1,2 GHI
zero_kt_12 = np.full(n, np.nan)
zero_kt_12_flag6 = 0
zero_kt_12_flag5 = 0
zero_kt_12_flag4 = 0
zero_kt_12_flag3 = 0
zero_kt_12_flag1 = 0

for i in range(n):
    if kt_ghi[i] == flag6:
        zero_kt_12[i] = flag6
        zero_kt_12_flag6 += 1
    elif kt_ghi[i] == flag5:
        zero_kt_12[i] = flag5
        zero_kt_12_flag5 += 1
    elif kt_ghi[i] == flag4:
        zero_kt_12[i] = flag4
        zero_kt_12_flag4 += 1
    else:
        if kt_ghi[i] < 0 or kt_ghi[i] > 1.2:
            zero_kt_12[i] = flag3
            zero_kt_12_flag3 += 1
        else:
            zero_kt_12[i] = flag1
            zero_kt_12_flag1 += 1

m['0<kt<1,2 GHI'] = zero_kt_12
# Note que em Python, o operador lógico para "ou" é "or", e para "e" é "and"

# %%
# FP min

fpmin = -4

fpmax = (1.5 * iox * cosAZS12) + 100

fp_ghi = np.full(n, np.nan)
fp_ghi_flag6 = 0
fp_ghi_flag5 = 0
fp_ghi_flag4 = 0
fp_ghi_flag3 = 0
fp_ghi_flag1 = 0

for i in range(n):
    if zero_kt_12[i] == flag6:
        fp_ghi[i] = flag6
        fp_ghi_flag6 += 1
    elif zero_kt_12[i] == flag5:
        fp_ghi[i] = flag5
        fp_ghi_flag5 += 1
    elif zero_kt_12[i] == flag4 or zero_kt_12[i] == flag3:
        fp_ghi[i] = flag4
        fp_ghi_flag4 += 1
    else:
        if ghi_avg[i] < fpmin:
            fp_ghi[i] = flag3
            fp_ghi_flag3 += 1
        else:
            if ghi_avg[i] < fpmax[i]:
                fp_ghi[i] = flag1
                fp_ghi_flag1 += 1
            else:
                fp_ghi[i] = flag3
                fp_ghi_flag3 += 1

m['GHI FP min'] = fpmin
m['GHI FPmax'] = fpmax
m['FP GHI'] = fp_ghi
# %%
# Extremamente Raro
er_min = -2
er_max = (1.2 * iox * cosAZS12) + 50

er_ghi = pd.Series(np.full(n, np.nan))
er_ghi_flag6 = 0
er_ghi_flag5 = 0
er_ghi_flag4 = 0
er_ghi_flag3 = 0
er_ghi_flag2 = 0
er_ghi_flag1 = 0

for i in range(n):
    if fp_ghi[i] == flag6:
        er_ghi[i] = flag6
        er_ghi_flag6 += 1
    elif fp_ghi[i] == flag5:
        er_ghi[i] = flag5
        er_ghi_flag5 += 1
    elif fp_ghi[i] == flag3 or fp_ghi[i] == flag4:
        er_ghi[i] = flag4
        er_ghi_flag4 += 1
    else:
        if ghi_avg[i] < fpmin:
            er_ghi[i] = flag3
            er_ghi_flag3 += 1
        else:
            if ghi_avg[i] < er_min:
                er_ghi[i] = flag2
                er_ghi_flag2 += 1
            else:
                if ghi_avg[i] < er_max[i]:
                    er_ghi[i] = flag1
                    er_ghi_flag1 += 1
                elif ghi_avg[i] > er_max[i]:
                    er_ghi[i] = flag2
                    er_ghi_flag2 += 1
                else:
                    er_ghi[i] = flag3
                    er_ghi_flag3 += 1
m['GHI ERmin'] = er_min
m['GHI ERmax'] = er_max
m['GHI ER'] = er_ghi

# %%
# 14 GHI CLEAR SKY
ghi_mcc_clear_x_13 = ghi_mcc_clear*1.3

m['1,3 GHI Clear Sky'] = ghi_mcc_clear_x_13
# %%
# GHI CLEAR SKY

ghi_clear_sky = pd.Series(np.full(n, np.nan))

ghi_clear_sky_flag6 = 0
ghi_clear_sky_flag5 = 0
ghi_clear_sky_flag4 = 0
ghi_clear_sky_flag2 = 0
ghi_clear_sky_flag1 = 0

for i in range(n):
    if er_ghi[i] == flag6:
        ghi_clear_sky[i] = flag6
        ghi_clear_sky_flag6 += 1
    elif er_ghi[i] == flag5:
        ghi_clear_sky[i] = flag5
        ghi_clear_sky_flag5 += 1
    elif er_ghi[i] == flag4 or er_ghi[i] == flag3:
        ghi_clear_sky[i] = flag4
        ghi_clear_sky_flag4 += 1
    elif er_ghi[i] == flag2:
        ghi_clear_sky[i] = flag2
        ghi_clear_sky_flag2 += 1
    else:
        if ghi_avg[i] > ghi_mcc_clear_x_13[i]:
            ghi_clear_sky[i] = flag2
            ghi_clear_sky_flag2 += 1
        else:
            ghi_clear_sky[i] = flag1
            ghi_clear_sky_flag1 += 1
m['Clear sky GHI'] = ghi_clear_sky
m.to_excel('_CQD_GHI.xlsx', engine='xlsxwriter', index=False)   
# %%
# Consistência Temporal GHI