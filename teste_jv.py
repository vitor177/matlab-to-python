# %%
import pandas as pd
arquivo = 'data/RN06-2024-06.xlsx'
arquivo2 = 'data/RN06-2024-06 (2)_ALANN.xlsx'

header = pd.read_excel(arquivo)
header2 = pd.read_excel(arquivo2)

df_alan = header2.iloc[1443:].reset_index(drop=True)

df_vitor = header.iloc[1443:].reset_index(drop=True)

# P Q R
# avg, max, min




# %%
var = 14
ghi_min_alan = df_alan.iloc[:,var]

ghi_min_vitor = df_vitor.iloc[:,var]
# %%
ghi_min_alan



# %%
comparacao = ghi_min_alan == ghi_min_vitor
# %%
diferencas = pd.DataFrame({
    'ghi_min_alan': ghi_min_alan[~comparacao],
    'ghi_min_vitor': ghi_min_vitor[~comparacao]
})

print(diferencas)
# %%
