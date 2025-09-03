# Yuumi Automação

Este é o frontend, Automação e banco de dados do sistema de lanchonete desenvolvido em Django, n8n e postgres respectivamente.

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