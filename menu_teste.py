'''Fazer o menu principal para carregar o menu de eventos e o de tarefas.'''
import os
from storage import garantir_arquivos, carregar_eventos
from menus import menu_principal


def menu_escolha():
    """Menu de selecao entre funcionalidades (eventos, tarefas, sair)."""
    while True:
        print("\n=== Menu Principal ===")
        print("1. Eventos")
        print("2. Tarefas")
        print("3. Sair")
        op = input("Escolha o menu: ").strip()

        if op == "1":
            # carrega eventos e delega ao menu de eventos
            eventos = carregar_eventos()
            menu_principal(eventos)
        elif op == "2":
            # funcionalidade de tarefas ainda nao implementada
            print("Menu de tarefas ainda não implementado.")
        elif op == "3":
            print("Saindo do aplicativo.")
            break
        else:
            print("Opção inválida")

        