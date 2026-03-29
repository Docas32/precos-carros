import logging
import pandas as pd
from zenml import step
from src.model_dev import LinearRegressionModel
from sklearn.base import RegressorMixin
from sklearn.linear_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor
from zenml.client import Client



@step
def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str = "LinearRegression",
) -> RegressorMixin:
    """Passos para treinamento do modelo.
    Args:
        X_train: Conjunto de dados de treinamento.
        y_train: Rótulos de treinamento.
        X_test: Conjunto de dados de teste.
        y_test: Rótulos de teste.
    """
    try:
        model = None
        if model_name == "LinearRegression":
            model_wrapper = LinearRegressionModel()
            # Se o .train() apenas treina mas não retorna o modelo,
            # a linha abaixo tornaria model = None.
            # Vamos garantir que retornamos o objeto treinado.
            trained_model = model_wrapper.train(X_train, y_train)
            logging.info("Modelo treinado com sucesso.")
            return trained_model # Certifique-se que isso não é None
        
        
        if model_name == "RandomForest":
            
            model = RandomForestRegressor()
            model.fit(X_train, y_train)
            logging.info("Modelo Random Forest treinado com sucesso.")
            return model
      
        else:
            logging.error(f"Modelo {model_name} não suportado.")
            raise ValueError(f"Modelo {model_name} não suportado.")
    except Exception as e:
        logging.error(f"Erro ao treinar o modelo: {e}")
        raise

