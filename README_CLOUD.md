# ☁️ Deploy Quantitativo Analyzer - Google Cloud Run

## 📋 Arquivos para Cloud Run

### 🌐 app.py
Versão web do `quantitativo_analyzer.py` adaptada para Cloud Run:
- Interface Streamlit para upload de arquivos
- Processamento em memória (sem dependência de paths locais)
- Geração de relatórios para download
- Visualizações interativas

### 📦 requirements-cloud.txt
Dependências otimizadas para Cloud Run:
```
streamlit==1.28.0
pandas==2.0.3
plotly==5.15.0
openpyxl==3.1.2
numpy==1.24.3
python-dateutil==2.8.2
xlrd==2.0.1
xlsxwriter==3.1.9
Pillow==10.0.0
gunicorn==21.2.0
```

### 🐳 Dockerfile.cloud
Configuração Docker otimizada para Cloud Run:
- Python 3.11 slim
- Porta 8080 (padrão Cloud Run)
- Gunicorn para produção
- Health checks configurados

### ⚙️ app.yaml
Configuração do Google App Engine (alternativa ao Cloud Run):
- Auto-scaling configurado
- Health checks
- Recursos otimizados

### 🚀 deploy-cloud.sh
Script automatizado de deploy:
- Configura Google Cloud
- Cria repositório no Artifact Registry
- Build e deploy da imagem
- Retorna URL do serviço

### 🔄 cloudbuild.yaml
Configuração para CI/CD com Cloud Build:
- Build automatizado
- Deploy automático
- Integração com GitHub/GitLab

## 🚀 Como Fazer Deploy

### Pré-requisitos
```bash
# 1. Instalar Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 2. Autenticar
gcloud auth login
gcloud auth application-default login

# 3. Criar projeto no Google Cloud Console
# https://console.cloud.google.com

# 4. Configurar projeto
gcloud config set project SEU_PROJECT_ID
```

### Método 1: Script Automático (Recomendado)
```bash
# 1. Tornar script executável
chmod +x deploy-cloud.sh

# 2. Editar configurações no script
nano deploy-cloud.sh
# Altere PROJECT_ID para seu ID do projeto

# 3. Executar deploy
./deploy-cloud.sh
```

### Método 2: Manual Passo a Passo
```bash
# 1. Habilitar APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# 2. Criar repositório
gcloud artifacts repositories create quantitativo-analyzer-repo \
    --repository-format=docker \
    --location=us-central1

# 3. Build imagem
docker build -f Dockerfile.cloud -t quantitativo-analyzer .

# 4. Tag e push
docker tag quantitativo-analyzer us-central1-docker.pkg.dev/SEU_PROJECT_ID/quantitativo-analyzer-repo/quantitativo-analyzer:latest
docker push us-central1-docker.pkg.dev/SEU_PROJECT_ID/quantitativo-analyzer-repo/quantitativo-analyzer:latest

# 5. Deploy no Cloud Run
gcloud run deploy quantitativo-analyzer \
    --image=us-central1-docker.pkg.dev/SEU_PROJECT_ID/quantitativo-analyzer-repo/quantitativo-analyzer:latest \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated
```

### Método 3: Google App Engine
```bash
# 1. Deploy com App Engine
gcloud app deploy app.yaml

# 2. Acessar
gcloud app browse
```

## 🌐 Acesso à Aplicação

Após o deploy, acesse a URL retornada pelo script ou:
- **Cloud Run**: `https://quantitativo-analyzer-[hash]-[region].a.run.app`
- **App Engine**: `https://SEU_PROJECT_ID.appspot.com`

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
```bash
# Adicionar variáveis no deploy
gcloud run deploy quantitativo-analyzer \
    --set-env-vars="NODE_ENV=production,DEBUG=false"
```

### Domínio Personalizado
```bash
# Configurar domínio personalizado
gcloud run domain-mappings create \
    --service=quantitativo-analyzer \
    --domain=analyzer.seudominio.com
```

### Monitoramento
```bash
# Ver logs em tempo real
gcloud logs tail /run.googleapis.com%2Fquantitativo-analyzer --region=us-central1

# Ver métricas
gcloud run services describe quantitativo-analyzer --region=us-central1
```

## 📊 Funcionalidades da Versão Cloud

### ✅ Características Principais
- **Upload Múltiplo**: Vários arquivos Excel simultaneamente
- **Processamento em Nuvem**: Sem dependência local
- **Relatórios Instantâneos**: Download direto do navegador
- **Visualizações**: Gráficos interativos com Plotly
- **Auto-scaling**: Ajuste automático de recursos
- **Segurança**: HTTPS por padrão

### 📋 Relatórios Gerados
1. **Excel Consolidado**: Todos os dados processados
2. **Excel Power BI**: Otimizado para análise no Power BI

### 🎯 Vantagens do Cloud Run
- **Serverless**: Sem gerenciamento de servidores
- **Pay-per-use**: Pague apenas pelo que usar
- **Escalabilidade**: De 0 a 1000 instâncias
- **Global**: Distribuição mundial
- **Integração**: Com ecossistema Google Cloud

## 🔍 Troubleshooting

### Erros Comuns
```bash
# Permissão negada
gcloud auth login

# Projeto não encontrado
gcloud config set project SEU_PROJECT_ID

# API não habilitada
gcloud services enable run.googleapis.com

# Build falhou
docker build -f Dockerfile.cloud -t test .
```

### Debug Local
```bash
# Testar localmente
docker build -f Dockerfile.cloud -t quantitativo-analyzer .
docker run -p 8080:8080 quantitativo-analyzer
```

### Logs e Monitoramento
```bash
# Logs detalhados
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Métricas de performance
gcloud run services describe quantitativo-analyzer --region=us-central1 --format="table(spec.template.spec.containers[0].resources)"
```

## 💰 Custos Estimados

### Cloud Run (Gratuito até limites)
- **CPU**: 400.000 vCPU-seconds/mês (grátis)
- **Memória**: 2 GB-horas/mês (grátis)
- **Requests**: 2 milhões/mês (grátis)
- **Networking**: 1 GB/mês (grátis)

### Acima dos limites gratuitos:
- **CPU**: ~$0.000024/vCPU-second
- **Memória**: ~$0.0000025/GB-second
- **Requests**: ~$0.40/milhão

## 🔄 CI/CD com GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v0.2.0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      - name: Configure Docker
        run: gcloud auth configure-docker
      - name: Build and Push
        run: |
          docker build -f Dockerfile.cloud -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/quantitativo-analyzer .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/quantitativo-analyzer
      - name: Deploy
        run: |
          gcloud run deploy quantitativo-analyzer \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/quantitativo-analyzer \
            --region us-central1 \
            --allow-unauthenticated
```

---
**Desenvolvido por: Matheus Resende**  
**Versão Cloud: 1.0**  
**Plataforma: Google Cloud Run**
