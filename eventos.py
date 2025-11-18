"""Funcoes que manipulam os eventos cadastrados no sistema."""

from storage import salvar_eventos
from utils import ler_numero_inteiro, ler_numero_decimal, descricao_contagem, validar_data

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
    tipo_evento = int(input("Digite: \n [1] Aniversario\n [2] Casamento\n [3] Churrasco\n [4] Natal\n [5] São João"))
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
