#!/usr/bin/env python3
"""
Script para fazer previsões com dados customizados.
Uso: python3 predict_custom.py --data sua_dados.csv --output predicoes.csv
"""

import click
import pandas as pd
import sys
from pathlib import Path
from zenml.client import Client
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()


def load_model_from_latest_run():
    """Carrega o modelo do último pipeline run."""
    try:
        client = Client()
        runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")

        if not runs:
            console.print("[bold red]Erro: Nenhum pipeline run foi encontrado.[/bold red]")
            return None

        last_run = runs[0]
        train_step = last_run.steps.get("train_model")

        if not train_step or not train_step.output:
            console.print("[bold red]Erro: Modelo não encontrado.[/bold red]")
            return None

        model = train_step.output.load()
        return model
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar o modelo: {e}[/bold red]")
        return None


@click.command()
@click.option(
    "--data",
    type=click.Path(exists=True),
    required=True,
    help="Arquivo CSV com dados para previsão"
)
@click.option(
    "--output",
    type=click.Path(),
    default="predicoes_custom.csv",
    help="Arquivo de saída para as previsões. Padrão: predicoes_custom.csv"
)
@click.option(
    "--show-results",
    is_flag=True,
    default=True,
    help="Mostrar resultados no terminal."
)
def predict_custom(data: str, output: str, show_results: bool):
    """
    Faz previsões usando o modelo treinado com dados customizados.
    """
    try:
        console.print(f"[bold blue]Carregando dados de {data}...[/bold blue]")

        # Carrega os dados
        df = pd.read_csv(data)
        console.print(f"✓ {len(df)} linhas carregadas")

        # Carrega o modelo
        console.print("[bold blue]Carregando modelo treinado...[/bold blue]")
        model = load_model_from_latest_run()

        if model is None:
            sys.exit(1)

        console.print("✓ Modelo carregado com sucesso")

        # Faz previsões
        console.print("[bold blue]Gerando previsões...[/bold blue]")
        predictions = model.predict(df)

        # Converte para Series se necessário
        if not isinstance(predictions, pd.Series):
            predictions = pd.Series(predictions, name="prediction")

        # Salva as previsões
        predictions.to_csv(output, index=False)
        console.print(f"[bold green]✓ Previsões salvas em: {output}[/bold green]")

        if show_results:
            # Mostra estatísticas
            console.print("\n[bold]Estatísticas das Previsões:[/bold]")
            table = Table(title="Resumo das Previsões")
            table.add_column("Métrica", style="cyan")
            table.add_column("Valor", style="magenta")

            table.add_row("Total de observações", str(len(predictions)))
            table.add_row("Preço médio previsto", f"R$ {predictions.mean():,.2f}")
            table.add_row("Preço mínimo previsto", f"R$ {predictions.min():,.2f}")
            table.add_row("Preço máximo previsto", f"R$ {predictions.max():,.2f}")
            table.add_row("Desvio padrão", f"R$ {predictions.std():,.2f}")

            console.print(table)

            # Mostra primeiras previsões
            console.print("\n[bold]Primeiras 10 previsões:[/bold]")
            print(predictions.head(10).to_string())

        console.print("\n[bold green]✓ Previsão concluída com sucesso![/bold green]")

    except Exception as e:
        console.print(f"[bold red]✗ Erro: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    predict_custom()
