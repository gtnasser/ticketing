DOCKER

Para execução em containeres é necessário:
- Arquivos de containerização (Dockerfile, docker-compose, .dockerignore)
- Ajuste necessário no database.py para persistência do banco
- Seção do README.Dockerfile

**Dockerfile**
```
FROM python:3.11-slim

WORKDIR /app

# Dependências primeiro (aproveita o cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY . .

EXPOSE 8501

# Healthcheck — o Streamlit expõe /_stcore/health
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

**.dockerignore**
```
venv/
__pycache__/
*.pyc
.git/
.gitignore
data/
*.db
.DS_Store
```

O data/ e *.db são ignorados de propósito: o banco é criado em tempo de execução no volume, não deve entrar na imagem

**docker-compose.yml**
```
services:
  ticketing:
    build: .
    container_name: ticketing
    ports:
      - "8501:8501"
    environment:
      - DB_PATH=/app/data/occurrences.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**Ajuste na persistência do banco**

Sem isso, o banco ficaria dentro do container e seria perdido a cada rebuild. A mudança é mínima — o caminho passa a aceitar uma variável de ambiente, mantendo o comportamento local atual:

**database.py**
```
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", str(Path(__file__).parent / "occurrences.db")))
```

- Local (sem Docker): nada muda — usa occurrences.db na pasta do projeto.
- Docker: o compose define DB_PATH=/app/data/occurrences.db, e o volume ./data:/app/data mantém o arquivo no host.


## Execução com Docker

**Pré-requisito:** Docker e Docker Compose instalados.

**1. Construir e subir o container**
```bash
docker compose up -d --build
```

**2. Criar os usuários** (o banco é criado no volume `./data`)
```bash
docker compose run --rm ticketing python create_user.py admin senha123
```

**3. Acessar nop navegador**
```
http://localhost:8501
```

**4. Parar o serviço**
```bash
docker compose down
``` 

**Observações:**
- O banco `occurrences.db` fica em `./data` no host (volume persistente) — sobrevive a `docker compose down` e a rebuilds.
- Para backup, copie o arquivo `./data/occurrences.db`.
- Para atualizar a aplicação: `git pull` + `docker compose up -d --build`.
- Os arquivos criados em `./data` pertencem ao usuário do container (root por padrão). Se precisar de outro dono, ajuste com `chown` após o primeiro `up`.


## Produção

Diferenças em relação ao compose de desenvolvimento: a porta é exposta apenas no localhost (o Nginx faz o proxy), e há limites de recursos definidos.

**docker-compose.dev.yml**
```
services:
  ticketing:
    build: .
    container_name: ticketing
    ports:
      - "8501:8501"
    environment:
      - DB_PATH=/app/data/occurrences.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**docker-compose.prod.yml**
```
services:
  ticketing:
    build: .
    container_name: ticketing
    #  apenas no localhost — o Nginx faz o proxy reverso
    ports:
      - "127.0.0.1:8501:8501"
    environment:
      - DB_PATH=/app/data/occurrences.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
```

O **127.0.0.1:8501:8501** garante que o Streamlit **não fique acessível diretamente pela rede** — só o Nginx (na mesma máquina) consegue alcançá-lo. Os limites de CPU/memória evitam que o container consuma recursos sem controle.

## Deploy com Docker + Nginx (produção)

Para produção, o padrão recomendado é Docker + Nginx como proxy reverso:

**Subir o container com o compose de produção**
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

**Configurar o Nginx** (```/etc/nginx/sites-available/ticketing```):
```
    server {
        listen 80;
        server_name ticketing.exemplo.com;

        location / {
            proxy_pass http://127.0.0.1:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }
    }
```

**Instalar o Nginx**
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/ticketing   # colar a config acima
```

**Ativar o site e recarregar**
```bash
sudo ln -s /etc/nginx/sites-available/ticketing /etc/nginx/sites-enabled/
sudo nginx -t # valida a sintaxe
sudo systemctl reload nginx
```

**HTTPS com Certbot (opcional, recomendado)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ticketing.exemplo.com
```

**Observações:**
- O compose de produção expõe a porta **apenas no localhost** (`127.0.0.1:8501:8501`) — o Nginx é o único ponto de entrada.
- As linhas `Upgrade` e `Connection "upgrade"` são obrigatórias: o Streamlit usa WebSocket, e sem elas a interface congela após alguns segundos.
- O `proxy_read_timeout 86400` evita que conexões longas sejam cortadas.


