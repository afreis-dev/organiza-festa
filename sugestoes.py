import random 
from utils import limpar_tela, aguardar_enter
from eventos import mostrar_eventos, encontrar_evento_por_id

"""Funções para gerar sugestões com base no evento"""

s_cardapio = {"aniversario": ["kibe", "coxinha", "pastel", "mini sanduíche", "cachorro-quente", "brigadeiro", "bem-casado", "beijinho)"],
              "aniversário": ["kibe", "coxinha", "pastel", "mini sanduíche", "cachorro-quente", "brigadeiro", "bem-casado", "beijinho)"],
              "casamento": ["coqueteis", "tábua de frios", "vinhos", "buffet", "doces finos", "ilha de sorvete"],
              "churrasco": ["carne vermelha(maminha, picanha, contra-filé...)", "pão de alho", "queijo coalho", "cerveja", "refrigerante"],
              "natal": ["peru", "chester", "lombo", "bacalhau", "arroz à grega", "salpicão", "panetone", "pudim"],
              "festa junina": ["pamonha", "milho cozido", "milho assado", "munguzá", "bolo de milho", "pé de moleque", "paçoca", "canjica"]
              }
s_decoracao = {"aniversario":[],
               "aniversário":[],
               "casamento": [],
               "natal": [],
               "festa junina": []
               }
s_diversao = {"aniversario": [],
              "aniversário":[],
              "casamento": [],
              "churrasco": [],
              "natal": [],
              "festa junina": []
              }

def obter_sugestao(dicionarios_de_sugestoes, tipo_evento):
    opcoes=dicionarios_de_sugestoes.get(tipo_evento.lower(), [])

    if len(opcoes) == 0:
        return "Nenhuma sugestão encontrada para este tipo."
    return random.choice(opcoes)


def gerar_sugestoes(evento):
    limpar_tela()
    print(f"=== Sugestões para: {evento['nome']} ===")
    
    tipo = evento["tipo"]

    print(f"Tipo: {tipo}")
    
    # 1. Sugestao de Cardapio
    sugestao_cardapio = obter_sugestao(s_cardapio, tipo)
    print(f"🍴 Cardápio Recomendado:")
    print(f"   {sugestao_cardapio}")

    # 2. Sugestao de Decoracao
    sugestao_decoracao = obter_sugestao(s_decoracao, tipo)
    print(f"\nDecoração Adequada:")
    print(f"   {sugestao_decoracao}")

    # 3. Sugestao de Entretenimento
    sugestao_diversao = obter_sugestao(s_diversao, tipo)
    print(f"\nEntretenimento sugerido:")
    print(f"   {sugestao_diversao}")