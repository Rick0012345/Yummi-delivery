FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/django/.local/bin:$PATH" \
    PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        libpq5 \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r django && useradd -r -g django django

# Criar diretório da aplicação
WORKDIR /app

# Copiar arquivos e instalar dependências
COPY requirements.txt .

# Instalar dependências como usuário root para garantir permissões adequadas
RUN pip install -r requirements.txt

# Copiar o restante da aplicação
COPY --chown=django:django . .

# Criar diretórios para arquivos estáticos, mídia e logs com permissões adequadas
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R django:django /app/staticfiles /app/media /app/logs && \
    chmod -R 755 /app/staticfiles /app/media /app/logs

# Mudar para o usuário não-root
USER django

# Expor porta da aplicação
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check || exit 1

# Script para iniciar a aplicação
CMD ["/bin/bash", "-c", "\
    # Aguardar banco de dados se as variáveis estiverem definidas
    if [ -n \"$POSTGRES_HOST\" ] && [ -n \"$POSTGRES_PORT\" ]; then \
        echo \"Aguardando banco de dados...\" && \
        while ! pg_isready -h \"$POSTGRES_HOST\" -p \"$POSTGRES_PORT\" -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -q; do \
            echo \"Banco de dados não está pronto. Aguardando...\" && \
            sleep 2; \
        done && \
        echo \"Banco de dados está pronto!\"; \
    fi

# O Railway usará o startCommand do railway.toml para inicializar a aplicação
