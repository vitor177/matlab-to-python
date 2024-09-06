import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def total_xplot_over(variavel1, variavel2, variavel3, data, num_figura, titulo, dia_final, mes, ano, lim_sy, lim_iy, und_y, tam_font, var1, var2, var3, nome_arquivo):
    # Títulos dos subplots
    titulo01 = f'{titulo} (01 a 10 de {mes} de {ano})'
    titulo02 = f'{titulo} (11 a 20 de {mes} de {ano})'
    titulo03 = f'{titulo} (21 a {dia_final} de {mes} de {ano})'
    plt.ioff()
    cor1 = 'k'
    cor2 = 'b'
    cor3 = 'r'

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

    # Criação da figura e subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))
    fig.suptitle(titulo, fontsize=tam_font)

    day_format = mdates.DateFormatter('%d')

    # Primeiro subplot
    axs[0].plot(datap1, variavelp1, color=cor1)
    axs[0].plot(datap1, variavel2p1, color=cor2)
    axs[0].plot(datap1, variavel3p1, color=cor3)
    axs[0].set_title(titulo01, fontsize=tam_font)
    axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[0].set_ylim([lim_iy, lim_sy])
    axs[0].set_ylabel(und_y)
    axs[0].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[0].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[0].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[0].xaxis.set_major_formatter(day_format)

    # Segundo subplot
    axs[1].plot(datap2, variavelp2, color=cor1)
    axs[1].plot(datap2, variavel2p2, color=cor2)
    axs[1].plot(datap2, variavel3p2, color=cor3)
    axs[1].set_title(titulo02, fontsize=tam_font)
    axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[1].set_ylim([lim_iy, lim_sy])
    axs[1].set_ylabel(und_y)
    axs[1].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[1].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[1].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[1].xaxis.set_major_formatter(day_format)

    # Terceiro subplot
    axs[2].plot(datap3, variavelp3, color=cor1)
    axs[2].plot(datap3, variavel2p3, color=cor2)
    axs[2].plot(datap3, variavel3p3, color=cor3)
    axs[2].set_title(titulo03, fontsize=tam_font)
    axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[2].set_ylim([lim_iy, lim_sy])
    axs[2].set_ylabel(und_y)
    axs[2].legend([var1, var2, var3], loc='upper right', ncol=3)
    axs[2].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[2].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[2].xaxis.set_major_formatter(day_format)

    # Ajustar layout
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    # Salvar a figura em PDF e PNG
    fig.savefig(f'{nome_arquivo}_{titulo}_comp.pdf', format='pdf')
    fig.savefig(f'{nome_arquivo}_{titulo}_comp.svg', format='svg', bbox_inches='tight')

