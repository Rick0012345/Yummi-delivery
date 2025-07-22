#!/bin/bash
set -e

echo "Iniciando aplicação Django..."

# Executar migrações
python manage.py migrate --noinput

echo "Iniciando servidor na porta 9999..."
# Usar runserver para desenvolvimento
python manage.py runserver 0.0.0.0:9999 