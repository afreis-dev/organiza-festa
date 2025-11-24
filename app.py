from flask import Flask, render_template, request, redirect, url_for, flash

import eventos
import storage
import tarefas
import utils

app = Flask(__name__)
app.secret_key = "organiza-festa-web"

storage.garantir_arquivos()


def carregar_dados():
    """Carrega listas atualizadas de eventos e tarefas do CSV."""
    lista_eventos = storage.carregar_eventos()
    lista_tarefas = storage.carregar_tarefas()
    return lista_eventos, lista_tarefas


@app.context_processor
def helpers_template():
    """Disponibiliza funcoes uteis nos templates."""
    return {
        "formatar_moeda": utils.formatar_moeda,
        "descricao_contagem": utils.descricao_contagem,
        "preco_unitario_tarefa": tarefas.calcular_preco_unitario_da_tarefa,
    }


@app.route("/")
def index():
    eventos_cadastrados, _ = carregar_dados()
    eventos_ordenados = sorted(eventos_cadastrados, key=lambda e: int(e.get("id", "0")))
    return render_template("index.html", eventos=eventos_ordenados)


@app.post("/evento/novo")
def criar_evento_web():
    eventos_cadastrados, _ = carregar_dados()

    nome = request.form.get("nome", "").strip().replace(",", ";")
    tipo = request.form.get("tipo", "").strip().replace(",", ";")
    data = request.form.get("data", "").strip()
    local = request.form.get("local", "").strip().replace(",", ";")
    orcamento_texto = request.form.get("orcamento_total", "0").strip().replace(",", ".")
    convidados_texto = request.form.get("convidados", "0").strip()

    if not nome or not tipo or not data or not local:
        flash("Preencha todos os campos obrigatorios do evento.", "erro")
        return redirect(url_for("index"))

    if not utils.validar_data(data):
        flash("Data invalida. Use o formato DD/MM/AAAA.", "erro")
        return redirect(url_for("index"))

    try:
        orcamento_total = float(orcamento_texto)
    except Exception:
        orcamento_total = 0.0

    if convidados_texto.isdigit():
        convidados = convidados_texto
    else:
        convidados = "0"

    novo_evento = {
        "id": eventos.gerar_novo_id(eventos_cadastrados),
        "nome": nome,
        "tipo": tipo,
        "data": data,
        "local": local,
        "orcamento_total": str(orcamento_total),
        "convidados": convidados,
    }

    eventos_cadastrados.append(novo_evento)
    storage.salvar_eventos(eventos_cadastrados)
    flash("Evento criado com sucesso!", "sucesso")
    return redirect(url_for("index"))


@app.route("/evento/<id_evento>")
def detalhes_evento(id_evento):
    eventos_cadastrados, tarefas_cadastradas = carregar_dados()
    evento = eventos.encontrar_evento_por_id(eventos_cadastrados, id_evento)

    if evento is None:
        flash("Evento nao encontrado.", "erro")
        return redirect(url_for("index"))

    try:
        orcamento_total = float(evento.get("orcamento_total", 0))
    except Exception:
        orcamento_total = 0.0

    gasto_total = tarefas.total_gasto_no_evento(tarefas_cadastradas, id_evento)
    saldo = orcamento_total - gasto_total
    percentual_gasto = (gasto_total / orcamento_total * 100) if orcamento_total > 0 else 0
    pendentes, feitas = eventos.contar_tarefas_do_evento(tarefas_cadastradas, id_evento)
    tarefas_do_evento = [t for t in tarefas_cadastradas if t["evento_id"] == id_evento]
    tarefas_do_evento = sorted(tarefas_do_evento, key=lambda t: int(t.get("id", "0")))
    sugestoes = eventos.sugerir_para_evento(evento)

    return render_template(
        "evento.html",
        evento=evento,
        contagem=utils.descricao_contagem(evento.get("data", "")),
        orcamento_total=orcamento_total,
        gasto_total=gasto_total,
        saldo=saldo,
        percentual_gasto=percentual_gasto,
        pendentes=pendentes,
        feitas=feitas,
        tarefas_do_evento=tarefas_do_evento,
        sugestoes=sugestoes,
    )


@app.post("/evento/<id_evento>/tarefas/nova")
def criar_tarefa_web(id_evento):
    eventos_cadastrados, tarefas_cadastradas = carregar_dados()
    evento = eventos.encontrar_evento_por_id(eventos_cadastrados, id_evento)
    if evento is None:
        flash("Evento nao encontrado.", "erro")
        return redirect(url_for("index"))

    descricao = request.form.get("descricao", "").strip()
    quantidade_texto = request.form.get("quantidade", "1").strip()
    preco_unitario_texto = request.form.get("preco_unitario", "0").strip().replace(",", ".")
    fornecedor = request.form.get("fornecedor", "").strip()

    if not descricao:
        flash("A descricao da tarefa nao pode ficar vazia.", "erro")
        return redirect(url_for("detalhes_evento", id_evento=id_evento))

    try:
        quantidade = int(quantidade_texto)
    except Exception:
        quantidade = 1

    if quantidade <= 0:
        quantidade = 1

    try:
        preco_unitario = float(preco_unitario_texto)
    except Exception:
        preco_unitario = 0.0

    custo_total = quantidade * preco_unitario

    nova_tarefa = {
        "id": tarefas.gerar_novo_id_tarefa(tarefas_cadastradas),
        "evento_id": id_evento,
        "descricao": descricao.replace(",", ";"),
        "quantidade": str(quantidade),
        "custo": str(custo_total),
        "status": "pendente",
        "fornecedor": fornecedor.replace(",", ";"),
    }

    tarefas_cadastradas.append(nova_tarefa)
    storage.salvar_tarefas(tarefas_cadastradas)
    flash("Tarefa adicionada com sucesso!", "sucesso")
    return redirect(url_for("detalhes_evento", id_evento=id_evento))


@app.post("/evento/<id_evento>/tarefas/<id_tarefa>/fazer")
def marcar_tarefa_feita_web(id_evento, id_tarefa):
    eventos_cadastrados, tarefas_cadastradas = carregar_dados()
    tarefa = tarefas.encontrar_tarefa_por_id(tarefas_cadastradas, id_evento, id_tarefa)
    if tarefa is None:
        flash("Tarefa nao encontrada.", "erro")
        return redirect(url_for("detalhes_evento", id_evento=id_evento))

    tarefa["status"] = "feito"
    storage.salvar_tarefas(tarefas_cadastradas)
    flash("Tarefa marcada como feita!", "sucesso")
    return redirect(url_for("detalhes_evento", id_evento=id_evento))


@app.post("/evento/<id_evento>/tarefas/<id_tarefa>/excluir")
def excluir_tarefa_web(id_evento, id_tarefa):
    eventos_cadastrados, tarefas_cadastradas = carregar_dados()
    nova_lista = []
    removida = False
    for tarefa in tarefas_cadastradas:
        if tarefa["evento_id"] == id_evento and tarefa["id"] == id_tarefa:
            removida = True
            continue
        nova_lista.append(tarefa)

    if removida:
        storage.salvar_tarefas(nova_lista)
        flash("Tarefa removida.", "sucesso")
    else:
        flash("Tarefa nao encontrada.", "erro")

    return redirect(url_for("detalhes_evento", id_evento=id_evento))


@app.post("/evento/<id_evento>/excluir")
def excluir_evento_web(id_evento):
    eventos_cadastrados, tarefas_cadastradas = carregar_dados()
    nova_lista_eventos = []
    encontrado = False

    for evento in eventos_cadastrados:
        if evento["id"] == id_evento:
            encontrado = True
        else:
            nova_lista_eventos.append(evento)

    if encontrado:
        storage.salvar_eventos(nova_lista_eventos)
        tarefas_restantes = [t for t in tarefas_cadastradas if t["evento_id"] != id_evento]
        storage.salvar_tarefas(tarefas_restantes)
        flash("Evento e tarefas relacionadas removidos.", "sucesso")
    else:
        flash("Evento nao encontrado.", "erro")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)