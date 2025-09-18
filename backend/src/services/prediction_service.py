# backend/src/services/prediction_service.py
# Servicio para manejar predicciones del modelo

import numpy as np
import tensorflow as tf
from typing import List, Dict, Any, Optional, Union
import os
from utils.logger import setup_logger

logger = setup_logger()

class PredictionService:
    """Servicio para manejar predicciones del modelo de temperatura."""
    
    def __init__(self):
        self.model: Optional[tf.keras.Model] = None
        self.model_path = "models/temperature_model.keras"
        self._load_model()
    
    def _load_model(self) -> bool:
        """Carga el modelo entrenado si existe."""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info("Modelo cargado exitosamente para predicciones")
                return True
            else:
                logger.warning(f"Modelo no encontrado en {self.model_path}")
                return False
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            return False
    
    def is_model_available(self) -> bool:
        """Verifica si el modelo está disponible para predicciones."""
        return self.model is not None
    
    def predict_single(self, celsius: float) -> Dict[str, Any]:
        """
        Realiza una predicción individual.
        
        Args:
            celsius: Temperatura en Celsius
            
        Returns:
            Dict con celsius, fahrenheit predicho y confianza
        """
        if not self.is_model_available():
            raise ValueError("Modelo no disponible. Entrena el modelo primero.")
        
        # Validar entrada
        if not isinstance(celsius, (int, float)):
            raise ValueError("El valor de Celsius debe ser numérico")
        
        if celsius < -273.15:  # Cero absoluto
            raise ValueError("Temperatura no puede ser menor al cero absoluto (-273.15°C)")
        
        try:
            # Realizar predicción
            celsius_array = np.array([[float(celsius)]])
            prediction = self.model.predict(celsius_array, verbose=0)
            fahrenheit_pred = float(prediction[0][0])
            
            # Calcular confianza basada en la distancia del rango de entrenamiento
            confidence = self._calculate_confidence(celsius)
            
            return {
                'celsius': celsius,
                'fahrenheit': fahrenheit_pred,
                'confidence': confidence,
                'fahrenheit_real': celsius * 1.8 + 32  # Valor real para comparación
            }
            
        except Exception as e:
            logger.error(f"Error en predicción individual: {e}")
            raise ValueError(f"Error realizando predicción: {str(e)}")
    
    def predict_batch(self, celsius_values: List[float]) -> Dict[str, Any]:
        """
        Realiza predicciones por lotes.
        
        Args:
            celsius_values: Lista de temperaturas en Celsius
            
        Returns:
            Dict con predicciones y estadísticas
        """
        if not self.is_model_available():
            raise ValueError("Modelo no disponible. Entrena el modelo primero.")
        
        if not celsius_values or len(celsius_values) == 0:
            raise ValueError("Lista de valores no puede estar vacía")
        
        if len(celsius_values) > 1000:  # Límite de seguridad
            raise ValueError("Máximo 1000 valores por lote")
        
        try:
            predictions = []
            errors = []
            
            for i, celsius in enumerate(celsius_values):
                try:
                    result = self.predict_single(celsius)
                    predictions.append(result)
                except Exception as e:
                    errors.append({'index': i, 'value': celsius, 'error': str(e)})
            
            # Calcular estadísticas del lote
            if predictions:
                fahrenheit_preds = [p['fahrenheit'] for p in predictions]
                fahrenheit_reals = [p['fahrenheit_real'] for p in predictions]
                
                # Calcular métricas de error
                mae = np.mean(np.abs(np.array(fahrenheit_preds) - np.array(fahrenheit_reals)))
                mse = np.mean((np.array(fahrenheit_preds) - np.array(fahrenheit_reals)) ** 2)
                
                stats = {
                    'total_predictions': len(predictions),
                    'successful_predictions': len(predictions),
                    'failed_predictions': len(errors),
                    'mae': float(mae),
                    'mse': float(mse),
                    'avg_confidence': np.mean([p['confidence'] for p in predictions])
                }
            else:
                stats = {
                    'total_predictions': 0,
                    'successful_predictions': 0,
                    'failed_predictions': len(errors),
                    'mae': None,
                    'mse': None,
                    'avg_confidence': None
                }
            
            return {
                'predictions': predictions,
                'errors': errors,
                'statistics': stats
            }
            
        except Exception as e:
            logger.error(f"Error en predicción por lotes: {e}")
            raise ValueError(f"Error realizando predicciones por lotes: {str(e)}")
    
    def _calculate_confidence(self, celsius: float) -> float:
        """
        Calcula la confianza de la predicción basada en el rango de entrenamiento.
        
        Args:
            celsius: Temperatura en Celsius
            
        Returns:
            Confianza entre 0 y 1
        """
        # Rango típico de entrenamiento: -200 a 200°C
        train_min, train_max = -200, 200
        
        if train_min <= celsius <= train_max:
            # Dentro del rango de entrenamiento: alta confianza
            return 0.95
        elif train_min - 50 <= celsius <= train_max + 50:
            # Cerca del rango: confianza media
            return 0.75
        else:
            # Fuera del rango: baja confianza
            distance = min(abs(celsius - train_min), abs(celsius - train_max))
            confidence = max(0.1, 0.75 - (distance - 50) / 1000)
            return min(confidence, 0.75)