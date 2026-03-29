#!/usr/bin/env python3
"""
Preprocessador de dados para a aplicação Streamlit
Aplica o mesmo pré-processamento usado no treino
"""

import pandas as pd
import numpy as np
from zenml.client import Client


class PredictionPreprocessor:
    """Preprocessa dados para previsão usando o mesmo método do treino."""

    def __init__(self):
        """Inicializa com os encodings do dataset."""
        self.load_encodings()

    def load_encodings(self):
        """Carrega os encodings de target encoding do dataset."""
        try:
            df = pd.read_csv('data/dataset_carros_brasil.csv')

            # Aplicar a limpeza básica
            df['Quilometragem'] = pd.to_numeric(df['Quilometragem'], errors='coerce')
            df['Ano'] = df['Ano'].fillna(df.groupby('Modelo')['Ano'].transform('median'))
            df['Quilometragem'] = df['Quilometragem'].fillna(df.groupby('Ano')['Quilometragem'].transform('median'))
            df = df[df['Valor_Venda'] < 1000000].copy()

            # Armazenar valores únicos para interfaces
            self.marca_valores = sorted(df['Marca'].unique())
            self.modelo_valores = sorted(df['Modelo'].unique())
            self.cor_valores = sorted(df['Cor'].unique())
            self.cambio_valores = sorted(df['Cambio'].unique())
            self.combustivel_valores = sorted(df['Combustivel'].unique())

            # Carregar modelos por marca (NOVO)
            self.modelos_por_marca = {}
            for marca in self.marca_valores:
                modelos = sorted(df[df['Marca'] == marca]['Modelo'].unique())
                self.modelos_por_marca[marca] = modelos

            # Calcular target encodings
            self.marca_encoding = df.groupby('Marca')['Valor_Venda'].mean().to_dict()
            self.modelo_encoding = df.groupby('Modelo')['Valor_Venda'].mean().to_dict()
            self.cor_encoding = df.groupby('Cor')['Valor_Venda'].mean().to_dict()

        except Exception as e:
            print(f"Erro ao carregar encodings: {e}")
            raise

    def preprocess(self, marca, modelo, ano, quilometragem, cor, cambio, combustivel, portas):
        """
        Preprocessa dados de entrada para previsão.

        Args:
            marca: str - Marca do veículo
            modelo: str - Modelo do veículo
            ano: int - Ano do veículo
            quilometragem: int - Quilometragem
            cor: str - Cor do veículo
            cambio: str - Tipo de câmbio
            combustivel: str - Tipo de combustível
            portas: int - Número de portas

        Returns:
            pd.DataFrame com features codificadas
        """
        # Criar DataFrame com os valores
        data = {
            'Marca': [marca],
            'Modelo': [modelo],
            'Ano': [float(ano)],
            'Quilometragem': [int(quilometragem)],
            'Cor': [cor],
            'Cambio': [cambio],
            'Combustivel': [combustivel],
            'Portas': [int(portas)],
        }

        df = pd.DataFrame(data)

        # Aplicar one-hot encoding para Cambio e Combustivel
        df_encoded = pd.get_dummies(df[['Cambio', 'Combustivel']], drop_first=True)

        # Aplicar target encoding
        df['Marca_Encoded'] = df['Marca'].map(self.marca_encoding)
        df['Modelo_Encoded'] = df['Modelo'].map(self.modelo_encoding)
        df['Cor_Encoded'] = df['Cor'].map(self.cor_encoding)

        # Preparar features finais na ordem correta
        features = pd.DataFrame({
            'Ano': df['Ano'],
            'Quilometragem': df['Quilometragem'],
            'Portas': df['Portas'],
        })

        # Adicionar one-hot features
        for col in df_encoded.columns:
            features[col] = df_encoded[col].values

        # Adicionar target encoded features
        features['Marca_Encoded'] = df['Marca_Encoded']
        features['Modelo_Encoded'] = df['Modelo_Encoded']
        features['Cor_Encoded'] = df['Cor_Encoded']

        # Garantir ordem correta dos nomes de features
        feature_names = ['Ano', 'Quilometragem', 'Portas', 'Cambio_Manual',
                        'Combustivel_Flex', 'Combustivel_Gasolina',
                        'Marca_Encoded', 'Modelo_Encoded', 'Cor_Encoded']

        # Adicionar features faltantes com valor 0
        for fname in feature_names:
            if fname not in features.columns:
                features[fname] = 0

        return features[feature_names]

    def get_unique_values(self):
        """Retorna valores únicos para cada campo categórico."""
        return {
            'marca': self.marca_valores,
            'modelo': self.modelo_valores,
            'cor': self.cor_valores,
            'cambio': self.cambio_valores,
            'combustivel': self.combustivel_valores,
        }

    def get_modelos_por_marca(self, marca):
        """Retorna modelos disponíveis para uma marca específica."""
        return self.modelos_por_marca.get(marca, [])


def test_preprocessor():
    """Testa o preprocessador."""
    preprocessor = PredictionPreprocessor()

    # Teste com valores de exemplo
    features = preprocessor.preprocess(
        marca='Ford',
        modelo='EcoSport',
        ano=2020,
        quilometragem=50000,
        cor='Azul',
        cambio='Automático',
        combustivel='Flex',
        portas=4
    )

    print("Features preprocessadas:")
    print(features)
    print(f"\nShape: {features.shape}")
    print(f"Colunas: {list(features.columns)}")


if __name__ == '__main__':
    test_preprocessor()
