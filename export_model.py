from zenml.client import Client
import joblib
import os

def export_latest_model():
    client = Client()
    runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")
    if not runs:
        print("Erro: Nenhum pipeline run encontrado localmente!")
        return
    
    last_run = runs[0]
    train_step = last_run.steps.get("train_model")
    if not train_step or not train_step.output:
        print("Erro: Modelo não encontrado no último run")
        return
        
    model = train_step.output.load()
    
    os.makedirs("savad_model", exist_ok=True)
    joblib.dump(model, "savad_model/model.joblib")
    print("Modelo exportado com sucesso para savad_model/model.joblib!")

if __name__ == "__main__":
    export_latest_model()
