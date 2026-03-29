from pipelines.deployment_pipeline import deployment_pipeline, inference_pipeline
import click
from rich import print
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.integrations.mlflow.model_deployers import (MLFlowModelDeployer)
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from pipelines.deployment_pipeline import continuous_deployment_pipeline
from zenml.integrations.mlflow.steps.mlflow_deployer import mlflow_model_deployer_step as mlflow_deployment_step

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"

@click.command()
@click.option(
    "--config",
    
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT], case_sensitive=False),
    default=DEPLOY_AND_PREDICT,
    help="Choose the pipeline to run: deploy, predict, or deploy_and_predict.",
)

@click.option(
    "--min-accuracy",
    default=0.92,
    help="Minimum accuracy threshold for deployment. Only applicable when --config is set to deploy or deploy_and_predict.",
)

def run_deployment(config: str, min_accuracy: float):
    mlflow_model_deployer_component = MLFlowModelDeployer.get_active_model_deployer()
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT
    if deploy:
        continuous_deployment_pipeline(
            min_accuracy=min_accuracy,
            workers=3,
            timeout=60,
        )
        
    if predict:
        inference_pipeline()
        
    print("Voce pode acessar o MLflow UI para monitorar os experimentos e implantações em: [bold blue]{}[/bold blue]".format(get_tracking_uri()))

if __name__ == "__main__":
    run_deployment()
