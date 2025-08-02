# Lanchonete Frontend

Este é o frontend do sistema de lanchonete desenvolvido em Django.

## 🏗️ Estrutura de Settings

O projeto agora possui **3 arquivos de configuração**:

- **`lanchonete/settings.py`** - Configurações base (compartilhadas)
- **`lanchonete/settings_production.py`** - Configurações para produção (Railway)

## 🛠️ Desenvolvimento Local

### Usando Docker (Recomendado)

1. Clone o repositório
2. Na pasta do projeto, execute:
```bash
docker-compose up --build
```

O Docker Compose automaticamente usa `settings_local.py`.

### Desenvolvimento Local sem Docker

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

3. Configure as variáveis de ambiente:
```bash
export DJANGO_SETTINGS_MODULE=lanchonete.settings_local
export POSTGRES_DB=lanchonete_db
export POSTGRES_USER=lanchonete_user
export POSTGRES_PASSWORD=lanchonete_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Inicie o servidor:
```bash
python manage.py runserver
```

## 🚀 Deploy no Railway

### 1. Configuração Automática

O Railway automaticamente usa `settings_production.py` através do comando no `railway.toml`.

### 2. Variáveis de Ambiente Necessárias

Configure estas variáveis no painel do Railway:

```bash
# Obrigatórias (configuradas automaticamente pelo Railway PostgreSQL)
PGDATABASE=railway
PGUSER=postgres
PGPASSWORD=sua-senha-postgres
PGHOST=postgres.railway.internal
PGPORT=5432

# Opcionais (configurar manualmente)
DJANGO_SECRET_KEY=sua-chave-secreta-super-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.railway.app,.up.railway.app
DJANGO_CSRF_ORIGINS=https://*.railway.app,https://*.up.railway.app
DJANGO_CORS_ORIGINS=https://*.railway.app,https://*.up.railway.app
DJANGO_SECURE_SSL_REDIRECT=True
```

### 3. Deploy

```bash
railway up
```

## 📁 Estrutura do Projeto

```
lanchonete-frontend/
├── lanchonete/
│   ├── settings.py              # Configurações base
│   ├── settings_local.py        # Configurações local
│   ├── settings_production.py   # Configurações produção
│   ├── urls.py                  # URLs principais
│   └── wsgi.py                  # WSGI para produção
├── core/                        # App principal
├── static/                      # Arquivos estáticos
├── templates/                   # Templates HTML
├── Dockerfile                   # Configuração Docker
├── docker-compose.yml           # Docker Compose (local)
├── railway.toml                 # Configuração Railway
└── requirements.txt             # Dependências Python
```

## 🔧 Diferenças entre Ambientes

### Local (`settings_local.py`)
- ✅ DEBUG = True
- ✅ Segurança relaxada para desenvolvimento
- ✅ CORS permitindo localhost
- ✅ Banco local via Docker Compose

### Produção (`settings_production.py`)
- ✅ DEBUG = False
- ✅ Segurança máxima ativada
- ✅ CORS restrito para domínios Railway
- ✅ Banco Railway via variáveis de ambiente

## 🐛 Troubleshooting

### Erro de Settings
- **Local**: Verifique se `DJANGO_SETTINGS_MODULE=lanchonete.settings_local`
- **Railway**: Verifique se o `railway.toml` está correto

### Erro de Banco
- **Local**: Verifique se o container PostgreSQL está rodando
- **Railway**: Verifique se o plugin PostgreSQL foi adicionado

## 🔄 Comandos Úteis

```bash
# Local com settings específico
DJANGO_SETTINGS_MODULE=lanchonete.settings_local python manage.py runserver

# Railway com settings específico
railway run -- DJANGO_SETTINGS_MODULE=lanchonete.settings_production python manage.py migrate
``` 