#!/bin/bash
set -e

echo "Iniciando aplicação Django..."

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

echo "Iniciando servidor Gunicorn na porta 8000..."
# Iniciar Gunicorn
exec gunicorn lanchonete.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60 