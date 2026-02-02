# 🏗️ Dashboard EPR IGUAÇU - Deploy

## 📋 Arquivos de Configuração

### 📦 requirements.txt
Lista de dependências Python necessárias para o dashboard:
- streamlit==1.28.0
- pandas==2.0.3
- plotly==5.15.0
- openpyxl==3.1.2
- numpy==1.24.3
- python-dateutil==2.8.2
- xlrd==2.0.1
- xlsxwriter==3.1.9
- Pillow==10.0.0

### 🐳 Dockerfile
Configuração do container Docker:
- Base: Python 3.11 slim
- Porta: 8501
- Health check configurado
- Otimizado para produção

### ⚙️ docker-compose.yml
Orquestração do serviço:
- Mapeamento de porta 8501:8501
- Volume para dados
- Restart automático
- Health check

### 🚫 .dockerignore
Arquivos ignorados no build:
- `__pycache__/`, `.git/`, `venv/`
- Arquivos temporários
- IDE configs

## 🚀 Como Fazer o Deploy

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
chmod +x deploy.sh

# Executar deploy
./deploy.sh
```

### Método 2: Manual
```bash
# Build da imagem
docker-compose build

# Iniciar o container
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Método 3: Docker Puro
```bash
# Build
docker build -t dashboard-epr .

# Executar
docker run -d \
  --name dashboard-epr \
  -p 8501:8501 \
  -v $(pwd)/quantitativo_consolidado.xlsx:/app/quantitativo_consolidado.xlsx \
  dashboard-epr
```

## 🌐 Acesso ao Dashboard

Após o deploy, acesse:
- **Local**: http://localhost:8501
- **Rede**: http://IP_DO_SERVIDOR:8501

## 📊 Estrutura de Arquivos

```
├── dashboard_versao_final.py    # Aplicação principal
├── quantitativo_consolidado.xlsx # Dados
├── requirements.txt            # Dependências
├── Dockerfile                  # Config Docker
├── docker-compose.yml          # Orquestração
├── .dockerignore              # Ignorados
├── deploy.sh                  # Script deploy
└── README_DEPLOY.md           # Este arquivo
```

## 🔧 Comandos Úteis

```bash
# Ver status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f dashboard

# Parar o serviço
docker-compose down

# Reiniciar
docker-compose restart

# Atualizar (após mudanças)
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Limpar tudo
docker-compose down -v
docker system prune -f
```

## 🐛 Troubleshooting

### Porta em uso
```bash
# Verificar processo na porta 8501
sudo lsof -i :8501

# Matar processo
sudo kill -9 <PID>
```

### Permissões
```bash
# Ajustar permissões dos arquivos
chmod 644 *.xlsx
chmod 755 *.py
chmod +x deploy.sh
```

### Logs de erro
```bash
# Ver logs completos
docker-compose logs --tail=100 dashboard

# Ver logs do container
docker logs dashboard-epr-iguaçu_dashboard_1
```

## 🔄 Atualizações

Para atualizar o dashboard:
1. Atualize os arquivos
2. Execute: `./deploy.sh`
3. Confirme em http://localhost:8501

## 📈 Monitoramento

### Health Check
O container inclui health check automático:
- Intervalo: 30s
- Timeout: 30s
- Endpoint: `/_stcore/health`

### Recursos
- **Memória**: ~512MB
- **CPU**: ~0.5 core
- **Disco**: ~1GB

## 🔐 Segurança

- Dashboard em modo headless
- Sem exposição de arquivos do sistema
- Volume somente leitura para dados
- Health check configurado

---
**Desenvolvido por: Matheus Resende**  
**Versão: 1.0**  
**Última atualização: 2025**
