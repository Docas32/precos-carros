import logging
import pandas as pd
from zenml import step


class IngestData:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def get_data(self):
        logging.info(f"Ingesting data from {self.data_path}")
        return pd.read_csv(self.data_path)
    
@step
def ingest_df(data_path: str) -> pd.DataFrame:
    """Passos para ingestão de dados.
    Args:
        data_path: O caminho para o arquivo CSV contendo os dados.
    Returns:
        Um DataFrame do pandas contendo os dados ingestados."""
    try:
        ingest_data = IngestData(data_path)
        df = ingest_data.get_data()
        return df
    except Exception as e:
        logging.error(f"Erro ao ingerir dados de {data_path}: {e}")
        raise e