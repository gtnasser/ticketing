# ticketing

## Proposta

Criar um sistema simples para armazenar e consultar ocorrências e as soluções adotadas, com o objetivo de formar uma base de conhecimento compartilhada. Deve ser simples e leve o suficiente para ser executado em um desktop ou servidor Linux, por um pequeno grupo de usuários.

**Características principais:**
- Registro, em cada ocorrência, da solução provisória e da solução definitiva adotadas.
- Pesquisa por texto (título, soluções e usuário) com filtros por tipo e período.
- Multiusuário, com autenticação simples (usuário/senha).
- Extremamente leve: Streamlit + SQLite, uma única dependência.


**Requisitos funcionais:**
- Multiusuário, com autenticação simples (usuário/senha) validada no banco local.
- Cadastro e pesquisa de ocorrências (edição/exclusão: evolução futura).
- Pesquisa por texto com filtros (tipo e período).
- Criação de usuários via script de linha de comando (`create_user.py`).
- Atributos da ocorrência:
  - Data da ocorrência
  - Título
  - Tipo (Erro de sistema, Erro de operação, Outros)
  - Solução provisória (texto)
  - Solução definitiva (texto)
  - Nome do usuário
  - Data/hora do registro da ocorrência
- Atributos do usuário:
  - username
  - password (armazenada com hash PBKDF2)


**Requisitos não funcionais:**
- Banco de dados local (SQLite, arquivo único).
- Autenticação simples (usuário/senha), no mesmo banco.
- Senhas armazenadas com hash PBKDF2, nunca em texto puro.
- Estimativa de usuários: 6.
- Estimativa de ocorrências: 24/dia (4 por usuário).
- Backup: basta copiar o arquivo do banco (`occurrences.db`).


## TODO: Evoluções futuras

- Edição e exclusão de ocorrências, com registro de quem alterou.
- Tela de administração de usuários (criar, desativar, redefinir senha) na interface, em vez de script CLI.
- Usuário redefinir a sua senha, e forçar a troca de senha periódica.
- Exportação dos resultados em CSV/Excel.
- Relatório com gráficos (evolução temporal, contagem por mês).
- Log de acesso (quem logou/deslogou, data/hora) e estatísticas de uso.
- Autenticação com sessão expirada (logout automático por inatividade).
- Backup automático
- execucao em docker



## Como executar

**Pré-requisito:** Python 3.9 ou superior.

**1. Obter o código**
```bash
git clone https://github.com/username/ticketing.git ./ticketing
cd ticketing
```

**2. Criar e ativar o ambiente virtual**

Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
    source venv/bin/activate
```

**3. Instalar a dependência**
```bash
pip install -r requirements.txt
```

**4. Criar os usuários**
```bash
python create_user.py admin senha123        # cria o primeiro usuário
python create_user.py john wick             # cria outro usuario
```

**5. Executar em desktop (uso local)**
```bash
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

**6. Executar em servidor Linux (acesso pela rede)**
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Os usuários acessam pelo IP do servidor, ex.: `http://192.168.1.50:8501`.

**Notas:**
- O banco `occurrences.db` é criado automaticamente na primeira execução.
- Para backup, basta copiar o arquivo `occurrences.db`.
- Para adicionar uma nova versão ao histórico, use o `release.py`:
```bash
python release.py 1.6.0 "feat: exportar ocorrências em CSV" "fix: filtro por período"
```

-----


## Conteúdo adicional:


## 1. Estrutura do peojeto

```text
    ticketing/
    ├── app.py                  # orquestração: login, menu lateral e roteamento
    ├── login.py                # fluxo de login/logout (do_login, do_logout)
    ├── auth.py                 # sessão e autenticação (is_auth, validate, create_user)
    ├── database.py             # camada de banco (SQLite)
    ├── create_user.py          # script CLI para criar usuários
    ├── home.py                 # página inicial
    ├── ticket_register.py      # página de cadastro de ocorrências
    ├── ticket_search.py        # página de pesquisa de ocorrências
    ├── reports.py              # página de relatório
    ├── about.py                # página Sobre (lê history.log)
    ├── history.log             # histórico de versões
    ├── release.py              # script para adicionar versões ao history.log
    ├── requirements.txt        # dependências (streamlit)
    └── occurrences.db          # banco (criado automaticamente)
```

## 2. Tecnologias utilizadas

- **Python 3.9+** — linguagem de desenvolvimento.
- **Streamlit** — framework web para a interface (única dependência externa).
- **SQLite** — banco de dados local em arquivo único, sem servidor.
- **PBKDF2 (hashlib)** — criptografia das senhas, nunca armazenadas em texto puro.

## 3. Arquitetura

O sistema segue uma arquitetura simples de camadas, com responsabilidades bem definidas:
```text
    Navegador (usuário)
        │
        ▼
    app.py ──────────────── orquestração: login, menu lateral e roteamento
        │
        ├── login.py ─────── fluxo de login/logout (do_login, do_logout)
        ├── auth.py ──────── sessão e autenticação (is_auth, validate, create_user)
        ├── database.py ──── camada de acesso ao banco (SQLite)
        │
        └── páginas (run())
            ├── home.py
            ├── ticket_register.py
            ├── ticket_search.py
            ├── reports.py
            └── about.py
        │
        ▼
    occurrences.db (SQLite)
```

**Decisões de design:**
- **Roteamento por dicionário**: o menu lateral e o roteamento usam a mesma estrutura `PAGES = {rótulo: função}` — adicionar uma página é uma linha no dicionário.
- **Sessão centralizada**: `auth.py` é o único módulo que manipula `st.session_state` (via `is_auth`, `get_current_user`, `clear_session`); as páginas nunca acessam a sessão diretamente.
- **Login/logout concentrados**: `login.py` é o ponto único do fluxo de entrada/saída, facilitando futuras implementações de log e estatísticas de acesso.
- **Banco isolado**: nenhuma página cria conexão própria — tudo passa por `database.py`.
- **Páginas com `run()`**: cada página expõe um único ponto de entrada público; o `app.py` só orquestra.


## 4. Execução como serviço permanente no Linux (systemd)

Para o sistema ficar rodando continuamente no servidor, sem depender de um terminal aberto, use o systemd.

**Criar o arquivo de serviço**
```bash
sudo nano /etc/systemd/system/ticketing.service
```

**Conteúdo do arquivo** (ajuste os caminhos conforme o seu projeto):
```text
    [Unit]
    Description=Ticketing - Sistema de Ocorrências
    After=network.target

    [Service]
    Type=simple
    User=ticketing
    WorkingDirectory=/opt/ticketing
    ExecStart=/opt/ticketing/venv/bin/streamlit run app.py --server.address 0.0.0.0 --server.port 8501
    Restart=always
    RestartSec=5
    Environment=PYTHONUNBUFFERED=1

    [Install]
    WantedBy=multi-user.target
```

**Recarregar o systemd e ativar o serviço**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ticketing   # inicia junto com o sistema
sudo systemctl start ticketing    # inicia agora
```

**Verificar o status e os logs**
```bash
sudo systemctl status ticketing
journalctl -u ticketing -f        # acompanha os logs em tempo real
```

**Comandos úteis**
```bash
sudo systemctl restart ticketing  # reinicia o serviço
sudo systemctl stop ticketing     # para o serviço
```

**Observações:**
- **Usuário dedicado**: o exemplo usa o usuário `ticketing`. Crie com `sudo useradd -m ticketing` e dê permissão de escrita no diretório do projeto (o banco `occurrences.db` precisa ser gravável).
- **Caminho do venv**: o `ExecStart` aponta para o executável do Streamlit dentro do ambiente virtual (`venv/bin/streamlit`). Se não usar venv, use `streamlit` direto.
- **Firewall**: libere a porta 8501 se houver firewall ativo (`sudo ufw allow 8501`).
- **Backup**: com o serviço rodando, o backup continua sendo copiar o arquivo `occurrences.db` (de preferência com o serviço parado ou em horário de baixo uso).


