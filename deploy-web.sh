#!/bin/bash

# Script de Deploy do Dashboard Streamlit Web
# Autor: Matheus Resende

echo "=========================================="
echo "🌐 DEPLOY DASHBOARD STREAMLIT WEB"
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

# Verifica se o arquivo do dashboard existe
if [ ! -f "dashboard_versao_final.py" ]; then
    echo "❌ Arquivo dashboard_versao_final.py não encontrado."
    exit 1
fi

# Verifica se o arquivo de dados existe
if [ ! -f "quantitativo_consolidado.xlsx" ]; then
    echo "⚠️ Arquivo quantitativo_consolidado.xlsx não encontrado. O dashboard pode não funcionar corretamente."
fi

# Para containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f docker-compose.web.yml down

# Remove imagens antigas (opcional)
read -p "Deseja remover imagens antigas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ Removendo imagens antigas..."
    docker system prune -f
fi

# Build e start
echo "🔨 Build da imagem Docker..."
docker-compose -f docker-compose.web.yml build

echo "🚀 Iniciando o dashboard..."
docker-compose -f docker-compose.web.yml up -d

# Verifica status
echo "⏳ Verificando status do container..."
sleep 15

if docker-compose -f docker-compose.web.yml ps | grep -q "Up"; then
    echo "✅ Dashboard está rodando com sucesso!"
    echo "📊 Acesse o dashboard em: http://localhost:8501"
    echo ""
    echo "📋 Comandos úteis:"
    echo "  Ver logs: docker-compose -f docker-compose.web.yml logs -f"
    echo "  Parar: docker-compose -f docker-compose.web.yml down"
    echo "  Reiniciar: docker-compose -f docker-compose.web.yml restart"
    echo "  Atualizar: ./deploy-web.sh"
    echo ""
    echo "🔍 Para monitorar: docker-compose -f docker-compose.web.yml logs -f dashboard"
else
    echo "❌ Falha ao iniciar o dashboard. Verificando logs..."
    docker-compose -f docker-compose.web.yml logs
    exit 1
fi

echo "=========================================="
echo "🎉 Deploy concluído com sucesso!"
echo "=========================================="
