# 🚀 Guia Rápido de Início

## ⚡ 5 Passos para Começar

### 1️⃣ Verificar Status

```bash
python3 check_status.py
```

### 2️⃣ Ativar Ambiente Virtual

```bash
source .venv/bin/activate
```

### 3️⃣ Treinar Modelo (se necessário)

```bash
python3 predict.py
```

### 4️⃣ Iniciar Aplicação

**Opção A - Automática (Recomendado):**
```bash
./run_app.sh
```

**Opção B - Direta:**
```bash
streamlit run app.py
```

### 5️⃣ Acessar Aplicação

Abra no navegador:
```
http://localhost:8501
```

---

## 🎯 Casos de Uso

### Fazer Uma Previsão Rápida

```bash
python3 predict.py
```

→ Gera: `predicoes.csv`

### Fazer Previsão com Seus Dados

```bash
python3 predict_custom.py --data seus_carros.csv --output resultado.csv
```

→ Gera: `resultado.csv`

### Interface Web Completa

```bash
./run_app.sh
```

→ Abre: `http://localhost:8501`

### API/Runner Completo

```bash
python3 run_deployment.py --config predict
```

→ Executa pipeline completo

---

## 📊 Estrutura de Arquivos Importantes

```
precos-carros/
├── app.py                    # 🟢 Aplicação Streamlit (NOVO)
├── run_app.sh               # 🟢 Script para iniciar (NOVO)
├── check_status.py          # 🟢 Verificador de status (NOVO)
├── predict.py              # Previsão (dataset teste)
├── predict_custom.py       # Previsão (dados customizados)
├── run_deployment.py       # Runner principal
│
├── .streamlit/
│   └── config.toml         # 🟢 Configuração Streamlit (NOVO)
│
├── pipelines/
│   └── deployment_pipeline.py
│
├── steps/
│   ├── model_train.py
│   ├── predict_model.py
│   ├── evaluate_model.py
│   ├── ingest_data.py
│   └── clean_data.py
│
├── data/
│   └── dataset_carros_brasil.csv
│
└── README_*.md
    ├── README_PREDICOES.md      # Documentação de previsões
    └── README_STREAMLIT.md      # Documentação Streamlit (NOVO)
```

---

## 🔍 Verificação Rápida

### Modelo Treinado?
```bash
ls -lh predicoes.csv
```

### ZenML ativo?
```bash
zenml stack describe
```

### Portas disponíveis?
```bash
netstat -tuln | grep 8501  # Streamlit
netstat -tuln | grep 5000  # MLflow
```

---

## 🆘 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: streamlit` | `pip install streamlit` |
| `Modelo não encontrado` | `python3 predict.py` |
| `Porta 8501 em uso` | `streamlit run app.py --server.port 8502` |
| `ZenML não configurado` | `zenml init` |
| Aplicação lenta | `streamlit cache clear` |

---

## 📱 Interface Streamlit

### Menu Principal (Sidebar)

- 🏠 **Home** - Informações e status
- 🔮 **Fazer Previsão** - Previsão individual
- 📊 **Analytics** - Visualizações e gráficos
- 📁 **Upload de Dados** - Previsão em lote
- 📈 **Histórico** - Histórico de previsões

### Funcionalidades

✅ Previsão em tempo real com sliders
✅ Upload de arquivos CSV
✅ Gráficos e estatísticas
✅ Histórico persistente
✅ Download de resultados
✅ Modelo cachado (2-3s de carregamento)

---

## 💡 Dicas

1. **Performance**: Primeira execução é mais lenta (carrega modelo)
2. **Cache**: Streamlit faz cache automático - não se preocupe
3. **Histórico**: Todos os uploads são salvos em `predicoes_historico.csv`
4. **Template**: Baixe template de exemplo na página de Upload

---

## 📚 Documentação Completa

- [README_PREDICOES.md](README_PREDICOES.md) - Detalhes de previsões
- [README_STREAMLIT.md](README_STREAMLIT.md) - Documentação da web app
- [README.md](README.md) - Documentação geral do projeto

---

## 🎓 Primeiro Acesso

1. Execute `check_status.py` para verificar tudo
2. Execute `./run_app.sh` para iniciar
3. Vá para page "Home" para entender
4. Teste "Fazer Previsão" com sliders
5. Depois teste "Upload de Dados" com CSV

---

**Pronto? Vá para:**

```bash
./run_app.sh
```

🚀 Acesso a aplicação em: `http://localhost:8501`
