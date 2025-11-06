"""Leitura e escrita dos arquivos usados pelo aplicativo."""

ARQUIVO_EVENTOS = "data/eventos.csv"
ARQUIVO_TAREFAS = "data/tarefas.csv"


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


def garantir_arquivo_tarefas():
    """Cria o arquivo data/tarefas.csv caso ele ainda nao exista."""
    try:
        arquivo_t = open(ARQUIVO_TAREFAS, "r", encoding="utf-8")
        arquivo_t.close()
    except:
        arquivo_t = open(ARQUIVO_TAREFAS, "w", encoding="utf-8")
        arquivo_t.write("id, evento_do_id, descricao, custo, status, fornecedor\n")
        arquivo_t.close()

def carregar_tarefas():
    """Ler as tarefas do arquivo csv e passar para um dicionario"""
    lista_de_tarefas = []
    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readlines()
    except:
        return [] #retornar uma lista vazia caso nao haja arquivo
    while True:
        linha = 1 
        for linha in conteudo:
            linha_atual = linha.strip()
            if linha_atual != "": #ignorar linhas vazias
                lista_elementos = linha_atual.split(",")
                tarefas = {
                    "id": lista_elementos[0],
                    "evento_do_id": lista_elementos[1],
                    "descricao": lista_elementos[2],
                    "custo": lista_elementos[3],
                    "status": lista_elementos[4],
                    "fornecedor": lista_elementos[5],
                }
                lista_de_tarefas.append(tarefas) #lista de dicionarios
            linha += 1
        break

def salvar_tarefas(tarefas):
    """Sobrescrever o csv com a lista de tarefas atual"""


def garantir_arquivos():
    """Executa as verificacoes necessarias antes de iniciar o programa."""
    garantir_pasta_data()
    garantir_arquivo_eventos()
    garantir_arquivo_tarefas()
