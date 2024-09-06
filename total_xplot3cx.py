import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

def total_xplot3cx(variavel1, variavel2, variavel3, data, num_figura, titulo, dia_final, mes, ano, lim_sy, lim_iy, und_y, tam_font, var1, var2, var3, nome_arquivo):
    cor1='red'
    cor2='b'
    cor3=[1, 0.75, 0.035]
    plt.ioff()
    # Criando títulos para os subplots
    titulo01 = f'{titulo} (01 a 10 de {mes} de {ano})'
    titulo02 = f'{titulo} (11 a 20 de {mes} de {ano})'
    titulo03 = f'{titulo} (21 a {dia_final} de {mes} de {ano})'

        # Transformando o formato da data
    if isinstance(data, (np.ndarray, pd.Series)):
        data = pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S')
    elif isinstance(data, list):
        data = pd.to_datetime(pd.Series(data), format='%d/%m/%Y %H:%M:%S')

    # Dividindo os dados em três partes
    datap1 = data[0:14400]
    datap2 = data[14400:28800]
    datap3 = data[28800:]

    variavelp1 = variavel1[0:14400]
    variavelp2 = variavel1[14400:28800]
    variavelp3 = variavel1[28800:]

    variavel2p1 = variavel2[0:14400]
    variavel2p2 = variavel2[14400:28800]
    variavel2p3 = variavel2[28800:]

    variavel3p1 = variavel3[0:14400]
    variavel3p2 = variavel3[14400:28800]
    variavel3p3 = variavel3[28800:]

    # Criando a figura
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))
    day_format = mdates.DateFormatter('%d')

    # Primeiro subplot
    axs[0].plot(datap1, variavelp1, color=cor1, label=var1)
    axs[0].plot(datap1, variavel2p1, color=cor2, label=var2)
    axs[0].plot(datap1, variavel3p1, color=cor3, label=var3)
    axs[0].set_title(titulo01)
    axs[0].grid(True, which='minor')
    axs[0].set_ylim([lim_iy, lim_sy])
    axs[0].set_ylabel(und_y)
    axs[0].legend(loc='lower right', ncol=3)
    axs[0].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[0].xaxis.set_major_formatter(day_format)

    # Segundo subplot
    axs[1].plot(datap2, variavelp2, color=cor1, label=var1)
    axs[1].plot(datap2, variavel2p2, color=cor2, label=var2)
    axs[1].plot(datap2, variavel3p2, color=cor3, label=var3)
    axs[1].set_title(titulo02)
    axs[1].grid(True, which='minor')
    axs[1].set_ylim([lim_iy, lim_sy])
    axs[1].set_ylabel(und_y)
    axs[1].legend(loc='lower right', ncol=3)
    axs[1].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[1].xaxis.set_major_formatter(day_format)

    # Terceiro subplot
    axs[2].plot(datap3, variavelp3, color=cor1, label=var1)
    axs[2].plot(datap3, variavel2p3, color=cor2, label=var2)
    axs[2].plot(datap3, variavel3p3, color=cor3, label=var3)
    axs[2].set_title(titulo03)
    axs[2].grid(True, which='minor')
    axs[2].set_ylim([lim_iy, lim_sy])
    axs[2].set_ylabel(und_y)
    axs[2].legend(loc='lower right', ncol=3)
    axs[2].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[2].xaxis.set_major_formatter(day_format)

    # Ajustando o layout
    fig.tight_layout()

    # Salvando a figura
    plt.savefig(f'{nome_arquivo}_{titulo}_comp.pdf', format='pdf')
    plt.savefig(f'{nome_arquivo}_{titulo}_comp.svg', format='svg', bbox_inches='tight')

    #plt.show()
