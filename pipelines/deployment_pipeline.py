import numpy as np
import pandas as pd
from zenml import pipeline, step
from zenml.config import DockerSettings
from zenml.constants import DEFAULT_SERVICE_START_STOP_TIMEOUT
from zenml.integrations.mlflow.model_deployers import MLFlowModelDeployer
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from pydantic import BaseModel
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step as mlflow_deployment_step

from steps.clean_data import clean_df
from steps.evaluation import evaluate_model
from steps.ingest_data import ingest_df
from steps.model_train import train_model
from steps.predict_model import predict_model

docker_settings = DockerSettings(
    required_integrations=["mlflow"])



@step
def deployment_trigger(
    acuracy: float,
    min_accuracy: float = 0.92,
):
    """Step para verificar se o modelo atende ao critério de acurácia para implantação.
    Args:
        acuracy: Acurácia do modelo avaliada no passo de avaliação.
        config: Configurações para o gatilho de implantação, incluindo a acurácia mínima.
    Returns:
        bool: True se o modelo atender ao critério de acurácia, False caso contrário.
    """
    return acuracy >= min_accuracy
@pipeline(enable_cache=True, settings={"docker": docker_settings})

def continuous_deployment_pipeline(
    min_accuracy: float = 0.92,
    workers: int = 1,
    timeout: int = DEFAULT_SERVICE_START_STOP_TIMEOUT,
):
    # O nome do argumento (data_path) deve ser o mesmo que você definiu no @step ingest_df
    df = ingest_df(data_path="/home/docas32/precos-carros/data/dataset_carros_brasil.csv")
    X_train, X_test, y_train, y_test = clean_df(df)

    model = train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, model_name="LinearRegression")

    mse_score, r2_score, rmse_score = evaluate_model(model, X_test, y_test)

    deployment_decision = deployment_trigger(acuracy=r2_score, min_accuracy=min_accuracy)

@pipeline(enable_cache=True, settings={"docker": docker_settings})
def deployment_pipeline(
    min_accuracy: float = 0.92,
):
    # 1. Ingestão
    df = ingest_df(data_path="/home/docas32/precos-carros/data/dataset_carros_brasil.csv")

    # 2. Limpeza e Divisão (Chame apenas uma vez)
    X_train, X_test, y_train, y_test = clean_df(df)

    # 3. Treinamento (Passe apenas o que o modelo precisa para treinar)
    model = train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, model_name="LinearRegression")

    # 4. Avaliação
    mse_score, r2_score, rmse_score = evaluate_model(model, X_test, y_test)

    # 5. Gatilho de Deploy (Cuidado com o nome do parâmetro 'accuracy')
    deployment_decision = deployment_trigger(acuracy=r2_score, min_accuracy=min_accuracy)

@pipeline(enable_cache=False, settings={"docker": docker_settings})
def inference_pipeline():
    # Pipeline de inferência - treina, faz previsões e também avalia o modelo.
    df = ingest_df(data_path="/home/docas32/precos-carros/data/dataset_carros_brasil.csv")
    X_train, X_test, y_train, y_test = clean_df(df)
    model = train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, model_name="LinearRegression")
    predictions = predict_model(model=model, X=X_test)
    mse_score, r2_score, rmse_score = evaluate_model(model, X_test, y_test)

    return predictions

