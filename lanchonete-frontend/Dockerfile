FROM python:3.12-slim

# Configurações do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /usr/src/app

# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Criar usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /usr/src/app
USER appuser

# Expor a porta
EXPOSE 8000

# Comando para Railway (será sobrescrito pelo railway.toml se necessário)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "lanchonete.wsgi:application"]