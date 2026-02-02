# 🌐 Deploy Dashboard Streamlit - Web

## 📋 Arquivos para Deploy Web

### 📦 requirements-web.txt
Dependências essenciais para o dashboard Streamlit:
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
```

### 🐳 Dockerfile.web
Configuração Docker otimizada para o dashboard:
- Python 3.11 slim
- Porta 8501 (Streamlit)
- Health check configurado
- Arquivos de dados incluídos

### ⚙️ docker-compose.web.yml
Orquestração simplificada:
- Apenas o serviço do dashboard
- Porta 8501:8501
- Volume para dados
- Restart automático

### 🚀 deploy-web.sh
Script de deploy automatizado:
- Verificação de arquivos
- Build e deploy
- Status monitoring
- Logs e comandos úteis

## 🚀 Como Fazer Deploy

### Pré-requisitos
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Método 1: Script Automático (Recomendado)
```bash
# Tornar script executável
chmod +x deploy-web.sh

# Executar deploy
./deploy-web.sh

# Acessar
http://localhost:8501
```

### Método 2: Manual
```bash
# Build da imagem
docker-compose -f docker-compose.web.yml build

# Iniciar o container
docker-compose -f docker-compose.web.yml up -d

# Verificar status
docker-compose -f docker-compose.web.yml ps

# Acessar
http://localhost:8501
```

### Método 3: Docker Puro
```bash
# Build
docker build -f Dockerfile.web -t dashboard-streamlit .

# Executar
docker run -d \
  --name dashboard-streamlit \
  -p 8501:8501 \
  -v $(pwd)/quantitativo_consolidado.xlsx:/app/quantitativo_consolidado.xlsx \
  dashboard-streamlit
```

## 🌐 Acesso ao Dashboard

Após o deploy, acesse:
- **Local**: http://localhost:8501
- **Rede**: http://IP_DO_SERVIDOR:8501

## 📊 Estrutura de Arquivos

```
├── dashboard_versao_final.py    # Dashboard principal
├── quantitativo_consolidado.xlsx # Dados
├── requirements-web.txt        # Dependências web
├── Dockerfile.web             # Config Docker web
├── docker-compose.web.yml     # Orquestração web
├── deploy-web.sh              # Script deploy web
└── README_WEB.md              # Este arquivo
```

## 🔧 Comandos Úteis

```bash
# Ver status
docker-compose -f docker-compose.web.yml ps

# Ver logs em tempo real
docker-compose -f docker-compose.web.yml logs -f dashboard

# Parar o serviço
docker-compose -f docker-compose.web.yml down

# Reiniciar
docker-compose -f docker-compose.web.yml restart

# Atualizar (após mudanças)
docker-compose -f docker-compose.web.yml down
docker-compose -f docker-compose.web.yml build --no-cache
docker-compose -f docker-compose.web.yml up -d

# Limpar tudo
docker-compose -f docker-compose.web.yml down -v
docker system prune -f
```

## 🌍 Opções de Hospedagem

### 1. VPS/Dedicado
```bash
# Em seu servidor
git clone <repositorio>
cd dashboard
./deploy-web.sh
```

### 2. Heroku
```bash
# Criar Procfile
echo "web: streamlit run dashboard_versao_final.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create seu-dashboard
git push heroku main
```

### 3. Railway
```bash
# Adicionar railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run dashboard_versao_final.py --server.port=$PORT --server.address=0.0.0.0"
  }
}

# Deploy
railway up
```

### 4. Render
```bash
# Adicionar render.yaml
services:
  type: web
  name: dashboard-epr
  env: python
  buildCommand: pip install -r requirements-web.txt
  startCommand: streamlit run dashboard_versao_final.py --server.port=$PORT --server.address=0.0.0.0
```

### 5. Google Cloud Run
```bash
# Build e push
gcloud builds submit --tag gcr.io/PROJECT-ID/dashboard-streamlit

# Deploy
gcloud run deploy dashboard-streamlit \
  --image gcr.io/PROJECT-ID/dashboard-streamlit \
  --platform managed \
  --allow-unauthenticated
```

### 6. AWS ECS
```bash
# Usar Dockerfile.web
# Configurar ECS task definition
# Deploy via AWS Console ou CLI
```

## 🐛 Troubleshooting

### Porta em uso
```bash
# Verificar processo na porta 8501
sudo lsof -i :8501

# Matar processo
sudo kill -9 <PID>

# Usar outra porta
docker-compose -f docker-compose.web.yml up -d --scale dashboard=1
```

### Arquivo de dados não encontrado
```bash
# Verificar se o arquivo existe
ls -la quantitativo_consolidado.xlsx

# Copiar para o container
docker cp quantitativo_consolidado.xlsx $(docker-compose -f docker-compose.web.yml ps -q dashboard):/app/
```

### Permissões
```bash
# Ajustar permissões dos arquivos
chmod 644 *.xlsx
chmod 755 *.py
chmod +x deploy-web.sh
```

### Logs de erro
```bash
# Ver logs completos
docker-compose -f docker-compose.web.yml logs --tail=100 dashboard

# Ver logs do container
docker logs dashboard-streamlit-web_dashboard_1
```

## 📈 Performance e Monitoramento

### Recursos Recomendados
- **CPU**: 1 core mínimo
- **RAM**: 1GB mínimo
- **Disco**: 5GB
- **Rede**: 10Mbps

### Health Check
O container inclui health check automático:
- Endpoint: `/_stcore/health`
- Intervalo: 30s
- Timeout: 30s

### Backup dos Dados
```bash
# Backup do arquivo de dados
cp quantitativo_consolidado.xlsx backup/quantitativo_consolidado_$(date +%Y%m%d).xlsx

# Backup completo
docker-compose -f docker-compose.web.yml down
tar -czf dashboard_backup_$(date +%Y%m%d).tar.gz *.py *.xlsx *.yml *.sh *.txt
```

## 🔐 Segurança

### Boas Práticas
- Dashboard em modo headless
- Sem exposição de arquivos do sistema
- Firewall configurado (porta 8501 apenas)
- HTTPS recomendado em produção

### HTTPS com Nginx
```nginx
server {
    listen 443 ssl;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 Atualizações Automáticas

### Cron Job para atualização
```bash
# Adicionar ao crontab
0 2 * * * cd /path/to/dashboard && git pull && ./deploy-web.sh
```

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboard
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          scp -r . user@server:/path/to/dashboard/
          ssh user@server 'cd /path/to/dashboard && ./deploy-web.sh'
```

---
**Desenvolvido por: Matheus Resende**  
**Versão Web: 1.0**  
**Última atualização: 2025**
