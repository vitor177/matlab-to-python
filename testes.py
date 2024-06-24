from total_dados_entrada import total_dados_entrada
from total_VarRad import total_VarRad
import pandas as pd

longitude_ref = 0
isc = 1367
horalocal_ref = 0

raw_rad = pd.read_excel('data/RN01-2024-05.xlsx', skiprows=1444, header=None)

print(raw_rad[0].head())