def tarefas():
    
    print("\n--- Tarefas e do Evento ---")
    decoracao = input("Decoração do evento: ").strip()
    buffet = input("Buffet: ").strip()
    musica_evento = input("Música do evento: ").strip()
    return decoracao, buffet, musica_evento
    """ pode ter mais opçoes """
    

def custo_tarefas():
    custo_decoracao = float(input("Custo da decoração:"))    
    custo_buffet = float(input("Custo do buffet:"))
    custo_musica_evento = float(input("Custo da música do evento:"))
    custo_total_tarefas = custo_decoracao + custo_buffet + custo_musica_evento 
    """valor que será descontado do orçamento total do evento"""
    return custo_total_tarefas
    """ pode ter mais opçoes """

""""descontar custos do orçamento total do evento"""

def descontar_custos_orcamento_total(custo_total_evento, custo_total_tarefas):
    orcamento_final_evento = custo_total_evento - custo_total_tarefas 
    """valor atual do orçamento do evento"""
    return orcamento_final_evento