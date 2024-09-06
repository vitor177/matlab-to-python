import pandas as pd

def flags(raw_rad, m, m1, nome_arquivo):
    # Extrair a primeira coluna de raw_rad
    data = raw_rad.iloc[:, 0].to_numpy()

    # Criar o DataFrame inicial
    aux = ['Data']
    data = pd.DataFrame(data, columns=aux)

    # Construir o DataFrame com os dados adicionais
    x = pd.concat([
        data, 
        pd.DataFrame(m1.iloc[:, 26]), 
        pd.DataFrame(m.iloc[:, 10]), 
        pd.DataFrame(m.iloc[:, 14]), 
        pd.DataFrame(m.iloc[:, 22])
    ], axis=1)

    #aux = x.copy()

    # Adicionar o cabeçalho
    headers = ['Data', 'GHI', 'Temperatura do Ar', 'UR do Ar', 'Velocidade do vento']
    x.columns = headers

    # Escrever o DataFrame em um arquivo Excel
    x.to_excel(f'{nome_arquivo}_FLAGS.xlsx', index=False, engine='openpyxl')

    return x