FROM python:3.12-slim

# Hoje em dia, utiliza-se key=value, ao invés de key value.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema.
RUN apt-get update \
    && apt-get install -y python3-dev postgresql-client libpq-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Francamente, eu não sei porque, mas sempre funcionou em /usr/src/app.
WORKDIR /usr/src/app

COPY requirements.txt .

# Atualizar pip para a versão mais recente por segurança.
RUN pip install --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos e o entrypoint junto.
COPY . /usr/src/app/

# Configurar permissões para o entrypoint.sh.
# Nesse ponto, só faço isso por costume.
RUN chmod +x /usr/src/app/entrypoint.sh

# Coletar arquivos estáticos (recomendo whitenoise para lidar com eles)
RUN python manage.py collectstatic --noinput

# Rodar o entrypoint.sh.
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# CMD foi removido. Será utilizado o entrypoint.sh.
EXPOSE 9999