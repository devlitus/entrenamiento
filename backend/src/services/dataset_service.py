"""
Servicio para generar y gestionar el dataset de entrenamiento.
Mantiene consistencia con la lógica de train_model.py
"""

import numpy as np
from typing import Dict, List, Any, Tuple
import math

class DatasetService:
    """Servicio para generar y gestionar datasets de entrenamiento."""
    
    def __init__(self):
        """Inicializa el servicio con configuración por defecto."""
        self.seed = 42
        np.random.seed(self.seed)
    
    def generate_temperature_dataset(self, 
                                   data_size_percent: float = 1.0,
                                   noise_std: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Genera el dataset de temperatura usando la misma lógica que train_model.py
        
        Args:
            data_size_percent: Porcentaje del dataset completo a usar (0.0 a 1.0)
            noise_std: Desviación estándar del ruido gaussiano
            
        Returns:
            Tuple con (celsius, fahrenheit_real, fahrenheit_noisy)
        """
        # Generar datos base (misma lógica que train_model.py)
        C = np.arange(-200, 200, 0.1)
        F_real = C * 1.8 + 32
        
        # Añadir ruido
        np.random.seed(self.seed)
        noise = np.random.normal(0, noise_std, size=len(C))
        F_noisy = F_real + noise
        
        # Aplicar muestreo
        num_samples = int(len(C) * data_size_percent)
        C_sampled = C[:num_samples]
        F_real_sampled = F_real[:num_samples]
        F_noisy_sampled = F_noisy[:num_samples]
        
        return C_sampled, F_real_sampled, F_noisy_sampled
    
    def get_dataset_page(self, 
                        page: int = 1, 
                        limit: int = 50,
                        data_size_percent: float = 1.0,
                        sort_by: str = 'index',
                        sort_order: str = 'asc',
                        noise_std: float = 2.0) -> Dict[str, Any]:
        """
        Obtiene una página del dataset con paginación.
        
        Args:
            page: Número de página (empezando en 1)
            limit: Número de registros por página
            data_size_percent: Porcentaje del dataset a usar
            sort_by: Campo por el cual ordenar ('index', 'celsius', 'fahrenheit')
            sort_order: Orden ('asc' o 'desc')
            
        Returns:
            Diccionario con datos, paginación y estadísticas
        """
        # Generar dataset completo
        celsius, fahrenheit_real, fahrenheit_noisy = self.generate_temperature_dataset(
            data_size_percent=data_size_percent,
            noise_std=noise_std
        )
        
        # Crear array de datos estructurado
        dataset = []
        for i, (c, f_real, f_noisy) in enumerate(zip(celsius, fahrenheit_real, fahrenheit_noisy)):
            dataset.append({
                'index': i,
                'celsius': round(float(c), 1),
                'fahrenheit_real': round(float(f_real), 2),
                'fahrenheit_noisy': round(float(f_noisy), 2),
                'noise': round(float(f_noisy - f_real), 2)
            })
        
        # Aplicar ordenamiento
        if sort_by in ['celsius', 'fahrenheit_real', 'fahrenheit_noisy', 'noise']:
            reverse = sort_order == 'desc'
            dataset.sort(key=lambda x: x[sort_by], reverse=reverse)
        elif sort_by == 'index' and sort_order == 'desc':
            dataset.reverse()
        
        # Calcular paginación
        total_records = len(dataset)
        total_pages = math.ceil(total_records / limit)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        # Obtener página actual
        page_data = dataset[start_idx:end_idx]
        
        # Calcular estadísticas
        stats = self._calculate_stats(celsius, fahrenheit_real, fahrenheit_noisy)
        
        return {
            'data': page_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_records,
                'pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'stats': stats,
            'metadata': {
                'data_size_percent': data_size_percent,
                'noise_std': noise_std,
                'temperature_increment': 0.1,  # Incremento dinámico del dataset
                'temperature_range': {
                    'celsius': {'min': -200.0, 'max': 199.9},
                    'fahrenheit': {'min': -328.0, 'max': 391.82}
                }
            }
        }
    
    def _calculate_stats(self, celsius: np.ndarray, 
                        fahrenheit_real: np.ndarray, 
                        fahrenheit_noisy: np.ndarray) -> Dict[str, Any]:
        """Calcula estadísticas del dataset."""
        noise = fahrenheit_noisy - fahrenheit_real
        
        return {
            'celsius': {
                'min': float(np.min(celsius)),
                'max': float(np.max(celsius)),
                'mean': float(np.mean(celsius)),
                'std': float(np.std(celsius))
            },
            'fahrenheit_real': {
                'min': float(np.min(fahrenheit_real)),
                'max': float(np.max(fahrenheit_real)),
                'mean': float(np.mean(fahrenheit_real)),
                'std': float(np.std(fahrenheit_real))
            },
            'fahrenheit_noisy': {
                'min': float(np.min(fahrenheit_noisy)),
                'max': float(np.max(fahrenheit_noisy)),
                'mean': float(np.mean(fahrenheit_noisy)),
                'std': float(np.std(fahrenheit_noisy))
            },
            'noise': {
                'min': float(np.min(noise)),
                'max': float(np.max(noise)),
                'mean': float(np.mean(noise)),
                'std': float(np.std(noise))
            },
            'total_samples': len(celsius)
        }