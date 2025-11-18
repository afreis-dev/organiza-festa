"""Ponto de entrada do aplicativo de organizacao de eventos."""

from storage import garantir_arquivos, carregar_eventos
from menus import menu_principal
from sugestoes import gerar_sugestoes


def main():
    """Prepara o ambiente e delega o controle para o menu principal."""
    garantir_arquivos()  # cria pasta/arquivo se nao existirem
    eventos = carregar_eventos()  # carrega a lista atual de eventos salvos
    menu_principal(eventos)  # mostra o menu e cuida da interacao com o usuario


if __name__ == "__main__":
    main()
