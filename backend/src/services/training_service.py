# backend/src/services/training_service.py
"""
Servicio unificado para manejo de entrenamientos de redes neuronales.

Este servicio consolida toda la funcionalidad de entrenamiento previamente
fragmentada en múltiples archivos, siguiendo los patrones establecidos.
"""

import threading
import time
from typing import Dict, Any, Optional
import sys
import os

# Importar desde el config del directorio raíz
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, backend_root)
from config import Config as RootConfig
from utils.logger import setup_logger

# Imports locales consolidados
from .training.model_builder import ModelBuilder
from .training.data_generator import DataGenerator
from .training.event_emitter import EventEmitter
from .training.advanced_callbacks import AdvancedTrainingCallback

logger = setup_logger()

class TrainingService:
    """Servicio unificado para manejo de entrenamientos de redes neuronales.
    
    Este servicio encapsula toda la lógica relacionada con el entrenamiento
    de modelos, incluyendo configuración, ejecución y monitoreo.
    
    Attributes:
        socketio: Instancia de SocketIO para comunicación en tiempo real
        is_training: Estado actual del entrenamiento
        training_thread: Hilo de ejecución del entrenamiento
    """
    
    def __init__(self, socketio):
        """Inicializa el servicio de entrenamiento.
        
        Args:
            socketio: Instancia de SocketIO para comunicación
        """
        self.socketio = socketio
        self.is_training = False
        self.is_paused = False
        self.should_stop = False
        self.training_thread = None
        self.event_emitter = EventEmitter(socketio)
        self.logger = setup_logger()
    
    def start_training(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Inicia un proceso de entrenamiento.
        
        Args:
            params: Parámetros de entrenamiento
            
        Returns:
            Resultado del inicio del entrenamiento
            
        Raises:
            Exception: Si ocurre un error durante el inicio
        """
        try:
            # Detener entrenamiento previo si existe
            if self.is_training:
                self.logger.info("Deteniendo entrenamiento anterior...")
                self.stop_training()
                time.sleep(1)
            
            # Resetear estado
            self._reset_state()
            
            # Iniciar entrenamiento en hilo separado
            self.training_thread = threading.Thread(
                target=self._execute_training,
                args=(params,)
            )
            self.training_thread.daemon = True
            self.training_thread.start()
            
            return {'status': 'started', 'message': 'Entrenamiento iniciado'}
            
        except Exception as e:
            self.logger.error(f"Error iniciando entrenamiento: {e}")
            raise
    
    def stop_training(self) -> None:
        """Detiene el entrenamiento actual."""
        if self.is_training:
            self.should_stop = True
            self.is_paused = False
            self.socketio.emit('training_stopped')
            self.logger.info("Entrenamiento detenido")
    
    def pause_training(self) -> None:
        """Pausa el entrenamiento actual."""
        if self.is_training and not self.is_paused:
            self.is_paused = True
            self.socketio.emit('training_paused')
            self.logger.info("Entrenamiento pausado")
    
    def resume_training(self) -> None:
        """Reanuda el entrenamiento pausado."""
        if self.is_training and self.is_paused:
            self.is_paused = False
            self.logger.info("Entrenamiento reanudado")
    
    def _execute_training(self, params: Dict[str, Any]) -> None:
        """Ejecuta el entrenamiento con métricas avanzadas."""
        try:
            self._set_training_active()
            
            # Extraer parámetros
            epochs = params.get('epochs', RootConfig.DEFAULT_EPOCHS)
            learning_rate = params.get('learningRate', RootConfig.DEFAULT_LEARNING_RATE)
            batch_size = params.get('batchSize', RootConfig.DEFAULT_BATCH_SIZE)
            dataset_size = params.get('datasetSize', 1000)
            
            self.event_emitter.emit_log(
                f'Configuración: {epochs} épocas, dataset {dataset_size}, '
                f'batch {batch_size}, lr {learning_rate}'
            )
            
            # Generar datos
            X, y = DataGenerator.generate_data(dataset_size=dataset_size)
            X_train, X_val, y_train, y_val = DataGenerator.split_data(X, y)
            
            # Crear modelo
            architecture = params.get('architecture', None)
            model = ModelBuilder.create_model(learning_rate, architecture)
            
            # Callback avanzado
            callback = AdvancedTrainingCallback(
                self.event_emitter, X_train, y_train, X_val, y_val
            )
            
            # Entrenamiento
            model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                callbacks=[callback],
                verbose=0
            )
            
            # Guardar modelo si no fue detenido
            if self._should_continue():
                model.save(RootConfig.MODEL_PATH)
                self.event_emitter.emit_training_complete()
                
        except Exception as e:
            self.logger.error(f"Error en entrenamiento: {e}")
            self.event_emitter.emit_error(str(e))
        finally:
            self._set_training_inactive()
    
    def _reset_state(self) -> None:
        """Resetea el estado del servicio."""
        self.should_stop = False
        self.is_paused = False
        self.is_training = False
    
    def _set_training_active(self) -> None:
        """Marca el entrenamiento como activo."""
        self.is_training = True
    
    def _set_training_inactive(self) -> None:
        """Marca el entrenamiento como inactivo."""
        self.is_training = False
        self.is_paused = False
        self.should_stop = False
    
    def _should_continue(self) -> bool:
        """Verifica si el entrenamiento debe continuar."""
        return not self.should_stop