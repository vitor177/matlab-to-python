from datetime import datetime, timedelta
import json

def total_dados_entrada(Arquivo: str):

    nome_arquivo = Arquivo.split('.')[0]
    parts = Arquivo.split('-')
    RN = parts[0]
    ano = int(parts[1])
    mes_num = int(parts[2][:2])

    data_inicio = datetime(ano, mes_num, 1)
    dia_juliano_ref = data_inicio.timetuple().tm_yday

    if mes_num == 12:
        dia_final = 31
    else:
        dia_final = (datetime(ano, mes_num + 1, 1) - timedelta(days=1)).day

    mes_nomes = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    mes = mes_nomes[mes_num - 1]    
    #print(dia_final)

# Dicionário com dados de latitude, longitude e variáveis adicionais
    locations = {
    'RN01': {'Latitude': -5.706841, 'Longitude': -36.232853, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200},
    'RN02': {'Latitude': -5.296237, 'Longitude': -36.272845, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200},
    'RN03': {'Latitude': -6.144001, 'Longitude': -38.190438, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200},
    'RN04': {'Latitude': -6.228709, 'Longitude': -36.027581, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200},
    'RN05': {'Latitude': -6.46888, 'Longitude': -35.445526, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200},
    'RN06': {'Latitude': -5.176129, 'Longitude': -37.343413, 'Temp_min': 15, 'Temp_max': 45, 'prec_max': 200}
}
    locations_json = json.dumps(locations, indent=4)

    if RN in locations:
        latitude = locations[RN]['Latitude']
        longitude = locations[RN]['Longitude']
        temp_min = locations[RN]['Temp_min']
        temp_max = locations[RN]['Temp_max']
        prec_max = locations[RN]['prec_max']
    else:
        print("ERRO COM A ESTAÇÃO: " , RN)
        latitude = None
        longitude = None
        temp_min = None
        temp_max = None
        prec_max = None
    print("Latitude: ", latitude)

    print("Longitude: ",longitude)
    return RN, nome_arquivo, ano, mes, dia_juliano_ref, dia_final, latitude, longitude, temp_min, temp_max, prec_max


if __name__ == "__main__":
    print(total_dados_entrada('data/RN01-2024-05.xlsx'))