from readline import backend

from pipelines.training_pipeline import training_pipeline
from steps.config import ModelNameConfig
from zenml.client import Client
import mlflow


if __name__ == "__main__":
    print(Client().active_stack.experiment_tracker.get_tracking_uri())  # Verifique o stack ativo antes de executar o pipeline
    # Define paths for data and model
    data_path = "data/dataset_carros_brasil.csv"
    model_path = "models/trained_model.pkl"
    # Create a configuration for the model
    modelos = ["LinearRegression"]
    for name in modelos:
        config = ModelNameConfig(model_name=name)  # Escolha entre "Lasso" ou "RandomForest"
        # Run the training pipeline
        training_pipeline(data_path, config=config)
# mlflow ui --backend-store-uri "file:/home/docas32/.config/zenml/local_stores/684d0f8c-3705-4ae9-a8e4-b4e1a53510bb/mlruns"