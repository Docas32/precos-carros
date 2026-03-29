import logging
from typing import Any, Dict, Union
import pandas as pd
from abc import ABC, abstractmethod
import numpy as np
from sklearn.model_selection import train_test_split
from sqlmodel import col

class DataStrategy(ABC):
    """Interface para estratégias de limpeza de dados."""
    @abstractmethod
    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass 

class DataPreprocessor(DataStrategy):
    """Implementação concreta da estratégia de limpeza de dados."""
    def handle_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpeza de dados utilizando pandas."""
        try:
            logging.info("Iniciando limpeza de dados.")
            # Converter coluna Quilometragem para numérica, tratando erros
            df['Quilometragem'] = pd.to_numeric(df['Quilometragem'], errors='coerce')
            # prencher valores ausentes com a mediana da coluna Ano e Quilometragem
            df['Ano'] = df['Ano'].fillna(df.groupby('Modelo')['Ano'].transform('median'))
            df['Quilometragem'] = df['Quilometragem'].fillna(df.groupby('Ano')['Quilometragem'].transform('median'))
            df_limpo = df[df['Valor_Venda'] < 1000000].copy()
            df_final = pd.get_dummies(df_limpo, columns=['Cambio', 'Combustivel'], drop_first=True)
            for col in ['Marca', 'Modelo', 'Cor']:
                target_mean = df_final.groupby(col)['Valor_Venda'].mean()
                df_final[col + '_Encoded'] = df_final[col].map(target_mean)
                df_final.drop(col, axis=1, inplace=True)
            return df_final


            
            logging.info("Limpeza de dados concluída.")
        except Exception as e:
            logging.error(f"Erro ao limpar dados: {e}")
        return df
    

class DataDivideStrategy(DataStrategy):
    """Implementação concreta da estratégia de divisão de dados."""
    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """Divide os dados em conjuntos de treino e teste."""
        try:
            logging.info("Iniciando divisão de dados.")
            X = df.drop('Valor_Venda', axis=1)
            y = df['Valor_Venda']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            logging.info("Divisão de dados concluída.")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(f"Erro ao dividir dados: {e}")
            raise

class DataCleaning:
    """ Classe principal para limpeza e divisão de dados,
      utilizando as estratégias definidas. """
    def __init__(self, data: pd.DataFrame, strategy: DataStrategy):
        self.data = data
        self.strategy = strategy

    def handle_data(self) -> Union[pd.DataFrame, pd.Series]:
        """Executa a estratégia de limpeza ou divisão de dados."""
        try:
            return self.strategy.handle_data(self.data)
        except Exception as e:
            logging.error(f"Erro ao processar dados: {e}")
            raise