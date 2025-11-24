"""Aplicacao web Flask para o Organiza Festa reaproveitando a camada de negocio existente."""

from flask import Flask, render_template, request, redirect, url_for, flash

import eventos
import storage
import tarefas
import utils

app = Flask(__name__)
app.secret_key = "organiza-festa-web"


# Garante que a estrutura minima exista antes de usar
storage.garantir_arquivos()


def sanitizar_para_csv(texto):
    """Remove virgulas para evitar quebra de formato no CSV."""
    return texto.replace(",", ";") if isinstance(texto, str) else texto


def obter_evento_ou_404(eventos_lista, id_evento):
    evento = eventos.encontrar_evento_por_id(eventos_lista, id_evento)
    if evento is None:
        return None
    return evento


def calcular_resumo_evento(evento, lista_de_tarefas):
    try:
        orcamento_total = float(evento.get("orcamento_total", 0))
    except Exception:
        orcamento_total = 0.0

    gasto_total = tarefas.total_gasto_no_evento(lista_de_tarefas, evento["id"])
    saldo = orcamento_total - gasto_total
    percentual_gasto = (gasto_total / orcamento_total * 100) if orcamento_total > 0 else 0.0
    pendentes, feitas = eventos.contar_tarefas_do_evento(lista_de_tarefas, evento["id"])

    return {
        "orcamento_total": orcamento_total,
        "gasto_total": gasto_total,
        "saldo": saldo,
        "percentual_gasto": percentual_gasto,
        "pendentes": pendentes,
        "feitas": feitas,
        "contagem_texto": utils.descricao_contagem(evento["data"]),
    }


@app.route("/")
def index():
    lista_de_eventos = storage.carregar_eventos()
    lista_de_tarefas = storage.carregar_tarefas()

    eventos_enriquecidos = []
    for evento_atual in lista_de_eventos:
        resumo = calcular_resumo_evento(evento_atual, lista_de_tarefas)
        eventos_enriquecidos.append({"dados": evento_atual, "resumo": resumo})

    return render_template(
        "index.html",
        eventos=eventos_enriquecidos,
        formatar_moeda=utils.formatar_moeda,
    )


@app.route("/evento/novo", methods=["POST"])
def criar_evento():
    lista_de_eventos = storage.carregar_eventos()

    nome = request.form.get("nome", "").strip()
    tipo = request.form.get("tipo", "").strip()
    data = request.form.get("data", "").strip()
    local = request.form.get("local", "").strip()
    orcamento = request.form.get("orcamento", "0").replace(",", ".").strip()
    convidados = request.form.get("convidados", "0").strip()

    if not nome or not tipo or not data or not local:
        flash("Preencha todos os campos obrigatórios.")
        return redirect(url_for("index"))

    if not utils.validar_data(data):
        flash("Data inválida. Use o formato DD/MM/AAAA.")
        return redirect(url_for("index"))

    try:
        orcamento_total = float(orcamento)
    except Exception:
        orcamento_total = 0.0

    try:
        numero_convidados = int(convidados)
    except Exception:
        numero_convidados = 0

    novo_evento = {
        "id": eventos.gerar_novo_id(lista_de_eventos),
        "nome": sanitizar_para_csv(nome),
        "tipo": sanitizar_para_csv(tipo),
        "data": data,
        "local": sanitizar_para_csv(local),
        "orcamento_total": str(orcamento_total),
        "convidados": str(numero_convidados),
    }

    lista_de_eventos.append(novo_evento)
    storage.salvar_eventos(lista_de_eventos)
    flash("Evento criado com sucesso!")
    return redirect(url_for("detalhar_evento", id_evento=novo_evento["id"]))


@app.route("/evento/<id_evento>")
def detalhar_evento(id_evento):
    lista_de_eventos = storage.carregar_eventos()
    lista_de_tarefas = storage.carregar_tarefas()

    evento = obter_evento_ou_404(lista_de_eventos, id_evento)
    if evento is None:
        flash("Evento não encontrado.")
        return redirect(url_for("index"))

    resumo = calcular_resumo_evento(evento, lista_de_tarefas)

    tarefas_do_evento = []
    for tarefa_atual in lista_de_tarefas:
        if tarefa_atual["evento_id"] == id_evento:
            quantidade = tarefas.obter_quantidade_da_tarefa(tarefa_atual)
            valor_unitario = tarefas.calcular_preco_unitario_da_tarefa(tarefa_atual)
            tarefas_do_evento.append(
                {
                    "dados": tarefa_atual,
                    "quantidade": quantidade,
                    "valor_unitario": valor_unitario,
                }
            )

    sugestoes = eventos.sugerir_para_evento(evento)

    return render_template(
        "evento.html",
        evento=evento,
        resumo=resumo,
        tarefas=tarefas_do_evento,
        sugestoes=sugestoes,
        formatar_moeda=utils.formatar_moeda,
    )


@app.route("/evento/<id_evento>/tarefas/nova", methods=["POST"])
def criar_tarefa(id_evento):
    lista_de_tarefas = storage.carregar_tarefas()
    lista_de_eventos = storage.carregar_eventos()

    evento = obter_evento_ou_404(lista_de_eventos, id_evento)
    if evento is None:
        flash("Evento não encontrado.")
        return redirect(url_for("index"))

    descricao = request.form.get("descricao", "").strip()
    custo_total_texto = request.form.get("custo", "0").replace(",", ".").strip()
    fornecedor = request.form.get("fornecedor", "").strip()

    if descricao == "":
        flash("A descrição da tarefa não pode ficar vazia.")
        return redirect(url_for("detalhar_evento", id_evento=id_evento))

    try:
        custo_total = float(custo_total_texto)
    except Exception:
        custo_total = 0.0

    nova_tarefa = {
        "id": tarefas.gerar_novo_id_tarefa(lista_de_tarefas),
        "evento_id": id_evento,
        "descricao": sanitizar_para_csv(descricao),
        "quantidade": "1",
        "custo": str(custo_total),
        "status": "pendente",
        "fornecedor": sanitizar_para_csv(fornecedor),
    }

    lista_de_tarefas.append(nova_tarefa)
    storage.salvar_tarefas(lista_de_tarefas)
    flash("Tarefa criada com sucesso!")
    return redirect(url_for("detalhar_evento", id_evento=id_evento))


@app.route("/evento/<id_evento>/tarefas/<id_tarefa>/feito", methods=["POST"])
def marcar_tarefa_feita(id_evento, id_tarefa):
    lista_de_tarefas = storage.carregar_tarefas()
    alterado = False

    for tarefa_atual in lista_de_tarefas:
        if tarefa_atual["evento_id"] == id_evento and tarefa_atual["id"] == id_tarefa:
            tarefa_atual["status"] = "feito"
            alterado = True
            break

    if alterado:
        storage.salvar_tarefas(lista_de_tarefas)
        flash("Tarefa marcada como feita!")
    else:
        flash("Tarefa não encontrada.")

    return redirect(url_for("detalhar_evento", id_evento=id_evento))


@app.route("/evento/<id_evento>/tarefas/<id_tarefa>/excluir", methods=["POST"])
def excluir_tarefa(id_evento, id_tarefa):
    lista_de_tarefas = storage.carregar_tarefas()
    nova_lista = []
    removido = False

    for tarefa_atual in lista_de_tarefas:
        if tarefa_atual["evento_id"] == id_evento and tarefa_atual["id"] == id_tarefa:
            removido = True
            continue
        nova_lista.append(tarefa_atual)

    if removido:
        storage.salvar_tarefas(nova_lista)
        flash("Tarefa removida.")
    else:
        flash("Tarefa não encontrada.")

    return redirect(url_for("detalhar_evento", id_evento=id_evento))


@app.route("/evento/<id_evento>/excluir", methods=["POST"])
def excluir_evento(id_evento):
    lista_de_eventos = storage.carregar_eventos()
    nova_lista = []
    removido = False

    for evento_atual in lista_de_eventos:
        if evento_atual["id"] == id_evento:
            removido = True
            continue
        nova_lista.append(evento_atual)

    if removido:
        storage.salvar_eventos(nova_lista)
        eventos.remover_tarefas_relacionadas(id_evento)
        flash("Evento excluído com sucesso.")
    else:
        flash("Evento não encontrado.")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
