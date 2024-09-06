import pandas as pd
import numpy as np
import numpy as np


def ywrite(raw_met, n1, n, nome_arquivo):
    # Step 1: Prepare the X matrix
    X = n1.iloc[:, 12].values  # MATLAB indices are 1-based, Python indices are 0-based
    X = np.array(X)
    n = pd.DataFrame(n)
    Y = n.iloc[:, [5, 9, 15]].values
    X = np.column_stack((X, Y))

    X
    # %%

    dados_possiveis = len(raw_met) - 1440

    D = np.zeros((6, 9))
    aux = np.zeros((6, 9))

    D[:, 0] = dados_possiveis
    D[:, 1] = X[:, 0]  # GHI1
    D[:, 2] = X[:, 0] / dados_possiveis
    D[:, 3] = X[:, 1]  # Temp
    D[:, 4] = X[:, 1] / dados_possiveis
    D[:, 5] = X[:, 2]  # UR
    D[:, 6] = X[:, 2] / dados_possiveis
    D[:, 7] = X[:, 3]  # Vel
    D[:, 8] = X[:, 3] / dados_possiveis

    aux = np.flipud(D)

    aux_df = pd.DataFrame(aux)
    a_aux = ['dados possíveis', 'ghi 1', '%', 'temp', '%', 'ur', '%', 'vel', '%']
    tab = pd.DataFrame(np.vstack([a_aux, aux_df]), columns=None)

    # %%
    aux = np.zeros((5, 16))
    aux[0, :] = n.iloc[5, :].values
    aux[1, :] = n.iloc[4, :].values
    aux[2, :] = n.iloc[3, :] + n.iloc[2, :].values
    aux[3, :] = n.iloc[1, :].values
    aux[4, :] = n.iloc[0, :].values


    # %%
    temp = aux[:, :6].T
    temp = temp[:-1].tolist()
    temp = pd.DataFrame(temp)

    ur = aux[:, 6:10].T
    ur = ur[:-1].tolist()

    vel = aux[:, 10:16].T
    vel = vel[:-1].tolist()



    auxx_temp = pd.DataFrame(['Desvio padrão', 'Posicionamento',  'Fisicamente possível', 'Extremamente raro', 'Evolução temporal'])
    auxx_ur = pd.DataFrame(['Desvio padrão', 'Posicionamento',  'Fisicamente possível'])
    auxx_vel = pd.DataFrame(['Desvio padrão', 'Posicionamento',  'Fisicamente possível', 'Extremamente raro', 'Evolução temporal'])

    # %%
    temp
    # %%
    temp = pd.DataFrame(np.concat([auxx_temp, temp], axis=1))
    headers = ['TEMP', 'Não disponível', 'Não testado', 'Anômalo', 'Suspeito', 'Bom']
    headers_df = pd.DataFrame([headers], columns=temp.columns)
    temp_df = pd.concat([headers_df, temp], ignore_index=True)

    #temp_df

    # %%
    ur = pd.DataFrame(ur)

    # %%
    ur = pd.concat([auxx_ur, ur], axis=1)
    headers = ['UR', 'Não disponível', 'Não testado', 'Anômalo', 'Suspeito', 'Bom']
    headers_df = pd.DataFrame([headers], columns=ur.columns)
    ur_df = pd.concat([headers_df, ur], ignore_index=True)

    #ur_df

    # %%

    vel = pd.DataFrame(vel)
    vel = pd.concat([auxx_vel, vel], axis=1)
    headers = ['VEL', 'Não disponível', 'Não testado', 'Anômalo', 'Suspeito', 'Bom']
    headers_df = pd.DataFrame([headers], columns=vel.columns)
    vel_df = pd.concat([headers_df, vel], ignore_index=True)

    #vel_df

    # %%
    GHIX = n1.iloc[:, 1:-1]
    GHIX = np.hstack([GHIX.values[:, :4], GHIX.values[:, 5:]])
    GHIX_df = pd.DataFrame(GHIX)

    GHIX_df = GHIX_df[::-1].T.copy()
    GHIX_df

    # %%
    auxx_labels = [
        'Limite físico', 'Elevação', 'Desvio padrão', 
        'Posicionamento', 'Índice de transmissividade', 
        'Fisicamente possível', 'Extremamente raro', 
        'Modelo de Céu claro', 'Consistência temporal', 'Persistência'
    ]
    auxx_labels = pd.DataFrame(auxx_labels)

    GHIX_df = pd.concat([auxx_labels, GHIX_df], axis=1)

    # %%
    GHIX_df.reset_index()
    GHIX_df

    # Verifique o DataFrame
    #GHIX_df
    # %%
    def write_dfs_to_excel(writer, dfs, sheet_name='Sheet1'):
        workbook  = writer.book
        worksheet = workbook.add_worksheet(sheet_name)  # Cria a planilha se não existir
        row = 0  # Start at the first row

        for df in dfs:
            df.to_excel(writer, sheet_name=sheet_name, startrow=row, index=False)
            row += len(df) + 1  # Move to the next section with a blank row

    # Criação do arquivo Excel
    output_filename = f'{nome_arquivo}_Relatório.xlsx'

    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        write_dfs_to_excel(writer, [tab, temp_df, ur_df, vel_df, GHIX_df])
