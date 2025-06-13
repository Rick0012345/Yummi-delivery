#!/bin/sh
set -e

# Deveria ter algo aqui, mas, enquanto o settings.py não for configurado, o entrypoint não deve tentar
# esperar por uma database.
# "--silent foi alterado para -q"
# until pg_isready -h "$DJANGO_DB_HOST" -p "$DJANGO_DB_PORT" -U "$DJANGO_DB_USER" -d "$DJANGO_DB_NAME" -q; do
#   echo "Esperando resposta da database em $DJANGO_DB_HOST na porta $DJANGO_DB_PORT..."
#   sleep 2
# done

# echo "Database rodando."

# Rodar migrações
python manage.py migrate

# Criar superuser se ele não existir (optional) (irá rodar se conter tais variáveis de ambiente)
# if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
#   python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || true
# fi

# Iniciar Gunicorn
exec gunicorn lanchonete.wsgi:application --bind 0.0.0.0:9999