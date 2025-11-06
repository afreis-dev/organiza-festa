import os
from storage import garantir_arquivos, carregar_eventos
from menus import menu_principal
from datetime import datetime


def registrar_erro(mensagem, exc=None):
    """Registra erros simples em um arquivo de log local (erro_app.log)."""
    try:
        # garante que o diretório exista se for especificado no futuro
        with open("erro_app.log", "a", encoding="utf-8") as f:  # (aqui mantemos o arquivo na raiz do projeto)
            f.write(f"{datetime.now().isoformat()} - {mensagem}\n")
            if exc is not None:
                # registra uma representação simples da exceção (sem stack trace)
                try:
                    f.write(repr(exc) + "\n")
                except Exception:
                    # não propagar erro de logging
                    pass
    except Exception:
        # nunca propagar erro de logging
        pass


def menu_escolha():
    '''Menu para escolher entre eventos e tarefas.'''
    try:
        while True:
            print("\n=== Menu Principal ===")
            print("1. Eventos")
            print("2. Tarefas")
            print("3. Sair")
            op = input("Escolha o menu: ").strip()

            if op == "1":
                # garante que a pasta/arquivo existam antes de carregar
                try:
                    garantir_arquivos()
                except Exception as e:
                    registrar_erro("Falha ao garantir arquivos", e)

                # tenta carregar eventos com tratamento
                try:
                    eventos = carregar_eventos()
                except Exception as e:
                    registrar_erro("Falha ao carregar eventos", e)
                    print("Não foi possível carregar os eventos no momento. Tente novamente mais tarde.")
                    continue

                # garante tipo esperado
                if not isinstance(eventos, list):
                    registrar_erro("carregar_eventos retornou tipo inesperado", eventos)
                    eventos = []

                # chama menu de eventos com proteção para exceções internas
                try:
                    menu_principal(eventos)
                except Exception as e:
                    registrar_erro("Erro dentro de menu_principal", e)
                    print("Ocorreu um erro ao abrir o menu de eventos. Voltando ao menu principal.")
                    continue

            elif op == "2":
                # funcionalidade de tarefas ainda nao implementada
                print("Menu de tarefas ainda não implementado.")

            elif op == "3":
                print("Saindo do aplicativo.")
                break

            else:
                print("Opção inválida. Digite 1, 2 ou 3.")

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Até mais!")

    except Exception as e:
        registrar_erro("Erro inesperado no menu_escolha", e)
        print("Erro inesperado. Verifique 'erro_app.log' para detalhes.")

        