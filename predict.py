#!/usr/bin/env python3
"""
Script de previsão - Faz previsões de preço de carros usando o modelo treinado.
Uso: python3 predict.py --input seu_arquivo.csv --output predicoes.csv
"""

import click
import pandas as pd
import sys
from pathlib import Path
from pipelines.deployment_pipeline import inference_pipeline
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()


@click.command()
@click.option(
    "--input",
    type=click.Path(exists=True),
    help="Arquivo CSV com dados para previsão (opcional). Se não fornecido, usa o dataset padrão de teste."
)
@click.option(
    "--output",
    type=click.Path(),
    default="predicoes.csv",
    help="Arquivo de saída para as previsões. Padrão: predicoes.csv"
)
@click.option(
    "--show-results",
    is_flag=True,
    default=True,
    help="Mostrar resultados no terminal."
)
def predict(input: str, output: str, show_results: bool):
    """
    Executa previsões usando o pipeline de inferência treinado.

    Se nenhum arquivo de entrada for fornecido, treina um novo modelo
    e faz previsões no conjunto de teste.
    """
    try:
        console.print("[bold blue]Iniciando pipeline de previsão...[/bold blue]")

        # Executa o pipeline de inferência
        inference_pipeline()

        # Obtém as previsões do último run
        from zenml.client import Client
        client = Client()
        runs = client.list_pipeline_runs(pipeline_name="inference_pipeline")

        if not runs:
            console.print("[bold red]Erro: Nenhum pipeline run foi encontrado.[/bold red]")
            sys.exit(1)

        last_run = runs[0]
        predict_step = last_run.steps.get("predict_model")

        if not predict_step or not predict_step.output:
            console.print("[bold red]Erro: Nenhuma previsão foi gerada.[/bold red]")
            sys.exit(1)

        # Carrega as previsões do artifact
        predictions = predict_step.output.load()

        if predictions is not None and len(predictions) > 0:
            # Salva as previsões
            predictions.to_csv(output, index=False)
            console.print(f"[bold green]✓ Previsões salvas em: {output}[/bold green]")

            if show_results:
                # Mostra estatísticas das previsões
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

                # Mostra primeiras 10 previsões
                console.print("\n[bold]Primeiras 10 previsões:[/bold]")
                print(predictions.head(10).to_string())
        else:
            console.print("[bold red]Erro: Nenhuma previsão foi gerada.[/bold red]")
            sys.exit(1)

        console.print("\n[bold green]✓ Previsão concluída com sucesso![/bold green]")

    except Exception as e:
        console.print(f"[bold red]✗ Erro durante a previsão: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    predict()
