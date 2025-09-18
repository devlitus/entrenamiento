"""
Callbacks avanzados para el entrenamiento de redes neuronales.
Migrado desde train_model.py para integración con el sistema moderno.
"""

import numpy as np
from tensorflow.keras.callbacks import Callback
from src.services.metrics_service import MetricsCalculator
from src.services.hardware_monitor import HardwareMonitor
from src.services.alert_service import AlertService
from src.services.metrics_storage import MetricsStorage
from utils.logger import setup_logger

logger = setup_logger()

class AdvancedTrainingCallback(Callback):
    """
    Callback avanzado que integra métricas, alertas y monitoreo de hardware.
    Versión moderna del AdvancedSocketIOProgressCallback legacy.
    """
    
    def __init__(self, event_emitter, X_train, y_train, X_val, y_val, model_type='regression'):
        super().__init__()
        self.event_emitter = event_emitter
        self.X_train = X_train
        self.y_train = y_train
        self.X_val = X_val
        self.y_val = y_val
        self.model_type = model_type
        
        # Servicios
        self.metrics_calculator = MetricsCalculator()
        self.hardware_monitor = HardwareMonitor()
        self.alert_service = AlertService()
        self.metrics_storage = MetricsStorage()
        
        # Historial de métricas
        self.train_loss_history = []
        self.val_loss_history = []
        self.train_metrics_history = []
        self.val_metrics_history = []
        
        # Sesión de entrenamiento
        self.training_session_id = None
        
    def on_train_begin(self, logs=None):
        """Inicializa el monitoreo al comenzar el entrenamiento."""
        try:
            # Iniciar monitoreo de hardware
            self.hardware_monitor.start_monitoring()
            
            # Crear sesión de entrenamiento si no existe
            if not self.training_session_id:
                self.training_session_id = self.metrics_storage.create_training_session(
                    name=f"Training_{self.model_type}",
                    hyperparameters={
                        'model_type': self.model_type,
                        'train_samples': len(self.X_train),
                        'val_samples': len(self.X_val)
                    },
                    model_type=self.model_type
                )
            
            self.event_emitter.emit_log('Monitoreo avanzado iniciado')
            
        except Exception as e:
            logger.error(f"Error iniciando callback avanzado: {e}")
            
    def on_epoch_end(self, epoch, logs=None):
        """Procesa métricas avanzadas al final de cada época."""
        try:
            # Métricas básicas
            train_loss = logs.get('loss', 0)
            val_loss = logs.get('val_loss', 0)
            train_mae = logs.get('mae', 0)
            val_mae = logs.get('val_mae', 0)
            
            # Agregar al historial
            self.train_loss_history.append(train_loss)
            self.val_loss_history.append(val_loss)
            
            # Calcular métricas avanzadas
            advanced_metrics = self._calculate_advanced_metrics(epoch)
            
            # Detectar problemas de entrenamiento
            self._check_training_issues()
            
            # Verificar pérdidas NaN/Inf
            self.alert_service.check_nan_loss(train_loss)
            self.alert_service.check_nan_loss(val_loss)
            
            # Análisis de tasa de aprendizaje
            lr_analysis = self.metrics_calculator.calculate_learning_rate_effectiveness(
                self.train_loss_history
            )
            
            # Preparar datos completos
            update_data = {
                'epoch': epoch + 1,
                'basic_metrics': {
                    'loss': float(train_loss),
                    'val_loss': float(val_loss),
                    'mae': float(train_mae),
                    'val_mae': float(val_mae)
                },
                'advanced_metrics': advanced_metrics,
                'learning_rate_analysis': lr_analysis,
                'training_analysis': {
                    'overfitting': int(self.metrics_calculator.detect_overfitting(
                        self.train_loss_history, self.val_loss_history
                    ).get('overfitting', False)),
                    'underfitting': int(self.metrics_calculator.detect_underfitting(
                        self.train_loss_history, self.val_loss_history
                    ).get('underfitting', False))
                },
                'active_alerts': len(self.alert_service.get_active_alerts())
            }
            
            # Almacenar métricas
            if self.training_session_id:
                self.metrics_storage.store_epoch_metrics(
                    self.training_session_id, epoch + 1, update_data
                )
            
            # Emitir métricas avanzadas
            self.event_emitter.emit_advanced_metrics(update_data)
            
            # Emitir estadísticas de hardware
            hardware_stats = self.hardware_monitor.get_current_stats()
            if hardware_stats:
                self._emit_hardware_stats(hardware_stats)
                
        except Exception as e:
            logger.error(f"Error en callback época {epoch}: {e}")
            
    def on_train_end(self, logs=None):
        """Finaliza el monitoreo al terminar el entrenamiento."""
        try:
            # Detener monitoreo de hardware
            self.hardware_monitor.stop_monitoring()
            
            # Finalizar sesión de entrenamiento
            if self.training_session_id:
                final_loss = self.val_loss_history[-1] if self.val_loss_history else None
                total_epochs = len(self.train_loss_history)
                self.metrics_storage.finish_training_session(
                    self.training_session_id, 'completed', final_loss, total_epochs
                )
            
            # Enviar resumen final
            final_summary = {
                'total_epochs': len(self.train_loss_history),
                'final_metrics': {
                    'train_loss': self.train_loss_history[-1] if self.train_loss_history else 0,
                    'val_loss': self.val_loss_history[-1] if self.val_loss_history else 0
                },
                'alerts_summary': {
                    'total_alerts': len(self.alert_service.alerts),
                    'critical_alerts': len(self.alert_service.get_alerts_by_level('CRITICAL')),
                    'warning_alerts': len(self.alert_service.get_alerts_by_level('WARNING'))
                }
            }
            
            self.event_emitter.emit_training_summary(final_summary)
            self.event_emitter.emit_log('Monitoreo avanzado finalizado')
            
        except Exception as e:
            logger.error(f"Error finalizando callback: {e}")
    
    def _calculate_advanced_metrics(self, epoch):
        """Calcula métricas avanzadas para la época actual."""
        try:
            # Hacer predicciones
            train_pred = self.model.predict(self.X_train, verbose=0)
            val_pred = self.model.predict(self.X_val, verbose=0)
            
            # Calcular métricas según el tipo de modelo
            if self.model_type == 'regression':
                train_metrics = self.metrics_calculator.calculate_regression_metrics(
                    self.y_train.flatten(), train_pred.flatten()
                )
                val_metrics = self.metrics_calculator.calculate_regression_metrics(
                    self.y_val.flatten(), val_pred.flatten()
                )
            else:
                train_metrics = {}
                val_metrics = {}
            
            # Guardar en historial
            self.train_metrics_history.append(train_metrics)
            self.val_metrics_history.append(val_metrics)
            
            # Obtener ejemplos de predicciones
            prediction_examples = self.metrics_calculator.get_prediction_examples(
                self.X_val[:20], self.y_val[:20].flatten(), val_pred[:20].flatten(),
                model_type=self.model_type, n_examples=5
            )
            
            return {
                'train': train_metrics,
                'validation': val_metrics,
                'prediction_examples': prediction_examples
            }
            
        except Exception as e:
            logger.error(f"Error calculando métricas avanzadas: {e}")
            return {
                'train': {},
                'validation': {},
                'prediction_examples': {'correct': [], 'incorrect': [], 'borderline': []}
            }
    
    def _check_training_issues(self):
        """Verifica problemas comunes de entrenamiento."""
        if len(self.train_loss_history) >= 5:
            # Verificar overfitting
            self.alert_service.check_overfitting(
                self.train_loss_history, self.val_loss_history
            )
            
            # Verificar underfitting
            self.alert_service.check_underfitting(
                self.train_loss_history, self.val_loss_history
            )
            
            # Verificar aprendizaje estancado
            self.alert_service.check_stagnant_learning(self.train_loss_history)
    
    def _emit_hardware_stats(self, stats):
        """Emite estadísticas de hardware con verificación de alertas."""
        try:
            # Verificar alertas de hardware
            hardware_alerts = self.alert_service.check_hardware_alerts(stats)
            
            # Almacenar métricas de hardware
            if self.training_session_id:
                self.metrics_storage.store_hardware_metrics(self.training_session_id, stats)
            
            # Emitir estadísticas
            self.event_emitter.emit_hardware_stats(stats)
            
        except Exception as e:
            logger.error(f"Error emitiendo estadísticas de hardware: {e}")