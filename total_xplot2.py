import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def total_xplot2(variavel1, variavel2, data, num_figura, titulo, dia_final, mes, ano, lim_sy, lim_iy, und_y, tam_font, cor1, cor2, nome_arquivo):
    # Títulos dos subplots
    titulo01 = f"{titulo} do dia 01 ao dia 10 de {mes} de {ano}"
    titulo02 = f"{titulo} do dia 11 ao dia 20 de {mes} de {ano}"
    titulo03 = f"{titulo} do dia 01 ao dia {dia_final} de {mes} de {ano}"
    plt.ioff()
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

    fig, axs = plt.subplots(3, 1, figsize=(12, 6))
    day_format = mdates.DateFormatter('%d')

    axs[0].plot(datap1, variavelp1, color=cor1, label='OverIrradiance', marker='+')
    axs[0].plot(datap1, variavel2p1, color=cor2, label='Ioh')
    axs[0].legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2)
    axs[0].set_title(titulo01)
    axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[0].set_ylim(lim_iy, lim_sy)
    axs[0].set_ylabel(und_y)
    axs[0].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[0].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[0].xaxis.set_major_formatter(day_format)

    axs[1].plot(datap2, variavelp2, color=cor1, label='OverIrradiance', marker='+')
    axs[1].plot(datap2, variavel2p2, color=cor2, label='Ioh')
    axs[1].legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2)
    axs[1].set_title(titulo02)
    axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[1].set_ylim(lim_iy, lim_sy)
    axs[1].set_ylabel(und_y)
    axs[1].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[1].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[1].xaxis.set_major_formatter(day_format)

    axs[2].plot(datap3, variavelp3, color=cor1, label='OverIrradiance', marker='+')
    axs[2].plot(datap3, variavel2p3, color=cor2, label='Ioh')
    axs[2].legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2)
    axs[2].set_title(titulo03)
    axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[2].set_ylim(lim_iy, lim_sy)
    axs[2].set_ylabel(und_y)
    axs[2].tick_params(axis='both', which='major', labelsize=tam_font)
    axs[2].tick_params(axis='both', which='minor', labelsize=tam_font)
    axs[2].xaxis.set_major_formatter(day_format)

    fig.tight_layout()

    plt.savefig(f"{nome_arquivo}_{titulo}.pdf", format='pdf')
    plt.savefig(f"{nome_arquivo}_{titulo}.svg", format='svg', bbox_inches='tight')

#total_xplot2(over_irradiance_plot, ioh, data, 16, 'Overirradiance Events - GHI', 31, 'May', 2024, 1800, 0, 'W/m²', 10, 'blue', 'k', arquivo)
