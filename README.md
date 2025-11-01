## Como contribuir com o projeto (via Fork)

Eu fiz um mini-tutorial para ajudar vocês a contribuirem com o Git/Github sem bagunçar o repositório principal:

---
###  1. Faça um Fork do projeto
1. Vá até o repositório original:  
    [https://github.com/afreis-dev/organiza-festa](https://github.com/afreis-dev/organiza-festa)
2. Clique no botão **Fork** (canto superior direito da tela).
3. Isso vai criar uma cópia do projeto no **seu perfil** do GitHub.

---

###  2. Clone o seu Fork
No terminal, baixe o projeto para o seu computador:

```bash
git clone https://github.com/SEU_USUARIO/organiza-festa.git
cd organiza-festa
```

---

###  3. Crie uma branch para sua modificação
Cada nova funcionalidade ou correção deve ser feita em uma **branch separada**:

```bash
git checkout -b feature/nome-da-sua-mudanca
```
Exemplo:
```bash
git checkout -b feature/criar-crud-eventos
```

---

###  4. Faça suas alterações
Edite o código, adicione arquivos ou melhore algo no projeto.
Quando terminar, salve e crie um commit:

```bash
git add .
git commit -m "feat: descrição clara da mudança"
```
Exemplo:
```bash
git commit -m "feat: adicionar cálculo de contagem regressiva"
```

---

###  5. Envie suas alterações para o seu Fork
```bash
git push origin feature/nome-da-sua-mudanca
```

---

###  6. Envie um Pull Request
1. Vá até o seu repositório no Github (seu fork)
2. Clique no botão **Compare & pull request**
3. Verifique se está pedindo para mesclar com o repositório original
**(afreis/organiza-festa -> main)**
4. Adicione uma descrição clara do que você fez
5. Clique em **Create Pull Request**

pronto, agora o dono do projeto (Arthur), vai poder revisar e aceitar a contribuição.

---

###  7. Mantenha seu fork atualizado
Depois que o projeto principal receber novas mudanças, atualize o seu fork:

```bash
git remote add upstream https://github.com/afreis-dev/organiza-festa.git
git fetch upstream
git merge upstream/main
git push
```

---

##  Perguntas/Dúvidas Frequentes (FAQ)

###  Git e GitHub

**1. Preciso instalar algo pra usar o Git?**  
sim. baixe e instale o [Git](https://git-scm.com/downloads) no seu computador.  
depois, reinicie o vscode e abra o terminal.

---

**2. Clonei o projeto, mas não vejo nada. O que eu faço?**  
Verifique se entrou na pasta do projeto:  
```bash
cd organiza-festa
```

---

**3. Como faço pra atualizar meu código com o do grupo?**  
use o comando:
```bash
git pull
```
isso baixa as alterações mais recentes do GitHub

---

**4. Fiz um commit, mas ele não aparece no GitHub. Por quê?**  
você precisa enviar as mudanças com:
```bash
git push
```

---

**5. o Git pede senha, mas não aceita.**  
o GitHub não usa mais senha.  
use o **token pessoal** (PAT) ou faça login pelo **VS Code**

---

**6. O que é branch e pra que serve?**  
é uma "versão paralela" do código onde você pode trabalhar sem afetar o código principal.  

Crie uma nova branch com:
```bash
git checkout -b feature/nome-da-branch
```

---

**7. Como eu apago uma branch que não preciso mais?**  
Local:
```bash
git branch -d nome-da-branch
```
Remota (no GitHub):
```bash
git push origin --delete nome-da-branch
```

---

**8. Deu "merge conflict", o que é isso?**  
significa que duas pessoas editaram o mesmo trecho de código.
Abra o arquivo, veja as partes marcadas por ``<<<<<<<`` e escolha qual versão manter.

---

**9. Todos do grupo precisam usar Git?**  
Sim. Cada membro deve fazer commits para mostrar participação individual.

---

**10. Posso só mandar o código pra Arthur subir?**  
pode ué, mas você perde o registro da sua contribuição no histórico do grupo.  
o ideal é aprender a dar commit e push pelo menos uma vez.

---

## Dicas
* use mensagens de commit curtas e descritivas
* sempre atualize o seu fork antes de começar uma nova funcionalidade
* teste seu código antes de enviar o pull request

depois eu termino de fazer o resto do README.md
