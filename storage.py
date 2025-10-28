"""Leitura e escrita dos arquivos usados pelo aplicativo."""

ARQUIVO_EVENTOS = "data/eventos.csv"


def garantir_pasta_data():
    """Garante que a pasta data/ exista antes de criar/abrir arquivos."""
    try:
        import os

        if not os.path.exists("data"):
            os.mkdir("data")
    except:
        # Se algo der errado (permissao, etc.), deixamos passar e tratamos adiante
        pass


def garantir_arquivo_eventos():
    """Cria o arquivo eventos.csv com cabecalho caso ele ainda nao exista."""
    try:
        arquivo = open(ARQUIVO_EVENTOS, "r", encoding="utf-8")
        arquivo.close()
    except:
        arquivo = open(ARQUIVO_EVENTOS, "w", encoding="utf-8")
        arquivo.write("id,nome,tipo,data,local,orcamento_total,convidados\n")
        arquivo.close()


def carregar_eventos():
    """Retorna uma lista de dicionarios lendo cada linha do CSV."""
    lista_de_eventos = []
    try:
        arquivo = open(ARQUIVO_EVENTOS, "r", encoding="utf-8")
        linhas_do_arquivo = arquivo.readlines()
        arquivo.close()
    except:
        # Se nao houver arquivo ainda, devolve lista vazia para o resto do programa
        return []

    indice_linha = 1  # pula a linha do cabecalho
    while indice_linha < len(linhas_do_arquivo):
        linha_atual = linhas_do_arquivo[indice_linha].strip()
        if linha_atual != "":
            partes = linha_atual.split(",")
            evento = {
                "id": partes[0],
                "nome": partes[1],
                "tipo": partes[2],
                "data": partes[3],
                "local": partes[4],
                "orcamento_total": partes[5],  # valores numericos sao guardados como texto
                "convidados": partes[6],
            }
            lista_de_eventos.append(evento)
        indice_linha = indice_linha + 1

    return lista_de_eventos


def salvar_eventos(eventos):
    """Sobrescreve o CSV com a lista de eventos mais recente."""
    garantir_pasta_data()
    arquivo = open(ARQUIVO_EVENTOS, "w", encoding="utf-8")
    arquivo.write("id,nome,tipo,data,local,orcamento_total,convidados\n")

    indice = 0
    while indice < len(eventos):
        evento = eventos[indice]
        linha = (
            evento["id"]
            + ","
            + evento["nome"]
            + ","
            + evento["tipo"]
            + ","
            + evento["data"]
            + ","
            + evento["local"]
            + ","
            + str(evento["orcamento_total"])
            + ","
            + str(evento["convidados"])
            + "\n"
        )
        arquivo.write(linha)
        indice = indice + 1

    arquivo.close()


def garantir_arquivos():
    """Executa as verificacoes necessarias antes de iniciar o programa."""
    garantir_pasta_data()
    garantir_arquivo_eventos()
