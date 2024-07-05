import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

def total_xplot_dia(variavel1, variavel2, variavel3, data, numfigura, 
                    titulo, dia, lim_sy=1800, lim_iy=0, und_y='W/m²', tam_font=15, 
                    var1='Ioh', var2='Clear', var3='GHI', save_file=False, file_prefix='Day_Event'):

    # Selecionando dados para o dia do evento mais intenso
    start_idx = (dia - 1) * 1440
    end_idx = dia * 1440

    data = data[start_idx:end_idx]
    variavel1 = variavel1[start_idx:end_idx]
    variavel2 = variavel2[start_idx:end_idx]
    variavel3 = variavel3[start_idx:end_idx]

    # Criação da figura e plotagem
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(data, variavel1, '--', color='k', linewidth=1.5, label=var1)
    ax.plot(data, variavel2, color='k', linewidth=1.5, label=var2)
    ax.plot(data, variavel3, color='r', linewidth=1, label=var3)

    ax.set_title(titulo, fontsize=tam_font)
    ax.set_xlabel('Time', fontsize=tam_font)
    ax.set_ylabel(und_y, fontsize=tam_font)
    ax.set_ylim([lim_iy, lim_sy])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=tam_font)
    ax.tick_params(axis='both', which='minor', labelsize=tam_font)

    # Formatação da data no eixo x
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))  # Intervalo de 2 horas
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Legenda
    ax.legend(loc='upper right', ncol=3)
    ax.get_legend().set_frame_on(False)

    # Incluir dia e mês no rodapé
    plt.text(0.98, 0.02, f'Day {dia}', verticalalignment='bottom', horizontalalignment='right',
             transform=ax.transAxes, color='blue', fontsize=12)

    # Ajustar layout
    plt.tight_layout()

    # Salvar a figura se especificado
    if save_file:
        fig.savefig(f'{file_prefix}_{titulo}.pdf', format='pdf')
        fig.savefig(f'{file_prefix}_{titulo}.png', format='png')

    # Mostrar a figura
    plt.show()

# Exemplo de uso:
# plot_day_event(Variavel1, Variavel2, Variavel3, data, NumFigura, titulo, dia, limSY, limIY, undY, tamFont, var1, var2, var3)
