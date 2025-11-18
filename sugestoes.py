import random 
from utils import limpar_tela, aguardar_enter
from eventos import mostrar_eventos, encontrar_evento_por_id

"""Funções para gerar sugestões com base no evento"""

s_cardapio = {"aniversario": ["kibe", "coxinha", "pastel", "mini sanduíche", "cachorro-quente", "brigadeiro", "bem-casado", "beijinho"],
              "aniversário": ["kibe", "coxinha", "pastel", "mini sanduíche", "cachorro-quente", "brigadeiro", "bem-casado", "beijinho"],
              "casamento": ["coqueteis", "tábua de frios", "vinhos", "buffet", "doces finos", "ilha de sorvete"],
              "churrasco": ["carne vermelha(maminha, picanha, contra-filé...)", "pão de alho", "queijo coalho", "cerveja", "refrigerante"],
              "natal": ["peru", "chester", "lombo", "bacalhau", "arroz à grega", "salpicão", "panetone", "pudim"],
              "festa junina": ["pamonha", "milho cozido", "milho assado", "munguzá", "bolo de milho", "pé de moleque", "paçoca", "canjica"],
              "sao joao": ["pamonha", "milho cozido", "milho assado", "munguzá", "bolo de milho", "pé de moleque", "paçoca", "canjica"],
              "são joão": ["pamonha", "milho cozido", "milho assado", "munguzá", "bolo de milho", "pé de moleque", "paçoca", "canjica"]
              }
s_decoracao = {"aniversario": ["balões coloridos", "painel de fotos", "velas personalizadas", "chapéus de festa", "banner temático"],
               "aniversário": ["balões coloridos", "painel de fotos", "velas personalizadas", "chapéus de festa", "banner temático"],
               "casamento": ["flores brancas", "iluminação amarela", "arranjos de mesa", "tapete vermelho"],
               "natal": ["pisca-pisca", "árvore de natal", "guirlanda", "presépio"],
               "festa junina": ["bandeirinhas", "fogueira", "balão de são joão", "toalha xadrez", "barracas"],
               "sao joao": ["bandeirinhas", "fogueira", "balão de são joão", "toalha xadrez", "barracas"],
               "são joão": ["bandeirinhas", "fogueira", "balão de são joão", "toalha xadrez", "barracas"]
              }
s_diversao = {"aniversario": ["música (DJ, caixa de som...)", "pula-pula", "futsabao", "maquiagem artistica", "magico" ],
              "aniversário":["música (DJ, caixa de som...)",  "pula-pula", "futsabao", "maquiagem artistica", "magico"],
              "casamento": ["banda ao vivo", "dj", "fotografo", "cabine de fotos"],
              "churrasco": ["banda ao vivo", "karaokê", "beer pong", "futmesa" ],
              "natal": ["amigo secreto", "troca de presentes", "filme de natal"],
              "festa junina": ["quadrilha", "touro mecanico", "tiro ao alvo", "corrida de saco", "pescaria"],
              "sao joao": ["quadrilha", "touro mecanico", "tiro ao alvo", "corrida de saco", "pescaria"],
              "são joão": ["quadrilha", "touro mecanico", "tiro ao alvo", "corrida de saco", "pescaria"]
              }

def obter_sugestao(dicionarios_de_sugestoes, tipo_evento):
    opcoes=dicionarios_de_sugestoes.get(tipo_evento.lower(), [])

    if len(opcoes) == 0:
        return "Nenhuma sugestão encontrada para este tipo."
    quantidade= min(2, len(opcoes))
    escolhidos=random.sample(opcoes, quantidade)

    return ", ".join(escolhidos)


def gerar_sugestoes(evento):
    limpar_tela()
    print(f"\n\n\n=== Sugestões para: {evento['nome']} ===")
    
    tipo = evento["tipo"]

    try:
        convidados=int(evento["convidados"])
    except:
        convidados=0

    print(f"Tipo: {tipo} | Convidados: {convidados}")
    
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

    # Sugestão por quantia de convidados: 
    print("\n💡 Dica pelo Número de Convidados:")
    if convidados > 100:
        print("Com mais de 100 convidados, (colocar sugestão).")
    elif convidados > 50:
        print("Para mais de 50 pessoas, (colocar sugestão).")
    elif convidados > 20:
        print("Com mais de 20 pessoas, (colocar sugestão).")
    else:
        print("É um evento pequeno. Foque no conforto e em uma boa conversa.")

def pegar_comida_valores():
    comida_valores = {
        "kibe": 2.5,
        "coxinha": 3.0,
        "pastel": 4.0,
        "mini sanduíche": 5.0,
        "cachorro-quente": 6.0,
        "brigadeiro": 1.5,
        "bem-casado": 2.0,
        "beijinho": 1.5,
        "coqueteis": 15.0,
        "tábua de frios": 25.0,
        "vinhos": 40.0,
        "buffet": 50.0,
        "doces finos": 30.0,
        "ilha de sorvete": 20.0,
        "carne vermelha(maminha, picanha, contra-filé...)": 30.0,
        "pão de alho": 5.0,
        "queijo coalho": 7.0,
        "cerveja": 8.0,
        "refrigerante": 4.0,
        "peru": 60.0,
        "chester": 55.0,
        "lombo": 50.0,
        "bacalhau": 70.0,
        "arroz à grega": 20.0,
        "salpicão": 25.0,
        "panetone": 15.0,
        "pudim": 10.0,
        "pamonha": 6.0,
        "milho cozido": 4.0,
        "milho assado": 5.0,
        "munguzá": 7.0,
        "bolo de milho": 8.0,
        "pé de moleque": 3.0,
        "paçoca": 2.0,
        "canjica": 6.0
    }
    return comida_valores

def pegar_decoracao_valores():
    decoracao_valores = {
        "balões coloridos": 20.0,
        "painel de fotos": 50.0,
        "velas personalizadas": 15.0,
        "chapéus de festa": 10.0,
        "banner temático": 30.0,
        "flores brancas": 100.0,
        "iluminação amarela": 80.0,
        "arranjos de mesa": 60.0,
        "tapete vermelho": 150.0,
        "pisca-pisca": 40.0,
        "árvore de natal": 120.0,
        "guirlanda": 35.0,
        "presépio": 70.0,
        "bandeirinhas": 25.0,
        "fogueira": 100.0,
        "balão de são joão": 30.0,
        "toalha xadrez": 20.0,
        "barracas": 150.0
    }
    return decoracao_valores

def pegar_entretenimento_valores():
    entretenimento_valores = {
        "música (DJ, caixa de som...)": 300.0,
        "pula-pula": 150.0,
        "futsabao": 200.0,
        "maquiagem artistica": 100.0,
        "magico": 250.0,
        "banda ao vivo": 500.0,
        "dj": 350.0,
        "fotografo": 400.0,
        "cabine de fotos": 300.0,
        "karaokê": 150.0,
        "beer pong": 100.0,
        "futmesa": 200.0,
        "amigo secreto": 50.0,
        "troca de presentes": 75.0,
        "filme de natal": 80.0,
        "quadrilha": 250.0,
        "touro mecanico": 300.0,
        "tiro ao alvo": 150.0,
        "corrida de saco": 100.0,
        "pescaria": 120.0
    }
    return entretenimento_valores