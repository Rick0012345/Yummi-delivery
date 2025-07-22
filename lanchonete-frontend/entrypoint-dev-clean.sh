#!/bin/bash
set -e

echo "🧹 === MODO DESENVOLVIMENTO - LIMPEZA DE CACHE === 🧹"

# Limpar cache do Python
echo "🐍 Limpando cache do Python..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Limpar cache do Django
echo "🌟 Limpando cache do Django..."
python manage.py clear_cache 2>/dev/null || echo "Cache Django não disponível ou já limpo"

# Limpar sessões expiradas
echo "🔐 Limpando sessões expiradas..."
python manage.py clearsessions 2>/dev/null || echo "Limpeza de sessões concluída"

# Remover arquivos temporários
echo "🗑️ Removendo arquivos temporários..."
rm -rf /tmp/django_cache/* 2>/dev/null || true
rm -rf /var/tmp/* 2>/dev/null || true

# Limpar e recriar arquivos estáticos
echo "📁 Limpando e recriando arquivos estáticos..."
rm -rf /usr/src/app/staticfiles/* 2>/dev/null || true
python manage.py collectstatic --noinput --clear

# Executar migrações
echo "🔄 Executando migrações..."
python manage.py migrate --noinput

echo "✅ Sistema limpo e pronto para desenvolvimento!"
echo "🔧 Iniciando Django runserver na porta 8000..."
echo "🌐 Acesse: http://localhost:8000"
echo "🔄 Auto-reload ativado para desenvolvimento"

# Usar runserver para desenvolvimento (auto-reload)
exec python manage.py runserver 0.0.0.0:8000 