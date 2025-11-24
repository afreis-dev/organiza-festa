# Manual do Usuário - Organiza Festa

## Visão geral
O Organiza Festa permite planejar eventos e controlar tarefas usando arquivos CSV. A aplicação funciona tanto via terminal (arquivo `main.py`) quanto pela interface web em Flask (arquivo `app.py`). Ambos os modos compartilham a mesma base de dados na pasta `data/`.

## Pré-requisitos
- Python 3 instalado.
- Permissão de escrita na pasta do projeto para gravar os arquivos CSV em `data/`.

## Como iniciar a aplicação
### Versão web (Flask)
1. Instale dependências padrão do Flask (caso não tenha):
   ```bash
   pip install flask
   ```
2. Inicie o servidor:
   ```bash
   python app.py
   ```
3. Acesse no navegador: `http://localhost:5000`.

### Versão para terminal
1. Execute:
   ```bash
   python main.py
   ```
2. Navegue pelos menus para gerenciar eventos e tarefas pelo console.

## Usando a versão web
### Criar um novo evento
1. Na página inicial, preencha Nome, Tipo, Data (DD/MM/AAAA), Local, Orçamento total e número de Convidados.
2. Clique em **Criar evento**. O sistema gera um ID automaticamente e leva você para a página de detalhes.

### Visualizar detalhes do evento
- A página `/evento/<id>` mostra contagem de dias, orçamento total, gasto acumulado, saldo, percentual de uso e quantidade de tarefas feitas/pendentes.
- Há uma lista com todas as tarefas vinculadas ao evento.

### Adicionar tarefa
1. No formulário de **Nova tarefa**, informe Descrição, Custo total e, opcionalmente, o Fornecedor.
2. Clique em **Adicionar tarefa** para salvar. O custo entra automaticamente no cálculo do gasto e do saldo do evento.

### Concluir ou remover tarefa
- Use **Marcar feita** para definir o status como feito.
- Use **Excluir** para remover a tarefa definitivamente do CSV.

### Excluir evento
- O botão **Excluir evento** remove o evento e todas as tarefas associadas.

## Usando a versão em terminal
1. Abra o menu principal pelo `main.py`.
2. Selecione as opções para cadastrar, listar, editar ou excluir eventos.
3. Dentro de um evento, acesse o menu de tarefas para criar, editar, marcar como feita ou excluir tarefas.

## Estrutura dos dados
- `data/eventos.csv`: armazena eventos com colunas `id,nome,tipo,data,local,orcamento_total,convidados`.
- `data/tarefas.csv`: armazena tarefas com colunas `id,evento_id,descricao,quantidade,custo,status,fornecedor`.

## Restrições e observações
- Campos de data devem estar no formato `DD/MM/AAAA`.
- Valores monetários são salvos como número decimal simples no CSV (ponto ou vírgula são aceitos na interface web).
- Caracteres de vírgula nos textos são substituídos por `;` para não quebrar o formato dos arquivos CSV.
- Os arquivos CSV são criados automaticamente se não existirem, mas é necessário ter permissão de gravação na pasta do projeto.

## Suporte
Se encontrar problemas ou desejar novas funcionalidades, registre uma issue no repositório ou entre em contato com a equipe responsável.
