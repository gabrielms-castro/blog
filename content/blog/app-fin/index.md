---
title: Cansei de planilhas: fiz meu próprio app de finanças (e você pode usar também)
tags: python, vibecoding, IA, DIY, tutorial, desenvolvimento, software, finanças
---

# Cansei de planilhas: fiz meu próprio app de finanças (e você pode usar também)

Eu sempre tive problemas para organizar minhas finanças. Não porque eu não saiba como fazer, mas porque, na prática, sempre acabo deixando para a última hora. Na correria do dia a dia são trabalho, estudos, família... Passa o cartão aqui, passa ali e, no fim das contas, você não sabe quanto gastou nem se ainda está dentro do orçamento. "Que compra é essa? Não lembro disso."

Eu sou uma pessoa de papel e caneta. Trabalho com tecnologia, mas anoto tudo. Acho mais prático: anotar minhas ideias e me organizar com uma caneta na mão, fazendo a atividade de forma mecânica, por assim dizer, me ajuda a desacelerar, parar para pensar e até a ser mais criativo.

Todo mês eu fazia minhas finanças assim. Pegava papel e caneta, abria os aplicativos dos bancos, verificava onde e com o que eu tinha gastado, anotava quanto dinheiro tinha entrado, quanto precisava guardar, quais contas tinha que pagar e quanto ficaria disponível para o mês seguinte (levando em conta que eu uso cartão de crédito para tudo e trabalho com um orçamento para o mês que vem).

Minha segunda tentativa foi uma planilha. O problema é que, de novo, eu precisava lembrar de lançar os gastos assim que chegasse em casa, ou separar um dia da semana para isso, se quisesse controlar o orçamento direito e sem aquela dúvida: "será que estourei o orçamento?" (Bom, eu já estourei, e não é legal.)

Sinceramente? Teve mês em que eu sequer abri a planilha. Uma tremenda bagunça.

"Mas, Gabriel, por que você simplesmente não baixa um app para controlar suas finanças?" Eu tentei. Um deles tinha uma ideia bem bacana, com integração ao Open Finance para eu não ter que lançar as compras manualmente, mas era terrivelmente lento. Além disso, até onde eu sei (hoje pode ser diferente), nenhum deles permitia controlar o orçamento considerando compras parceladas, respeitando as parcelas e a data de fechamento do cartão de crédito. Foi aí que pensei: "Quer saber? Vou fazer o meu. Eu faço aplicações para os outros, vou fazer uma para mim. Já tenho tudo na cabeça, inclusive como modelar isso."

Então cá estou eu, escrevendo este tutorial sobre como pegar o app que eu fiz e colocá-lo em produção você mesmo, para uso pessoal.

Mas qual a diferença de baixar um app na store ou ter uma planilha? Bom, primeiro: é de graça. Segundo: Tá na palma da sua mão e é super fácil.

![Dashboard do Fin App](/images/fin-app/dashboard-top.png)

> **O que você vai ter no final:** o Fin App rodando em `https://seuusuario.pythonanywhere.com`, só seu, protegido por login, acessível do computador e do celular. Custo: zero.

---

## O que o app faz

Antes de colocar a mão na massa, um resumo rápido do que você vai ganhar:

- **Lançamentos** em dinheiro, débito, Pix, crédito, boleto ou transferência.
- **Cartões de crédito com faturas de verdade:** você informa o dia de fechamento e o de vencimento, e o app calcula em qual fatura cada compra (e cada parcela) vai cair.
- **Compras parceladas** distribuídas automaticamente nos meses certos.
- **Contas fixas e assinaturas** lançadas sozinhas todo mês (ou todo ano).
- **Orçamento por blocos**, no padrão 50/30/20: Essenciais, Estilo de vida e Prioridades financeiras.
- **Projeção dos próximos 12 meses**, mostrando quanto da sua renda já está comprometida com parcelas e recorrentes.
- **Dívidas e investimentos** com acompanhamento de saldo, metas e rendimentos.

O app é feito em Django + Django REST Framework, com banco SQLite e um frontend em JavaScript puro. Nada de servidor caro: ele roda tranquilamente no plano gratuito do PythonAnywhere.

O roteiro é este:

1. [Criar uma conta no GitHub](#1-criar-uma-conta-no-github)
2. [Criar uma conta no PythonAnywhere](#2-criar-uma-conta-no-pythonanywhere)
3. [Configurar a integração entre as plataformas](#3-configurar-a-integração-entre-as-plataformas)
4. [Fazer o deploy da aplicação](#4-deploy-da-aplicação)
5. [Usar o sistema](#5-usando-o-sistema)

---

## 1. Criar uma conta no GitHub

O GitHub é onde o código do app fica guardado. Você vai criar a sua própria cópia do projeto (um *fork*) para ter controle sobre ela e poder receber as atualizações que eu fizer depois.

1. Acesse [github.com/signup](https://github.com/signup).
2. Informe seu e-mail, crie uma senha e escolha um nome de usuário.
3. Resolva a verificação e confirme o código enviado para o seu e-mail.
4. Recomendo ativar a **autenticação em dois fatores** em *Settings → Password and authentication*. É sua conta, afinal.

![Sign Up do GitHub](/images/fin-app/github-signup.png)

### Fazendo o fork do projeto

Com a conta criada e logado:

1. Acesse o repositório: [github.com/gabrielms-castro/fin-app](https://github.com/gabrielms-castro/fin-app).
2. Clique em **Fork**, no canto superior direito.
3. Mantenha o nome `fin-app` e clique em **Create fork**.

Pronto: agora existe um `https://github.com/SEU_USUARIO/fin-app`, que é seu.

![Sign Up do GitHub](/images/fin-app/github-fork-button.png)

> **Dica:** quando eu publicar melhorias, aparece um botão **Sync fork** na página do seu fork. Um clique e o seu repositório recebe as novidades; no passo 4 eu mostro como levá-las para o servidor.

---

## 2. Criar uma conta no PythonAnywhere

O [PythonAnywhere](https://www.pythonanywhere.com) é um serviço de hospedagem focado em Python. O plano gratuito (*Beginner*) dá direito a um app web no endereço `seuusuario.pythonanywhere.com`, e é isso que vamos usar.

1. Acesse [pythonanywhere.com/pricing](https://www.pythonanywhere.com/pricing/) e clique em **Create a Beginner account**.
2. Escolha um nome de usuário. **Atenção:** ele vira o endereço do seu app (`https://seuusuario.pythonanywhere.com`), então escolha com carinho.
3. Informe e-mail e senha e confirme o e-mail.

![Sign Up do Python Anywhere](/images/fin-app/pythonanywhere-signup.png)

> **Sobre o plano gratuito:** o app fica no ar, mas de tempos em tempos o PythonAnywhere pede que você entre no painel e clique em **Run until 3 months from today**, na aba **Web**, para mantê-lo ativo. Eles mandam um e-mail avisando antes de desativar; só não ignore esse e-mail.

---

## 3. Configurar a integração entre as plataformas

Agora vamos fazer o PythonAnywhere enxergar o seu fork no GitHub. Na prática, isso significa clonar o repositório dentro do servidor e deixá-lo pronto para receber atualizações com um `git pull`.

1. No painel do PythonAnywhere, abra a aba **Consoles** e clique em **Bash**. Um terminal vai abrir no navegador.
2. Clone o seu fork (troque `SEU_USUARIO` pelo seu usuário do **GitHub**):

   ```bash
   git clone https://github.com/SEU_USUARIO/fin-app.git ~/fin-app
   ```
![comando git clone](/images/fin-app/git-clone-command.png)

Output esperado:
![comando git clone - sucesso](/images/fin-app/git-clone-command-sucesso.png)

3. Confirme que deu certo:

```bash
git remote -v

# Resultado esperado:
# origin  https://github.com/SEU_USUARIO/fin-app.git (fetch)
# origin  https://github.com/SEU_USUARIO/fin-app.git (push)
```

Como o fork é público, não é preciso senha nenhuma para clonar e puxar atualizações.


---

## 4. Deploy da aplicação

Hora de colocar no ar. Todos os comandos abaixo rodam no console **Bash** do PythonAnywhere, dentro de `~/fin-app`.

### 4.1. Ambiente virtual e dependências

```bash
cd ~/fin-app
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4.2. Variáveis de ambiente (`.env`)

O app lê as configurações sensíveis de um arquivo `.env`, que **não** vai para o GitHub. Primeiro, gere uma chave secreta:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copie o resultado, crie o `.env` a partir do exemplo e edite:

```bash
cp .env.example .env
nano .env
```

Deixe assim, trocando `seuusuario` pelo seu usuário do **PythonAnywhere** e colando a chave gerada:

```ini
SECRET_KEY=cole-aqui-a-chave-que-voce-gerou
DEBUG=False
ALLOWED_HOSTS=seuusuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://seuusuario.pythonanywhere.com
```

No `nano`, salve com `Ctrl + O`, `Enter` e saia com `Ctrl + X`.
 
> ⚠️ Nunca deixe `DEBUG=True` em produção: com ele ligado, qualquer erro mostra detalhes internos da aplicação para quem estiver acessando.

### 4.3. Banco de dados, usuário e arquivos estáticos

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

O `createsuperuser` vai pedir usuário, e-mail (opcional) e senha. **Esse é o login que você vai usar no app.** Os blocos, naturezas e grupos de gasto padrão são criados automaticamente para o usuário novo.

### 4.4. Criando o app web

1. Vá para a aba **Web** e clique em **Add a new web app**.
2. Clique em **Next** e escolha **Manual configuration** (não escolha "Django"; vamos configurar na mão).
3. Selecione **Python 3.13**, a mesma versão usada no ambiente virtual.

<!-- 📸 Sugestão de imagem: wizard "Add a new web app" com Manual configuration -->

Na página de configuração do app web, ajuste três coisas:

**Virtualenv.** Na seção *Virtualenv*, informe:

```
/home/seuusuario/fin-app/.venv
```

**Arquivo WSGI.** Na seção *Code*, clique no link do *WSGI configuration file* (algo como `/var/www/seuusuario_pythonanywhere_com_wsgi.py`), apague **todo** o conteúdo e coloque:

```python
import os
import sys

path = "/home/seuusuario/fin-app"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Clique em **Save**. Não precisa configurar nada do `.env` aqui: o `settings.py` já carrega esse arquivo sozinho.

**Arquivos estáticos.** Na seção *Static files*, adicione:

| URL        | Directory                               |
|------------|-----------------------------------------|
| `/static/` | `/home/seuusuario/fin-app/staticfiles`  |

Por fim, na seção *Security*, ative **Force HTTPS**.

### 4.5. No ar! 🚀

Role até o topo da aba **Web** e clique no botão verde **Reload**. Acesse `https://seuusuario.pythonanywhere.com` e você deve ver a tela de login:

![Tela de login](/images/fin-app/login.png)

Entre com o usuário que você criou no `createsuperuser`.

> **Deu erro?** Na aba **Web** há links para o *Error log* e o *Server log*. Os problemas mais comuns são: caminho do virtualenv errado, `seuusuario` esquecido no arquivo WSGI ou em `ALLOWED_HOSTS`, ou o `.env` sem a `SECRET_KEY`.

### 4.6. Atualizando depois

Quando houver novidades (lembre-se do **Sync fork** no GitHub), abra o console Bash e rode:

```bash
cd ~/fin-app
source .venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

E clique em **Reload** na aba **Web**.

### 4.7. Backup

Todos os seus dados ficam em um único arquivo: `~/fin-app/db.sqlite3`. De vez em quando, baixe uma cópia pela aba **Files** do PythonAnywhere. Leva dez segundos e evita uma dor de cabeça enorme.

---

## 5. Usando o sistema

Para as imagens abaixo, eu populei o app com dados fictícios de alguns meses. A ordem que eu recomendo no primeiro acesso é esta: **configurações → receitas → cartões → contas fixas e assinaturas → lançamentos**. Depois disso, o dia a dia é só lançar as compras.

### 5.1. Configurações: blocos, naturezas e grupos

O orçamento é dividido em **blocos**, e cada bloco recebe uma fatia da sua entrada. O padrão é a regra 50/30/20:

- **Essenciais (50%)**: o que mantém a vida funcionando (moradia, mercado, transporte, saúde...).
- **Estilo de vida (30%)**: escolhas e prazeres (restaurantes, viagens, assinaturas...). É onde cortar primeiro quando apertar.
- **Prioridades financeiras (20%)**: reserva de emergência, investimentos e quitação de dívidas.

Cada **grupo de gasto** (Mercado, Restaurantes e delivery, Moradia...) pertence a uma **natureza**, e cada natureza aponta para um bloco. Na hora de lançar, você só escolhe o grupo; natureza e bloco vêm automaticamente.

![Configurações](/images/fin-app/config-top.png)

Você pode mudar as porcentagens, criar blocos com valor fixo e criar ou renomear grupos à vontade.

### 5.2. Receitas

Cadastre suas **fontes de receita** (salário, freelas...). A soma delas vira a **entrada esperada** do mês, que é a base do orçamento por bloco. Quando o dinheiro cair, clique em **Recebi** para registrar o recebimento.

![Receitas](/images/fin-app/receitas-top.png)

> Mês atípico? No dashboard, dá para editar a entrada esperada só daquele mês.

### 5.3. Cartões e faturas

Aqui está o motivo de eu ter feito este app. Ao cadastrar um cartão, você informa o **dia de fechamento** e o **dia de vencimento**. A partir disso, o app sabe em qual fatura cada compra cai:

- compra **antes** do fechamento → entra na fatura que fecha neste mês;
- compra **no dia do fechamento ou depois** → vai para a fatura seguinte.

O card ainda mostra o limite usado, o disponível e o "melhor dia de compra".

![Cartões](/images/fin-app/cartoes.png)

Clicando no cartão, você vê a linha do tempo das faturas, inclusive as futuras, já com as parcelas que vão cair nelas. Quando pagar a fatura no banco, marque-a como paga aqui.

![Faturas do cartão](/images/fin-app/fatura.png)

> ⚠️ **Não lance o pagamento da fatura como um gasto.** As compras já foram contadas quando você as lançou; marcar a fatura como paga só dá baixa nas parcelas. Se lançar o pagamento também, o gasto conta em dobro.

### 5.4. Contas fixas e assinaturas

Aluguel, condomínio, energia, internet, plano de saúde... Cadastre uma vez e o app lança sozinho todo mês. Assinaturas (Netflix, Spotify, academia) ficam em uma tela própria, com o total mensal, o total anual e a próxima cobrança, e também aceitam cobrança **anual**.

![Contas fixas](/images/fin-app/recorrentes-top.png)

![Assinaturas](/images/fin-app/assinaturas.png)

### 5.5. Lançamentos

É aqui que você vai passar a maior parte do tempo. Clique em **Novo**, preencha a descrição, o valor, a forma de pagamento e o grupo. Se for no crédito, escolha o cartão e o número de parcelas: o app mostra na hora em qual fatura a compra vai cair e até quando vão as parcelas.

![Novo lançamento parcelado](/images/fin-app/novo-lancamento.png)

Na lista, você filtra por mês, cartão, bloco, grupo e status, vê o que está pago e o que está pendente e pode exportar tudo para CSV.

![Lançamentos](/images/fin-app/lancamentos-top.png)

### 5.6. Dívidas

Empréstimos e financiamentos ficam separados das compras do dia a dia. Você informa o credor, os juros, o número de parcelas e o valor de cada uma, e acompanha o saldo devedor caindo mês a mês.

![Dívidas](/images/fin-app/dividas.png)

### 5.7. Investimentos

Cadastre seus investimentos com meta total e meta de aporte mensal. **Aportes** entram no orçamento do mês (no bloco de Prioridades financeiras); **resgates** e **rendimentos** só mudam o saldo. O botão **Atualizar saldo** é uma mão na roda: você informa o saldo que aparece no banco e o app registra a diferença como rendimento.

![Investimentos](/images/fin-app/investimentos.png)

### 5.8. Dashboard: a visão do mês

Com tudo cadastrado, o dashboard responde à pergunta que me tirava o sono: **"será que estourei o orçamento?"**

- **Entrada esperada, recebido, gasto no mês e saldo previsto** logo no topo.
- **Orçamento por bloco**: quanto foi usado, quanto estava orçado e quanto resta em cada bloco. No exemplo, os Essenciais passaram 4% do orçamento, e o app mostra isso em vermelho, sem dó.
- **Gráficos por natureza e por grupo**, para entender para onde o dinheiro está indo.
- **Projeção de 12 meses**: quanto da renda de cada mês futuro já está comprometido com parcelas e recorrentes. É ótimo para decidir se dá para encarar aquela compra parcelada.
- Resumo das **faturas do mês**, dos **investimentos**, das **assinaturas** e das **dívidas**.

![Dashboard completo](/images/fin-app/dashboard.png)

### 5.9. No celular

O layout é responsivo, com barra de navegação embaixo e um botão **+** para lançar compras rapidinho, na fila do caixa mesmo. Dica: no navegador do celular, use **Adicionar à tela inicial** para abrir o app como se fosse nativo.

<p align="center"><img src="/images/fin-app/mobile.png" alt="Fin App no celular" width="320"></p>

---

## Conclusão

Agora tenho controle real dos meus gastos (ou algo bem próximo disso) por conta da facilidade de usar o app que eu fiz pensado para minhas necessidades e idealização sobre como acho que deveria ser um app desse tipo: orçamento do mês que vem, cartão de crédito com fechamento e vencimento, parcelas no lugar certo e saber como estou no mês atual e seguinte (e também nos anteriores)

Estou pensando em evoluir o app para possuir um MCP nativo onde o usuário consegue autenticar em algum harness como o Claude, uma Abacus ou até mesmo criar seu próprio agente para interagir com o sistema. Imagine só: pelo whatsapp ou telegram enviar um audio ou uma screenshot da notificação de compra e já registrar no seu app? Ou solicitar uma análise sobre como você está no mês corrente. Bão demais.

Se você colocar o seu no ar, me conta como foi! E, se encontrar algum bug ou tiver uma ideia, abra uma *issue* no [repositório](https://github.com/gabrielms-castro/fin-app).
