"""Funcoes que manipulam os eventos cadastrados no sistema."""

from storage import salvar_eventos
from utils import ler_numero_inteiro, ler_numero_decimal, descricao_contagem, validar_data, formatar_moeda
from tarefas import total_gasto_no_evento

def gerar_novo_id(lista_de_eventos):
    """Encontra o maior ID atual e devolve o proximo numero como texto."""
    if len(lista_de_eventos) == 0:
        return "1"

    maior_id_encontrado = 0
    indice = 0
    while indice < len(lista_de_eventos):
        try:
            valor_atual = int(lista_de_eventos[indice]["id"])
            # guardamos o maior numero encontrado ate agora
            if valor_atual > maior_id_encontrado:
                maior_id_encontrado = valor_atual
        except:
            # ignora IDs corrompidos para nao travar a geracao do proximo numero
            pass
        indice = indice + 1

    return str(maior_id_encontrado + 1)


def mostrar_eventos(lista_de_eventos):
    """Exibe a tabela de eventos na tela."""
    print("\n=== LISTA DE EVENTOS ===")
    if len(lista_de_eventos) == 0:
        print("(sem eventos cadastrados)")
        return

    print("ID | Data       | Situação        | Nome")
    print("------------------------------------------------------")

    indice = 0
    while indice < len(lista_de_eventos):
        evento_atual = lista_de_eventos[indice]
        # usamos rjust/ljust para alinhar as colunas sem complicacao
        situacao = descricao_contagem(evento_atual["data"])
        print(
            evento_atual["id"].rjust(2), "|", evento_atual["data"].ljust(10), "|",
            situacao.ljust(15), "|",
            evento_atual["nome"]
            )
        indice = indice + 1


def criar_evento(lista_de_eventos):
    """Coleta os dados do usuario, cria o evento e salva no arquivo."""
    print("\n--- Criar Evento ---")

    # Todos os campos sao lidos como texto primeiro
    nome_evento = input("Nome: ").strip()
    tipo_evento = input("Tipo (aniversario/casamento/reuniao/...): ").strip()
    data_evento = input("Data (DD/MM/AAAA): ").strip()
    if not validar_data(data_evento):
        print(">> Data invalida. Use o formato DD/MM/AAAA.")
        return
    local_evento = input("Local: ").strip()

    # Numeros usam helpers para validar os valores
    orcamento_total_evento = ler_numero_decimal("Orcamento total (somente numero): R$ ")
    numero_convidados_evento = ler_numero_inteiro("Numero de convidados: ")

    # Sem esses dados nao faz sentido salvar o evento
    if nome_evento == "" or tipo_evento == "" or data_evento == "" or local_evento == "":
        print(">> Preencha todos os campos obrigatorios.")
        return

    novo_evento = {
        "id": gerar_novo_id(lista_de_eventos),
        "nome": nome_evento,
        "tipo": tipo_evento,
        "data": data_evento,
        "local": local_evento,
        "orcamento_total": str(orcamento_total_evento),  # guardamos como texto para simplificar o CSV
        "convidados": str(numero_convidados_evento),
    }

    lista_de_eventos.append(novo_evento)
    salvar_eventos(lista_de_eventos)
    print(">> Evento criado com sucesso!")


def encontrar_evento_por_id(lista_de_eventos, id_buscado):
    """Procura na lista pelo ID informado e devolve o evento correspondente."""
    indice = 0
    while indice < len(lista_de_eventos):
        if lista_de_eventos[indice]["id"] == id_buscado:
            return lista_de_eventos[indice]
        indice = indice + 1

    # Quando nao encontra, devolve None para que a funcao chamadora trate a situacao
    return None


def editar_evento(lista_de_eventos):
    """Permite alterar os campos de um evento escolhido."""
    print("\n--- Editar Evento ---")
    mostrar_eventos(lista_de_eventos)
    id_escolhido = input("\nDigite o ID do evento que deseja editar: ").strip()

    evento = encontrar_evento_por_id(lista_de_eventos, id_escolhido)
    if evento is None:
        print(">> ID nao encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Nome [{evento['nome']}]: ").strip()
    novo_tipo = input(f"Tipo [{evento['tipo']}]: ").strip()
    nova_data = input(f"Data (DD/MM/AAAA) [{evento['data']}]: ").strip()
    novo_local = input(f"Local [{evento['local']}]: ").strip()
    novo_orc = input(f"Orcamento total [{evento['orcamento_total']}]: ").strip()
    novo_conv = input(f"Convidados [{evento['convidados']}]: ").strip()

    # Atualiza somente os campos onde o usuario digitou algo
    if novo_nome != "":
        evento["nome"] = novo_nome
    if novo_tipo != "":
        evento["tipo"] = novo_tipo
    if nova_data != "":
        evento["data"] = nova_data
    if novo_local != "":
        evento["local"] = novo_local

    if novo_orc != "":
        novo_orc = novo_orc.replace(",", ".")
        try:
            float(novo_orc)
            evento["orcamento_total"] = novo_orc
        except:
            print(">> Orcamento invalido. Mantido o valor anterior.")

    if novo_conv != "":
        if novo_conv.isdigit():
            evento["convidados"] = novo_conv
        else:
            print(">> Numero de convidados invalido. Mantido o valor anterior.")

    salvar_eventos(lista_de_eventos)
    print(">> Evento atualizado com sucesso!")


def excluir_evento(lista_de_eventos):
    """Remove um evento da lista a partir do ID informado."""
    print("\n--- Excluir Evento ---")
    mostrar_eventos(lista_de_eventos)
    id_escolhido = input("\nDigite o ID do evento que deseja excluir: ").strip()

    nova_lista = []
    encontrado = False
    indice = 0

    # Criamos uma nova lista com todos os itens, menos o selecionado
    while indice < len(lista_de_eventos):
        if lista_de_eventos[indice]["id"] == id_escolhido:
            encontrado = True
        else:
            nova_lista.append(lista_de_eventos[indice])
        indice = indice + 1

    if encontrado:
        salvar_eventos(nova_lista)
        print(">> Evento excluido com sucesso!")

        # Reaproveitamos o objeto de lista original para manter a referencia em todo o programa
        lista_de_eventos.clear()
        indice = 0
        while indice < len(nova_lista):
            lista_de_eventos.append(nova_lista[indice])
            indice = indice + 1
    else:
        print(">> ID nao encontrado. Nada foi excluido.")


def sugerir_para_evento(evento):
    """Gera sugestoes simples com base no tipo e na quantidade de convidados."""
    tipo = evento["tipo"].lower()
    try:
        quantidade_convidados = int(evento["convidados"])
    except:
        quantidade_convidados = 0

    # Classifica o porte do evento
    if quantidade_convidados <= 20:
        porte = "pequeno"
    elif quantidade_convidados <= 50:
        porte = "medio"
    else:
        porte = "grande"

    sugestoes = []

    # Sugestoes basicas por tipo de evento
    if "aniversario" in tipo:
        sugestoes.append("Fornecedor: confeitaria especializada em bolos personalizados.")
        sugestoes.append("Decoração: painel com baloes e fotos do aniversariante.")
        sugestoes.append("Cardapio: salgadinhos variados, cachorro-quente e doces simples.")
        sugestoes.append("Atividade: brincadeiras, musica animada e espaço para fotos.")

    elif "casamento" in tipo:
        sugestoes.append("Fornecedor: buffet completo (entrada, prato principal e sobremesa).")
        sugestoes.append("Decoração: flores, velas e iluminação mais elegante.")
        sugestoes.append("Cardapio: pratos quentes, opções sem carne e sobremesa refinada.")
        sugestoes.append("Atividade: pista de dança e playlist definida pelos noivos.")

    elif "churrasco" in tipo:
        sugestoes.append("Fornecedor: fornecedor de carnes e carvao em quantidade adequada.")
        sugestoes.append("Decoração: mesas simples, area externa e iluminação aconchegante.")
        sugestoes.append("Cardapio: carnes variadas, pao de alho, saladas e refrigerantes.")
        sugestoes.append("Atividade: musica ambiente e jogos de mesa ou cartas.")

    elif "reuniao" in tipo or "corporativo" in tipo:
        sugestoes.append("Fornecedor: coffee break (cafe, sucos, bolos e salgados).")
        sugestoes.append("Decoração: ambiente simples, com cadeiras confortaveis e projetor.")
        sugestoes.append("Cardapio: lanches leves que nao façam muita sujeira.")
        sugestoes.append("Atividade: intervalo para networking e perguntas.")

    else:
        sugestoes.append("Fornecedor: pesquise um buffet ou fornecedor especializado no seu tipo de evento.")
        sugestoes.append("Decoração: escolha um tema simples que represente bem o objetivo do evento.")
        sugestoes.append("Cardapio: pense em algo que agrade a maioria dos convidados.")
        sugestoes.append("Atividade: planeje pelo menos uma atividade para quebrar o gelo.")

    # Ajuste basico pelo porte (quantidade de convidados)
    if porte == "pequeno":
        sugestoes.append("Como o evento é pequeno, foque em algo mais intimista e personalizado.")
    elif porte == "medio":
        sugestoes.append("Com quantidade media de convidados, vale organizar a melhor fila de buffet e assentos.")
    else:
        sugestoes.append("Como o evento é grande, considere equipe extra de apoio e controle de entrada.")

    return sugestoes


def detalhar_evento_completo(lista_de_eventos, lista_de_tarefas):
    """Mostra um resumo completo do evento: dados, data, orçamento, tarefas e sugestões."""
    print("\n--- Detalhar evento ---")
    mostrar_eventos(lista_de_eventos)
    id_escolhido = input("\nDigite o ID do evento que deseja ver os detalhes: ").strip()

    evento_encontrado = encontrar_evento_por_id(lista_de_eventos, id_escolhido)
    if evento_encontrado is None:
        print(">> ID não encontrado.")
        return
    
    nome = evento_encontrado["nome"]
    tipo = evento_encontrado["tipo"]
    data = evento_encontrado["data"]
    local = evento_encontrado["local"]
    texto_situacao_data = descricao_contagem(data)

    try:
        orcamento_total = float(evento_encontrado["orcamento_total"])
    except:
        orcamento_total = 0.0

    gasto_total = total_gasto_no_evento(lista_de_tarefas, id_escolhido)
    saldo = orcamento_total - gasto_total
    
    if orcamento_total > 0:
        percentual_gasto = (gasto_total / orcamento_total) * 100
    else:
        percentual_gasto = 0.0

    # Tarefas
    quantidade_pendentes, quantidade_feitas = contar_tarefas_do_evento(lista_de_tarefas, id_escolhido)

    # Sugestoes personalizadas
    lista_de_sugestoes = sugerir_para_evento(evento_encontrado)

    print("\n=== DETALHES DO EVENTO ===")
    print("Nome:       ", nome)
    print("Tipo:       ", tipo)
    print("Data:       ", data, " | ", texto_situacao_data)
    print("Local:      ", local)
    print("------------------------------------------")
    print("Orcamento:  ", formatar_moeda(orcamento_total))
    print("Gasto:      ", formatar_moeda(gasto_total), f"({percentual_gasto:.0f}% do orcamento)")
    print("Saldo:      ", formatar_moeda(saldo))

    if saldo < 0:
        print("ATENCAO: o evento estourou o orcamento!")

    print("------------------------------------------")
    print("Tarefas:    ", quantidade_feitas, "feitas /", quantidade_pendentes, "pendentes")

    print("\n=== SUGESTOES PARA ESSE EVENTO ===")
    for sugestao in lista_de_sugestoes:
        print("-", sugestao)

def contar_tarefas_do_evento(lista_de_tarefas, id_evento):
    """
    Conta quantas tarefas do evento estao pendentes e quantas estao feitas.
    Retorna: (pendentes, feitas)
    """
    quantidade_pendentes = 0
    quantidade_feitas = 0

    for tarefa in lista_de_tarefas:
        if tarefa["evento_id"] == id_evento:
            if tarefa["status"] == "feito":
                quantidade_feitas += 1
            else:
                quantidade_pendentes += 1

    return quantidade_pendentes, quantidade_feitas