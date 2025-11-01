"""Funcoes auxiliares para entrada de dados e interface."""

import os
from datetime import date, datetime


def limpar_tela():
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system("cls" if os.name == "nt" else "clear")


def ler_numero_inteiro(mensagem):
    """Solicita um numero inteiro ate o usuario informar um valor valido."""
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print(">> Digite um número inteiro válido.")


def ler_numero_decimal(mensagem):
    """Solicita um numero decimal (float) validando a entrada do usuario."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            return float(texto)
        except:
            print(">> Digite um número válido (ex.: 1500 ou 1500,00).")


def aguardar_enter():
    """Mantem a tela visivel ate o usuario pressionar Enter."""
    input("\nPressione Enter para voltar ao menu...")


def dias_ate(data_iso: str) -> int: 
    try: 
        date_evento = datetime.strptime(data_iso, "%Y-%m-%d").date()
        return (date_evento - date.today()).days
    except:
        return 0
    
