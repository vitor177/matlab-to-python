import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def total_xplot3c(variavel1, variavel2, variavel3, data, num_figura, titulo, diafinal, mes, ano, lim_sy, lim_iy, und_y, tam_font, var1, var2, var3, nome_arquivo):
    if isinstance(data, list):
        # Converte a lista para uma Série Pandas e, em seguida, para datetime
        data = pd.to_datetime(pd.Series(data), format='%d/%m/%Y %H:%M:%S')
    elif isinstance(data, pd.DataFrame):
        # Aqui você precisa especificar o nome da coluna que contém as datas
        data_col_name = data.columns[0]  # Supondo que a coluna de datas seja a primeira
        data = pd.to_datetime(data[data_col_name], format='%d/%m/%Y %H:%M:%S')
    else:
        raise ValueError("Formato de dados não reconhecido para 'data'.")
    plt.ioff()
    if isinstance(data, (np.ndarray, pd.Series)):
        data = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')
    elif isinstance(data, list):
        data = pd.to_datetime(pd.Series(data), format='%d/%m/%Y %H:%M:%S')
    
    # Dividindo os dados em três partes
    datap1 = data[:14400]
    datap2 = data[14400:28800]
    datap3 = data[28800:]
    
    variavelp1 = variavel1[:14400]
    variavelp2 = variavel1[14400:28800]
    variavelp3 = variavel1[28800:]
    
    variavel2p1 = variavel2[:14400]
    variavel2p2 = variavel2[14400:28800]
    variavel2p3 = variavel2[28800:]
    
    variavel3p1 = variavel3[:14400]
    variavel3p2 = variavel3[14400:28800]
    variavel3p3 = variavel3[28800:]

    plt.close('all')
    
    # Criando a figura e subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))
    fig.suptitle(titulo, fontsize=tam_font)
    
    # Formatador de datas
    day_format = mdates.DateFormatter('%d')
    
    # Primeiro subplot
    axs[0].plot(datap1, variavelp1, color='r')
    axs[0].plot(datap1, variavel2p1, color='#1F9CFF', linestyle='--', marker=None)
    axs[0].plot(datap1, variavel3p1, color='#FFBF5A', linestyle='-')
    axs[0].set_title(f'{titulo} (1 a 10 de {mes} de {ano})')
    axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[0].set_ylim([lim_iy, lim_sy])
    axs[0].set_ylabel(und_y)
    axs[0].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[0].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[0].xaxis.set_major_formatter(day_format)
    
    # Segundo subplot
    axs[1].plot(datap2, variavelp2, color='r')
    axs[1].plot(datap2, variavel2p2, color='#1F9CFF', linestyle='--', marker=None)
    axs[1].plot(datap2, variavel3p2, color='#FFBF5A', linestyle='-')
    axs[1].set_title(f'{titulo} (11 a 20 de {mes} de {ano})')
    axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[1].set_ylim([lim_iy, lim_sy])
    axs[1].set_ylabel(und_y)
    axs[1].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[1].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[1].xaxis.set_major_formatter(day_format)
    
    # Terceiro subplot
    axs[2].plot(datap3, variavelp3, color='r')
    axs[2].plot(datap3, variavel2p3, color='#1F9CFF', linestyle='--', marker=None)
    axs[2].plot(datap3, variavel3p3, color='#FFBF5A', linestyle='-')
    axs[2].set_title(f'{titulo} (21 a {diafinal} de {mes} de {ano})')
    axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[2].set_ylim([lim_iy, lim_sy])
    axs[2].set_ylabel(und_y)
    axs[2].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[2].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[2].xaxis.set_major_formatter(day_format)
    
    # Ajustando o layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Salvando os gráficos
    plt.savefig(f'{nome_arquivo}_{titulo}_comp.pdf', format='pdf')
    plt.savefig(f'{nome_arquivo}_{titulo}_comp.svg', format='svg', bbox_inches='tight')
    
    # Mostrando o gráfico
    #plt.show()
