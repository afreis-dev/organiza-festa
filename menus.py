"""Menus e fluxo principal do aplicativo."""

from eventos import (mostrar_eventos, criar_evento, editar_evento, excluir_evento, encontrar_evento_por_id)
from utils import limpar_tela, aguardar_enter
from sugestoes import gerar_sugestoes


def mostrar_menu():
    """Exibe as opcoes disponiveis para o usuario."""
    print("\n=== Organiza Festa - Eventos ===")
    print("[1] Listar eventos")
    print("[2] Criar evento")
    print("[3] Editar evento")
    print("[4] Excluir evento")
    print("[5] Ver sugestões")
    print("[0] Sair")


def menu_principal(eventos):
    """Loop principal: mostra o menu, le a opcao e chama a acao correspondente."""
    while True:
        limpar_tela()
        mostrar_menu()
        opcao_escolhida = input("> ").strip()

        if opcao_escolhida == "1":
            mostrar_eventos(eventos)
            aguardar_enter()
        elif opcao_escolhida == "2":
            criar_evento(eventos)
            aguardar_enter()
        elif opcao_escolhida == "3":
            editar_evento(eventos)
            aguardar_enter()
        elif opcao_escolhida == "4":
            excluir_evento(eventos)
            aguardar_enter()
        elif opcao_escolhida == "5":
            mostrar_eventos(eventos)
            id_escolhido = input("Digite o evento para mostrar sugestões: ").strip()
            evento_encontrado = encontrar_evento_por_id(eventos, id_escolhido)

            if evento_encontrado:
                gerar_sugestoes(evento_encontrado)
                aguardar_enter()
            else:
                print(">> ID não encontrado.")
                aguardar_enter()
        elif opcao_escolhida == "0":
            print("Até mais!")
            break
        else:
            print(">> Opção inválida. Tente novamente.")
            aguardar_enter()
