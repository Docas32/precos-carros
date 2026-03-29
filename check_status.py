#!/usr/bin/env python3
"""
Verificador de dependências e status da aplicação
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    required = [
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'zenml',
        'mlflow',
        'click',
        'rich'
    ]

    print("🔍 Verificando dependências...\n")

    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing.append(package)

    return missing


def check_model():
    """Verifica se o modelo foi treinado."""
    print("\n🤖 Verificando modelo...\n")

    if Path("predicoes.csv").exists():
        print("✓ Modelo treinado (predicoes.csv encontrado)")
        return True
    else:
        print("✗ Modelo não encontrado")
        print("  Execute: python3 predict.py")
        return False


def check_zenml_stack():
    """Verifica stack do ZenML."""
    print("\n🏗️  Verificando ZenML Stack...\n")

    try:
        result = subprocess.run(
            ["zenml", "stack", "describe"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print("✓ ZenML Stack ativo")
            lines = result.stdout.split('\n')
            for line in lines[:10]:
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print("✗ ZenML Stack não configurado")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar ZenML: {e}")
        return False


def main():
    """Executa todas as verificações."""
    print("=" * 50)
    print("🚗 Verificador de Aplicação")
    print("=" * 50 + "\n")

    # Verificações
    missing = check_dependencies()
    model_ok = check_model()
    zenml_ok = check_zenml_stack()

    print("\n" + "=" * 50)
    print("📊 Resumo de Status")
    print("=" * 50 + "\n")

    if missing:
        print(f"❌ Dependências faltando: {', '.join(missing)}")
        print("   Execute: pip install -r requirements.txt\n")

    if model_ok and zenml_ok:
        print("✅ Sistema pronto para usar!")
        print("\n🚀 Inicie a aplicação com:")
        print("   ./run_app.sh")
        print("   ou")
        print("   streamlit run app.py\n")
    else:
        print("⚠️  Sistema não está completamente configurado")
        print("\n📖 Siga os passos:")
        print("   1. pip install -r requirements.txt")
        print("   2. python3 predict.py  (treinar modelo)")
        print("   3. streamlit run app.py\n")

    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
