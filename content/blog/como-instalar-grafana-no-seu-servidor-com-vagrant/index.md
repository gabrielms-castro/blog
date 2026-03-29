---
title: Como Instalar o Grafana no seu Servidor com Vagrant
tags: linux, devops, grafana, observabilidade, vagrant
---

# Como Instalar o Grafana no seu Servidor com Vagrant

O **Grafana** é uma plataforma indispensável para quem precisa monitorar e visualizar dados em tempo real. Com ele, você pode analisar métricas de recursos computacionais, bancos de dados e muito mais, tudo através de dashboards intuitivos.

Recentemente, precisei colocar um servidor Grafana em produção para observar as métricas da nossa infraestrutura. Passamos por um incidente crítico onde a aplicação principal travou porque a CPU do servidor atingiu o limite máximo e não tínhamos visibilidade disso. Aprendemos a lição e decidimos implementar a cultura de **observabilidade** para que isso não aconteça novamente. Com o Grafana, configuramos alertas específicos e melhoramos drasticamente nossa resposta a incidentes.

Neste artigo, vou te guiar na configuração de um ambiente controlado utilizando **Vagrant** e **VirtualBox**.

## Preparando o ambiente

Para este guia, utilizaremos o Vagrant para gerenciar nossa máquina virtual. Certifique-se de ter os dois softwares abaixo instalados:

- **[VirtualBox](https://www.virtualbox.org/wiki/Downloads)**
- **[Vagrant](https://developer.hashicorp.com/vagrant/install)**

**Dica para usuários Windows:** Se você utiliza WSL, recomendo instalar o Vagrant e o VirtualBox diretamente no Windows para facilitar a comunicação entre as ferramentas.


## Criando e Configurando a VM

### 1. Prepare o diretório do projeto

Crie uma pasta dedicada para os arquivos da sua máquina virtual:

```bash
mkdir aula-grafana
cd aula-grafana
```

### 2. Instanciando a VM com Vagrant

Utilizaremos uma box do **CentOS 7** para este estudo. Você pode explorar outras opções no [Vagrant Boxes](https://portal.cloud.hashicorp.com/vagrant/discover).

Execute o comando para inicializar o projeto:

```bash
vagrant init centos/7
```

### 3. Editando o Vagrantfile

Precisamos ajustar o arquivo `Vagrantfile` para permitir o acesso externo à aplicação. Abra o arquivo com seu editor de preferência (ex: `vim` ou `Notepad`) e adicione as seguintes configurações de rede:

```bash
config.vm.network "forwarded_port", guest: 3000, host: 3000, host_ip: "127.0.0.1"
config.vm.network "public_network"
```

*Isso irá redirecionar a porta 3000 da VM para o seu localhost e colocar a VM na sua rede local.*

**OBS:** Em um servidor real (ex: RHEL/CentOS), ao invés do port forwarding do Vagrant, você expõe a porta diretamente pelo firewall do sistema com o firewall-cmd:

```bash
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload
```

Isso libera a porta 3000 no firewall para que a aplicação seja acessível na rede.

### 4. Subindo o servidor

Agora, inicie a máquina virtual:

```bash
vagrant up
```

**Nota:** O Vagrant pode solicitar que você escolha uma interface de rede. Geralmente, a opção **1** (sua conexão local ativa) é a correta.

Após o término do processo, acesse a VM via SSH:

```bash
vagrant ssh
```

## Instalando o Grafana

Com o acesso à VM estabelecido, vamos baixar e instalar a versão Enterprise do Grafana diretamente dos repositórios oficiais.

```bash
sudo yum install -y https://dl.grafana.com/grafana-enterprise/release/12.4.2/grafana-enterprise_12.4.2_23531306697_linux_amd64.rpm
```

### Gerenciando o serviço

Após a instalação, utilize o `systemctl` para habilitar e iniciar o servidor do Grafana:

```bash
# Habilita para iniciar junto com o sistema e inicia agora
sudo systemctl enable --now grafana-server

# Verifica o status do serviço
sudo systemctl status grafana-server
```

Se o status aparecer como `active (running)`, a instalação foi um sucesso!


## Acessando a Interface Web

Agora você pode acessar o painel do Grafana diretamente do navegador da sua máquina física através do endereço:

**[http://127.0.0.1:3000](http://127.0.0.1:3000)**

*   **Usuário padrão:** admin
*   **Senha padrão:** admin


## Conclusão

Instalar o Grafana é um processo direto, mas que abre portas para um controle muito maior sobre sua infraestrutura. Ter visibilidade do que acontece no servidor evita surpresas e permite agir antes que o problema afete o usuário final.

Nos próximos artigos, pretendo mostrar como configurar o **Prometheus** e utilizar **Exporters** para enviar dados reais para este painel. Até a próxima!


*Escrito por Gabriel Castro - 29/03/2026*
