import numpy as np

def flag_plot(variavel, resultado):
    n = variavel.shape[0]

    flag6 = 60000
    flag5 = 50000
    flag4 = 40000
    flag3 = 30000
    flag2 = 20000
    flag1 = 10000

    flag = np.full((n, 6), np.nan)
    plot_flag6 = np.full(n, np.nan)
    plot_flag5 = np.full(n, np.nan)
    plot_flag4 = np.full(n, np.nan)
    plot_flag3 = np.full(n, np.nan)
    plot_flag2 = np.full(n, np.nan)
    plot_flag1 = np.zeros(n)

    for i in range(n):
        if resultado[i] == flag6:
            plot_flag6[i] = 0
        elif resultado[i] == flag5 and variavel[i] > 0:
            plot_flag5[i] = variavel[i]
        elif resultado[i] == flag4 and variavel[i] > 0:
            plot_flag4[i] = variavel[i]
        elif resultado[i] == flag3 and variavel[i] > 0:
            plot_flag3[i] = variavel[i]
        elif resultado[i] == flag2 and variavel[i] > 0:
            plot_flag2[i] = variavel[i]
        else:
            plot_flag1[i] = variavel[i]

    flag[:, 0] = plot_flag1.flatten()
    flag[:, 1] = plot_flag2.flatten()
    flag[:, 2] = plot_flag3.flatten()
    flag[:, 3] = plot_flag4.flatten()
    flag[:, 4] = plot_flag5.flatten()
    flag[:, 5] = plot_flag6.flatten()

    return flag
