#!/bin/bash

# Script de deploy para diferentes plataformas
# Uso: ./deploy.sh [streamlit|railway|huggingface|docker-local]

set -e

DEPLOY_TYPE=${1:-streamlit}
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "════════════════════════════════════════════════════════════"
echo "🚀 Deploy: Preços de Carros"
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar dependências
check_deps() {
    local missing=()

    if ! command -v git &> /dev/null; then
        missing+=("git")
    fi

    if [[ ! -f "$PROJECT_DIR/.gitignore" ]]; then
        echo "⚠️  .gitignore não encontrado. Criando..."
        cp /dev/null "$PROJECT_DIR/.gitignore"
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        echo "❌ Erro: Ferramentas faltando: ${missing[*]}"
        exit 1
    fi

    echo "✅ Dependências verificadas"
}

# Deploy Streamlit Cloud
deploy_streamlit() {
    echo ""
    echo "📁 Preparando para Streamlit Cloud..."
    echo ""

    check_deps

    # Verificar se é um repo git
    if [[ ! -d "$PROJECT_DIR/.git" ]]; then
        echo "🔧 Inicializando repositório Git..."
        cd "$PROJECT_DIR"
        git init
        git add .
        git commit -m "Initial commit - Preços de Carros"
        echo ""
        echo "⚠️  Você precisa fazer push para GitHub!"
        echo ""
        echo "Passos:"
        echo "1. Crie um repositório em: https://github.com/new"
        echo "2. Execute:"
        echo "   git remote add origin https://github.com/SEU_USUARIO/precos-carros.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo ""
        echo "3. Acesse: https://share.streamlit.io/"
        echo "4. Clique 'New app' e selecione seu repositório"
        exit 0
    fi

    # Verificar se há mudanças
    if [[ -n $(cd "$PROJECT_DIR" && git status -s) ]]; then
        echo "📝 Commit mudanças..."
        cd "$PROJECT_DIR"
        git add .
        git commit -m "Deploy update $(date '+%Y-%m-%d %H:%M:%S')"
    fi

    echo ""
    echo "✅ Pronto para Streamlit Cloud!"
    echo ""
    echo "Próximos passos:"
    echo "1. Certifique-se que o código foi pushado:"
    echo "   git push"
    echo ""
    echo "2. Acesse: https://share.streamlit.io/"
    echo "3. Clique 'New app'"
    echo "4. Selecione seu repositório GitHub"
    echo "5. Pronto! 🎉"
}

# Deploy Docker Local
deploy_docker_local() {
    echo ""
    echo "🐳 Build e run no Docker localmente..."
    echo ""

    if ! command -v docker &> /dev/null; then
        echo "❌ Erro: Docker não está instalado"
        echo "Instale em: https://www.docker.com/get-started"
        exit 1
    fi

    cd "$PROJECT_DIR"

    echo "📦 Build image..."
    docker build -t precos-carros:latest .

    echo ""
    echo "🚀 Iniciando container..."
    docker run -p 8501:8501 -v "$PROJECT_DIR":/app precos-carros:latest
}

# Deploy Railway
deploy_railway() {
    echo ""
    echo "🚂 Preparando para Railway..."
    echo ""

    check_deps

    echo "📋 Checklist:"
    echo "[ ] Conta criada em: https://railway.app/"
    echo "[ ] Conectado com GitHub"
    echo "[ ] Código no GitHub"
    echo ""

    if [[ ! -f "$PROJECT_DIR/Procfile" ]]; then
        echo "❌ Procfile não encontrado!"
        exit 1
    fi

    echo "✅ Pronto para Railway!"
    echo ""
    echo "Próximos passos:"
    echo "1. Acesse: https://railway.app/dashboard"
    echo "2. Clique 'New Project'"
    echo "3. Selecione 'Deploy from GitHub'"
    echo "4. Selecione seu repositório"
    echo "5. Railway faz deploy automaticamente! 🎉"
}

# Deploy HuggingFace Spaces
deploy_huggingface() {
    echo ""
    echo "🤗 Preparando para HuggingFace Spaces..."
    echo ""

    check_deps

    echo "📋 Checklist:"
    echo "[ ] Conta criada em: https://huggingface.co/"
    echo "[ ] Git LFS instalado"
    echo ""

    if ! command -v git-lfs &> /dev/null; then
        echo "⚠️  Aviso: Git LFS não instalado"
        echo "Instale com: apt-get install git-lfs"
    fi

    echo "✅ Pronto para HuggingFace Spaces!"
    echo ""
    echo "Próximos passos:"
    echo "1. Crie um Space em: https://huggingface.co/spaces"
    echo "2. Selecione SDK: Docker"
    echo "3. Clone o repositório"
    echo "4. Copie arquivos para o Space"
    echo "5. Git push"
    echo "6. Deploy automático! 🎉"
}

# Main
case $DEPLOY_TYPE in
    streamlit)
        deploy_streamlit
        ;;
    railway)
        deploy_railway
        ;;
    huggingface)
        deploy_huggingface
        ;;
    docker-local)
        deploy_docker_local
        ;;
    *)
        echo "❌ Tipo de deploy inválido: $DEPLOY_TYPE"
        echo ""
        echo "Opções disponíveis:"
        echo "  streamlit      - Deploy no Streamlit Cloud (RECOMENDADO)"
        echo "  railway        - Deploy no Railway"
        echo "  huggingface    - Deploy no HuggingFace Spaces"
        echo "  docker-local   - Build e run Docker localmente"
        echo ""
        echo "Uso: $0 [streamlit|railway|huggingface|docker-local]"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Script concluído!"
echo "════════════════════════════════════════════════════════════"
