ARQUIVO_EVENTOS = "eventos.csv"

def garantir_arquivo_eventos():
    try:
        arquivo = open(ARQUIVO_EVENTOS, "r", encoding="utf-8")
        arquivo.close()
    except:
        arquivo = open(ARQUIVO_EVENTOS, "w", encoding="utf-8")
        cabecalho = "id,nome,tipo,data,local,orcamento_total,convidados\n"
        arquivo.write(cabecalho)
        arquivo.close()