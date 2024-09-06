import matplotlib.pyplot as plt

def plot_boxplot(bxpstats):

    # Criar a figura e os subplots
    fig, ax = plt.subplots(1, 3, figsize=(12, 6))
    labels = ['Vel', 'Temp', 'Rh']

    # Loop para adicionar os boxplots e os valores de whislo, whishi, e mediana
    for i in range(3):
        ax[i].bxp([bxpstats[i]])
        whislo = bxpstats[i]['whislo']
        whishi = bxpstats[i]['whishi']
        mediana = bxpstats[i]['med']    
        
        ax[i].text(1.05, whislo, f'Min: {whislo:.2f}', ha='left', va='center', fontsize=10, color='blue')
        ax[i].text(1.05, whishi, f'Max: {whishi:.2f}', ha='left', va='center', fontsize=10, color='blue')
        ax[i].text(1.05, mediana, f'Med: {mediana:.2f}', ha='left', va='center', fontsize=10, color='red')

        ax[i].set_title(labels[i])
        ax[i].set_xticks([])

    # Ajustar layout
    plt.tight_layout()

    # Salvar e exibir o gráfico
    plt.savefig('box_plots.svg')
    #plt.show()