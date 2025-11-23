"""Menus e fluxo principal do aplicativo."""

from eventos import (
    mostrar_eventos,
    criar_evento,
    editar_evento,
    excluir_evento,
)
from tarefas import (
    listar_tarefas_de_evento,
    criar_tarefa,
    editar_tarefa,
    excluir_tarefa,
    marcar_tarefa_feita,
)
from storage import carregar_eventos, carregar_tarefas
from utils import limpar_tela, aguardar_enter

def mostrar_menu():
    """Exibe as opcoes disponiveis para o usuario."""
    print("\n=== Organiza Festa - Eventos ===")
    print("[1] Listar eventos")
    print("[2] Criar evento")
    print("[3] Editar evento")
    print("[4] Excluir evento")
    print("[0] Sair")


def menu_tarefas(lista_de_tarefas, id_evento):
    """Menu especifico para gerenciar as tarefas de um evento."""
    while True:
        limpar_tela()
        print(f"\n=== Tarefas do evento {id_evento} ===")
        print("[1] Listar tarefas")
        print("[2] Criar tarefa")
        print("[3] Editar tarefa")
        print("[4] Excluir tarefa")
        print("[5] Marcar tarefa como feita")
        print("[0] Voltar")
        opcao_escolhida = input("> ").strip()

        if opcao_escolhida == "1":
            listar_tarefas_de_evento(lista_de_tarefas, id_evento)
            aguardar_enter()

        elif opcao_escolhida == "2":
            criar_tarefa(lista_de_tarefas, id_evento)
            # recarrega do CSV para manter sincronizado
            tarefas_atualizadas = carregar_tarefas()
            lista_de_tarefas.clear()
            lista_de_tarefas.extend(tarefas_atualizadas)
            aguardar_enter()

        elif opcao_escolhida == "3":
            editar_tarefa(lista_de_tarefas, id_evento)
            tarefas_atualizadas = carregar_tarefas()
            lista_de_tarefas.clear()
            lista_de_tarefas.extend(tarefas_atualizadas)
            aguardar_enter()

        elif opcao_escolhida == "4":
            excluir_tarefa(lista_de_tarefas, id_evento)
            tarefas_atualizadas = carregar_tarefas()
            lista_de_tarefas.clear()
            lista_de_tarefas.extend(tarefas_atualizadas)
            aguardar_enter()

        elif opcao_escolhida == "5":
            marcar_tarefa_feita(lista_de_tarefas, id_evento)
            tarefas_atualizadas = carregar_tarefas()
            lista_de_tarefas.clear()
            lista_de_tarefas.extend(tarefas_atualizadas)
            aguardar_enter()

        elif opcao_escolhida == "0":
            break

        else:
            print(">> Opcao invalida. Tente novamente.")
            aguardar_enter()


def menu_principal(lista_de_eventos, lista_de_tarefas):
    """Menu principal do sistema Organiza Festa."""
    while True:
        limpar_tela()
        print("\n=== Organiza Festa — Eventos ===")
        print("[1] Listar eventos")
        print("[2] Criar evento")
        print("[3] Editar evento")
        print("[4] Excluir evento")
        print("[5] Gerenciar tarefas de um evento")
        print("[0] Sair")
        opcao_escolhida = input("> ").strip()

        if opcao_escolhida == "1":
            mostrar_eventos(lista_de_eventos)
            aguardar_enter()

        elif opcao_escolhida == "2":
            criar_evento(lista_de_eventos)
            eventos_atualizados = carregar_eventos()
            lista_de_eventos.clear()
            lista_de_eventos.extend(eventos_atualizados)
            aguardar_enter()

        elif opcao_escolhida == "3":
            editar_evento(lista_de_eventos)
            eventos_atualizados = carregar_eventos()
            lista_de_eventos.clear()
            lista_de_eventos.extend(eventos_atualizados)
            aguardar_enter()

        elif opcao_escolhida == "4":
            excluir_evento(lista_de_eventos)
            eventos_atualizados = carregar_eventos()
            lista_de_eventos.clear()
            lista_de_eventos.extend(eventos_atualizados)
            aguardar_enter()

        elif opcao_escolhida == "5":
            # escolhe o evento primeiro
            mostrar_eventos(lista_de_eventos)
            id_evento_escolhido = input("\nDigite o ID do evento para gerenciar as tarefas: ").strip()
            menu_tarefas(lista_de_tarefas, id_evento_escolhido)

        elif opcao_escolhida == "0":
            print("Até mais!")
            break

        else:
            print(">> Opcao invalida. Tente novamente.")
            aguardar_enter()