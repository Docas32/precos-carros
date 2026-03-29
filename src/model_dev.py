import logging
from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

class Model(ABC):
    """Interface para modelos de machine learning."""
    @abstractmethod
    def train(self, X_train, y_train):
        """Treina o modelo\n        Args:
            X_train: Conjunto de dados de treinamento.
            y_train: Rótulos de treinamento."""
        pass

    @abstractmethod
    def predict(self, X_test):
        """Faz previsões usando o modelo treinado.
        Args:
            X_test: Conjunto de dados de teste."""
        pass

class LinearRegressionModel(Model):
    """Implementação do modelo de regressão linear."""
    def __init__(self):
        
        self.model = LinearRegression()

    def train(self, X_train, y_train):
        """Treina o modelo de regressão linear."""
        try:
            logging.info("Iniciando treinamento do modelo de regressão linear.")
            self.model.fit(X_train, y_train)
            logging.info("Treinamento concluído.")
            return self.model
        except Exception as e:
            logging.error(f"Erro ao treinar o modelo: {e}")

    def predict(self, X_test):
        """Faz previsões usando o modelo de regressão linear treinado."""
        try:
            logging.info("Iniciando previsão com o modelo de regressão linear.")
            y_pred = self.model.predict(X_test)
            logging.info("Previsão concluída.")
            return y_pred
        except Exception as e:
            logging.error(f"Erro ao fazer previsões: {e}")
            return None

class RandomForestModel(Model):
    """Implementação do modelo de Random Forest."""
    def __init__(self):
        from sklearn.ensemble import RandomForestRegressor
        self.model = RandomForestRegressor()

    def train(self, X_train, y_train):
        """Treina o modelo de Random Forest."""
        try:
            logging.info("Iniciando treinamento do modelo de Random Forest.")
            self.model.fit(X_train, y_train)
            logging.info("Treinamento concluído.")
            return self.model
        except Exception as e:
            logging.error(f"Erro ao treinar o modelo: {e}")

    def predict(self, X_test):
        """Faz previsões usando o modelo de Random Forest treinado."""
        try:
            logging.info("Iniciando previsão com o modelo de Random Forest.")
            y_pred = self.model.predict(X_test)
            logging.info("Previsão concluída.")
            return y_pred
        except Exception as e:
            logging.error(f"Erro ao fazer previsões: {e}")
            return None
        


