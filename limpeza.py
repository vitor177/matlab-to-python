import os
import shutil

def limpar_e_mover_arquivos(diretorio_atual, nome_arquivo):
    # Verificar se a pasta 'resultados' já existe e, se existir, removê-la
    pasta_resultados = os.path.join(diretorio_atual, 'resultados', nome_arquivo)
    if os.path.exists(pasta_resultados):
        shutil.rmtree(pasta_resultados)

    # Criar a pasta 'resultados'
    os.makedirs(pasta_resultados)

    # Listar arquivos no diretório atual
    arquivos = os.listdir(diretorio_atual)

    # Extensões que queremos verificar e mover
    extensoes = ['.svg', '.pdf', '.xlsx']

    # Iterar sobre os arquivos no diretório atual
    for arquivo in arquivos:
        # Verificar se o arquivo tem uma das extensões desejadas
        if any(arquivo.endswith(ext) for ext in extensoes):
            # Caminho completo do arquivo atual
            caminho_arquivo = os.path.join(diretorio_atual, arquivo)
            print(f"Movendo {caminho_arquivo} para {pasta_resultados}")
            shutil.move(caminho_arquivo, pasta_resultados)


    # # Excluir os arquivos que não foram movidos para 'resultados'
    # arquivos_restantes = os.listdir(diretorio_atual)
    # for arquivo in arquivos_restantes:
    #     caminho_arquivo = os.path.join(diretorio_atual, arquivo)
    #     #os.remove(caminho_arquivo)

    # print("Arquivos movidos para 'resultados' e os demais foram excluídos do diretório principal.")

# Teste da função (opcional)
if __name__ == "__main__":
    diretorio_atual = './'  # Substitua pelo seu caminho
    limpar_e_mover_arquivos(diretorio_atual, "LAJES")
