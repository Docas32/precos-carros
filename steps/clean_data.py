import logging
import pandas as pd
from zenml import step
from src.data_cleaning import DataCleaning, DataPreprocessor, DataDivideStrategy
from typing import Tuple, Annotated

@step
def clean_df(df: pd.DataFrame) -> Tuple[Annotated[pd.DataFrame, "X_train"], Annotated[pd.DataFrame, "X_test"], Annotated[pd.Series, "y_train"], Annotated[pd.Series, "y_test"]]:
    """Passos para limpeza de dados.
    Args:
        df: Um DataFrame do pandas contendo os dados a serem limpos.
    Returns:
        X_train, X_test, y_train, y_test ."""
    try:
        process_strategy = DataPreprocessor()
        data_cleaning = DataCleaning(df, process_strategy)
        process_data = data_cleaning.handle_data()
        divide_strategy = DataDivideStrategy()
        data_cleaning = DataCleaning(process_data, divide_strategy)
        X_train, X_test, y_train, y_test = data_cleaning.handle_data()
        logging.info("Dados limpos e divididos com sucesso.")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error(f"Erro ao limpar e dividir dados: {e}")
