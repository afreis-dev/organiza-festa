ARQUIVO_EVENTOS = "eventos.csv"

def garantir_arquivo_eventos():
    # aqui essa função verifica se o arquivo eventos.csv existe. se não, cria com o cabeçalho apropriado
    try:
        arquivo = open(ARQUIVO_EVENTOS, "r", encoding="utf-8")
        arquivo.close()
    except:
        arquivo = open(ARQUIVO_EVENTOS, "w", encoding="utf-8")
        cabecalho = "id,nome,tipo,data,local,orcamento_total,convidados\n"
        arquivo.write(cabecalho)
        arquivo.close()

def carregar_eventos():
    # essa função lê o arquivo eventos.csv e retorna uma lista de dicionários, cada um representando um evento
    lista_de_eventos = []

    arquivo = open(ARQUIVO_EVENTOS, "r", encoding="utf-8")
    linhas_do_arquivo = arquivo.readlines()
    arquivo.close()

    indice_linha = 1
    while indice_linha < len(linhas_do_arquivo):
        linha_atual = linhas_do_arquivo[indice_linha].strip()
        if linha_atual != "":
            partes = linha_atual.split(",")
            evento = {
                "id": partes[0],
                "nome": partes[1],
                "tipo": partes[2],
                "data": partes[3],              # formato sugerido: AAAA-MM-DD a gente usa assim pq o python não entende o formato normal
                "local": partes[4],
                "orcamento_total": partes[5],   # guardado como texto, converta só quando precisar :)
                "convidados": partes[6]
            }
            lista_de_eventos.append(evento)
        indice_linha = indice_linha + 1

    return lista_de_eventos