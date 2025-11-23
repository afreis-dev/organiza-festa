from storage import salvar_tarefas, carregar_eventos
from utils import ler_numero_decimal, ler_numero_inteiro, formatar_moeda


def obter_orcamento_do_evento(id_evento):
    """Lê o orçamento do evento em eventos.csv e devolve em float."""
    lista_de_eventos = carregar_eventos()
    for evento in lista_de_eventos:
        if evento["id"] == id_evento:
            try:
                return float(evento["orcamento_total"])
            except:
                return 0.0
    return 0.0


def total_gasto_no_evento(lista_de_tarefas, id_evento):
    """Soma os custos de todas as tarefas daquele evento."""
    soma = 0.0
    for tarefa in lista_de_tarefas:
        if tarefa["evento_id"] == id_evento:
            try:
                soma = soma + float(tarefa["custo"])
            except:
                # Se o valor tiver estranho, simplesmente ignora
                pass
    return soma


def saldo_disponivel_do_evento(lista_de_tarefas, id_evento):
    """Calcula quanto ainda sobra do orçamento do evento."""
    orcamento = obter_orcamento_do_evento(id_evento)
    gasto = total_gasto_no_evento(lista_de_tarefas, id_evento)
    return orcamento - gasto


def obter_quantidade_da_tarefa(tarefa):
    """Converte o campo quantidade da tarefa para inteiro, padronizando valores inválidos."""
    try:
        quantidade = int(tarefa.get("quantidade", "1"))
        if quantidade <= 0:
            return 1
        return quantidade
    except:
        return 1


def calcular_preco_unitario_da_tarefa(tarefa):
    """Determina o preço unitário usando o total dividido pela quantidade."""
    quantidade = obter_quantidade_da_tarefa(tarefa)
    try:
        total = float(tarefa.get("custo", 0))
    except:
        total = 0.0

    if quantidade <= 0:
        return total

    return total / quantidade


def gerar_novo_id_tarefa(lista_de_tarefas):
    """Encontra o maior ID atual de tarefa e devolve o próximo numero como texto."""
    if len(lista_de_tarefas) == 0:
        return "1"
    
    maior_id_encontrado = 0
    for tarefa in lista_de_tarefas:
        try:
            valor_atual = int(tarefa["id"])
            if valor_atual > maior_id_encontrado:
                maior_id_encontrado = valor_atual
        except:
            pass

    return str(maior_id_encontrado + 1)



def listar_tarefas_de_evento(lista_de_tarefas, id_evento):
    """Mostra na tela as tarefas do evento e o resumo de orçamento."""
    print(f"\n=== TAREFAS DO EVENTO {id_evento} ===")

    orcamento = obter_orcamento_do_evento(id_evento)
    gasto = total_gasto_no_evento(lista_de_tarefas, id_evento)
    saldo = orcamento - gasto
    print("Orçamento:", formatar_moeda(orcamento))
    print("Gasto:    ", formatar_moeda(gasto))
    print("Saldo:    ", formatar_moeda(saldo))
    print("---------------------------------------------")

    encontrou_alguma = False

    for tarefa in lista_de_tarefas:
        if tarefa["evento_id"] == id_evento:
            encontrou_alguma = True
            quantidade = obter_quantidade_da_tarefa(tarefa)
            valor_unitario = calcular_preco_unitario_da_tarefa(tarefa)
            print(
                tarefa["id"].rjust(2),
                "|",
                tarefa["descricao"],
                "| Qtd:",
                str(quantidade),
                "| Unit:",
                formatar_moeda(valor_unitario),
                "| Total:",
                formatar_moeda(tarefa["custo"]),
                "|",
                tarefa["status"],
                "| fornecedor:",
                tarefa["fornecedor"],
            )

    if not encontrou_alguma:
        print("(nenhuma tarefa cadastrada para este evento)")



def criar_tarefa(lista_de_tarefas, id_evento):
    """Cria uma nova tarefa para o evento, atualizando o orçamento disponível."""
    print(f"\n--- Criar tarefa para o evento {id_evento} ---")

    # Mostra o resumo antes
    orcamento = obter_orcamento_do_evento(id_evento)
    gasto_atual = total_gasto_no_evento(lista_de_tarefas, id_evento)
    saldo_atual = orcamento - gasto_atual
    print("Orçamento:", formatar_moeda(orcamento))
    print("Gasto:    ", formatar_moeda(gasto_atual))
    print("Saldo:    ", formatar_moeda(saldo_atual))
    print("---------------------------------------------")

    descricao_tarefa = input("Descricao: ").strip()
    quantidade_tarefa = ler_numero_inteiro("Quantidade: ")
    while quantidade_tarefa <= 0:
        print(">> A quantidade deve ser pelo menos 1.")
        quantidade_tarefa = ler_numero_inteiro("Quantidade: ")

    custo_unitario = ler_numero_decimal("Preco unitario (somente numero): R$ ")
    custo_tarefa = quantidade_tarefa * custo_unitario
    fornecedor_tarefa = input("Fornecedor (opcional): ").strip()

    if descricao_tarefa == "":
        print(">> A descricao nao pode ficar vazia.")
        return

    # Verifica se o custo vai estourar o saldo
    if custo_tarefa > saldo_atual:
        diferenca = custo_tarefa - saldo_atual
        print(">> ATENCAO: esta tarefa ultrapassa o orçamento disponível em", formatar_moeda(diferenca))
        confirmar = input("Deseja continuar mesmo assim? [s/N] ").strip().lower()
        if confirmar != "s":
            print(">> Operacao cancelada.")
            return

    print("Total calculado:", formatar_moeda(custo_tarefa))

    nova_tarefa = {
        "id": gerar_novo_id_tarefa(lista_de_tarefas),
        "evento_id": id_evento,
        "descricao": descricao_tarefa.replace(",", ";"),
        "quantidade": str(quantidade_tarefa),
        "custo": str(custo_tarefa),
        "status": "pendente",
        "fornecedor": fornecedor_tarefa.replace(",", ";"),
    }

    lista_de_tarefas.append(nova_tarefa)
    salvar_tarefas(lista_de_tarefas)
    print(">> Tarefa criada com sucesso!")

    # Mostra o novo saldo depois da criacao
    gasto_novo = total_gasto_no_evento(lista_de_tarefas, id_evento)
    saldo_novo = orcamento - gasto_novo
    print("Novo saldo do evento:", formatar_moeda(saldo_novo))


def encontrar_tarefa_por_id(lista_de_tarefas, id_evento, id_tarefa):
    """Procrua uma tarefa especifica de um evento pelo ID."""
    for tarefa in lista_de_tarefas:
        if tarefa["evento_id"] == id_evento and tarefa["id"] == id_tarefa:
            return tarefa
    return None



def editar_tarefa(lista_de_tarefas, id_evento):
    """Permite alterar os campos de uma tarefa escolhida."""
    print("\n--- Editar tarefa ---")
    listar_tarefas_de_evento(lista_de_tarefas, id_evento)
    id_escolhido = input("\nDigite o ID da tarefa que deseja editar: ").strip()

    tarefa = encontrar_tarefa_por_id(lista_de_tarefas, id_evento, id_escolhido)
    if tarefa is None:
        print(">> ID nao encontrado para este evento.")
        return

    quantidade_atual = obter_quantidade_da_tarefa(tarefa)
    preco_unitario_atual = calcular_preco_unitario_da_tarefa(tarefa)

    print("Deixe em branco para manter o valor atual.")
    nova_descricao = input(f"Descricao [{tarefa['descricao']}]: ").strip()
    nova_quantidade = input(f"Quantidade [{quantidade_atual}]: ").strip()
    novo_preco_unitario = input(f"Preco unitario [{formatar_moeda(preco_unitario_atual)}]: ").strip()
    novo_status = input(f"Status (pendente/feito) [{tarefa['status']}]: ").strip()
    novo_fornecedor = input(f"Fornecedor [{tarefa['fornecedor']}]: ").strip()

    if nova_descricao != "":
        tarefa["descricao"] = nova_descricao.replace(",", ";")

    quantidade_final = quantidade_atual
    if nova_quantidade != "":
        if nova_quantidade.isdigit():
            novo_valor = int(nova_quantidade)
            if novo_valor > 0:
                quantidade_final = novo_valor
            else:
                print(">> Quantidade deve ser maior que zero. Mantido o valor anterior.")
        else:
            print(">> Quantidade invalida. Use apenas numeros inteiros.")

    preco_unitario_final = preco_unitario_atual
    if novo_preco_unitario != "":
        texto_preco = novo_preco_unitario.replace(",", ".")
        try:
            novo_valor_preco = float(texto_preco)
            if novo_valor_preco >= 0:
                preco_unitario_final = novo_valor_preco
            else:
                print(">> Preco unitario nao pode ser negativo. Mantido o valor anterior.")
        except:
            print(">> Preco unitario invalido. Mantido o valor anterior.")

    tarefa["quantidade"] = str(quantidade_final)
    tarefa["custo"] = str(quantidade_final * preco_unitario_final)

    if novo_status in ["pendente", "feito"]:
        tarefa["status"] = novo_status
    elif novo_status != "":
        print(">> Status invalido. Use 'pendente' ou 'feito'.")

    if novo_fornecedor != "":
        tarefa["fornecedor"] = novo_fornecedor.replace(",", ";")

    salvar_tarefas(lista_de_tarefas)
    print(">> Tarefa atualizada com sucesso!")


def excluir_tarefa(lista_de_tarefas, id_evento):
    """Remove uma tarefa da lista, a partir do ID informado."""
    print("\n--- Excluir tarefa ---")
    listar_tarefas_de_evento(lista_de_tarefas, id_evento)
    id_escolhido = input("\nDigite o ID da tarefa que deseja excluir: ").strip()

    nova_lista = []
    tarefa_encontrada = False

    for tarefa in lista_de_tarefas:
        if tarefa["evento_id"] == id_evento and tarefa["id"] == id_escolhido:
            tarefa_encontrada = True
        else:
            nova_lista.append(tarefa)

    if tarefa_encontrada:
        salvar_tarefas(nova_lista)
        # Mantemos a mesma lista que o programa usa, atualizando o conteudo
        lista_de_tarefas.clear()
        lista_de_tarefas.extend(nova_lista)
        print(">> Tarefa excluida com sucesso!")
    else:
        print(">> ID nao encontrado. Nada foi excluido.")


def marcar_tarefa_feita(lista_de_tarefas, id_evento):
    """Marca uma tarefa como 'feito'."""
    print("\n--- Marcar tarefa como feita ---")
    listar_tarefas_de_evento(lista_de_tarefas, id_evento)
    id_escolhido = input("\nDigite o ID da tarefa que deseja marcar como feita: ").strip()

    tarefa = encontrar_tarefa_por_id(lista_de_tarefas, id_evento, id_escolhido)
    if tarefa is None:
        print(">> ID nao encontrado para este evento.")
        return

    tarefa["status"] = "feito"
    salvar_tarefas(lista_de_tarefas)
    print(">> Tarefa marcada como feita!")
