#!/bin/bash

echo "🧹 === SCRIPT DE LIMPEZA MANUAL === 🧹"

# Parar containers se estiverem rodando
echo "⏹️ Parando containers..."
docker-compose down 2>/dev/null || true

# Limpar imagens antigas
echo "🗑️ Removendo imagens antigas..."
docker image rm lanchonete-frontend-web:latest 2>/dev/null || true

# Limpar cache do Docker
echo "🐳 Limpando cache do Docker..."
docker builder prune -f 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Limpar arquivos de cache locais
echo "📁 Limpando arquivos de cache locais..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
rm -rf staticfiles/* 2>/dev/null || true

echo "✅ Limpeza completa realizada!"
echo "🚀 Para rebuildar: docker-compose up --build"
echo "🛠️ Para desenvolvimento: docker-compose -f docker-compose.dev.yml up --build" 