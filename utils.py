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


def dias_ate(data_str: str) -> int:
    """
    Recebe uma data no formato 'DD/MM/AAAA' e retorna:
    > 0 -> faltam X dias
    = 0 -> é hoje
    < 0 -> já passaram X dias (ai o valor é negativo)
    """
    try: 
        data_evento = datetime.strptime(data_str, "%d/%m/%Y").date()
        return (data_evento - date.today()).days
    except:
        return 0 # se o formato estiver errado, evita erros retornando 0

def descricao_contagem(data_str: str) -> str:
    """
    transforma a diferença de dias em uma frase legível.
    """
    dias = dias_ate(data_str)
    if dias > 0:
        return f"Faltam {dias} dia{'s' if dias > 1 else ''}"
    elif dias == 0:
        return "É hoje!"
    else: return f"Passaram {-dias} dia{'s' if dias < -1 else ''}"

def validar_data(data_str: str) -> bool:
    """
    Verifica se a data está no formato 'DD/MM/AAAA' e é uma data válida.
    Retorna True se for válida, False caso contrário.
    """
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except:
        return False