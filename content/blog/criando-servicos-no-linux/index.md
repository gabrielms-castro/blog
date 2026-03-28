---
title: Criando Serviços no Linux com systemd
tags: linux, systemd, devops, segurança
---

# Criando Serviços no Linux com systemd

O systemd é o sistema de init padrão na grande maioria das distribuições Linux modernas — Debian, Ubuntu, Fedora, Arch, RHEL e derivados. Ele é responsável por inicializar o sistema, gerenciar processos e, o que mais interessa aqui, controlar serviços que precisam rodar em background.

Neste artigo você vai aprender a instalar um binário corretamente, criar um usuário dedicado sem privilégios desnecessários, definir um arquivo `.service` e gerenciar o ciclo de vida do serviço com `systemctl` e `journalctl`.

## Preparando o ambiente

O cenário mais comum ao instalar um serviço de terceiros é: baixar o binário, colocá-lo no lugar certo e dar as permissões adequadas. A convenção no Linux é usar `/opt` para softwares que não pertencem ao gerenciador de pacotes da distro.

Baixe o binário em `/tmp` — é um diretório temporário, ideal para downloads que ainda serão processados:

```bash
wget -O /tmp/meu-servico https://exemplo.com/releases/meu-servico-linux-amd64
```

ou com `curl`:

```bash
curl -L -o /tmp/meu-servico https://exemplo.com/releases/meu-servico-linux-amd64
```

Crie o diretório em `/opt` e mova o binário para lá:

```bash
sudo mkdir -p /opt/meu-servico
sudo mv /tmp/meu-servico /opt/meu-servico/meu-servico
```

Torne o binário executável:

```bash
sudo chmod +x /opt/meu-servico/meu-servico
```

## Criando um usuário de sistema

Rodar um serviço como `root` é um erro clássico. Se o processo for comprometido, o atacante tem controle total da máquina. O princípio do menor privilégio diz: dê ao processo apenas o acesso que ele precisa para funcionar.

Para isso, crie um usuário de sistema dedicado ao serviço. Esse usuário não terá home directory, não poderá fazer login interativo e não aparecerá como um usuário comum no sistema:

```bash
sudo useradd \
  --system \
  --no-create-home \
  --shell /usr/sbin/nologin \
  meu-servico
```

- `--system`: cria um usuário de sistema com UID baixo (abaixo de 1000), sem grupo primário separado por padrão
- `--no-create-home`: não cria `/home/meu-servico`
- `--shell /usr/sbin/nologin`: impede qualquer tentativa de login interativo com esse usuário

Agora transfira a propriedade dos arquivos do serviço para esse usuário:

```bash
sudo chown -R meu-servico:meu-servico /opt/meu-servico
```

## Criando o arquivo .service

Os arquivos de unit do systemd ficam em `/etc/systemd/system/`. Crie o arquivo do seu serviço:

```bash
sudo nano /etc/systemd/system/meu-servico.service
```

Conteúdo do arquivo:

```ini
[Unit]
Description=Meu Servico de Exemplo
Documentation=https://exemplo.com/docs
After=network.target

[Service]
Type=simple
User=meu-servico
Group=meu-servico
ExecStart=/opt/meu-servico/meu-servico
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Entendendo as diretivas principais:

`[Unit]`

- `After=network.target`: garante que o serviço só inicia após a rede estar disponível

`[Service]`

- `Type=simple`: o processo iniciado pelo `ExecStart` é o processo principal (padrão para a maioria dos casos)
- `User` e `Group`: define sob qual usuário e grupo o processo roda — aqui entra o usuário que criamos
- `ExecStart`: caminho absoluto para o binário e seus argumentos
- `Restart=on-failure`: reinicia automaticamente se o processo encerrar com código de erro
- `RestartSec=5s`: aguarda 5 segundos antes de tentar reiniciar

`[Install]`

- `WantedBy=multi-user.target`: o serviço é iniciado no runlevel multiusuário (equivalente ao modo normal de operação)

## Gerenciando o serviço

Após criar ou modificar qualquer arquivo `.service`, você precisa informar ao systemd que houve mudanças:

```bash
sudo systemctl daemon-reload
```

Habilite o serviço para iniciar automaticamente no boot e inicie-o imediatamente:

```bash
sudo systemctl enable --now meu-servico
```

Os comandos do dia a dia:

```bash
# Iniciar
sudo systemctl start meu-servico

# Parar
sudo systemctl stop meu-servico

# Reiniciar
sudo systemctl restart meu-servico

# Ver status atual
sudo systemctl status meu-servico
```

O `status` mostra se o serviço está ativo, o PID, quando foi iniciado e as últimas linhas de log — útil para diagnóstico rápido.

Para verificar se o serviço está habilitado para iniciar no boot:

```bash
systemctl is-enabled meu-servico
```

## Consultando logs com journalctl

O systemd centraliza todos os logs no `journald`. Para ver os logs do seu serviço:

```bash
sudo journalctl -u meu-servico
```

Seguir os logs em tempo real (equivalente ao `tail -f`):

```bash
sudo journalctl -u meu-servico -f
```

Ver apenas logs da última hora:

```bash
sudo journalctl -u meu-servico --since "1 hour ago"
```

Filtrar por intervalo de tempo:

```bash
sudo journalctl -u meu-servico --since "2026-03-28 10:00:00" --until "2026-03-28 11:00:00"
```

Ver apenas as últimas N linhas:

```bash
sudo journalctl -u meu-servico -n 50
```

Os logs do journald persistem entre reinicializações por padrão nas distros modernas, então você consegue investigar o que aconteceu antes de um crash.

## Recapitulando

O fluxo completo para subir um serviço de forma segura no Linux:

1. Baixar o binário em `/tmp`
2. Mover para `/opt/nome-do-servico/` e tornar executável
3. Criar usuário de sistema com `useradd --system --no-create-home --shell /usr/sbin/nologin`
4. Transferir propriedade com `chown`
5. Criar o arquivo `.service` em `/etc/systemd/system/`
6. Executar `systemctl daemon-reload`
7. Habilitar e iniciar com `systemctl enable --now`
8. Monitorar com `journalctl -u nome -f`

Seguindo esse fluxo, o serviço roda com o mínimo de privilégios necessários, reinicia sozinho em caso de falha e seus logs ficam centralizados no journal do sistema.
