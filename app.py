import streamlit as st
import pandas as pd
import os
import re
from difflib import SequenceMatcher
from datetime import datetime
import numpy as np
from pathlib import Path
import warnings
import tempfile
import shutil
from io import BytesIO
import base64
warnings.filterwarnings('ignore')

class QuantitativoWebAnalyzer:
    def __init__(self):
        self.resultados = []
        self.arquivos_processados = set()
        
        # Configurações para Cloud Run (sem paths locais)
        self.paths_configured = False
        
    def configure_paths(self, uploaded_files):
        """Configura paths baseado nos arquivos uploaded"""
        if uploaded_files:
            self.paths_configured = True
            return True
        return False
    
    def process_uploaded_files(self, uploaded_files):
        """Processa arquivos uploaded via interface web"""
        st.info("📁 Processando arquivos enviados...")
        
        total_registros = 0
        
        for uploaded_file in uploaded_files:
            try:
                # Salva arquivo temporariamente
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                
                # Processa o arquivo
                registros = self.processar_arquivo(tmp_path, uploaded_file.name)
                total_registros += registros
                
                # Remove arquivo temporário
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar {uploaded_file.name}: {str(e)}")
        
        return total_registros
    
    def processar_arquivo(self, caminho_arquivo, nome_arquivo):
        """Versão simplificada do processamento para web"""
        try:
            # Lê todas as abas do Excel
            excel_file = pd.ExcelFile(caminho_arquivo)
            contador_abas = 0
            
            for nome_aba in excel_file.sheet_names:
                try:
                    df = pd.read_excel(caminho_arquivo, sheet_name=nome_aba)
                    
                    if not df.empty:
                        # Adiciona resultado simplificado
                        self.resultados.append({
                            'Arquivo': nome_arquivo,
                            'Aba': nome_aba,
                            'Quantitativo': len(df),
                            'Path Completo': f"Uploaded/{nome_arquivo}",
                            'Local': 'Web Upload',
                            'Mês/Ano': datetime.now().strftime("%m/%Y"),
                            'Tipo Arquivo': nome_aba,
                            'Data Processamento': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        contador_abas += 1
                        
                except Exception as e:
                    continue
            
            return contador_abas
            
        except Exception as e:
            st.error(f"Erro ao ler arquivo {nome_arquivo}: {str(e)}")
            return 0
    
    def gerar_excel_consolidado(self):
        """Gera Excel consolidado para download"""
        if not self.resultados:
            return None
        
        df = pd.DataFrame(self.resultados)
        
        # Cria arquivo em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Consolidados', index=False)
        
        output.seek(0)
        return output
    
    def gerar_excel_power_bi(self):
        """Gera Excel Power BI para download"""
        if not self.resultados:
            return None
        
        df = pd.DataFrame(self.resultados)
        
        # Adiciona colunas derivadas
        df['Ano'] = df['Mês/Ano'].apply(lambda x: str(x).split('/')[-1] if '/' in str(x) else '2024')
        df['Mês'] = df['Mês/Ano'].apply(lambda x: str(x).split('/')[0] if '/' in str(x) else '01')
        df['Período'] = df['Ano'] + '-' + df['Mês'].str.zfill(2)
        df['Frente de Serviço'] = 'Upload Web'
        df['Status'] = 'Ativo'
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Aba 1: Dados Completos
            df.to_excel(writer, sheet_name='Dados_Completos', index=False)
            
            # Aba 2: Resumo
            resumo = df.groupby('Arquivo')['Quantitativo'].sum().reset_index()
            resumo.to_excel(writer, sheet_name='Resumo', index=False)
        
        output.seek(0)
        return output

def main():
    st.set_page_config(
        page_title="EPR IGUAÇU - Analyzer Web",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏗️ EPR IGUAÇU - Quantitativo Analyzer Web")
    st.markdown("---")
    
    # Inicializa analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = QuantitativoWebAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Sidebar
    st.sidebar.header("📋 Configurações")
    
    # Upload de arquivos
    st.sidebar.subheader("📁 Upload de Arquivos Excel")
    uploaded_files = st.sidebar.file_uploader(
        "Envie os arquivos Excel para análise",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos Excel para processar"
    )
    
    # Botão de processamento
    if st.sidebar.button("🚀 Processar Arquivos", type="primary"):
        if uploaded_files:
            with st.spinner("Processando arquivos..."):
                total_registros = analyzer.process_uploaded_files(uploaded_files)
                analyzer.configure_paths(uploaded_files)
                st.success(f"✅ Processados {total_registros} registros de {len(uploaded_files)} arquivos!")
        else:
            st.error("❌ Por favor, envie pelo menos um arquivo Excel")
    
    # Área principal
    if analyzer.resultados:
        st.header("📊 Resultados da Análise")
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📁 Total de Registros", len(analyzer.resultados))
        
        with col2:
            st.metric("📋 Arquivos Processados", len(set(r['Arquivo'] for r in analyzer.resultados)))
        
        with col3:
            st.metric("📊 Total de Abas", sum(r['Quantitativo'] for r in analyzer.resultados))
        
        with col4:
            st.metric("📅 Data Processamento", datetime.now().strftime("%d/%m/%Y"))
        
        # Tabela de resultados
        st.subheader("📋 Detalhes dos Arquivos Processados")
        df_resultados = pd.DataFrame(analyzer.resultados)
        st.dataframe(df_resultados, use_container_width=True)
        
        # Downloads
        st.header("⬇️ Downloads dos Relatórios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Excel Consolidado")
            excel_consolidado = analyzer.gerar_excel_consolidado()
            if excel_consolidado:
                st.download_button(
                    label="📥 Baixar Excel Consolidado",
                    data=excel_consolidado.getvalue(),
                    file_name=f"quantitativo_consolidado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            st.subheader("🔋 Excel Power BI")
            excel_power_bi = analyzer.gerar_excel_power_bi()
            if excel_power_bi:
                st.download_button(
                    label="📥 Baixar Excel Power BI",
                    data=excel_power_bi.getvalue(),
                    file_name=f"quantitativo_power_bi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        # Gráficos
        st.header("📈 Visualizações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Quantitativo por Arquivo")
            df_arquivos = df_resultados.groupby('Arquivo')['Quantitativo'].sum().reset_index()
            st.bar_chart(df_arquivos.set_index('Arquivo'))
        
        with col2:
            st.subheader("📋 Registros por Aba")
            df_abas = df_resultados.groupby('Aba')['Quantitativo'].sum().reset_index()
            st.bar_chart(df_abas.set_index('Aba'))
    
    else:
        st.info("👆 Envie os arquivos Excel na barra lateral e clique em 'Processar Arquivos' para começar a análise.")
        
        # Instruções
        st.markdown("""
        ## 📋 Como Usar:
        
        1. **Upload**: Na barra lateral, envie um ou mais arquivos Excel (.xlsx, .xls)
        2. **Processar**: Clique no botão "Processar Arquivos"
        3. **Analisar**: Visualize os resultados e gráficos
        4. **Download**: Baixe os relatórios em Excel
        
        ## 📊 Relatórios Gerados:
        
        - **Excel Consolidado**: Todos os dados processados
        - **Excel Power BI**: Otimizado para análise no Power BI
        
        ## 🔧 Funcionalidades:
        
        - ✅ Processamento múltiplos arquivos
        - ✅ Análise automática de abas
        - ✅ Geração de relatórios
        - ✅ Visualizações interativas
        - ✅ Downloads instantâneos
        """)

if __name__ == "__main__":
    main()
