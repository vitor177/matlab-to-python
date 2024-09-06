import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np

def total_xplot3(variavel1, variavel2, variavel3, data, numfigura, titulo, titulo_var, diafinal, mes, ano, limsy, limiy, undy, tamfont, cor1, cor2, cor3, nome_arquivo):
    # definindo os títulos dos subplots
    titulo01 = f'{titulo} (01 a 10 de {mes} de {ano})'
    titulo02 = f'{titulo} (11 a 20 de {mes} de {ano})'
    titulo03 = f'{titulo} (21 a {diafinal} de {mes} de {ano})'
    plt.ioff()
    if isinstance(data, (np.ndarray, pd.Series)):
        data = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')
    elif isinstance(data, list):
        data = pd.to_datetime(pd.Series(data), format='%d/%m/%Y %H:%M:%S')
    
    # dividindo os dados em três partes
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

    # criando a figura
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))
    day_format = mdates.DateFormatter('%d')

    # primeiro subplot
    axs[0].plot(datap1, variavelp1, color=cor1)
    axs[0].plot(datap1, variavel2p1, '--x', color=cor2, linewidth=1.5)
    axs[0].plot(datap1, variavel3p1, color=cor3, linewidth=1.5)
    axs[0].set_title(titulo01)
    axs[0].grid(True, which='minor')
    axs[0].set_ylim([limiy, limsy])
    axs[0].set_ylabel(undy)
    axs[0].legend([titulo_var, 'suspect', 'anomalous'], loc='upper right', ncol=3)
    axs[0].tick_params(axis='both', which='major', labelsize=tamfont)
    axs[0].xaxis.set_major_formatter(day_format)

    # segundo subplot
    axs[1].plot(datap2, variavelp2, color=cor1)
    axs[1].plot(datap2, variavel2p2, '--x', color=cor2, linewidth=1.5)
    axs[1].plot(datap2, variavel3p2, color=cor3, linewidth=1.5)
    axs[1].set_title(titulo02)
    axs[1].grid(True, which='minor')
    axs[1].set_ylim([limiy, limsy])
    axs[1].set_ylabel(undy)
    axs[1].legend([titulo_var, 'suspect', 'anomalous'], loc='upper right', ncol=3)
    axs[1].tick_params(axis='both', which='major', labelsize=tamfont)
    axs[1].xaxis.set_major_formatter(day_format)

    # terceiro subplot
    axs[2].plot(datap3, variavelp3, color=cor1)
    axs[2].plot(datap3, variavel2p3, '--x', color=cor2, linewidth=1.5)
    axs[2].plot(datap3, variavel3p3, color=cor3, linewidth=1.5)
    axs[2].set_title(titulo03)
    axs[2].grid(True, which='minor')
    axs[2].set_ylim([limiy, limsy])
    axs[2].set_ylabel(undy)
    axs[2].legend([titulo_var, 'suspect', 'anomalous'], loc='upper right', ncol=3)
    axs[2].tick_params(axis='both', which='major', labelsize=tamfont)
    axs[2].xaxis.set_major_formatter(day_format)

    # ajuste do layout
    fig.tight_layout()

    # salvando a figura
    plt.savefig(f'{nome_arquivo}_{titulo}.pdf', format='pdf')
    plt.savefig(f'{nome_arquivo}_{titulo}.svg', format='svg', bbox_inches='tight')

    #plt.show()
