#!/bin/bash

# Script de deploy para Railway
echo "🚀 Iniciando deploy no Railway..."

# Verificar se estamos no Railway
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Ambiente Railway detectado"
    
    # Executar migrações
    echo "📦 Executando migrações..."
    python manage.py migrate --noinput
    
    # Coletar arquivos estáticos
    echo "📁 Coletando arquivos estáticos..."
    python manage.py collectstatic --noinput
    
    # Iniciar servidor
    echo "🌐 Iniciando servidor..."
    exec gunicorn lanchonete.wsgi:application \
        --bind 0.0.0.0:$PORT \
        --workers 3 \
        --timeout 120 \
        --keep-alive 2 \
        --access-logfile - \
        --error-logfile -
else
    echo "🔧 Ambiente local detectado"
    echo "💡 Para deploy no Railway, use: railway up"
    exec python manage.py runserver 0.0.0.0:8000
fi 