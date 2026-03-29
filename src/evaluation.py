import logging
from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

class Evaluation(ABC):
    """Interface para avaliação de modelos de machine learning."""
    @abstractmethod
    def calculate_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula a pontuação do   modelo usando métricas apropriadas.
        Args:
            y_true: Rótulos verdadeiros.
            y_pred: Rótulos previstos pelo modelo."""
        pass

class MSE(Evaluation):
    """Implementação da métrica de erro quadrático médio (MSE)."""
    def calculate_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula o MSE entre os rótulos verdadeiros e previstos."""
        try:
            mse = mean_squared_error(y_true, y_pred)
            logging.info(f"MSE calculado: {mse}")
            return mse
        except Exception as e:
            logging.error(f"Erro ao calcular MSE: {e}")
            return float('inf')

class R2Score(Evaluation):
    """Implementação da métrica de coeficiente de determinação (R²)."""
    def calculate_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula o R² entre os rótulos verdadeiros e previstos."""
        try:
            r2 = r2_score(y_true, y_pred)
            logging.info(f"R² calculado: {r2}")
            return r2
        except Exception as e:
            logging.error(f"Erro ao calcular R²: {e}")
            return float('-inf')
        
class RMSE(Evaluation):
    """Implementação da métrica de raiz do erro quadrático médio (RMSE)."""
    def calculate_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula o RMSE entre os rótulos verdadeiros e previstos."""
        try:
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            logging.info(f"RMSE calculado: {rmse}")
            return rmse
        except Exception as e:
            logging.error(f"Erro ao calcular RMSE: {e}")
            return float('inf')
        
