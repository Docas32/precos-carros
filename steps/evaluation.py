import logging
import pandas as pd
from zenml import step
from zenml.client import Client
from src.evaluation import MSE, R2Score, RMSE
from sklearn.base import RegressorMixin
from typing import Tuple, Annotated
import mlflow

@step
def evaluate_model(
    model: RegressorMixin, 
    X_test: pd.DataFrame, 
    y_test: pd.Series
) -> Tuple[
    Annotated[float, "mse_score"], 
    Annotated[float, "r2_score"], 
    Annotated[float, "rmse_score"]
]:
    """Passos para avaliação do modelo."""
    try:
        prediction = model.predict(X_test)
        
        # Instanciando as classes de métricas
        mse_class = MSE()
        r2_class = R2Score()
        rmse_class = RMSE()

        # Calculando os scores
        mse_score = mse_class.calculate_score(y_test.values, prediction)
        mlflow.log_metric("mse", mse_score)
        
        r2_score = r2_class.calculate_score(y_test.values, prediction)
        mlflow.log_metric("r2_score", r2_score)
        
        rmse_score = rmse_class.calculate_score(y_test.values, prediction)
        mlflow.log_metric("rmse", rmse_score)

        return mse_score, r2_score, rmse_score
        
    except Exception as e:
        logging.error(f"Erro ao avaliar o modelo: {e}")
        raise e  # IMPORTANTE: Use raise para que o ZenML saiba que o step falhou