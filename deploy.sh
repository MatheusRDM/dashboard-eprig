#!/bin/bash

# Script de Deploy do Dashboard EPR IGUAÇU
# Autor: Matheus Resende

echo "=========================================="
echo "🚀 DEPLOY DASHBOARD EPR IGUAÇU"
echo "=========================================="

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verifica se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Para containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Remove imagens antigas (opcional)
read -p "Deseja remover imagens antigas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ Removendo imagens antigas..."
    docker system prune -f
fi

# Build e start
echo "🔨 Build da imagem Docker..."
docker-compose build

echo "🚀 Iniciando o dashboard..."
docker-compose up -d

# Verifica status
echo "⏳ Verificando status do container..."
sleep 10

if docker-compose ps | grep -q "Up"; then
    echo "✅ Dashboard está rodando com sucesso!"
    echo "📊 Acesse o dashboard em: http://localhost:8501"
    echo ""
    echo "📋 Comandos úteis:"
    echo "  Ver logs: docker-compose logs -f"
    echo "  Parar: docker-compose down"
    echo "  Reiniciar: docker-compose restart"
    echo ""
    echo "🔍 Para monitorar: docker-compose logs -f dashboard"
else
    echo "❌ Falha ao iniciar o dashboard. Verificando logs..."
    docker-compose logs
    exit 1
fi

echo "=========================================="
echo "🎉 Deploy concluído com sucesso!"
echo "=========================================="
