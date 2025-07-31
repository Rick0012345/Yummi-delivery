# Lanchonete Frontend

Este é o frontend do sistema de lanchonete desenvolvido em Django.

## Requisitos

- Python 3.11+
- Docker e Docker Compose

## Configuração do Ambiente

### Usando Docker (Recomendado)

1. Clone o repositório
2. Na pasta do projeto, execute:
```bash
docker-compose up --build
```

### Desenvolvimento Local

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Inicie o servidor:
```bash
python manage.py runserver
```

## Estrutura do Projeto

- `core/` - Aplicação principal
- `lanchonete/` - Configurações do projeto
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `templates/` - Templates HTML
- `media/` - Arquivos de mídia enviados pelos usuários

## Funcionalidades

- Sistema de autenticação
- Dashboard administrativo
- Gerenciamento de produtos
- Gerenciamento de pedidos

## Deploy no Railway

O Railway detecta automaticamente o Dockerfile e faz o deploy. Configure as variáveis de ambiente no painel do Railway:

### Variáveis de Ambiente Principais:

```bash
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1,.railway.app,.up.railway.app
DJANGO_CSRF_ORIGINS=http://localhost,http://127.0.0.1,https://*.railway.app,https://*.up.railway.app
DJANGO_CORS_ORIGINS=http://localhost,http://127.0.0.1,https://*.railway.app,https://*.up.railway.app
DJANGO_SECURE_SSL_REDIRECT=True

# Database
POSTGRES_DB=lanchonete_db
POSTGRES_USER=lanchonete_user
POSTGRES_PASSWORD=sua-senha
POSTGRES_HOST=seu-host-railway
POSTGRES_PORT=5432
``` 