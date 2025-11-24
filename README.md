# Organiza Festa

Organiza Festa é um organizador simples para planejar eventos, controlar tarefas e acompanhar orçamento direto pelo terminal ou pelo navegador.

## Como iniciar

### Modo terminal
1. Garanta que o Python 3 está instalado.
2. No diretório do projeto, execute:
   ```bash
   python main.py
   ```
3. O menu principal aparece no terminal com todas as opções de eventos e tarefas.

### Modo web (Flask)
1. Instale as dependências:
   ```bash
   pip install flask
   ```
   2. Inicie o servidor web:
   ```bash
   python app.py
   ```
3. Abra o navegador em `http://localhost:5000` para usar o painel visual.

## Usando o menu principal (terminal)
- **Listar eventos**: mostra todos os eventos cadastrados com data e situação (faltam X dias, é hoje ou já passou).
- **Criar evento**: registra nome, tipo, data (DD/MM/AAAA), local, orçamento e número de convidados.
- **Editar evento**: atualiza qualquer campo do evento escolhido.
- **Excluir evento**: remove o evento e também apaga as tarefas ligadas a ele.
- **Gerenciar tarefas de um evento**: abre o menu de tarefas para o evento selecionado.
- **Detalhar evento (resumo completo)**: mostra orçamento, gastos, saldo, progresso das tarefas e sugestões personalizadas.

## Gerenciando tarefas
- **Criar tarefa**: informe descrição, quantidade, preço unitário e fornecedor opcional. O custo total impacta o orçamento do evento.
- **Editar tarefa**: ajuste descrição, quantidade, preço, status ou fornecedor.
- **Excluir tarefa**: remove a tarefa e devolve o valor ao saldo disponível.
- **Marcar tarefa como feita**: muda o status para "feito" para acompanhar o progresso.

## Controle de orçamento
- Cada evento tem um orçamento total.
- A soma dos custos das tarefas gera o **gasto total**.
- O **saldo** é calculado automaticamente (orçamento total - gasto total).
- O painel mostra o **percentual do orçamento usado** e alerta quando o saldo fica negativo.

## Sugestões personalizadas
- Cada evento recebe dicas com base no tipo (aniversário, casamento, churrasco, reunião, etc.) e na quantidade de convidados (porte pequeno, médio ou grande).
- As sugestões aparecem no detalhamento do evento (terminal) e na página de detalhes do evento (web).

## Restrições e observações
- Funciona no terminal ou em um navegador local via Flask.
- Datas devem estar no formato **DD/MM/AAAA**.
- Os dados ficam salvos em arquivos CSV dentro da pasta `data/` (`eventos.csv` e `tarefas.csv`).
- Não há login ou controle de usuários; qualquer pessoa com acesso aos arquivos pode ver/editar os dados.
- Orçamentos e custos são números simples; não há controle de moedas diferentes nem arredondamento avançado.
- O sistema não valida conflitos de agenda entre eventos.