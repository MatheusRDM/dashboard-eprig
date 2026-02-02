import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuração da página com fonte Poppins e sem barra lateral
st.set_page_config(
    page_title="Dashboard Quantitativo Excel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Adicionar CSS personalizado para fonte Poppins e cores personalizadas
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.stTitle {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    font-size: 2.5rem !important;
    color: #00233B !important;
}

.stHeader {
    font-family: 'Poppins', sans-serif !important;
}

.stMarkdown {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
}

.stSubheader {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1.3rem !important;
    color: #00233B !important;
}

.stMetric {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
}

.stSelectbox > div > div > select {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
}

.stDataFrame {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
}

.stTabs [data-baseweb="tab-list"] {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: #00233B !important;
}

.stExpander {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
    background-color: #F2F1EF !important;
    border: 1px solid #00233B !important;
    border-radius: 8px !important;
}

/* Fundo principal branco */
.stApp {
    background-color: #FFFFFF !important;
}

.main .block-container {
    background-color: #FFFFFF !important;
    padding-top: 2rem;
    padding-bottom: 2rem;

    max-width: 1200px;
}

/* Títulos e textos em azul escuro */
h1, h2, h3, h4, h5, h6 {
    color: #00233B !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Textos normais */
p, span, div {
    color: #00233B !important;
}

/* Cards e containers */
div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
    background-color: #FFFFFF !important;
}

/* Info messages */
.stInfo {
    background-color: #f0f2f6 !important;
    border-left-color: #00233B !important;
    color: #00233B !important;
}

/* Success messages */
.stSuccess {
    background-color: #f0f8f0 !important;
    border-left-color: #00233B !important;
    color: #00233B !important;
}

/* Warning messages */
.stWarning {
    background-color: #fff8e1 !important;
    border-left-color: #00233B !important;
    color: #00233B !important;
}

/* Error messages */
.stError {
    background-color: #ffebee !important;
    border-left-color: #00233B !important;
    color: #00233B !important;
}

/* Manter barra lateral intacta - não alterar cores */

/* Ocultar barra lateral completamente */
.css-1d391kg {
    display: none !important;
}

.css-1lcbmhc {
    display: none !important;
}

/* Ajustar conteúdo principal para usar espaço total */
.main .block-container {
    max-width: 1400px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Botões de 3 pontinhos para tabelas - discretos e no canto inferior */
.stButton button[data-testid="baseButton-secondary"]:has(span:contains("⋮")) {
    background-color: transparent !important;
    color: #999999 !important;
    border: none !important;
    font-size: 18px !important;
    padding: 4px 8px !important;
    border-radius: 4px !important;
    font-family: monospace !important;
    font-weight: bold !important;
    box-shadow: none !important;
    position: relative !important;
    float: right !important;
    margin-top: 10px !important;
}

.stButton button[data-testid="baseButton-secondary"]:has(span:contains("⋮")):hover {
    background-color: #f0f0f0 !important;
    color: #666666 !important;
}

/* Ocultar botão de menu da barra lateral */
button[kind="header"] {
    display: none !important;
}

/* Botões do cabeçalho - manter rerun com azul padrão, remover azul de settings e run */
.stButton[aria-label="Rerun"] > button {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    border: 1px solid #00233B !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

.stButton[aria-label="Settings"] > button {
    background-color: transparent !important;
    color: #666666 !important;
    border: none !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 400 !important;
}

.stButton[aria-label="Run"] > button {
    background-color: transparent !important;
    color: #666666 !important;
    border: none !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 400 !important;
}

/* Botões de filtros inteligentes - plano de fundo #F2F1EF */
.stButton > button[kind="primary"] {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    border: 1px solid #00233B !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

.stButton > button[kind="secondary"] {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    border: 1px solid #00233B !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

/* Botões padrão também com fundo #F2F1EF */
.stButton > button {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    border: 1px solid #00233B !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

/* Selectboxes - filtros inteligentes com fundo #F2F1EF */
.stSelectbox > div > div > select {
    font-family: 'Poppins', sans-serif !important;
    color: #00233B !important;
    background-color: #F2F1EF !important;
    border: 1px solid #00233B !important;
}

/* Container do selectbox */
.stSelectbox > div {
    background-color: #F2F1EF !important;
}

/* Dropdown do selectbox */
.stSelectbox[data-testid="stSelectbox"] > div > div > div {
    background-color: #F2F1EF !important;
}

/* Elemento principal do selectbox */
[data-baseweb="select"] {
    background-color: #F2F1EF !important;
}

[data-baseweb="select"] > div {
    background-color: #F2F1EF !important;
}

/* Opções do selectbox */
.stSelectbox option {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Setas e ícones do selectbox */
.stSelectbox svg {
    fill: #00233B !important;
}

/* Focus states */
.stSelectbox > div > div > select:focus {
    background-color: #F2F1EF !important;
    color: #00233B !important;
    border-color: #00233B !important;
}

/* Menu dropdown do selectbox */
[data-baseweb="popover"] {
    background-color: #F2F1EF !important;
}

[data-baseweb="popover"] div {
    background-color: #F2F1EF !important;
    color: #00233B !important;
}

/* Hover states */
[data-baseweb="select"]:hover {
    background-color: #F2F1EF !important;
}

/* Texto de desenvolvedor no canto inferior direito */
.developer-text {
    position: fixed;
    bottom: 10px;
    right: 15px;
    font-family: 'Poppins', sans-serif;
    font-size: 11px;
    color: #00233B;
    opacity: 0.7;
    z-index: 999;
    font-weight: 400;
    letter-spacing: 0.3px;
}

.developer-text:hover {
    opacity: 1;
    transition: opacity 0.3s ease;
}

/* Garantir que todos os textos estejam em #00233B */
.stMarkdown {
    color: #00233B !important;
}

.stExpander {
    color: #00233B !important;
}

/* Textos dentro de expanders */
.streamlit-expanderHeader {
    color: #00233B !important;
}

/* Textos em write e markdown */
p, li, span {
    color: #00233B !important;
}

/* Títulos em expanders */
[data-testid="stExpander"] div p {
    color: #00233B !important;
}
</style>
""", unsafe_allow_html=True)

# Caminho absoluto para o arquivo Excel
arquivo_excel = "quantitativo_consolidado.xlsx"
output_path = r"C:\Users\AFIRMA-EVIAS INF086\OneDrive\Área de Trabalho\Banco de dados EPR IGUAÇU"
caminho_completo = os.path.join(output_path, arquivo_excel)

# Título e informações do arquivo no cabeçalho
col_logos, col_title = st.columns([1, 5])

with col_logos:
    # Container para as duas imagens coladas
    col_logo1, col_logo2 = st.columns([1, 1])
    
    with col_logo1:
        # Adicionar primeira logo (abaixada 37px total)
        try:
            st.markdown("""
            <div style="margin-top: 37px;">
            """, unsafe_allow_html=True)
            st.image(r"C:\Users\AFIRMA-EVIAS INF086\OneDrive\Área de Trabalho\Banco de dados EPR IGUAÇU\Imagens\EPR-COLOR-e1683896060262.png", width=130)
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        except:
            st.write("🏢")

    with col_logo2:
        # Adicionar segunda logo (subida 20%)
        try:
            st.markdown("""
            <div style="margin-top: -20px;">
            """, unsafe_allow_html=True)
            st.image(r"C:\Users\AFIRMA-EVIAS INF086\OneDrive\Área de Trabalho\Banco de dados EPR IGUAÇU\Imagens\Selo C Ass_2.png", width=130)
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        except:
            st.write("🏅")

with col_title:
    st.markdown("<h1 style='font-family: Poppins, sans-serif; color: #00233B; margin-top: 20px; font-weight: 600;'>Dashboard Quantitativo de Serviços</h1>", unsafe_allow_html=True)

# Cabeçalho com informações do arquivo e controles (movidos para baixo)
st.markdown("<br>", unsafe_allow_html=True)  # Espaço adicional
col_header2, col_header3 = st.columns([1, 1])

with col_header2:
    # Mostrar informações do arquivo
    try:
        import datetime
        mod_time = os.path.getmtime(caminho_completo)
        last_update = datetime.datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M:%S")
        st.info(f"📅 Última atualização: {last_update}")
    except:
        pass

with col_header3:
    # Botão para limpar cache e recarregar dados
    if st.button("🔄 Recarregar Dados"):
        st.cache_data.clear()
        st.rerun()

# Texto do desenvolvedor no canto inferior direito
st.markdown("""
<div class="developer-text">
    Developed by: Matheus Resende
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Verifica se o arquivo existe
if not os.path.exists(caminho_completo):
    st.error(f"❌ Arquivo não encontrado: {caminho_completo}")
    st.stop()

# Carregar dados
@st.cache_data(ttl=60)  # Cache com TTL de 60 segundos para forçar atualização
def load_data():
    try:
        df = pd.read_excel(caminho_completo, sheet_name="Dados Detalhados")
        st.success(f"✅ Dados carregados com sucesso! {len(df)} registros encontrados.")
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None

@st.cache_data(ttl=60)  # Cache com TTL de 60 segundos para forçar atualização
def load_data_com_abas():
    try:
        # Carregar todas as abas para extrair informações
        excel_file = pd.ExcelFile(caminho_completo)
        df_dados = pd.read_excel(caminho_completo, sheet_name="Dados Detalhados")
        
        # Adicionar informação da aba para cada linha
        df_dados['Aba'] = "Dados Detalhados"  # Padrão
        
        # Tentar extrair data de outras abas se existirem
        import re
        padroes_data = [
            r'(\d{2})\.(\d{2})',  # DD.MM ou MM.DD
            r'(\d{2})/(\d{2})',  # DD/MM ou MM/DD  
            r'(\d{2})-(\d{2})',  # DD-MM ou MM-DD
        ]
        
        for sheet_name in excel_file.sheet_names:
            if sheet_name != "Dados Detalhados":
                # Procurar por padrões de data no nome da aba
                for padrao in padroes_data:
                    matches = re.findall(padrao, sheet_name)
                    if matches:
                        dia, mes = matches[0]
                        if int(dia) <= 12 and int(mes) <= 12:
                            data_formatada = f"{mes.zfill(2)}/{dia.zfill(2)}"
                        else:
                            data_formatada = f"{dia.zfill(2)}/{mes.zfill(2)}"
                        
                        # Se encontrar data no nome da aba, usar como referência
                        # para linhas que não têm data
                        mascara = (df_dados['Mês/Ano'].isna()) | (df_dados['Mês/Ano'] == 'Não identificada') | (df_dados['Mês/Ano'] == '')
                        df_dados.loc[mascara, 'Aba'] = sheet_name
                        break
        
        st.success(f"✅ Dados carregados com sucesso! {len(df_dados)} registros encontrados.")
        return df_dados
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None

df = load_data_com_abas()

if df is not None:
    def extrair_data_disponivel(linha):
        """Extrai data da coluna Mês/Ano, do nome do arquivo, do path completo ou da aba do Excel"""
        import re
        from datetime import datetime
        
        # 1. Tentar usar a coluna Mês/Ano existente
        mes_ano = str(linha.get('Mês/Ano', '')).strip()
        if mes_ano and mes_ano != 'Não identificada' and mes_ano != 'nan':
            # Converter formato com ponto para formato padrão (ex: 07.12 -> 07/12)
            if re.match(r'^\d{2}\.\d{2}$', mes_ano):
                mes_ano = mes_ano.replace('.', '/')
            return mes_ano
        
        # 2. Tentar extrair do nome do arquivo
        arquivo = str(linha.get('Arquivo', ''))
        
        # Procurar por padrões de data no nome do arquivo
        # Padrões: DD.MM, DD/MM, MM.DD, MM/DD, DD-MM, MM-DD
        padroes_data = [
            r'(\d{2})\.(\d{2})',  # DD.MM ou MM.DD
            r'(\d{2})/(\d{2})',  # DD/MM ou MM/DD  
            r'(\d{2})-(\d{2})',  # DD-MM ou MM-DD
        ]
        
        for padrao in padroes_data:
            matches = re.findall(padrao, arquivo)
            if matches:
                dia, mes = matches[0]
                # Verificar se parece ser formato DD.MM (dia > 12)
                if int(dia) <= 12 and int(mes) <= 12:
                    # Ambos podem ser válidos, assumir formato MM.DD
                    data_formatada = f"{mes.zfill(2)}/{dia.zfill(2)}"
                else:
                    # Um deles é maior que 12, assume DD.MM
                    data_formatada = f"{dia.zfill(2)}/{mes.zfill(2)}"
                
                # Adicionar ano atual se não tiver
                ano_atual = datetime.now().year
                return f"{data_formatada}/{ano_atual}"
        
        # 3. Tentar extrair do path completo
        path = str(linha.get('Path Completo', ''))
        for padrao in padroes_data:
            matches = re.findall(padrao, path)
            if matches:
                dia, mes = matches[0]
                if int(dia) <= 12 and int(mes) <= 12:
                    data_formatada = f"{mes.zfill(2)}/{dia.zfill(2)}"
                else:
                    data_formatada = f"{dia.zfill(2)}/{mes.zfill(2)}"
                
                ano_atual = datetime.now().year
                return f"{data_formatada}/{ano_atual}"
        
        # 4. Tentar extrair do nome da aba (sheet) do Excel
        # Para isso, precisamos acessar os nomes das abas durante a carga
        try:
            # Se tiver informação da aba em alguma coluna (pode variar conforme o arquivo)
            aba = str(linha.get('Aba', '')).strip()  # Tentar coluna 'Aba'
            if not aba or aba == 'nan':
                # Tentar outras colunas que possam conter nome da aba
                for col in ['Sheet', 'Planilha', 'Worksheet', 'Guia']:
                    aba = str(linha.get(col, '')).strip()
                    if aba and aba != 'nan':
                        break
            
            if aba and aba != 'nan':
                # Procurar padrões de data no nome da aba
                for padrao in padroes_data:
                    matches = re.findall(padrao, aba)
                    if matches:
                        dia, mes = matches[0]
                        if int(dia) <= 12 and int(mes) <= 12:
                            data_formatada = f"{mes.zfill(2)}/{dia.zfill(2)}"
                        else:
                            data_formatada = f"{dia.zfill(2)}/{mes.zfill(2)}"
                        
                        # Usar 2025 como ano padrão para dados de usinas
                        return f"{data_formatada}/2025"
        except:
            pass  # Ignorar erros na extração da aba
        
        # 5. Se não encontrar nada, retornar valor padrão
        return "Sem Data"

    # Aplicar extração de dados na coluna Mês/Ano
    df['Mês/Ano'] = df.apply(extrair_data_disponivel, axis=1)
    
    def definir_camada(linha):
        path = str(linha.get('Path Completo', '')).upper()
        local = str(linha.get('Local', '')).upper()
        if 'FRESA E CAPA' in path:
            return 'FRESA_E_CAPA'
        if 'USINAS' in path or 'USINAGEM' in path:
            return 'USINAGEM'
        if 'PAVIMENTO' in path or 'CONCRETO' in path:
            return 'PAVIMENTO_RIGIDO'
        if 'MICRO' in path:
            return 'MICROREVESTIMENTO'
        return 'OUTROS'
    
    df['Frente de Serviço'] = df.apply(definir_camada, axis=1)
    
    def normalizar_tipo_fresa(linha):
        tipo = str(linha.get('Tipo Arquivo', '')).upper()
        arquivo = str(linha.get('Arquivo', '')).upper()
        if "MED" in tipo or "MED" in arquivo or "FORM 108" in arquivo or "RCT-MGC" in arquivo or "RCT MGC" in arquivo or "RCT-MGC -" in arquivo:
            return "Medição Geométrica"
        if "EXTRA" in tipo or "GRAN" in tipo or "CAUQ" in tipo or "EXTRA" in arquivo or "GRAN" in arquivo or "CAUQ" in arquivo:
            return "Extração e Granulometria"
        if "TAXA" in tipo or "PINTURA" in tipo or "APLIC" in tipo or "TAXA" in arquivo or "APLIC" in arquivo:
            return "Taxa de Aplicação"
        if "RESID" in tipo or "RESID" in arquivo or "04. RESÍDUO" in arquivo:
            return "Resíduo"
        if "MANCHA" in tipo or "MANCHA" in arquivo or "PENDULO" in arquivo:
            return "Mancha de Areia"
        if "CHECKLIST" in tipo or "CHECKLIST" in arquivo:
            return "Checklist Aplicação"
        return "Outros"

    def extrair_equipe(linha):
        """Extrai número da equipe do nome da pasta"""
        local = str(linha.get('Local', ''))
        
        # Padrões para encontrar equipe
        import re
        
        # Procura por "Eq X" ou "Eq.X" ou "EqX" onde X é o número
        match = re.search(r'Eq\.?\s*(\d+)', local, re.IGNORECASE)
        if match:
            return f"Equipe {int(match.group(1)):02d}"
        
        return "Não identificada"
    
    def extrair_rodovia(linha):
        """Extrai rodovias do nome da pasta"""
        local = str(linha.get('Local', ''))
        rodovias = []
        
        # Padrões para rodovias
        import re
        
        # Procura por BR seguida de número
        br_matches = re.findall(r'BR[-\s]*(\d+)', local, re.IGNORECASE)
        for br in br_matches:
            rodovias.append(f"BR {br}")
        
        # Procura por PR seguido de número
        pr_matches = re.findall(r'PR[-\s]*(\d+)', local, re.IGNORECASE)
        for pr in pr_matches:
            rodovias.append(f"PR {pr}")
        
        # Remove duplicatas e ordena
        rodovias = list(set(rodovias))
        rodovias.sort()
        
        return ", ".join(rodovias) if rodovias else "Não identificada"

    def render_secao(titulo, df_secao, mostrar_filtro=False):
        """Renderiza uma seção padrão com gráficos e tabelas"""
        if df_secao.empty:
            st.info(f"📋 {titulo}: Nenhum registro encontrado")
            return
        
        st.markdown("---")
        st.subheader(f"📊 {titulo}")
        
        # Gráfico principal
        df_tipos = df_secao.groupby('Tipo Arquivo')['Quantitativo'].sum().reset_index()
        if not df_tipos.empty:
            max_value = df_tipos['Quantitativo'].max()
            y_max = max_value * 1.1
            
            fig = px.bar(
                df_tipos.sort_values('Quantitativo', ascending=False),
                x='Tipo Arquivo',
                y='Quantitativo',
                title=f"{titulo} - Quantitativo por Tipo ({len(df_secao)} registros)",
                text='Quantitativo',
                color_discrete_sequence=['#00233B']
            )
            fig.update_xaxes(tickangle=45, tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
            fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(color='#00233B', family='Poppins'))
            fig.update_yaxes(range=[0, y_max], tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
            # Aplicar fonte Poppins aos gráficos
            fig.update_layout(
                font_family='Poppins',
                font_size=12,
                title_font_size=16,
                title_font_family='Poppins',
                plot_bgcolor='#F2F1EF',
                paper_bgcolor='#FFFFFF',
                font_color='#00233B',
                margin=dict(l=80, r=80, t=80, b=80)  # Zoom -10% (aumentar margens)
            )
            fig.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'))
            fig.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'))
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico mensal
        df_mensal = df_secao.groupby('Mês/Ano')['Quantitativo'].sum().reset_index()
        if not df_mensal.empty:
            fig_mensal = px.line(
                df_mensal.sort_values('Mês/Ano'),
                x='Mês/Ano',
                y='Quantitativo',
                title=f"{titulo} - Evolução Mensal",
                markers=True,
                text='Quantitativo',
                color_discrete_sequence=['#00233B']
            )
            fig_mensal.update_traces(texttemplate='%{y}', textposition='top center', textfont=dict(color='#00233B', family='Poppins'))
            # Aplicar fonte Poppins aos gráficos
            fig_mensal.update_layout(
                font_family='Poppins',
                font_size=12,
                title_font_size=16,
                title_font_family='Poppins',
                plot_bgcolor='#F2F1EF',
                paper_bgcolor='#FFFFFF',
                font_color='#00233B',
                margin=dict(l=80, r=80, t=80, b=80)  # Zoom -10% (aumentar margens)
            )
            fig_mensal.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
            fig_mensal.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
            st.plotly_chart(fig_mensal, use_container_width=True)
        
        # Botão discreto para tabela detalhada
        if st.button("⋮", key=f"detalhes_{titulo}", help=f"Ver {len(df_secao)} registros"):
            with st.expander(f"📋 Detalhes ({len(df_secao)} registros)", expanded=True):
                display_cols = ['Local', 'Mês/Ano', 'Arquivo', 'Tipo Arquivo', 'Quantitativo']
                if 'Equipe' in df_secao.columns:
                    display_cols.insert(1, 'Equipe')
                if 'Rodovia' in df_secao.columns:
                    display_cols.insert(2, 'Rodovia')
                
                st.dataframe(
                    df_secao[display_cols].sort_values(['Local', 'Mês/Ano']), 
                    use_container_width=True
                )

    st.markdown("### Frentes de Serviço")
    tabs = st.tabs([
        "**Fresagem e Recomposição**",
        "**Usinas**", 
        "**Pavimento Rígido**",
        "**Microrevestimento**",
        "**Resumo Geral**"
    ])

    with tabs[0]:
        df_fresa = df[df['Frente de Serviço'] == 'FRESA_E_CAPA'].copy()
        df_fresa['Tipo Fresa'] = df_fresa.apply(normalizar_tipo_fresa, axis=1)
        
        # Adicionar colunas de Equipe e Rodovia
        df_fresa['Equipe'] = df_fresa.apply(extrair_equipe, axis=1)
        df_fresa['Rodovia'] = df_fresa.apply(extrair_rodovia, axis=1)
        
        st.markdown("---")
        st.subheader("🔍 Filtros Inteligentes - Fresagem e Recomposição")
        
        # Criar colunas para os filtros
        col1, col2, col3 = st.columns(3)
        
        # Determinar qual filtro foi alterado para manter a consistência
        if 'ultima_equipe' not in st.session_state:
            st.session_state.ultima_equipe = 'Todas'
        if 'ultima_rodovia' not in st.session_state:
            st.session_state.ultima_rodovia = 'Todas'
        
        with col1:
            # Filtro de Equipe - dinâmico baseado na rodovia selecionada
            if st.session_state.ultima_rodovia != 'Todas':
                df_rodovia_filtrada = df_fresa[df_fresa['Rodovia'].str.contains(st.session_state.ultima_rodovia, na=False)]
                equipes_com_dados = df_rodovia_filtrada[df_rodovia_filtrada['Equipe'] != 'Não identificada']['Equipe'].value_counts()
            else:
                equipes_com_dados = df_fresa[df_fresa['Equipe'] != 'Não identificada']['Equipe'].value_counts()
            
            equipes_disponiveis = ['Todas'] + [f"{eq} ({count})" for eq, count in equipes_com_dados.items()]
            equipe_selecionada = st.selectbox("Filtrar por Equipe:", equipes_disponiveis)
            equipe_selecionada = equipe_selecionada.split(' (')[0] if ' (' in equipe_selecionada else equipe_selecionada
        
        with col2:
            # Filtro de Rodovia - dinâmico baseado na equipe selecionada
            if equipe_selecionada != 'Todas':
                df_equipe_filtrada = df_fresa[df_fresa['Equipe'] == equipe_selecionada]
                rodovias_com_dados = df_equipe_filtrada[df_equipe_filtrada['Rodovia'] != 'Não identificada']['Rodovia'].value_counts()
            else:
                rodovias_com_dados = df_fresa[df_fresa['Rodovia'] != 'Não identificada']['Rodovia'].value_counts()
            
            rodovias_disponiveis = ['Todas'] + [f"{rd} ({count})" for rd, count in rodovias_com_dados.items()]
            rodovia_selecionada = st.selectbox("Filtrar por Rodovia:", rodovias_disponiveis)
            rodovia_selecionada = rodovia_selecionada.split(' (')[0] if ' (' in rodovia_selecionada else rodovia_selecionada
        
        with col3:
            # Filtro de Tipo de Ensaio - dinâmico baseado nos outros filtros
            df_temp = df_fresa.copy()
            if equipe_selecionada != 'Todas':
                df_temp = df_temp[df_temp['Equipe'] == equipe_selecionada]
            if rodovia_selecionada != 'Todas':
                df_temp = df_temp[df_temp['Rodovia'].str.contains(rodovia_selecionada, na=False)]
            
            tipos_com_dados = df_temp['Tipo Fresa'].value_counts()
            tipos_disponiveis = ['Todos'] + [f"{tp} ({count})" for tp, count in tipos_com_dados.items()]
            tipo_selecionado = st.selectbox("Filtrar por Tipo de Ensaio:", tipos_disponiveis)
            tipo_selecionado = tipo_selecionado.split(' (')[0] if ' (' in tipo_selecionado else tipo_selecionado
        
        # Atualizar session_state para a próxima interação
        st.session_state.ultima_equipe = equipe_selecionada
        st.session_state.ultima_rodovia = rodovia_selecionada
        
        # Mostrar indicador de interação dos filtros
        if equipe_selecionada != 'Todas' or rodovia_selecionada != 'Todas':
            st.markdown("### 🔗 Interação dos Filtros")
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                if equipe_selecionada != 'Todas':
                    df_equipe_info = df_fresa[df_fresa['Equipe'] == equipe_selecionada]
                    rodovias_equipe = df_equipe_info[df_equipe_info['Rodovia'] != 'Não identificada']['Rodovia'].nunique()
                    st.info(f"👥 **{equipe_selecionada}**\n🛣️ {rodovias_equipe} rodovias")
            
            with col_info2:
                if rodovia_selecionada != 'Todas':
                    df_rodovia_info = df_fresa[df_fresa['Rodovia'].str.contains(rodovia_selecionada, na=False)]
                    equipes_rodovia = df_rodovia_info[df_rodovia_info['Equipe'] != 'Não identificada']['Equipe'].nunique()
                    st.info(f"🛣️ **{rodovia_selecionada}**\n👥 {equipes_rodovia} equipes")
            
            with col_info3:
                if equipe_selecionada != 'Todas' and rodovia_selecionada != 'Todas':
                    df_combinacao = df_fresa[
                        (df_fresa['Equipe'] == equipe_selecionada) & 
                        (df_fresa['Rodovia'].str.contains(rodovia_selecionada, na=False))
                    ]
                    st.success(f"🎯 **Combinação**\n📋 {len(df_combinacao)} registros")
                elif equipe_selecionada != 'Todas' or rodovia_selecionada != 'Todas':
                    st.info("💡 **Selecione o segundo filtro**\npara refinar ainda mais")
        
        # Botões de controle
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Limpar todos os filtros"):
                st.session_state.ultima_equipe = 'Todas'
                st.session_state.ultima_rodovia = 'Todas'
                st.rerun()
        with col_btn2:
            if st.button("🔄 Atualizar filtros"):
                st.rerun()
        
        # Aplicar filtros
        df_filtrado = df_fresa.copy()
        if equipe_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Equipe'] == equipe_selecionada]
        if rodovia_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Rodovia'].str.contains(rodovia_selecionada, na=False)]
        if tipo_selecionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Tipo Fresa'] == tipo_selecionado]
        
        # Mostrar informações sobre o filtro
        st.info(f"📊 Mostrando {len(df_filtrado)} registros (de {len(df_fresa)} total)")
        
        if len(df_filtrado) == 0:
            st.warning("⚠️ Nenhum registro encontrado com os filtros selecionados.")
            
            # Mostrar combinações disponíveis
            st.markdown("### 💡 Sugestões de combinações disponíveis:")
            
            with st.expander("📋 Equipes e Rodovias disponíveis"):
                for equipe in df_fresa[df_fresa['Equipe'] != 'Não identificada']['Equipe'].unique():
                    df_equipe = df_fresa[df_fresa['Equipe'] == equipe]
                    rodovias_equipe = df_equipe[df_equipe['Rodovia'] != 'Não identificada']['Rodovia'].value_counts()
                    tipos_equipe = df_equipe['Tipo Fresa'].value_counts()
                    
                    st.write(f"**{equipe}**:")
                    st.write(f"  🛣️ Rodovias: {', '.join(rodovias_equipe.index) if len(rodovias_equipe) > 0 else 'Não identificada'}")
                    st.write(f"  📋 Tipos: {', '.join(tipos_equipe.index[:3])}{'...' if len(tipos_equipe) > 3 else ''}")
                    st.write("---")
            
            with st.expander("🎯 Combinações que têm dados:"):
                combinacoes = df_fresa[df_fresa['Equipe'] != 'Não identificada'].groupby(['Equipe', 'Rodovia']).size().reset_index(name='Contagem')
                combinacoes = combinacoes[combinacoes['Rodovia'] != 'Não identificada']
                
                if not combinacoes.empty:
                    for _, row in combinacoes.iterrows():
                        st.write(f"• {row['Equipe']} + {row['Rodovia']} = {row['Contagem']} registros")
                else:
                    st.write("Nenhuma combinação encontrada com dados válidos.")
        else:
            # Gráficos específicos para Fresagem e Recomposição
            st.markdown("---")
            st.markdown("### 📈 <span style='color: #00233B;'>Fresagem e Recomposição - Análise Detalhada</span>", unsafe_allow_html=True)
            
            # Gráfico por Equipe
            if equipe_selecionada == 'Todas':
                col_eq1, col_eq2 = st.columns(2)
                with col_eq1:
                    df_equipe = df_filtrado.groupby('Equipe')['Quantitativo'].sum().reset_index()
                    df_equipe = df_equipe[df_equipe['Equipe'] != 'Não identificada'].sort_values('Quantitativo', ascending=False)
                    
                    if not df_equipe.empty:
                        fig_equipe = px.bar(
                            df_equipe,
                            x='Equipe',
                            y='Quantitativo',
                            title="Quantitativo por Equipe",
                            text='Quantitativo',
                            color_discrete_sequence=['#00233B']
                        )
                        fig_equipe.update_xaxes(tickangle=45)
                        fig_equipe.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(color='#00233B', family='Poppins'))
                        # Aplicar fonte Poppins
                        fig_equipe.update_layout(
                            font_family='Poppins',
                            font_size=12,
                            title_font_size=16,
                            title_font_family='Poppins',
                            plot_bgcolor='#F2F1EF',
                            paper_bgcolor='#FFFFFF',
                            font_color='#00233B',
                            height=480,  # Aumento de 20% (400 -> 480)
                            margin=dict(l=140, r=140, t=120, b=120)  # Zoom reduzido em 10% adicional
                        )
                        # Aumentar eixo Y em +20 para enquadrar dados
                        y_max_equipe = df_equipe['Quantitativo'].max() + 20
                        fig_equipe.update_yaxes(range=[0, y_max_equipe])
                        fig_equipe.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                        fig_equipe.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                        st.plotly_chart(fig_equipe, use_container_width=True)
                
                with col_eq2:
                    df_rodovia = df_filtrado.groupby('Rodovia')['Quantitativo'].sum().reset_index()
                    df_rodovia = df_rodovia[df_rodovia['Rodovia'] != 'Não identificada'].sort_values('Quantitativo', ascending=False)
                    
                    if not df_rodovia.empty:
                        fig_rodovia = px.bar(
                            df_rodovia,
                            x='Rodovia',
                            y='Quantitativo',
                            title="Quantitativo por Rodovia",
                            text='Quantitativo',
                            color_discrete_sequence=['#00233B']
                        )
                        fig_rodovia.update_xaxes(tickangle=45)
                        fig_rodovia.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(color='#00233B', family='Poppins'))
                        # Aplicar fonte Poppins
                        fig_rodovia.update_layout(
                            font_family='Poppins',
                            font_size=12,
                            title_font_size=16,
                            title_font_family='Poppins',
                            plot_bgcolor='#F2F1EF',
                            paper_bgcolor='#FFFFFF',
                            font_color='#00233B',
                            height=480,  # Aumento de 20% (400 -> 480)
                            margin=dict(l=140, r=140, t=120, b=120)  # Zoom reduzido em 10% adicional
                        )
                        # Aumentar eixo Y em +50 para enquadrar dados (+15 + 35)
                        y_max_rodovia = df_rodovia['Quantitativo'].max() + 50
                        fig_rodovia.update_yaxes(range=[0, y_max_rodovia])
                        fig_rodovia.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                        fig_rodovia.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                        st.plotly_chart(fig_rodovia, use_container_width=True)
            
            # Lista por Tipo
            st.markdown("---")
            st.subheader("📋 Listas por Tipo de Ensaio")
            
            # Agrupar por Tipo Fresa
            df_tipos_lista = df_filtrado.groupby('Tipo Fresa').agg({
                'Quantitativo': 'sum',
                'Local': 'count'
            }).reset_index()
            df_tipos_lista.columns = ['Tipo de Ensaio', 'Total Quantitativo', 'Número de Registros']
            df_tipos_lista = df_tipos_lista.sort_values('Total Quantitativo', ascending=False)
            
            if not df_tipos_lista.empty:
                col_lista1, col_lista2 = st.columns(2)
                
                with col_lista1:
                    st.markdown("##### 📊 Resumo por Tipo")
                    for _, row in df_tipos_lista.iterrows():
                        st.markdown(f"""
                        <div style="font-family: 'Poppins', sans-serif; padding: 10px; margin: 5px 0; 
                                    background-color: #f0f2f6; border-radius: 8px; border-left: 4px solid #1f77b4;">
                            <strong style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #00233B;">{row['Tipo de Ensaio']}</strong><br>
                            <span style="font-family: 'Poppins', sans-serif; font-size: 0.9em; color: #00233B;">
                                📋 {row['Número de Registros']} registros | 📊 {row['Total Quantitativo']} total
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_lista2:
                    st.markdown("##### 📈 Gráfico por Tipo")
                    fig_lista = px.bar(
                        df_tipos_lista,
                        x='Tipo de Ensaio',
                        y='Total Quantitativo',
                        title="Quantitativo por Tipo de Ensaio",
                        text='Total Quantitativo',
                        color_discrete_sequence=['#00233B']
                    )
                    fig_lista.update_xaxes(tickangle=45)
                    fig_lista.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(color='#00233B', family='Poppins'))
                    # Aplicar fonte Poppins
                    fig_lista.update_layout(
                        font_family='Poppins',
                        font_size=12,
                        title_font_size=14,
                        title_font_family='Poppins',
                        height=400,
                        plot_bgcolor='#F2F1EF',
                        paper_bgcolor='#FFFFFF',
                        font_color='#00233B',
                        margin=dict(l=120, r=120, t=100, b=100)  # Zoom reduzido para melhor visualização
                    )
                    fig_lista.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                    fig_lista.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
                    st.plotly_chart(fig_lista, use_container_width=True)
                
                # Botão discreto para tabela detalhada por tipo
                if st.button("⋮", key="detalhes_fresa_tipo", help="Ver detalhes completos por tipo"):
                    with st.expander(f"📋 Detalhes completos por tipo", expanded=True):
                        # Para cada tipo, mostrar os registros
                        for tipo in df_filtrado['Tipo Fresa'].unique():
                            if tipo != 'Outros':  # Mostrar tipos principais primeiro
                                df_tipo = df_filtrado[df_filtrado['Tipo Fresa'] == tipo]
                                if not df_tipo.empty:
                                    st.markdown(f"""
                                    <div style="font-family: 'Poppins', sans-serif; margin: 15px 0 10px 0;">
                                        <h6 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #00233B; margin: 0;">
                                            📌 {tipo} ({len(df_tipo)} registros)
                                        </h6>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    display_cols = ['Local', 'Equipe', 'Rodovia', 'Mês/Ano', 'Arquivo', 'Quantitativo']
                                    st.dataframe(
                                        df_tipo[display_cols].sort_values(['Equipe', 'Mês/Ano']), 
                                        use_container_width=True,
                                        hide_index=True
                                    )
                                    st.markdown("---")
                    
                    # Mostrar "Outros" por último se existir
                    if 'Outros' in df_filtrado['Tipo Fresa'].values:
                        df_outros = df_filtrado[df_filtrado['Tipo Fresa'] == 'Outros']
                        if not df_outros.empty:
                            st.markdown(f"""
                            <div style="font-family: 'Poppins', sans-serif; margin: 15px 0 10px 0;">
                                <h6 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #00233B; margin: 0;">
                                    📌 Outros ({len(df_outros)} registros)
                                </h6>
                            </div>
                            """, unsafe_allow_html=True)
                            display_cols = ['Local', 'Equipe', 'Rodovia', 'Mês/Ano', 'Arquivo', 'Quantitativo']
                            st.dataframe(
                                df_outros[display_cols].sort_values(['Equipe', 'Mês/Ano']), 
                                use_container_width=True,
                                hide_index=True
                            )
            else:
                st.info("📋 Nenhum dado encontrado para listar por tipo.")

            # Botão discreto para tabela detalhada geral
            if st.button("⋮", key="detalhes_fresa_geral", help=f"Ver {len(df_filtrado)} registros filtrados"):
                with st.expander(f"📋 Registros Filtrados ({len(df_filtrado)} registros)", expanded=True):
                    display_cols = ['Local', 'Equipe', 'Rodovia', 'Mês/Ano', 'Arquivo', 'Tipo Fresa', 'Quantitativo']
                    st.dataframe(df_filtrado[display_cols].sort_values(['Equipe', 'Mês/Ano']), use_container_width=True)

    with tabs[1]:
        df_usinagem = df[df['Frente de Serviço'] == 'USINAGEM']
        
        # Create subtabs for each usina - remover números da frente
        def limpar_nome_usina(nome):
            import re
            # Remover números e pontos do início (ex: "01." -> "")
            return re.sub(r'^\d+\.?\s*', '', nome.strip())
        
        usinas = ['Todos'] + sorted([limpar_nome_usina(usina) for usina in df_usinagem['Local'].unique() if usina != 'USINAS'])
        subtabs_usinas = st.tabs(usinas)
        
        for i, usina in enumerate(usinas):
            with subtabs_usinas[i]:
                if usina == 'Todos':
                    render_secao("USINAS - Todas", df_usinagem)
                else:
                    # Encontrar o nome original no dataframe para filtrar
                    nome_original = next((loc for loc in df_usinagem['Local'].unique() 
                                       if limpar_nome_usina(loc) == usina), usina)
                    df_usina_individual = df_usinagem[df_usinagem['Local'] == nome_original]
                    render_secao(f"USINA - {usina}", df_usina_individual)

    with tabs[2]:
        df_pavimento = df[df['Frente de Serviço'] == 'PAVIMENTO_RIGIDO'].copy()
        # Treat everything in concrete layer as Checklist Concreto
        df_pavimento['Tipo Arquivo'] = 'Checklist Concreto'
        render_secao("Pavimento Rígido", df_pavimento)

    with tabs[3]:
        df_micro = df[df['Frente de Serviço'] == 'MICROREVESTIMENTO']
        render_secao("Microrevestimento", df_micro)

    with tabs[4]:
        st.markdown("---")
        st.subheader("📊 Resumo Geral de Todas as Frentes de Serviço")
        
        # Estatísticas gerais
        col_total, col_camadas, col_tipos = st.columns(3)
        
        with col_total:
            st.metric("📁 Total de Registros", len(df))
        
        with col_camadas:
            camadas_count = df['Frente de Serviço'].nunique()
            st.metric("🏗️ Frentes de Serviço", camadas_count)
        
        with col_tipos:
            tipos_count = df['Tipo Arquivo'].nunique()
            st.metric("📋 Tipos de Arquivo", tipos_count)
        
        # Gráfico por camada
        df_camadas = df.groupby('Frente de Serviço')['Quantitativo'].sum().reset_index()
        fig_camadas = px.bar(
            df_camadas.sort_values('Quantitativo', ascending=False),
            x='Frente de Serviço',
            y='Quantitativo',
            title="Quantitativo por Frente de Serviço",
            text='Quantitativo',
            color_discrete_sequence=['#00233B']
        )
        fig_camadas.update_xaxes(tickangle=45, tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
        fig_camadas.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(color='#00233B', family='Poppins'))
        fig_camadas.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'), title_font=dict(color='#00233B', family='Poppins'))
        # Aplicar fonte Poppins
        fig_camadas.update_layout(
            font_family='Poppins',
            font_size=12,
            title_font_size=16,
            title_font_family='Poppins',
            plot_bgcolor='#F2F1EF',
            paper_bgcolor='#FFFFFF',
            font_color='#00233B',
            margin=dict(l=80, r=80, t=80, b=80)  # Zoom -10% (aumentar margens)
        )
        fig_camadas.update_xaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'))
        fig_camadas.update_yaxes(tickfont=dict(family='Poppins', size=10, color='#00233B'))
        st.plotly_chart(fig_camadas, use_container_width=True)
        
        # Botão discreto para tabela resumo
        if st.button("⋮", key="detalhes_resumo_geral", help="Ver dados detalhados de todas as frentes"):
            with st.expander("📋 Dados Detalhados - Todas as Frentes de Serviço", expanded=True):
                st.dataframe(df[['Frente de Serviço', 'Local', 'Mês/Ano', 'Arquivo', 'Tipo Arquivo', 'Quantitativo']].sort_values(['Frente de Serviço', 'Local', 'Mês/Ano']), use_container_width=True)

else:
    st.error("❌ Não foi possível carregar os dados. Verifique o arquivo Excel e tente novamente.")
