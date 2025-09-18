# c:/dev/entrenamiento/backend/src/services/training/training_executor.py
"""
Ejecutor del proceso de entrenamiento.
"""

import time
import sys
import os

# Importar desde el config del directorio raíz
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, backend_root)
from config import Config as RootConfig
from utils.logger import setup_logger
from .model_builder import ModelBuilder
from .data_generator import DataGenerator
from .metrics_calculator import MetricsCalculator
from .event_emitter import EventEmitter
from .advanced_callbacks import AdvancedTrainingCallback

logger = setup_logger()

class TrainingExecutor:
    """Ejecutor del proceso de entrenamiento."""
    
    def __init__(self, socketio):
        self.event_emitter = EventEmitter(socketio)
        
    def run_training(self, params, controller):
        """Ejecuta el entrenamiento con métricas avanzadas."""
        try:
            controller.set_training_active()
            
            # Parámetros
            epochs = params.get('epochs', RootConfig.DEFAULT_EPOCHS)
            learning_rate = params.get('learningRate', RootConfig.DEFAULT_LEARNING_RATE)
            batch_size = params.get('batchSize', RootConfig.DEFAULT_BATCH_SIZE)
            dataset_size = params.get('datasetSize', 1000)
            
            self.event_emitter.emit_log(f'Configuración recibida: {epochs} épocas, dataset de {dataset_size} muestras, batch size {batch_size}, learning rate {learning_rate}')
            
            self.event_emitter.emit_log('Iniciando entrenamiento con monitoreo avanzado...')
            
            # Datos sintéticos con tamaño personalizado
            X, y = DataGenerator.generate_data(dataset_size=dataset_size)
            X_train, X_val, y_train, y_val = DataGenerator.split_data(X, y)
            
            # Modelo con arquitectura personalizada
            architecture = params.get('architecture', None)
            model = ModelBuilder.create_model(learning_rate, architecture)
            
            # Obtener información de la arquitectura del modelo creado
            architecture_info = ModelBuilder.get_architecture_summary(model)
            
            # Emitir información de arquitectura al inicio del entrenamiento
            self.event_emitter.emit_architecture_info(architecture_info)
            self.event_emitter.emit_log(f'Modelo creado: {architecture_info["total_parameters"]} parámetros, {len(architecture_info["layers"])} capas')
            
            # Crear callback avanzado
            advanced_callback = AdvancedTrainingCallback(
                self.event_emitter, X_train, y_train, X_val, y_val, model_type='regression'
            )
            
            # Entrenamiento con callback avanzado
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                callbacks=[advanced_callback],
                verbose=0
            )
            
            # Guardar modelo solo si no fue detenido
            if controller.should_continue_training():
                model.save(RootConfig.MODEL_PATH)
                
                # Verificación post-entrenamiento de la arquitectura
                saved_architecture_info = ModelBuilder.get_architecture_summary(model)
                self.event_emitter.emit_log('Verificando arquitectura del modelo entrenado...')
                
                # Comparar arquitectura configurada vs arquitectura final
                if architecture:
                    configured_layers = len(architecture.get('hiddenLayers', []))
                    actual_layers = saved_architecture_info['hidden_layers']
                    
                    if configured_layers == actual_layers:
                        self.event_emitter.emit_log(f'[SUCCESS] Verificación exitosa: Modelo entrenado con {actual_layers} capas ocultas como se configuró')
                    else:
                        self.event_emitter.emit_log(f'⚠️ Discrepancia: Configurado {configured_layers} capas, entrenado con {actual_layers} capas', 'warning')
                else:
                    self.event_emitter.emit_log(f'[SUCCESS] Modelo entrenado con arquitectura por defecto: {len(saved_architecture_info["layers"])} capas totales')
                
                # Emitir resumen final de arquitectura
                self.event_emitter.emit_architecture_verification(saved_architecture_info, architecture)
                
                self.event_emitter.emit_log('Entrenamiento completado exitosamente')
                self.event_emitter.emit_training_complete()
            
        except Exception as e:
            logger.error(f"Error en entrenamiento: {e}")
            self.event_emitter.emit_error(str(e))
        finally:
            controller.set_training_inactive()
    
    def _train_epoch(self, model, X_train, y_train, X_val, y_val, epoch):
        """Entrena una época y retorna métricas."""
        history = model.fit(
            X_train, y_train, 
            epochs=1, 
            validation_data=(X_val, y_val), 
            verbose=0
        )
        
        return MetricsCalculator.calculate_epoch_metrics(history, epoch)