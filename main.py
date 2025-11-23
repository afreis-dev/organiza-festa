"""Ponto de entrada do aplicativo de organizacao de eventos."""

from storage import garantir_arquivos, carregar_eventos, carregar_tarefas
from menus import menu_principal


def main():
    """Prepara o ambiente e delega o controle para o menu principal."""
    garantir_arquivos()  # cria pasta/arquivo se nao existirem
    eventos = carregar_eventos()  # carrega a lista atual de eventos salvos
    tarefas = carregar_tarefas()  # carrega a lista atual de tarefas salvas
    menu_principal(eventos, tarefas)  # mostra o menu e cuida da interacao com o usuario


if __name__ == "__main__":
    main()
