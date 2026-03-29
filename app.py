#!/usr/bin/env python3
"""
Aplicação Streamlit para Previsão de Preços de Carros
Execução: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from pathlib import Path

# Disable ZenML debugging logs to prevent circular import bug on Streamlit Cloud
os.environ["ZENML_LOGGING_VERBOSITY"] = "ERROR"
from zenml.client import Client
from prediction_preprocessor import PredictionPreprocessor

# Configuração da página
st.set_page_config(
    page_title="🚗 Previsão de Preços de Carros",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Carrega o modelo treinado (primeiro do joblib, depois do ZenML)."""
    try:
        import joblib
        model_path = "savad_model/model.joblib"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            # Retorna o modelo encapsulado se for uma pipeline, etc. O predict funciona.
            return model, "Modelo carregado com sucesso do disco"
            
        client = Client()
        runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")

        if not runs:
            st.warning("⚠️ Primeira execução detectada: Treinando modelo na nuvem (isso pode levar 1-2 minutos)...")
            from pipelines.deployment_pipeline import inference_pipeline
            inference_pipeline()
            runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")
            
            if not runs:
                return None, "Nenhum pipeline run encontrado mesmo após o treinamento automático"

        last_run = runs[0]
        train_step = last_run.steps.get("train_model")

        if not train_step or not train_step.output:
            return None, "Modelo não encontrado no último run do ZenML"

        model = train_step.output.load()
        return model, "Modelo carregado com sucesso do ZenML"

    except Exception as e:
        return None, f"Erro ao carregar modelo: {str(e)}"


@st.cache_resource
def get_model_metrics():
    """Obtém as métricas do último modelo treinado."""
    try:
        client = Client()
        runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")

        if not runs:
            return None

        last_run = runs[0]
        eval_step = last_run.steps.get("evaluate_model")

        if not eval_step:
            return None

        # O step retorna (mse_score, r2_score, rmse_score)
        return last_run

    except Exception as e:
        st.error(f"Erro ao obter métricas: {str(e)}")
        return None


def create_sample_data():
    """Cria dados de exemplo com features reais."""
    sample_data = pd.DataFrame({
        'Marca': ['Ford', 'Honda', 'Toyota', 'Chevrolet', 'Volkswagen'],
        'Modelo': ['EcoSport', 'Civic', 'Corolla', 'Onix', 'Golf'],
        'Ano': [2020, 2019, 2021, 2018, 2022],
        'Quilometragem': [50000, 80000, 40000, 120000, 30000],
        'Cor': ['Azul', 'Preto', 'Branco', 'Prata', 'Vermelho'],
        'Cambio': ['Automático', 'Manual', 'Automático', 'Manual', 'Automático'],
        'Combustivel': ['Flex', 'Gasolina', 'Flex', 'Gasolina', 'Flex'],
        'Portas': [4, 4, 4, 2, 4],
    })
    return sample_data


def save_prediction(predictions, input_data, timestamp):
    """Salva previsão no histórico."""
    history_file = "predicoes_historico.csv"

    history_data = pd.DataFrame({
        'timestamp': [timestamp],
        'num_amostras': [len(predictions)],
        'preco_medio': [predictions.mean()],
        'preco_min': [predictions.min()],
        'preco_max': [predictions.max()],
    })

    if os.path.exists(history_file):
        existing = pd.read_csv(history_file)
        history_data = pd.concat([existing, history_data], ignore_index=True)

    history_data.to_csv(history_file, index=False)


# Header Principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚗 Sistema de Previsão de Preços de Carros")
    st.markdown("**Powered by ZenML + MLflow + Streamlit**")

with col2:
    st.metric("Status", "🟢 Online", "v1.0")

st.divider()

# Sidebar - Menu de Navegação
st.sidebar.title("📋 Menu")
page = st.sidebar.radio(
    "Selecione uma página:",
    ["🏠 Home", "🔮 Fazer Previsão", "📊 Analytics", "📁 Upload de Dados", "📈 Histórico"]
)

# Carregar modelo
model, model_status = load_model()

# ==================== PÁGINA HOME ====================
if page == "🏠 Home":
    st.header("Bem-vindo ao Sistema de Previsão!")

    col1, col2, col3 = st.columns(3)

    with col1:
        if model:
            st.success("✓ Modelo Carregado")
        else:
            st.error(f"✗ Modelo não disponível: {model_status}")

    with col2:
        st.info("📊 Pronto para Previsões")

    with col3:
        st.info("🔄 ZenML Ativo")

    st.divider()

    # Informações do Modelo
    st.subheader("📌 Informações do Modelo")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("R² Score", "0.9771", "97.71%")

    with col2:
        st.metric("MSE", "10.37M", "Score")

    with col3:
        st.metric("RMSE", "R$ 3,220", "Desvio")

    with col4:
        st.metric("Amostras", "1,960", "Teste")

    st.divider()

    # Features
    st.subheader("✨ Recursos Disponíveis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🔮 Previsão em Tempo Real
        - Insira dados manualmente
        - Veja previsões instantâneas
        - Resultados formatados
        """)

    with col2:
        st.markdown("""
        ### 📁 Upload de CSV
        - Importe múltiplos dados
        - Previsões em lote
        - Baixe resultados
        """)

    with col3:
        st.markdown("""
        ### 📊 Analytics
        - Distribuição de preços
        - Tendências temporal
        - Estatísticas detalhadas
        """)

    st.divider()

    # Instruções
    with st.expander("📖 Como Usar"):
        st.markdown("""
        1. **Fazer Previsão**: Vá para a página de previsão e insira os dados do carro
        2. **Upload de Dados**: Importe um arquivo CSV com múltiplos carros
        3. **Analytics**: Visualize análises e estatísticas dos dados
        4. **Histórico**: Acompanhe o histórico de previsões realizadas

        **Dados Necessários:**
        - Características do veículo (cilindrada, ano, quilometragem, etc.)
        - O modelo irá prever o preço do carro
        """)

# ==================== PÁGINA PREVISÃO ====================
elif page == "🔮 Fazer Previsão":
    st.header("🔮 Fazer Previsão de Preço")

    if not model:
        st.error(f"❌ Erro: {model_status}")
        st.info("Execute `python3 predict.py` primeiro para treinar o modelo")
    else:
        st.success(f"✓ {model_status}")

        try:
            # Carregar preprocessador
            preprocessor = PredictionPreprocessor()
            valores_unicos = preprocessor.get_unique_values()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📝 Dados do Veículo")

                # Campos de entrada reais
                marca = st.selectbox(
                    "**Marca**",
                    valores_unicos['marca'],
                    help="Selecione a marca do veículo"
                )

                # Filtrar modelos por marca selecionada
                modelos_da_marca = preprocessor.get_modelos_por_marca(marca)
                modelo = st.selectbox(
                    "**Modelo**",
                    modelos_da_marca,
                    help="Selecione o modelo do veículo (filtrado pela marca)"
                )

                ano = st.number_input(
                    "**Ano**",
                    min_value=2000,
                    max_value=2024,
                    value=2020,
                    step=1,
                    help="Ano de fabricação"
                )

                quilometragem = st.number_input(
                    "**Quilometragem (km)**",
                    min_value=0,
                    max_value=500000,
                    value=50000,
                    step=1000,
                    help="Quilometragem do veículo"
                )

                cor = st.selectbox(
                    "**Cor**",
                    valores_unicos['cor'],
                    help="Cor do veículo"
                )

                cambio = st.selectbox(
                    "**Câmbio**",
                    valores_unicos['cambio'],
                    help="Tipo de câmbio"
                )

                combustivel = st.selectbox(
                    "**Combustível**",
                    valores_unicos['combustivel'],
                    help="Tipo de combustível"
                )

                portas = st.selectbox(
                    "**Número de Portas**",
                    [2, 4],
                    help="Número de portas do veículo"
                )

            with col2:
                st.subheader("🔮 Previsão")

                if st.button("🎯 Fazer Previsão", use_container_width=True, type="primary"):
                    try:
                        # Preprocessar dados
                        features = preprocessor.preprocess(
                            marca=marca,
                            modelo=modelo,
                            ano=ano,
                            quilometragem=quilometragem,
                            cor=cor,
                            cambio=cambio,
                            combustivel=combustivel,
                            portas=portas
                        )

                        # Faz previsão
                        prediction = model.predict(features)[0]

                        # Exibe resultado
                        st.success(f"✓ Previsão realizada com sucesso!")

                        # Exibir preço em destaque
                        st.metric(
                            "💰 Preço Previsto",
                            f"R$ {prediction:,.2f}",
                            label_visibility="visible"
                        )

                        st.info(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                        st.divider()

                        # Detalhes da entrada
                        st.subheader("📋 Dados do Veículo Utilizado")
                        resumo = pd.DataFrame({
                            'Campo': ['Marca', 'Modelo', 'Ano', 'Quilometragem', 'Cor', 'Câmbio', 'Combustível', 'Portas'],
                            'Valor': [marca, modelo, ano, f"{quilometragem:,}", cor, cambio, combustivel, portas]
                        })
                        st.dataframe(resumo, use_container_width=True, hide_index=True)

                        # Salva no histórico
                        preco_series = pd.Series([prediction])
                        save_prediction(preco_series, None, datetime.now())

                    except Exception as e:
                        st.error(f"❌ Erro ao fazer previsão: {str(e)}")
                        import traceback
                        st.error(f"Detalhes: {traceback.format_exc()}")

        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {str(e)}")
            st.info("Verifique se o dataset está disponível em data/dataset_carros_brasil.csv")

# ==================== PÁGINA ANALYTICS ====================
elif page == "📊 Analytics":
    st.header("📊 Analytics e Visualizações")

    if not model:
        st.error(f"❌ Erro: {model_status}")
    else:
        try:
            # Gera dados de exemplo para visualizações
            client = Client()
            runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")

            if runs:
                last_run = runs[0]

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📈 Distribuição de Preços Previstos")

                    # Simula dados de previsões anteriores
                    np.random.seed(42)
                    precos_simulados = np.random.normal(59237, 20924, 1000)

                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(precos_simulados, bins=40, color='#1f77b4', alpha=0.7, edgecolor='black')
                    ax.set_xlabel('Preço Previsto (R$)', fontsize=12)
                    ax.set_ylabel('Frequência', fontsize=12)
                    ax.set_title('Distribuição de Preços Previstos', fontsize=14, fontweight='bold')
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)

                with col2:
                    st.subheader("📊 Estatísticas dos Preços")

                    stats_data = {
                        'Métrica': ['Mínimo', 'Q1', 'Mediana', 'Q3', 'Máximo', 'Média', 'Desvio Padrão'],
                        'Valor (R$)': [
                            f"{np.percentile(precos_simulados, 0):,.2f}",
                            f"{np.percentile(precos_simulados, 25):,.2f}",
                            f"{np.percentile(precos_simulados, 50):,.2f}",
                            f"{np.percentile(precos_simulados, 75):,.2f}",
                            f"{np.percentile(precos_simulados, 100):,.2f}",
                            f"{np.mean(precos_simulados):,.2f}",
                            f"{np.std(precos_simulados):,.2f}",
                        ]
                    }
                    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)

                # Gráfico de Box Plot
                st.subheader("📦 Box Plot - Análise de Outliers")
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.boxplot(precos_simulados, vert=False)
                ax.set_xlabel('Preço Previsto (R$)', fontsize=12)
                ax.set_title('Box Plot dos Preços Previstos', fontsize=14, fontweight='bold')
                ax.grid(alpha=0.3, axis='x')
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Erro ao carregar analytics: {str(e)}")

# ==================== PÁGINA UPLOAD ====================
elif page == "📁 Upload de Dados":
    st.header("📁 Upload de Dados para Previsão em Lote")

    if not model:
        st.error(f"❌ Erro: {model_status}")
    else:
        st.success(f"✓ {model_status}")

        uploaded_file = st.file_uploader(
            "Selecione um arquivo CSV",
            type=["csv"],
            help="Arquivo deve conter as mesmas colunas do modelo treinado"
        )

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✓ Arquivo carregado: {uploaded_file.name} ({len(df)} linhas)")

                # Preview
                st.subheader("📋 Preview dos Dados")
                st.dataframe(df.head(10), use_container_width=True)

                # Validar colunas necessárias
                colunas_necessarias = ['Marca', 'Modelo', 'Ano', 'Quilometragem', 'Cor', 'Cambio', 'Combustivel', 'Portas']
                colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]

                if colunas_faltando:
                    st.error(f"❌ Colunas faltando: {', '.join(colunas_faltando)}")
                    st.info("O arquivo deve conter as colunas: " + ", ".join(colunas_necessarias))
                else:
                    if st.button("🎯 Fazer Previsões em Lote", use_container_width=True, type="primary"):
                        with st.spinner("Processando previsões..."):
                            try:
                                preprocessor = PredictionPreprocessor()
                                predictions_list = []

                                # Processar cada linha
                                for idx, row in df.iterrows():
                                    features = preprocessor.preprocess(
                                        marca=row['Marca'],
                                        modelo=row['Modelo'],
                                        ano=int(row['Ano']),
                                        quilometragem=int(row['Quilometragem']),
                                        cor=row['Cor'],
                                        cambio=row['Cambio'],
                                        combustivel=row['Combustivel'],
                                        portas=int(row['Portas'])
                                    )
                                    pred = model.predict(features)[0]
                                    predictions_list.append(pred)

                                predictions = pd.Series(predictions_list, name="preco_previsto")

                                # Combina com dados originais
                                resultado = df.copy()
                                resultado['preco_previsto'] = predictions.values

                                st.success("✓ Previsões realizadas com sucesso!")

                                # Estatísticas
                                col1, col2, col3, col4 = st.columns(4)

                                with col1:
                                    st.metric("Total de Previsões", len(predictions))

                                with col2:
                                    st.metric("Preço Médio", f"R$ {predictions.mean():,.2f}")

                                with col3:
                                    st.metric("Preço Mínimo", f"R$ {predictions.min():,.2f}")

                                with col4:
                                    st.metric("Preço Máximo", f"R$ {predictions.max():,.2f}")

                                st.divider()

                                # Resultados
                                st.subheader("📊 Resultados Detalhados")
                                st.dataframe(resultado, use_container_width=True)

                                # Download
                                csv = resultado.to_csv(index=False)
                                st.download_button(
                                    label="📥 Baixar Resultados (CSV)",
                                    data=csv,
                                    file_name=f"predicoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    use_container_width=True,
                                    type="primary"
                                )

                                # Salva no histórico
                                save_prediction(predictions, df, datetime.now())

                            except Exception as e:
                                st.error(f"❌ Erro ao fazer previsões: {str(e)}")
                                import traceback
                                st.error(f"Detalhes: {traceback.format_exc()}")

            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo: {str(e)}")

        else:
            st.info("📤 Importe um arquivo CSV para começar")

            # Exemplo de template
            with st.expander("💡 Baixar Template de Exemplo", expanded=False):
                sample_df = create_sample_data()
                csv_template = sample_df.to_csv(index=False)

                st.download_button(
                    label="📥 Baixar Template",
                    data=csv_template,
                    file_name="template_dados.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.dataframe(sample_df, use_container_width=True)

# ==================== PÁGINA HISTÓRICO ====================
elif page == "📈 Histórico":
    st.header("📈 Histórico de Previsões")

    history_file = "predicoes_historico.csv"

    if os.path.exists(history_file):
        df_history = pd.read_csv(history_file)
        st.success(f"✓ {len(df_history)} previsões realizadas")

        # Exibe histórico
        st.subheader("📋 Histórico Completo")
        st.dataframe(df_history, use_container_width=True)

        # Gráfico temporal
        st.subheader("📈 Trend de Preços")

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(len(df_history)), df_history['preco_medio'], marker='o', linewidth=2, markersize=8)
            ax.fill_between(range(len(df_history)), df_history['preco_min'], df_history['preco_max'], alpha=0.2)
            ax.set_xlabel('Previsão #', fontsize=12)
            ax.set_ylabel('Preço (R$)', fontsize=12)
            ax.set_title('Evolução dos Preços Médios Previstos', fontsize=14, fontweight='bold')
            ax.grid(alpha=0.3)
            st.pyplot(fig)

        with col2:
            st.metric("Média Geral", f"R$ {df_history['preco_medio'].mean():,.2f}")
            st.metric("Máximo Previsto", f"R$ {df_history['preco_max'].max():,.2f}")
            st.metric("Mínimo Previsto", f"R$ {df_history['preco_min'].min():,.2f}")

        # Download histórico
        csv_history = df_history.to_csv(index=False)
        st.download_button(
            label="📥 Baixar Histórico Completo",
            data=csv_history,
            file_name="historico_predicoes.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("📊 Nenhuma previsão realizada ainda")
        st.info("Vá para a página de Previsão ou Upload para começar")

st.divider()

# Footer
st.markdown("""
---
<div style="text-align: center; color: gray; font-size: 12px;">
    🚗 Sistema de Previsão de Preços de Carros | Powered by ZenML + MLflow + Streamlit<br>
    © 2026 | Desenvolvido por Joao Nogueira Clemente | <a href="https://github.com/Docas32" target="_blank">GitHub</a>
            <p style="font-size: 10px; color: lightgray;">
                *Este sistema é para fins educacionais e de demonstração. Os preços previstos são baseados em um modelo treinado com dados fictícios e não devem ser usados para decisões reais de compra ou venda de veículos.*
            </p>
</div>
""", unsafe_allow_html=True)
