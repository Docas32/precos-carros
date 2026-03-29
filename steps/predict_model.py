import logging
import numpy as np
import pandas as pd
from typing import Union
from sklearn.base import RegressorMixin
from zenml import step

@step
def predict_model(model: RegressorMixin, X: pd.DataFrame) -> pd.Series:
    """Faz previsões usando um modelo treinado.

    Args:
        model: Modelo treinado que implementa predict().
        X: Dados de entrada para inferência.

    Returns:
        Uma Série do pandas com as previsões.
    """
    try:
        predictions = model.predict(X)
        if isinstance(predictions, np.ndarray):
            return pd.Series(predictions, index=X.index if hasattr(X, "index") else None, name="prediction")
        return pd.Series(predictions, index=X.index if hasattr(X, "index") else None, name="prediction")
    except Exception as e:
        logging.error(f"Erro ao gerar previsões: {e}")
        raise
