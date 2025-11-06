"""Ponto de entrada do aplicativo de organizacao de eventos."""

from storage import garantir_arquivos
from menu_teste import menu_escolha

def main():
    """Prepara o ambiente e delega o controle para o menu principal."""
    garantir_arquivos()  # cria pasta/arquivo se nao existirem
    menu_escolha() # chama o menu de escolha (ele carrega eventos quando necessario)



if __name__ == "__main__":
    main()
