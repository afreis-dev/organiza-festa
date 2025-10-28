# Organiza Festa

é um aplicativo em Python para organizar eventos de forma simples. O objetivo do projeto é praticar os fundamentos de programação (estruturas de dados básicas, funções, leitura/escrita de arquivos) enquanto a gente usa o Git para colaborar.

## O que já tá feito até agora?
- Cadastro, listagem, edição e exclusão de eventos que estão em `data/eventos.csv`.
- Menu interativo com validação básica de entradas numéricas.
- Separação do código em módulos (`main.py`, `menus.py`, `eventos.py`, `storage.py`, `utils.py`) com comentários explicando cada passo que foi dado.
- Estrutura de pastas criada automaticamente caso ainda não exista.

## Estrutura do projeto
- `main.py`: ponto de entrada. basicamente garante que os arquivos existam e inicia o menu principal.
- `menus.py`: controla o loop do menu e direciona as ações do usuário.
- `eventos.py`: funções para listar, criar, editar e remover eventos.
- `storage.py`: leitura e escrita do arquivo CSV que guarda os eventos.
- `utils.py`: funções auxiliares(helpers) (limpar tela, ler numeros com validacao, pausar a tela).
- `data/`: pasta onde fica o arquivo `eventos.csv`. Criada automaticamente.

## Como preparar o ambiente
1. Garanta que o Python 3 esteja instalado.
2. Clone o repositorio principal (vou te botar como colaborador. a gente não vai usar o fork):
   ```bash
   git clone https://github.com/afreis-dev/organiza-festa.git
   cd organiza-festa
   ```
3. Rode o programa para testar:
   ```bash
   python main.py
   ```

## Como colaborar (sem fork)
1. Aceite o convite de colaborador que eu mandei pra vocês.
2. Antes de comecar uma tarefa, atualize seu repositorio local:
   ```bash
   git checkout main
   git pull origin main
   ```
3. Crie uma branch descritiva para a sua tarefa:
   ```bash
   git checkout -b feature/nome-da-tarefa
   ```
4. Implemente as mudanças e veja se ta rodando de boa localmente (por exemplo, executando `python main.py`).  
5. Veja o que mudou:
   ```bash
   git status
   ```
6. Adicione os arquivos relevantes e crie um commit:
   ```bash
   git add caminho/do/arquivo.py
   git commit -m "feat: descricao objetiva da mudanca"
   ```
7. Envie a branch para o repositorio principal:
   ```bash
   git push origin feature/nome-da-tarefa
   ```
8. Abra um Pull Request apontando sua branch para `main`, descrevendo o que foi feito.
9. Aguarde revisao e, quando aprovado, faça merge (Arthur ou outra pessoa vai fazer).
10. Depois do merge, volte para a `main`, puxe as novidades e remova a branch local se quiser:
    ```bash
    git checkout main
    git pull origin main
    git branch -d feature/nome-da-tarefa
    git push origin --delete feature/nome-da-tarefa
    ```

## Comandos Git e para que servem
- `git clone URL`: baixa o repositorio remoto para o seu computador.
- `git status`: mostra arquivos modificados, novos e prontos para commit.
- `git checkout main`: troca para a branch principal local.
- `git pull origin main`: traz as atualizações da branch `main` remota e aplica na sua cópia local.
- `git checkout -b nova-branch`: cria uma branch e muda para ela.
- `git add arquivo`: prepara o arquivo para entrar no proximo commit.
- `git add .`: adiciona todas as mudanças do diretório atual (use com atenção pra nao dar errado).
- `git commit -m "mensagem"`: registra as mudancas marcadas com uma mensagem descritiva.
- `git log --oneline`: lista o historico de commits de forma resumida.
- `git push origin nome-da-branch`: envia a branch local para o repositório remoto.
- `git branch`: lista as branches locais.
- `git branch -d nome-da-branch`: remove uma branch local que ja foi mesclada.
- `git push origin --delete nome-da-branch`: apaga a branch no GitHub.
- `git diff`: mostra as diferenças entre o estado atual e o último commit.
- `git merge origem`: combina a branch informada com a branch atual (normalmente usado pela pessoa que revisa).

## FAQ (perguntas frequentes)
**Preciso de token ou senha ao usar `git push`?**  
Sim, o GitHub nao aceita senha simples. Use um token pessoal (PAT) ou configure login pelo VS Code/Git Credential Manager.

**Com quais arquivos devo me preocupar ao commitar?**  
Inclua apenas os arquivos que voce alterou e que fazem parte da solucao. Use `git status` antes de cada commit para conferir.

**O que fazer se o comando `git push` falhar dizendo que minha branch esta atrasada?**  
Execute `git pull origin main`, resolva possiveis conflitos, crie um novo commit com os ajustes e tente enviar novamente.

**Como resolver conflitos de merge?**  
Abra os arquivos marcados com `<<<<<<<` e escolha a versao correta. Depois remova os marcadores, salve e finalize com `git add` e `git commit`.

**Posso editar direto na branch main?**  
Evite. Trabalhe sempre em uma branch de funcionalidade para manter o historico organizado e facilitar a revisao.

**Como saber no que trabalhar?**  
Verifique as issues abertas ou manda mensagem no grupo ou no canal do discord para alinhar prioridades antes de criar uma branch.

**Encontrei um bug mas nao sei como corrigir agora. O que fazer?**  
Crie uma issue descrevendo o problema ou mande no discord ou no wpp para que alguem assuma o B.O.

**Esqueci de criar a branch antes de comecar. E agora?**  
Crie a branch depois (`git checkout -b feature/minha-tarefa`) e continue nela. Isso automaticamente leva seus arquivos modificados.

---

Se tiver duvidas novas, adicione-as aqui ou mande pra Arthur pra gente manter o README sempre atualizado.