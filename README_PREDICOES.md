# Preços de Carros - Sistema de Previsão

Sistema completo de pipeline ML para previsão de preços de carros usando ZenML e MLflow.

## ✨ Funcionalidades

- **Pipeline de Inferência**: Treina modelo e faz previsões no conjunto de teste
- **Previsões em Lote**: Faz previsões com dados customizados
- **Monitoramento**: Integração com MLflow para rastreamento de experimentos
- **Modelo de Regressão Linear**: Modelo treinado para prever preços

## 📊 Métricas do Modelo

- **R² Score**: 0.9771 (97.71% de variância explicada)
- **MSE**: 10,371,963.77
- **RMSE**: R$ 3,220.55

## 🚀 Uso

### 1. Ativar Ambiente Virtual

```bash
source .venv/bin/activate
```

### 2. Fazer Previsões no Dataset de Teste

```bash
python3 predict.py --output predicoes.csv
```

**Opções:**
- `--output`: Arquivo de saída (padrão: `predicoes.csv`)
- `--show-results`: Mostrar resultados no terminal (padrão: True)

### 3. Fazer Previsões com Dados Customizados

```bash
python3 predict_custom.py --data seu_arquivo.csv --output predicoes_custom.csv
```

**Opções:**
- `--data`: Arquivo CSV com dados para previsão (obrigatório)
- `--output`: Arquivo de saída (padrão: `predicoes_custom.csv`)
- `--show-results`: Mostrar resultados no terminal (padrão: True)

### 4. Runner de Deployment Completo

```bash
python3 run_deployment.py --config predict
```

**Opções de config:**
- `predict`: Apenas previsões
- `deploy`: Não implementado
- `deploy_and_predict`: Não implementado

```bash
python3 run_deployment.py --config predict --min-accuracy 0.92
```

## 📁 Estrutura de Arquivos

```
precos-carros/
├── predict.py              # Script de previsão (dataset de teste)
├── predict_custom.py       # Script de previsão (dados customizados)
├── run_deployment.py       # Runner principal
├── pipelines/              # Pipelines ZenML
│   └── deployment_pipeline.py
├── steps/                  # Steps individuais do pipeline
│   ├── model_train.py      # Treinamento do modelo
│   ├── predict_model.py    # Previsão
│   ├── evaluate_model.py   # Avaliação
│   ├── ingest_data.py      # Ingestão de dados
│   └── clean_data.py       # Limpeza de dados
├── src/                    # Código fonte
├── data/                   # Dados (CSV)
└── mlruns/                 # Artifacts do MLflow
```

## 📊 Visualizar Experimentos

Acesse a interface MLflow em modo local:

```bash
mlflow ui --backend-store-uri file:./mlruns
```

Depois acesse: `http://localhost:5000`

## 🔧 Variáveis de Ambiente

O projeto usa:
- **Python 3.12**
- **Pandas** para manipulação de dados
- **Scikit-learn** para ML
- **ZenML** para orchestração
- **MLflow** para rastreamento

## ✅ Status

- ✓ Model training implemented
- ✓ Prediction pipeline working
- ✓ MLflow integration active
- ✓ Custom data prediction ready
- ✓ Error handling fixed

## 📝 Exemplo de Saída

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

## 🐛 Troubleshooting

### Erro: "Invalid experiment ID: '.zen'"
- ✓ **Corrigido**: Removido `mlflow.sklearn.autolog()` que causava conflito

### Erro: "No pipeline run found"
- Execute `python3 predict.py` primeiro para gerar um run

### ZenML cache warning
- É uma aviso, não afeta o funcionamento

## 📚 Documentação Adicional

- [ZenML Documentation](https://docs.zenml.io/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Scikit-learn Regression](https://scikit-learn.org/stable/modules/linear_model.html)
