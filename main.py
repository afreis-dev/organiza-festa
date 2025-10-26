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

def salvar_eventos(lista_de_eventos):
    # essa função recebe uma lista de dicionários (eventos) e salva no arquivo eventos.csv
    arquivo = open(ARQUIVO_EVENTOS, "w", encoding="utf-8")
    arquivo.write("id,nome,tipo,data,local,orcamento_total,convidados\n")

    indice = 0
    while indice < len(lista_de_eventos):
        e = lista_de_eventos[indice]
        linha = (
            e["id"] + "," +
            e["nome"] + "," +
            e["tipo"] + "," +
            e["data"] + "," +
            e["local"] + "," +
            str(e["orcamento_total"]) + "," +
            str(e["convidados"]) + "\n"
        )
        arquivo.write(linha)
        indice = indice + 1

    arquivo.close()

def gerar_novo_id(lista_de_eventos):
    # essa função recebe a lista de eventos e retorna um novo id único (string)
    if len(lista_de_eventos) == 0:
        return "1"

    maior_id_encontrado = 0
    indice = 0
    while indice < len(lista_de_eventos):
        try:
            valor_atual = int(lista_de_eventos[indice]["id"])
            if valor_atual > maior_id_encontrado:
                maior_id_encontrado = valor_atual
        except:
            # se algum id estiver estranho, ignora
            pass
        indice = indice + 1

    proximo_id = maior_id_encontrado + 1
    return str(proximo_id)

def ler_numero_inteiro(mensagem):
    # lê um número inteiro do usuário, repetindo a pergunta até que o valor seja válido
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print(">> Digite um número inteiro válido.")

def ler_numero_decimal(mensagem):
    # lê um número decimal do usuário, repetindo a pergunta até que o valor seja válido
    while True:
        texto = input(mensagem).strip()
        texto = texto.replace(",", ".")
        try:
            valor = float(texto)
            return valor
        except:
            print(">> Digite um número válido (ex.: 1500 ou 1500,00).")

def mostrar_eventos(lista_de_eventos):
    # mostra a lista de eventos no terminal
    print("\n=== LISTA DE EVENTOS ===")
    if len(lista_de_eventos) == 0:
        print("(sem eventos cadastrados)")
        return

    print("ID | Data       | Nome")
    print("-------------------------------")
    indice = 0
    while indice < len(lista_de_eventos):
        e = lista_de_eventos[indice]
        print(e["id"].rjust(2), "|", e["data"].ljust(10), "|", e["nome"])
        indice = indice + 1

def criar_evento(lista_de_eventos):
    # função para criar um novo evento
    print("\n--- Criar Evento ---")
    nome_evento = input("Nome: ").strip()
    tipo_evento = input("Tipo (aniversário/casamento/reunião/...): ").strip()
    data_evento = input("Data (AAAA-MM-DD): ").strip()
    local_evento = input("Local: ").strip()
    orcamento_total_evento = ler_numero_decimal("Orçamento total (somente número): R$ ")
    numero_convidados_evento = ler_numero_inteiro("Número de convidados: ")

    # validação básica dos campos obrigatórios
    if nome_evento == "" or tipo_evento == "" or data_evento == "" or local_evento == "":
        print(">> Preencha todos os campos obrigatórios.")
        return

    novo_evento = {
        "id": gerar_novo_id(lista_de_eventos),
        "nome": nome_evento,
        "tipo": tipo_evento,
        "data": data_evento,
        "local": local_evento,
        "orcamento_total": str(orcamento_total_evento),  # salva como texto
        "convidados": str(numero_convidados_evento)
    }

    lista_de_eventos.append(novo_evento)
    salvar_eventos(lista_de_eventos)
    print(">> Evento criado com sucesso!")

def encontrar_evento_por_id(lista_de_eventos, id_buscado):
    # procura um evento pelo id na lista e retorna o dicionário do evento ou None se não encontrar
    indice = 0
    while indice < len(lista_de_eventos):
        if lista_de_eventos[indice]["id"] == id_buscado:
            return lista_de_eventos[indice]
        indice = indice + 1
    return None


def mostrar_menu():
    # mostra o menu principal
    print("\n=== Organiza Festa — Eventos ===")
    print("[1] Listar eventos")
    print("[2] Criar evento")
    print("[3] Editar evento")
    print("[4] Excluir evento")
    print("[0] Sair")

def main():
    # garantir que o arquivo de eventos existe e ponto de entrada do programa
    garantir_arquivo_eventos()
    eventos = carregar_eventos()

    while True:
        # mostra o menu e lê a opção do usuário
        mostrar_menu()
        opcao_escolhida = input("> ").strip()

        if opcao_escolhida == "1":
            mostrar_eventos(eventos)
            
        elif opcao_escolhida == "2":
            criar_evento(eventos)
            # recarrega do CSV para manter sincronizado (didático)
            eventos = carregar_eventos()

main()