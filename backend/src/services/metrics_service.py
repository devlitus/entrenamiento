# backend/src/services/metrics_service.py

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, mean_squared_error,
    mean_absolute_error, r2_score, classification_report
)
from typing import Dict, List, Tuple, Optional, Any
import tensorflow as tf

class MetricsCalculator:
    """Calculadora de métricas avanzadas para modelos de ML"""
    
    def __init__(self):
        self.history = []
        self.current_metrics = {}
        
    def calculate_classification_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                       y_pred_proba: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Calcula métricas para problemas de clasificación"""
        metrics = {}
        
        # Métricas básicas
        metrics['accuracy'] = float(accuracy_score(y_true, y_pred))
        metrics['precision'] = float(precision_score(y_true, y_pred, average='weighted', zero_division=0))
        metrics['recall'] = float(recall_score(y_true, y_pred, average='weighted', zero_division=0))
        metrics['f1_score'] = float(f1_score(y_true, y_pred, average='weighted', zero_division=0))
        
        # Matriz de confusión
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        # AUC-ROC para clasificación binaria
        if len(np.unique(y_true)) == 2 and y_pred_proba is not None:
            try:
                metrics['auc_roc'] = float(roc_auc_score(y_true, y_pred_proba))
            except ValueError:
                metrics['auc_roc'] = None
                
        # Reporte de clasificación detallado
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        metrics['classification_report'] = report
        
        return metrics
    
    def calculate_regression_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calcula métricas para problemas de regresión"""
        metrics = {}
        
        metrics['mse'] = float(mean_squared_error(y_true, y_pred))
        metrics['mae'] = float(mean_absolute_error(y_true, y_pred))
        metrics['rmse'] = float(np.sqrt(metrics['mse']))
        metrics['r2_score'] = float(r2_score(y_true, y_pred))
        
        # Métricas adicionales
        residuals = y_true - y_pred
        metrics['mean_residual'] = float(np.mean(residuals))
        metrics['std_residual'] = float(np.std(residuals))
        
        return metrics
    
    def detect_overfitting(self, train_loss: List[float], val_loss: List[float], 
                          threshold: float = 0.1) -> Dict[str, Any]:
        """Detecta overfitting comparando pérdidas de entrenamiento y validación"""
        if len(train_loss) < 5 or len(val_loss) < 5:
            return {'overfitting': False, 'confidence': 0.0, 'reason': 'Datos insuficientes'}
        
        # Calcular tendencia en las últimas épocas
        recent_epochs = min(10, len(train_loss))
        recent_train = train_loss[-recent_epochs:]
        recent_val = val_loss[-recent_epochs:]
        
        # Diferencia promedio entre validación y entrenamiento
        avg_diff = np.mean(np.array(recent_val) - np.array(recent_train))
        
        # Tendencia de la diferencia
        diffs = np.array(recent_val) - np.array(recent_train)
        trend = np.polyfit(range(len(diffs)), diffs, 1)[0]
        
        overfitting = avg_diff > threshold and trend > 0
        confidence = min(1.0, max(0.0, (avg_diff - threshold) / threshold))
        
        return {
            'overfitting': overfitting,
            'confidence': float(confidence),
            'avg_difference': float(avg_diff),
            'trend': float(trend),
            'reason': 'Pérdida de validación mayor que entrenamiento' if overfitting else 'Normal'
        }
    
    def detect_underfitting(self, train_loss: List[float], val_loss: List[float],
                           min_epochs: int = 10) -> Dict[str, Any]:
        """Detecta underfitting basado en métricas de rendimiento"""
        if len(train_loss) < min_epochs:
            return {'underfitting': False, 'confidence': 0.0, 'reason': 'Épocas insuficientes'}
        
        # Verificar si las pérdidas están estancadas
        recent_epochs = min(10, len(train_loss))
        recent_train = train_loss[-recent_epochs:]
        recent_val = val_loss[-recent_epochs:]
        
        # Variación en las últimas épocas
        train_variation = np.std(recent_train) / np.mean(recent_train) if np.mean(recent_train) > 0 else 0
        val_variation = np.std(recent_val) / np.mean(recent_val) if np.mean(recent_val) > 0 else 0
        
        # Si ambas variaciones son muy bajas, podría ser underfitting
        stagnation_threshold = 0.01
        underfitting = train_variation < stagnation_threshold and val_variation < stagnation_threshold
        
        confidence = 1.0 - max(train_variation, val_variation) / stagnation_threshold
        confidence = max(0.0, min(1.0, confidence))
        
        return {
            'underfitting': underfitting,
            'confidence': float(confidence),
            'train_variation': float(train_variation),
            'val_variation': float(val_variation),
            'reason': 'Métricas estancadas' if underfitting else 'Progreso normal'
        }
    
    def calculate_learning_rate_effectiveness(self, loss_history: List[float]) -> Dict[str, Any]:
        """Analiza la efectividad de la tasa de aprendizaje"""
        if len(loss_history) < 5:
            return {'status': 'insufficient_data', 'recommendation': 'Continuar entrenamiento'}
        
        # Calcular la tendencia de la pérdida
        x = np.arange(len(loss_history))
        slope, _ = np.polyfit(x, loss_history, 1)
        
        # Analizar la variabilidad
        recent_losses = loss_history[-10:] if len(loss_history) >= 10 else loss_history
        variability = np.std(recent_losses) / np.mean(recent_losses) if np.mean(recent_losses) > 0 else 0
        
        # Determinar recomendación
        if slope > 0:  # Pérdida aumentando
            status = 'increasing_loss'
            recommendation = 'Reducir tasa de aprendizaje'
        elif abs(slope) < 1e-6 and variability < 0.01:  # Estancada
            status = 'stagnant'
            recommendation = 'Aumentar tasa de aprendizaje o cambiar optimizador'
        elif variability > 0.1:  # Muy variable
            status = 'unstable'
            recommendation = 'Reducir tasa de aprendizaje para estabilizar'
        else:
            status = 'optimal'
            recommendation = 'Mantener configuración actual'
        
        return {
            'status': status,
            'slope': float(slope),
            'variability': float(variability),
            'recommendation': recommendation
        }
    
    def get_prediction_examples(self, X: np.ndarray, y_true: np.ndarray, 
                               y_pred: np.ndarray, model_type: str = 'regression',
                               n_examples: int = 5) -> Dict[str, List]:
        """Obtiene ejemplos de predicciones correctas e incorrectas"""
        examples = {
            'correct': [],
            'incorrect': [],
            'borderline': []
        }
        
        if model_type == 'classification':
            # Para clasificación
            correct_mask = y_true == y_pred
            incorrect_mask = ~correct_mask
            
            # Ejemplos correctos
            if np.any(correct_mask):
                correct_indices = np.where(correct_mask)[0][:n_examples]
                for idx in correct_indices:
                    examples['correct'].append({
                        'input': X[idx].tolist() if hasattr(X[idx], 'tolist') else float(X[idx]),
                        'true': int(y_true[idx]),
                        'predicted': int(y_pred[idx])
                    })
            
            # Ejemplos incorrectos
            if np.any(incorrect_mask):
                incorrect_indices = np.where(incorrect_mask)[0][:n_examples]
                for idx in incorrect_indices:
                    examples['incorrect'].append({
                        'input': X[idx].tolist() if hasattr(X[idx], 'tolist') else float(X[idx]),
                        'true': int(y_true[idx]),
                        'predicted': int(y_pred[idx])
                    })
        
        else:  # Regresión
            errors = np.abs(y_true - y_pred)
            error_percentiles = np.percentile(errors, [25, 75])
            
            # Ejemplos con error bajo (correctos)
            good_mask = errors <= error_percentiles[0]
            if np.any(good_mask):
                good_indices = np.where(good_mask)[0][:n_examples]
                for idx in good_indices:
                    examples['correct'].append({
                        'input': X[idx].tolist() if hasattr(X[idx], 'tolist') else float(X[idx]),
                        'true': float(y_true[idx]),
                        'predicted': float(y_pred[idx]),
                        'error': float(errors[idx])
                    })
            
            # Ejemplos con error alto (incorrectos)
            bad_mask = errors >= error_percentiles[1]
            if np.any(bad_mask):
                bad_indices = np.where(bad_mask)[0][:n_examples]
                for idx in bad_indices:
                    examples['incorrect'].append({
                        'input': X[idx].tolist() if hasattr(X[idx], 'tolist') else float(X[idx]),
                        'true': float(y_true[idx]),
                        'predicted': float(y_pred[idx]),
                        'error': float(errors[idx])
                    })
        
        return examples
