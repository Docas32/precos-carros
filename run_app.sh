#!/bin/bash
# Script para iniciar a aplicação Streamlit

echo "🚗 Iniciando Aplicação de Previsão de Preços de Carros..."
echo ""

# Ativa ambiente virtual
source .venv/bin/activate

# Verifica se o modelo foi treinado
if [ ! -f "predicoes.csv" ]; then
    echo "⚠️  Modelo não encontrado. Treinando modelo..."
    python3 predict.py > /dev/null 2>&1
    echo "✓ Modelo treinado!"
    echo ""
fi

# Inicia Streamlit
echo "✓ Iniciando servidor Streamlit..."
echo "📱 Acesse em: http://localhost:8501"
echo ""

streamlit run app.py
