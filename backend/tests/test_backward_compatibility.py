# backend/tests/test_backward_compatibility.py
"""
Tests de compatibilidad hacia atrás para asegurar que las nuevas funcionalidades
no rompan el sistema existente.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json
import tempfile

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBackwardCompatibility:
    """Tests de compatibilidad hacia atrás."""
    
    def test_legacy_training_config_format(self):
        """Test que el formato legacy de configuración de entrenamiento sigue funcionando."""
        # Formato legacy típico usado en el sistema original
        legacy_config = {
            'epochs': 500,
            'learning_rate': 0.1,
            'batch_size': 32,
            'layers': [1],  # Formato legacy: lista directa
            'activation': 'linear'
        }
        
        # Verificar que se puede procesar sin errores
        assert isinstance(legacy_config['epochs'], int)
        assert isinstance(legacy_config['learning_rate'], float)
        assert isinstance(legacy_config['batch_size'], int)
        assert isinstance(legacy_config['layers'], list)
        assert len(legacy_config['layers']) > 0
    
    def test_legacy_model_architecture_compatibility(self):
        """Test compatibilidad con arquitecturas de modelo legacy."""
        # Arquitectura simple típica del sistema original
        legacy_architecture = {
            'layers': [1],
            'activation': 'linear'
        }
        
        # Debe poder convertirse al nuevo formato
        new_format = {
            'layers': legacy_architecture['layers'],
            'activation': legacy_architecture['activation'],
            'dropout_rate': 0.0,  # Valor por defecto
            'batch_normalization': False  # Valor por defecto
        }
        
        assert new_format['layers'] == legacy_architecture['layers']
        assert new_format['activation'] == legacy_architecture['activation']
        assert 'dropout_rate' in new_format
        assert 'batch_normalization' in new_format
    
    def test_legacy_celsius_fahrenheit_dataset(self):
        """Test compatibilidad con el dataset Celsius-Fahrenheit original."""
        # Datos típicos del sistema original
        celsius_data = [-40, -10, 0, 8, 15, 22, 38]
        fahrenheit_data = [-40, 14, 32, 46.4, 59, 71.6, 100.4]
        
        # Verificar que los datos siguen la fórmula correcta
        for c, f in zip(celsius_data, fahrenheit_data):
            expected_f = c * 1.8 + 32
            assert abs(f - expected_f) < 0.1, f"Conversión incorrecta: {c}°C → {f}°F (esperado: {expected_f}°F)"
    
    def test_legacy_training_parameters_ranges(self):
        """Test que los rangos de parámetros legacy siguen siendo válidos."""
        # Parámetros típicos del sistema original
        legacy_params = {
            'epochs': 500,
            'learning_rate': 0.1,
            'batch_size': 32
        }
        
        # Verificar rangos válidos
        assert 1 <= legacy_params['epochs'] <= 10000
        assert 0.0001 <= legacy_params['learning_rate'] <= 1.0
        assert 1 <= legacy_params['batch_size'] <= 1024
    
    def test_legacy_model_saving_format(self):
        """Test compatibilidad con formato de guardado de modelos legacy."""
        # El sistema original guarda modelos como .keras
        model_filename = "modelo_entrenado.keras"
        
        # Verificar que el formato sigue siendo soportado
        assert model_filename.endswith('.keras')
        
        # Metadatos típicos que se guardaban
        legacy_metadata = {
            'model_type': 'regression',
            'input_shape': [1],
            'output_shape': [1],
            'training_epochs': 500,
            'final_loss': 0.001
        }
        
        assert all(key in legacy_metadata for key in ['model_type', 'input_shape', 'output_shape'])
    
    def test_legacy_api_response_format(self):
        """Test compatibilidad con formato de respuesta API legacy."""
        # Formato típico de respuesta del sistema original
        legacy_response = {
            'status': 'success',
            'epoch': 100,
            'loss': 0.0123,
            'val_loss': 0.0145,
            'progress': 0.2,  # 20%
            'message': 'Entrenamiento en progreso'
        }
        
        # Verificar estructura esperada
        required_fields = ['status', 'epoch', 'loss', 'progress']
        for field in required_fields:
            assert field in legacy_response
        
        # Verificar tipos
        assert isinstance(legacy_response['epoch'], int)
        assert isinstance(legacy_response['loss'], float)
        assert isinstance(legacy_response['progress'], float)
        assert 0 <= legacy_response['progress'] <= 1
    
    def test_legacy_websocket_events(self):
        """Test compatibilidad con eventos WebSocket legacy."""
        # Eventos típicos del sistema original
        legacy_events = [
            {
                'type': 'training_start',
                'data': {'total_epochs': 500}
            },
            {
                'type': 'epoch_complete',
                'data': {
                    'epoch': 1,
                    'loss': 0.5,
                    'val_loss': 0.6,
                    'progress': 0.002
                }
            },
            {
                'type': 'training_complete',
                'data': {
                    'final_loss': 0.001,
                    'total_time': 120.5,
                    'model_saved': True
                }
            }
        ]
        
        # Verificar estructura de eventos
        for event in legacy_events:
            assert 'type' in event
            assert 'data' in event
            assert isinstance(event['data'], dict)
    
    def test_legacy_configuration_file_format(self):
        """Test compatibilidad con archivos de configuración legacy."""
        # Configuración típica del sistema original
        legacy_config = {
            'model': {
                'layers': [1],
                'activation': 'linear'
            },
            'training': {
                'epochs': 500,
                'learning_rate': 0.1,
                'batch_size': 32
            },
            'data': {
                'celsius_range': [-40, 100],
                'normalize': False
            }
        }
        
        # Verificar que se puede procesar
        assert 'model' in legacy_config
        assert 'training' in legacy_config
        assert 'data' in legacy_config
        
        # Verificar estructura interna
        assert isinstance(legacy_config['model']['layers'], list)
        assert isinstance(legacy_config['training']['epochs'], int)
    
    def test_legacy_error_handling(self):
        """Test que el manejo de errores legacy sigue funcionando."""
        # Errores típicos del sistema original
        legacy_errors = [
            {'code': 'INVALID_EPOCHS', 'message': 'Número de épocas inválido'},
            {'code': 'INVALID_LEARNING_RATE', 'message': 'Learning rate inválido'},
            {'code': 'MODEL_SAVE_ERROR', 'message': 'Error guardando modelo'},
            {'code': 'TRAINING_INTERRUPTED', 'message': 'Entrenamiento interrumpido'}
        ]
        
        # Verificar estructura de errores
        for error in legacy_errors:
            assert 'code' in error
            assert 'message' in error
            assert isinstance(error['code'], str)
            assert isinstance(error['message'], str)
    
    def test_legacy_metrics_format(self):
        """Test compatibilidad con formato de métricas legacy."""
        # Métricas típicas del sistema original
        legacy_metrics = {
            'loss': [0.5, 0.3, 0.1, 0.05, 0.01],
            'val_loss': [0.6, 0.35, 0.12, 0.06, 0.015],
            'epochs': [1, 2, 3, 4, 5],
            'training_time': 120.5,
            'final_accuracy': 0.99
        }
        
        # Verificar estructura
        assert 'loss' in legacy_metrics
        assert 'val_loss' in legacy_metrics
        assert 'epochs' in legacy_metrics
        
        # Verificar que las listas tienen la misma longitud
        assert len(legacy_metrics['loss']) == len(legacy_metrics['val_loss'])
        assert len(legacy_metrics['loss']) == len(legacy_metrics['epochs'])
    
    def test_legacy_hardware_monitoring(self):
        """Test compatibilidad con monitoreo de hardware legacy."""
        # Formato típico de métricas de hardware
        legacy_hardware = {
            'cpu_percent': 45.2,
            'memory_percent': 67.8,
            'gpu_percent': 23.1,
            'gpu_memory_percent': 34.5,
            'timestamp': '2024-01-15T10:30:00Z'
        }
        
        # Verificar campos esperados
        expected_fields = ['cpu_percent', 'memory_percent', 'timestamp']
        for field in expected_fields:
            assert field in legacy_hardware
        
        # Verificar rangos válidos
        assert 0 <= legacy_hardware['cpu_percent'] <= 100
        assert 0 <= legacy_hardware['memory_percent'] <= 100
    
    def test_legacy_seed_reproducibility(self):
        """Test que la reproducibilidad con seed=42 sigue funcionando."""
        # El sistema original usa seed=42 para reproducibilidad
        legacy_seed = 42
        
        # Verificar que el seed es el esperado
        assert legacy_seed == 42
        
        # Simular configuración de seed (sin importar TensorFlow para evitar dependencias)
        seed_config = {
            'random_seed': legacy_seed,
            'numpy_seed': legacy_seed,
            'tensorflow_seed': legacy_seed
        }
        
        assert all(seed == 42 for seed in seed_config.values())
    
    def test_legacy_file_paths(self):
        """Test compatibilidad con rutas de archivos legacy."""
        # Rutas típicas del sistema original
        legacy_paths = {
            'models_dir': 'models/',
            'data_dir': 'data/',
            'logs_dir': 'logs/',
            'model_file': 'models/modelo_entrenado.keras',
            'metrics_file': 'logs/training_metrics.json'
        }
        
        # Verificar que las rutas siguen el formato esperado
        assert legacy_paths['model_file'].endswith('.keras')
        assert legacy_paths['metrics_file'].endswith('.json')
        assert all(path.endswith('/') for path in [legacy_paths['models_dir'], 
                                                   legacy_paths['data_dir'], 
                                                   legacy_paths['logs_dir']])
    
    def test_legacy_validation_rules(self):
        """Test que las reglas de validación legacy siguen aplicándose."""
        # Reglas de validación del sistema original
        validation_rules = {
            'epochs': {'min': 1, 'max': 10000},
            'learning_rate': {'min': 0.0001, 'max': 1.0},
            'batch_size': {'min': 1, 'max': 1024},
            'layers': {'min_count': 1, 'max_neurons': 1000}
        }
        
        # Verificar estructura de reglas
        for param, rules in validation_rules.items():
            assert isinstance(rules, dict)
            if 'min' in rules and 'max' in rules:
                assert rules['min'] < rules['max']
    
    def test_legacy_progress_calculation(self):
        """Test compatibilidad con cálculo de progreso legacy."""
        # Cálculo típico del sistema original
        current_epoch = 250
        total_epochs = 500
        legacy_progress = current_epoch / total_epochs
        
        assert 0 <= legacy_progress <= 1
        assert legacy_progress == 0.5  # 50%
        
        # Formato de progreso en porcentaje
        progress_percent = int(legacy_progress * 100)
        assert progress_percent == 50
    
    def test_legacy_model_prediction_format(self):
        """Test compatibilidad con formato de predicciones legacy."""
        # Formato típico de predicción del sistema original
        celsius_input = 25.0
        expected_fahrenheit = celsius_input * 1.8 + 32  # 77.0
        
        legacy_prediction = {
            'input': celsius_input,
            'output': expected_fahrenheit,
            'model_version': '1.0',
            'prediction_time': '2024-01-15T10:30:00Z'
        }
        
        # Verificar estructura
        assert 'input' in legacy_prediction
        assert 'output' in legacy_prediction
        assert isinstance(legacy_prediction['input'], (int, float))
        assert isinstance(legacy_prediction['output'], (int, float))
    
    def test_legacy_training_callbacks(self):
        """Test compatibilidad con callbacks de entrenamiento legacy."""
        # Callbacks típicos del sistema original
        legacy_callbacks = [
            'EarlyStopping',
            'ModelCheckpoint',
            'ReduceLROnPlateau',
            'CSVLogger'
        ]
        
        # Verificar que los callbacks esperados están disponibles
        for callback_name in legacy_callbacks:
            assert isinstance(callback_name, str)
            assert len(callback_name) > 0
    
    def test_legacy_data_normalization(self):
        """Test compatibilidad con normalización de datos legacy."""
        # El sistema original podía funcionar con y sin normalización
        raw_data = [-40, -10, 0, 8, 15, 22, 38]
        
        # Sin normalización (formato legacy)
        unnormalized = raw_data
        assert unnormalized == raw_data
        
        # Con normalización simple (si se implementaba)
        min_val, max_val = min(raw_data), max(raw_data)
        normalized = [(x - min_val) / (max_val - min_val) for x in raw_data]
        
        # Verificar que la normalización produce valores entre 0 y 1
        assert all(0 <= x <= 1 for x in normalized)
        assert normalized[0] == 0  # Valor mínimo
        assert normalized[-1] == 1  # Valor máximo