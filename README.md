# 🚗 Preços de Carros - Previsão com Streamlit

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Docas32-181717?style=for-the-badge&logo=github)](https://github.com/Docas32/precos-carros)

Aplicação web de **previsão de preços de carros** usando **Machine Learning** e **Streamlit**. Com interface intuitiva, analytics em tempo real e suporte para upload de dados em lote.

<div align="center">
  <img src="https://img.shields.io/badge/Modelo-Linear%20Regression-blue" alt="Modelo">
  <img src="https://img.shields.io/badge/R²-97.71%25-brightgreen" alt="R² Score">
  <img src="https://img.shields.io/badge/RMSE-R%24%203.220-orange" alt="RMSE">
</div>

---

## 📊 Visão Geral

Sistema completo de **Machine Learning** para prever preços de veículos brasileiros baseado em características como marca, modelo, ano, quilometragem, etc.

### ✨ Destaques

- 🎯 **Modelo Treinado**: Linear Regression com R² = 97.71%
- 🖥️ **Interface Web**: Streamlit com design responsivo
- 📈 **Analytics**: Dashboard com visualizações em tempo real
- 📁 **Upload em Lote**: Suporte para processamento de múltiplos dados
- 🔄 **Pipeline Automatizado**: ZenML + MLflow para orchestração
- 📊 **Histórico**: Rastreamento de todas as previsões
- 🌐 **Deploy Pronto**: Pronto para Streamlit Cloud, HuggingFace, Railway

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.12+
- pip ou conda
- 100 MB de espaço em disco

### Instalação Local

```bash
# 1. Clonar repositório
git clone https://github.com/Docas32/precos-carros.git
cd precos-carros

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py

# 5. Abrir navegador
# Acesse: http://localhost:8501
```

---

## 💻 Uso

### 🔮 Fazer Previsão Individual

1. Vá para a aba **"🔮 Fazer Previsão"**
2. Selecione os dados do veículo:
   - **Marca** → **Modelo** (filtra automaticamente)
   - Ano de fabricação
   - Quilometragem
   - Cor
   - Câmbio e Combustível
   - Número de portas (2 ou 4)
3. Clique **"Fazer Previsão"**
4. Veja o preço previsto e histórico

### 📁 Upload em Lote

1. Vá para **"📁 Upload de Dados"**
2. Baixe o template CSV
3. Preencha seus dados seguindo o formato
4. Upload do arquivo
5. Download das previsões

**Formato esperado:**
```csv
Marca,Modelo,Ano,Quilometragem,Cor,Cambio,Combustivel,Portas
Ford,EcoSport,2020,50000,Azul,Automático,Flex,4
Honda,Civic,2019,80000,Preto,Manual,Gasolina,2
```

### 📊 Analytics

- **Distribuição de Preços**: Histograma dos preços previstos
- **Estatísticas**: Min, máx, média, desvio padrão
- **Box Plot**: Visualização por características
- **Correlações**: Heatmap de correlações

### 📜 Histórico

- Visualize todas as previsões realizadas
- Download do histórico completo
- Tendências ao longo do tempo

---

## 📈 Métricas do Modelo

| Métrica | Valor |
|---------|-------|
| **Tipo de Modelo** | Linear Regression |
| **R² Score** | 0.9771 (97.71%) |
| **MSE** | 10,371,963.77 |
| **RMSE** | R$ 3,220.55 |
| **Amostras de Treino** | 1,960 |
| **Features** | 9 |

### Features Utilizadas

- Marca (Target Encoding)
- Modelo (Target Encoding)
- Ano de fabricação
- Quilometragem
- Cor (Target Encoding)
- Câmbio (One-Hot Encoding)
- Combustível (One-Hot Encoding)
- Número de portas

---

## 📁 Estrutura do Projeto

```
precos-carros/
├── 📄 app.py                           # Aplicação Streamlit principal
├── 📄 requirements.txt                 # Dependências Python
├── 📄 predict.py                       # Script de previsão (dataset teste)
├── 📄 predict_custom.py                # Script de previsão (dados customizados)
├── 📄 prediction_preprocessor.py       # Preprocessador de dados
│
├── 📁 pipelines/                       # Pipelines ZenML
│   ├── deployment_pipeline.py          # Pipeline de deployment
│   ├── training_pipeline.py            # Pipeline de treinamento
│   └── __init__.py
│
├── 📁 steps/                           # Steps individuais
│   ├── model_train.py                  # Treinamento do modelo
│   ├── predict_model.py                # Previsão
│   ├── evaluate_model.py               # Avaliação
│   ├── ingest_data.py                  # Ingestão de dados
│   ├── clean_data.py                   # Limpeza de dados
│   ├── config.py                       # Configurações
│   └── __init__.py
│
├── 📁 src/                             # Código-fonte
│   ├── model_dev.py                    # Desenvolvimento do modelo
│   └── __init__.py
│
├── 📁 data/                            # Dados
│   └── dataset_carros_brasil.csv       # Dataset de treino
│
├── 📁 .streamlit/                      # Configurações Streamlit
│   └── config.toml
│
├── 📁 mlruns/                          # Artifacts MLflow
├── 📁 .zen/                            # Configurações ZenML
│
├── 📄 run_deployment.py                # Runner do deployment
├── 📄 run_app.sh                       # Script para iniciar app
├── 📄 check_status.py                  # Verificador de status
│
├── 📚 Documentação/
│   ├── README.md                       # Este arquivo
│   ├── DEPLOY_GUIA.md                  # Guia de deployment
│   ├── MELHORIAS_IMPLEMENTADAS.md      # Mudanças recentes
│   ├── README_PREDICOES.md             # Guia de previsões
│   ├── README_STREAMLIT.md             # Guia da aplicação
│   └── QUICKSTART.md                   # Início rápido
│
└── 📄 .gitignore
```

---

## 🔧 Tecnologias Utilizadas

### Machine Learning
- **Scikit-learn** - Modelo Linear Regression
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica

### Orquestração & Tracking
- **ZenML** - Pipeline orchestration
- **MLflow** - Experiment tracking

### Interface Web
- **Streamlit** - Web framework
- **Plotly/Matplotlib** - Visualizações

### DevOps & Deploy
- **Docker** - Containerização
- **GitHub** - Versionamento
- **Streamlit Cloud** - Hosting

---

## 🌐 Deployment

### Opção 1: Streamlit Cloud (Recomendado)

Mais fácil e rápido:

```bash
# 1. Push code para GitHub
git push origin main

# 2. Acesse Streamlit Cloud
https://share.streamlit.io/

# 3. New app → Selecione seu repo
# Pronto! 🎉
```

URL: `https://seu-usuario-precos-carros.streamlit.app`

### Opção 2: Docker Local

```bash
# Build
docker build -t precos-carros:latest .

# Run
docker run -p 8501:8501 precos-carros:latest

# Acesse: http://localhost:8501
```

### Opção 3: HuggingFace Spaces

1. Acesse: https://huggingface.co/spaces
2. Create new Space (Docker)
3. Push code para HuggingFace

Veja `DEPLOY_GUIA.md` para mais detalhes.

---

## 📊 Usando Scripts de Previsão

### Previsão no Dataset de Teste

```bash
python3 predict.py --output predicoes.csv
```

Saída:
```
Iniciando pipeline de previsão...
✓ Previsões salvas em: predicoes.csv

Estatísticas das Previsões:
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Métrica               ┃ Valor         ┃
├───────────────────────┼───────────────┤
│ Total de observações  │ 1960          │
│ Preço médio previsto  │ R$ 59,237.26  │
│ Preço mínimo previsto │ R$ 8,468.05   │
│ Preço máximo previsto │ R$ 122,135.50 │
│ Desvio padrão         │ R$ 20,924.58  │
└───────────────────────┴───────────────┘
```

### Previsão com Dados Customizados

```bash
python3 predict_custom.py --data seu_arquivo.csv --output resultado.csv
```

---

## 🔍 Verificar Status

```bash
# Status geral do projeto
python3 check_status.py

# Verificar dataset
ls -lh data/dataset_carros_brasil.csv

# Ver pipeline runs
zenml stack describe

# MLflow UI
mlflow ui --backend-store-uri file:./mlruns
```

---

## 📝 Configuração

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[server]
port = 8501
headless = true
```

---

## 🧪 Testes

### Teste Local

```bash
# Ativar ambiente
source .venv/bin/activate

# Rodar app
streamlit run app.py

# Testar previsão
python3 predict.py
```

### Verify Features

```bash
python3 << 'EOF'
from prediction_preprocessor import PredictionPreprocessor

preprocessor = PredictionPreprocessor()
print(preprocessor.get_unique_values())
EOF
```

---

## 🐛 Troubleshooting

### Erro: "No pipeline run found"
```bash
# Solução: Execute o pipeline de previsão
python3 predict.py
```

### Erro: "Model not loaded"
```bash
# Verifique o status
python3 check_status.py

# Recrie o modelo
python3 run_deployment.py --config predict
```

### Port 8501 já em uso
```bash
# Use porta diferente
streamlit run app.py --server.port 8502
```

---

## 📚 Documentação Adicional

| Documento | Descrição |
|-----------|-----------|
| **DEPLOY_GUIA.md** | Guia completo para deploy na internet |
| **README_PREDICOES.md** | Scripts de previsão e uso |
| **README_STREAMLIT.md** | Documentação da aplicação web |
| **MELHORIAS_IMPLEMENTADAS.md** | Últimas mudanças do projeto |
| **QUICKSTART.md** | Início rápido com exemplos |

---

## 🎯 Roadmap

- [x] Modelo Machine Learning
- [x] Interface Streamlit
- [x] Scripts de previsão
- [x] Analytics dashboard
- [x] Upload em lote
- [x] Histórico de previsões
- [x] Documentação completa
- [ ] Autenticação de usuários
- [ ] Banco de dados para histórico persistente
- [ ] API REST
- [ ] Notificações por email
- [ ] Multiple models

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Faça um Fork
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit as mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📋 Requisitos

```
Python 3.12+
pip >= 23.0
RAM: 2GB mínimo
Disco: 100MB
Conexão: Internet (para download de dependências)
```

---

## 📦 Dependências Principais

```
streamlit==1.55.0       # Interface web
scikit-learn==1.8.0     # ML models
pandas==2.3.3           # Data manipulation
zenml==0.94.1           # Pipeline orchestration
mlflow==3.10.1          # Experiment tracking
click==8.2.1            # CLI
rich==14.3.3            # Terminal formatting
```

Veja `requirements.txt` para lista completa.

---

## 📊 Performance

| Operação | Tempo |
|----------|-------|
| Previsão Individual | < 1s |
| Upload 100 linhas | 2-3s |
| Train model | ~15s |
| Load model | < 1s |

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Docas32**
- GitHub: [@Docas32](https://github.com/Docas32)
- LinkedIn: [linkedin.com/in/docas32](https://linkedin.com/in/docas32)

---

## 🙏 Agradecimentos

- Dataset: [Dataset Carros Brasil](data/dataset_carros_brasil.csv)
- Framework: [Streamlit](https://streamlit.io/)
- ML: [Scikit-learn](https://scikit-learn.org/)
- Orchestration: [ZenML](https://zenml.io/)

---

## 📞 Suporte

Encontrou um problema?

1. Verifique [Issues](https://github.com/Docas32/precos-carros/issues)
2. Abra uma nova [Issue](https://github.com/Docas32/precos-carros/issues/new)
3. Veja a [Documentação](DEPLOY_GUIA.md)

---

## 🌟 Star o Projeto!

Se este projeto foi útil, considere dar uma ⭐ no GitHub!

```
https://github.com/Docas32/precos-carros
```

---

## 🔗 Links Úteis

- 🌐 [Streamlit Docs](https://docs.streamlit.io/)
- 🤖 [Scikit-learn Docs](https://scikit-learn.org/stable/)
- 📊 [MLflow Docs](https://mlflow.org/docs/latest/)
- 🏗️ [ZenML Docs](https://zenml.io/docs)
- 🐳 [Docker Docs](https://docs.docker.com/)

---

<div align="center">

**Desenvolvido com ❤️ usando Claude Code**

`Made with Streamlit • Powered by ML • Deployed to Cloud`

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red?logo=streamlit&logoColor=white)
![ML](https://img.shields.io/badge/ML-SKLearn-orange?logo=scikit-learn&logoColor=white)

[⬆ Voltar ao topo](#-preços-de-carros---previsão-com-streamlit)

</div>
