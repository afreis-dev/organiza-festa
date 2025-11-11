# api.py — API nativa (sem frameworks) para o Organiza Festa
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json, os

from storage import (
    garantir_arquivos, carregar_eventos, carregar_tarefas,
    salvar_eventos, salvar_tarefas
)

PASTA_PUBLICA = "public"
PORTA = 8000

def formatar_moeda(valor):
    """Converte para 'R$ 0,00'."""
    try:
        return "R$ " + f"{float(valor):.2f}".replace(".", ",")
    except:
        return "R$ 0,00"

def sanear_texto_para_csv(texto):
    """Remove vírgulas e espaços extras para não quebrar o CSV."""
    return (texto or "").replace(",", ";").strip()

class ServidorOrganizaFesta(BaseHTTPRequestHandler):
    def enviar_resposta_json(self, dados, status=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def enviar_arquivo_estatico(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            self.send_error(404); return
        if caminho_arquivo.endswith(".css"):
            mime = "text/css; charset=utf-8"
        elif caminho_arquivo.endswith(".js"):
            mime = "text/javascript; charset=utf-8"
        else:
            mime = "text/html; charset=utf-8"
        with open(caminho_arquivo, "rb") as arquivo:
            conteudo = arquivo.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.end_headers()
        self.wfile.write(conteudo)

    def do_GET(self):
        garantir_arquivos()
        caminho_requisicao = urlparse(self.path).path

        # API: lista de eventos com KPIs (orçamento/gasto/saldo)
        if caminho_requisicao == "/api/eventos":
            lista_eventos = carregar_eventos()
            lista_tarefas = carregar_tarefas()
            resposta = []

            for evento in lista_eventos:
                try:
                    orcamento_total = float(evento["orcamento_total"])
                except:
                    orcamento_total = 0.0

                gasto_total = 0.0
                for tarefa in lista_tarefas:
                    if tarefa["evento_id"] == evento["id"] and tarefa.get("custo"):
                        try:
                            gasto_total += float(tarefa["custo"])
                        except:
                            pass

                saldo = orcamento_total - gasto_total
                resposta.append({
                    "id": evento["id"],
                    "nome": evento["nome"],
                    "tipo": evento["tipo"],
                    "data": evento["data"],
                    "local": evento["local"],
                    "orcamento_total": orcamento_total,
                    "gasto_total": gasto_total,
                    "saldo": saldo,
                    "orcamento_txt": formatar_moeda(orcamento_total),
                    "gasto_txt": formatar_moeda(gasto_total),
                    "saldo_txt": formatar_moeda(saldo),
                })

            self.enviar_resposta_json(resposta); return

        # arquivos estáticos (pasta public/)
        if caminho_requisicao in ("", "/"):
            caminho_requisicao = "/index.html"
        self.enviar_arquivo_estatico(os.path.join(PASTA_PUBLICA, caminho_requisicao.lstrip("/")))

    def do_POST(self):
        garantir_arquivos()
        caminho_requisicao = urlparse(self.path).path
        tamanho_corpo = int(self.headers.get("Content-Length", 0))
        corpo_bruto = self.rfile.read(tamanho_corpo).decode("utf-8")

        # aceitar JSON e form-urlencoded
        if self.headers.get("Content-Type", "").startswith("application/json"):
            try:
                dados_requisicao = json.loads(corpo_bruto)
            except:
                dados_requisicao = {}
        else:
            dados_requisicao = {k: v[0] for k, v in parse_qs(corpo_bruto).items()}

        # criar evento
        if caminho_requisicao == "/api/eventos":
            lista_eventos = carregar_eventos()

            ids_existentes = [int(ev["id"]) for ev in lista_eventos if ev["id"].isdigit()]
            novo_id_evento = str(max(ids_existentes) + 1 if ids_existentes else 1)

            nome_evento = sanear_texto_para_csv(dados_requisicao.get("nome", ""))
            tipo_evento = sanear_texto_para_csv(dados_requisicao.get("tipo", ""))
            data_evento = sanear_texto_para_csv(dados_requisicao.get("data", ""))  # DD/MM/AAAA
            local_evento = sanear_texto_para_csv(dados_requisicao.get("local", ""))

            try:
                orcamento_total = str(float(str(dados_requisicao.get("orcamento_total", "0")).replace(",", ".")))
            except:
                orcamento_total = "0"

            numero_convidados = str(dados_requisicao.get("convidados", "0")).strip()
            if not numero_convidados.isdigit():
                numero_convidados = "0"

            if not nome_evento or not tipo_evento or not data_evento or not local_evento:
                self.enviar_resposta_json({"erro": "Preencha todos os campos obrigatórios."}, status=400); return

            novo_evento = {
                "id": novo_id_evento,
                "nome": nome_evento,
                "tipo": tipo_evento,
                "data": data_evento,
                "local": local_evento,
                "orcamento_total": orcamento_total,
                "convidados": numero_convidados,
            }

            lista_eventos.append(novo_evento)
            salvar_eventos(lista_eventos)
            self.enviar_resposta_json({"ok": True, "mensagem": "Evento criado."}); return

        # criar tarefa
        if caminho_requisicao == "/api/tarefas":
            lista_tarefas = carregar_tarefas()
            lista_eventos = carregar_eventos()

            id_evento = str(dados_requisicao.get("evento_id", "")).strip()
            evento_existe = any(ev["id"] == id_evento for ev in lista_eventos)
            if not evento_existe:
                self.enviar_resposta_json({"erro": "Evento inexistente."}, status=400); return

            ids_tarefas_existentes = [int(t["id"]) for t in lista_tarefas if t["id"].isdigit()]
            novo_id_tarefa = str(max(ids_tarefas_existentes) + 1 if ids_tarefas_existentes else 1)

            descricao_tarefa = sanear_texto_para_csv(dados_requisicao.get("descricao", ""))
            fornecedor_tarefa = sanear_texto_para_csv(dados_requisicao.get("fornecedor", ""))

            try:
                custo_tarefa = float(str(dados_requisicao.get("custo", "0")).replace(",", "."))
            except:
                self.enviar_resposta_json({"erro": "Custo inválido."}, status=400); return

            # orçamento do evento e validação
            try:
                orcamento_evento = float(next(ev["orcamento_total"] for ev in lista_eventos if ev["id"] == id_evento))
            except:
                orcamento_evento = 0.0

            gasto_atual_evento = 0.0
            for tarefa in lista_tarefas:
                if tarefa["evento_id"] == id_evento and tarefa.get("custo"):
                    try:
                        gasto_atual_evento += float(tarefa["custo"])
                    except:
                        pass

            saldo_disponivel = orcamento_evento - gasto_atual_evento
            if custo_tarefa > saldo_disponivel:
                excesso = custo_tarefa - saldo_disponivel
                self.enviar_resposta_json({"erro": f"Custo excede o saldo em {formatar_moeda(excesso)}."}, status=400); return

            nova_tarefa = {
                "id": novo_id_tarefa,
                "evento_id": id_evento,
                "descricao": descricao_tarefa,
                "custo": str(custo_tarefa),
                "status": "pendente",
                "fornecedor": fornecedor_tarefa,
            }

            lista_tarefas.append(nova_tarefa)
            salvar_tarefas(lista_tarefas)
            self.enviar_resposta_json({"ok": True, "mensagem": "Tarefa criada."}); return

        # rota desconhecida
        self.enviar_resposta_json({"erro": "Rota não encontrada."}, status=404)

if __name__ == "__main__":
    garantir_arquivos()
    print(f"🚀 Acesse: http://localhost:{PORTA}")
    HTTPServer(("", PORTA), ServidorOrganizaFesta).serve_forever()