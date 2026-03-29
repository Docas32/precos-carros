from zenml import pipeline
from steps import ingest_data
from steps.config import ModelNameConfig
from steps.ingest_data import ingest_df
from steps.clean_data import clean_df
from steps.model_train import train_model  
from steps.evaluation import evaluate_model

@pipeline(enable_cache=False)
def training_pipeline(data_path: str, config: ModelNameConfig):
    """Pipeline de treinamento para o modelo de previsão de preços de carros.
    Args:
        data_path: O caminho para o arquivo CSV contendo os dados de treinamento.
        config: Configuração do modelo.
    """
    df = ingest_df(data_path)
    X_train, X_test, y_train, y_test = clean_df(df)

    model = train_model(X_train, y_train, X_test, y_test, config=config)
    mse_score, r2_score, rmse_score = evaluate_model(model, X_test, y_test)
    print(f"MSE: {mse_score}, R2 Score: {r2_score}, RMSE: {rmse_score}")





