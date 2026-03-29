#!/bin/bash

# Setup.sh - Configurar projeto para GitHub e deploy
# Uso: ./setup_github.sh SEU_USUARIO

set -e

if [ -z "$1" ]; then
    echo "❌ Erro: Usuário GitHub não fornecido"
    echo "Uso: ./setup_github.sh seu_usuario_github"
    exit 1
fi

GITHUB_USER="$1"
REPO_NAME="precos-carros"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "════════════════════════════════════════════════════════════"
echo "🔧 Setup GitHub - Preços de Carros"
echo "════════════════════════════════════════════════════════════"
echo ""

# 1. Verificar se git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado"
    echo "Instale com: apt-get install git"
    exit 1
fi

echo "✅ Git detectado"
echo ""

# 2. Configurar git
echo "⚙️  Configurando Git..."
git config --global user.name "${GITHUB_USER}" 2>/dev/null || true
git config --global user.email "${GITHUB_USER}@users.noreply.github.com" 2>/dev/null || true
echo "✅ Git configurado"
echo ""

# 3. Inicializar repositório
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_DIR"

if [[ ! -d .git ]]; then
    echo "📁 Inicializando repositório Git..."
    git init
    echo "✅ Repositório inicializado"
else
    echo "✅ Repositório Git já existe"
fi

echo ""

# 4. Adicionar .gitignore (se não existir)
if [[ ! -f .gitignore ]]; then
    echo "📝 Criando .gitignore..."
    cat > .gitignore << 'EOF'
.venv/
venv/
env/
*.pyc
__pycache__/
.env
.env.local
secrets.toml
.streamlit/cache/
mlruns/
.zen/
*.db
*.log
.DS_Store
.idea/
.vscode/
EOF
    echo "✅ .gitignore criado"
else
    echo "✅ .gitignore já existe"
fi

echo ""

# 5. Adicionar todos os arquivos
echo "📝 Preparando arquivos..."
git add .
echo "✅ Arquivos preparados"
echo ""

# 6. Primeiro commit
if [[ -z $(git status -s) ]]; then
    echo "✅ Nenhuma mudança para commitar"
else
    echo "💾 Fazendo primeiro commit..."
    git commit -m "Initial commit: Preços de Carros Streamlit App" || true
    echo "✅ Primeiro commit realizado"
fi

echo ""

# 7. Instruções finais
echo "════════════════════════════════════════════════════════════"
echo "✅ Setup concluído!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1️⃣  Criar repositório no GitHub:"
echo "    https://github.com/new"
echo "    Nome: precos-carros"
echo "    Descrição: Aplicação Streamlit para Previsão de Preços de Carros"
echo ""
echo "2️⃣  Configure origin remoto:"
echo "    git remote add origin $REPO_URL"
echo ""
echo "3️⃣  Faça push:"
echo "    git branch -M main"
echo "    git push -u origin main"
echo ""
echo "4️⃣  Deploy com Streamlit Cloud:"
echo "    Acesse: https://share.streamlit.io/"
echo "    Clique: New app"
echo "    Selecione seu repositório"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "💡 Dica: Use './deploy.sh streamlit' para mais informações"
echo ""
