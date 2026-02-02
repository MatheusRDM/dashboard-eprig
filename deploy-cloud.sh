#!/bin/bash

# Script de Deploy para Google Cloud Run
# Autor: Matheus Resende

echo "=========================================="
echo "☁️  DEPLOY GOOGLE CLOUD RUN - ANALYZER"
echo "=========================================="

# Verifica se gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK não está instalado."
    echo "📥 Instale em: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado."
    exit 1
fi

# Configurações
PROJECT_ID="epr-iguacu-analyzer"
SERVICE_NAME="quantitativo-analyzer"
REGION="us-central1"
IMAGE_NAME="quantitativo-analyzer"
REPO_NAME="quantitativo-analyzer-repo"

echo "🔧 Configurações:"
echo "  Project ID: $PROJECT_ID"
echo "  Service: $SERVICE_NAME"
echo "  Region: $REGION"
echo ""

# Verifica se está logado no Google Cloud
echo "🔐 Verificando autenticação Google Cloud..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "📝 Faça login no Google Cloud:"
    gcloud auth login
fi

# Configura o projeto
echo "📋 Configurando projeto..."
gcloud config set project $PROJECT_ID

# Habilita APIs necessárias
echo "🔓 Habilitando APIs necessárias..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Cria repositório no Artifact Registry (se não existir)
echo "📦 Verificando Artifact Registry..."
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION --format="value(name)" 2>/dev/null; then
    echo "🏗️ Criando repositório no Artifact Registry..."
    gcloud artifacts repositories create $REPO_NAME \
        --repository-format=docker \
        --location=$REGION \
        --description="Repositório Docker para Quantitativo Analyzer"
fi

# Build da imagem Docker
echo "🏗️ Build da imagem Docker..."
docker build -f Dockerfile.cloud -t $IMAGE_NAME .

# Tag da imagem para Artifact Registry
IMAGE_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest"
echo "🏷️ Tag da imagem: $IMAGE_PATH"
docker tag $IMAGE_NAME $IMAGE_PATH

# Push da imagem
echo "📤 Enviando imagem para Artifact Registry..."
docker push $IMAGE_PATH

# Deploy no Cloud Run
echo "☁️ Fazendo deploy no Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_PATH \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --memory=1Gi \
    --cpu=1 \
    --timeout=120s \
    --concurrency=10 \
    --max-instances=10 \
    --min-instances=0 \
    --set-env-vars=PORT=8080

# Obtém a URL do serviço
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --region=$REGION \
    --format="value(status.url)")

echo ""
echo "=========================================="
echo "✅ Deploy concluído com sucesso!"
echo "=========================================="
echo "🌐 URL do serviço: $SERVICE_URL"
echo ""
echo "📋 Comandos úteis:"
echo "  Ver logs: gcloud logs tail /run.googleapis.com%2F$SERVICE_NAME --region=$REGION"
echo "  Ver status: gcloud run services describe $SERVICE_NAME --region=$REGION"
echo "  Atualizar: ./deploy-cloud.sh"
echo "  Remover: gcloud run services delete $SERVICE_NAME --region=$REGION"
echo ""
echo "🔍 Para monitorar:"
echo "  Console Cloud: https://console.cloud.google.com/run"
echo "  Logs: https://console.cloud.google.com/logs"
echo "=========================================="
