# 🚗 Aplicação Streamlit - Previsão de Preços de Carros

Aplicação web interativa para previsão de preços de carros usando Machine Learning.

## 🚀 Inicialização Rápida

### Opção 1: Script Automatizado (Recomendado)

```bash
chmod +x run_app.sh
./run_app.sh
```

### Opção 2: Comando Direto

```bash
# Ative o ambiente virtual
source .venv/bin/activate

# Inicie a aplicação
streamlit run app.py
```

### Opção 3: Com Porta Customizada

```bash
streamlit run app.py --server.port 8502 --server.address localhost
```

## 🌐 Acesso

Após iniciar, acesse no navegador:
```
http://localhost:8501
```

## 📖 Seções da Aplicação

### 🏠 Home
- **Informações do Modelo**
  - R² Score: 97.71%
  - MSE e RMSE
  - Número de amostras

- **Recursos Disponíveis**
  - Previsão em tempo real
  - Upload de arquivos
  - Analytics e visualizações

- **Instruções de Uso**

### 🔮 Fazer Previsão
- **Entrada de Dados em Tempo Real**
  - Sliders para cada feature
  - Valores numéricos ajustáveis
  - Preview dos dados

- **Previsão Instantânea**
  - Botão para calcular previsão
  - Resultado formatado em R$
  - Timestamp da previsão
  - Histórico automático

### 📊 Analytics
- **Visualizações Gráficas**
  - Distribuição de preços (histograma)
  - Box plot para outliers
  - Análise estatística

- **Estatísticas Detalhadas**
  - Mínimo e máximo
  - Quartis (Q1, Q2, Q3)
  - Média e desvio padrão

### 📁 Upload de Dados
- **Importar Arquivo CSV**
  - Selecionar arquivo CSV
  - Preview dos dados
  - Validação automática

- **Previsões em Lote**
  - Processar múltiplos registros
  - Resultados tabulados
  - Download de resultados

- **Template de Exemplo**
  - Download de template CSV
  - Estrutura correta de colunas

### 📈 Histórico
- **Histórico de Previsões**
  - Tabela com todas as previsões
  - Timestamp de cada previsão
  - Tendências gráficas

- **Estatísticas Temporais**
  - Evolução dos preços médios
  - Range de preços (min/max)
  - Download do histórico completo

## 📊 Dados de Entrada

O modelo espera as seguintes features:

```
feature_1: int (0-200)
feature_2: int (50-300)
feature_3: float (0.5-5.0)
feature_4: int (2000-2024)
```

## 💾 Arquivos Gerados

A aplicação gera os seguintes arquivos:

- `predicoes_historico.csv` - Histórico de todas as previsões
- `predicoes_custom.csv` - Últimas previsões em lote
- `.streamlit/config.toml` - Configuração da aplicação

## 🎨 Interface

- **Cores**: Tema profissional azul e branco
- **Layout**: Wide para melhor visualização
- **Responsivo**: Funciona em desktop e tablet
- **Otimizado**: Carregamento em cache do modelo

## ⚙️ Configurações

Arquivo: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = true
runOnSave = true
```

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Erro: "Modelo não disponível"

Execute primeiro para treinar:
```bash
python3 predict.py
```

### Aplicação lenta

Limpe o cache do Streamlit:
```bash
streamlit cache clear
```

### Porta 8501 já em uso

Use porta alternativa:
```bash
streamlit run app.py --server.port 8502
```

## 📱 Features Principais

✅ **Previsão em Tempo Real**
- Interface intuitiva com sliders
- Resultados instantâneos
- Formatação em moeda

✅ **Batch Processing**
- Upload de múltiplos dados
- Processamento paralelo
- Download de resultados

✅ **Analytics Avançado**
- Gráficos interativos
- Estatísticas completas
- Análise de distribuição

✅ **Histórico Persistente**
- Todas as previsões salvas
- Análise temporal
- Export de dados

✅ **User Experience**
- Interface responsiva
- Navegação intuitiva
- Feedback visual

## 🚀 Performance

- **Carregamento do Modelo**: ~2-3s (cache)
- **Previsão Única**: <1s
- **Batch (1000 linhas)**: ~5-10s
- **Memória**: ~500MB

## 📚 Documentação Adicional

- [Streamlit Docs](https://docs.streamlit.io/)
- [ZenML Docs](https://docs.zenml.io/)
- [MLflow Docs](https://mlflow.org/docs/)

## 👨‍💻 Desenvolvido por

Gerado com ❤️ usando Claude Code

## 📄 Licença

MIT License

---

**Dica**: Para melhor experiência, use um navegador moderno (Chrome, Firefox, Safari)
