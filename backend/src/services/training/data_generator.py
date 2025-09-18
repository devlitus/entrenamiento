# c:/dev/entrenamiento/backend/src/services/training/data_generator.py
"""
Generador de datos para entrenamiento.
"""

import numpy as np
from sklearn.model_selection import train_test_split

class DataGenerator:
    """Generador de datos sintéticos para entrenamiento."""
    
    @staticmethod
    def generate_data(seed=42, dataset_size=1000):
        """Genera datos sintéticos para entrenamiento."""
        np.random.seed(seed)
        X = np.random.randn(dataset_size, 1)
        y = X * 2 + 1 + np.random.randn(dataset_size, 1) * 0.1
        return X, y
    
    @staticmethod
    def split_data(X, y, test_size=0.2, random_state=42):
        """Divide los datos en conjuntos de entrenamiento y validación."""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)