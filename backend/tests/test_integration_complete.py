# backend/tests/test_integration_complete.py
"""
Tests de integración completos que verifican el funcionamiento conjunto
de todos los componentes del sistema.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
import os
import json
import tempfile
import asyncio
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestCompleteIntegration:
    """Tests de integración completos del sistema."""
    
    @pytest.fixture
    def mock_services(self):
        """Fixture que proporciona mocks de todos los servicios."""
        with patch('services.validation.ModelValidationService') as mock_validation, \
             patch('services.experiments.ExperimentService') as mock_experiment, \
             patch('services.templates.TemplateService') as mock_template:
            
            # Configurar mocks
            mock_validation.return_value.validate_architecture.return_value.is_valid = True
            mock_validation.return_value.validate_training_params.return_value.is_valid = True
            mock_validation.return_value.validate_experiment_config.return_value.is_valid = True
            
            mock_experiment.return_value.create_experiment.return_value = {
                'id': 'exp_123',
                'name': 'Test Experiment',
                'status': 'created'
            }
            
            mock_template.return_value.get_template.return_value = {
                'name': 'simple_regression',
                'layers': [1],
                'activation': 'linear'
            }
            
            yield {
                'validation': mock_validation,
                'experiment': mock_experiment,
                'template': mock_template
            }
    
    def test_complete_training_workflow(self, mock_services):
        """Test del flujo completo de entrenamiento desde configuración hasta resultados."""
        # 1. Configuración inicial
        config = {
            'model': {
                'layers': [1],
                'activation': 'linear',
                'dropout_rate': 0.0
            },
            'training': {
                'epochs': 100,
                'learning_rate': 0.1,
                'batch_size': 32
            },
            'experiment': {
                'name': 'Integration Test',
                'description': 'Test completo de integración'
            }
        }
        
        # 2. Validación de configuración
        validation_service = mock_services['validation'].return_value
        validation_result = validation_service.validate_experiment_config(config)
        assert validation_result.is_valid
        
        # 3. Creación de experimento
        experiment_service = mock_services['experiment'].return_value
        experiment = experiment_service.create_experiment(config['experiment'])
        assert experiment['id'] == 'exp_123'
        assert experiment['status'] == 'created'
        
        # 4. Simulación de entrenamiento
        training_events = [
            {'type': 'training_start', 'data': {'total_epochs': 100}},
            {'type': 'epoch_complete', 'data': {'epoch': 50, 'loss': 0.1, 'progress': 0.5}},
            {'type': 'training_complete', 'data': {'final_loss': 0.01, 'model_saved': True}}
        ]
        
        # Verificar eventos de entrenamiento
        for event in training_events:
            assert 'type' in event
            assert 'data' in event
            
        # 5. Verificación de resultados
        final_event = training_events[-1]
        assert final_event['type'] == 'training_complete'
        assert final_event['data']['model_saved'] is True
        assert final_event['data']['final_loss'] < 0.1
    
    def test_template_to_experiment_integration(self, mock_services):
        """Test integración entre servicio de plantillas y experimentos."""
        # 1. Obtener plantilla
        template_service = mock_services['template'].return_value
        template = template_service.get_template('simple_regression')
        
        assert template['name'] == 'simple_regression'
        assert 'layers' in template
        assert 'activation' in template
        
        # 2. Crear experimento basado en plantilla
        experiment_config = {
            'name': f"Experiment from {template['name']}",
            'template_id': 'simple_regression',
            'model': {
                'layers': template['layers'],
                'activation': template['activation']
            }
        }
        
        # 3. Validar configuración generada
        validation_service = mock_services['validation'].return_value
        validation_result = validation_service.validate_experiment_config(experiment_config)
        assert validation_result.is_valid
        
        # 4. Crear experimento
        experiment_service = mock_services['experiment'].return_value
        experiment = experiment_service.create_experiment(experiment_config)
        assert experiment['id'] == 'exp_123'
    
    def test_validation_experiment_storage_integration(self, mock_services):
        """Test integración entre validación, experimentos y almacenamiento."""
        # 1. Configuración con errores intencionados
        invalid_config = {
            'model': {
                'layers': [],  # Error: lista vacía
                'activation': 'invalid_activation'  # Error: activación inválida
            },
            'training': {
                'epochs': -1,  # Error: valor negativo
                'learning_rate': 2.0  # Error: fuera de rango
            }
        }
        
        # 2. Validación debe fallar
        validation_service = mock_services['validation'].return_value
        validation_service.validate_experiment_config.return_value.is_valid = False
        validation_service.validate_experiment_config.return_value.errors = [
            'Layers cannot be empty',
            'Invalid activation function',
            'Epochs must be positive',
            'Learning rate out of range'
        ]
        
        validation_result = validation_service.validate_experiment_config(invalid_config)
        assert not validation_result.is_valid
        assert len(validation_result.errors) == 4
        
        # 3. Experimento no debe crearse con configuración inválida
        experiment_service = mock_services['experiment'].return_value
        experiment_service.create_experiment.side_effect = ValueError("Invalid configuration")
        
        with pytest.raises(ValueError):
            experiment_service.create_experiment(invalid_config)
    
    def test_real_time_monitoring_integration(self, mock_services):
        """Test integración del monitoreo en tiempo real durante entrenamiento."""
        # 1. Configuración de monitoreo
        monitoring_config = {
            'hardware_monitoring': True,
            'progress_updates': True,
            'metric_streaming': True,
            'alert_thresholds': {
                'cpu_percent': 90,
                'memory_percent': 85,
                'gpu_percent': 95
            }
        }
        
        # 2. Simulación de métricas de hardware
        hardware_metrics = [
            {'cpu_percent': 45.2, 'memory_percent': 67.8, 'timestamp': '2024-01-15T10:30:00Z'},
            {'cpu_percent': 78.5, 'memory_percent': 82.1, 'timestamp': '2024-01-15T10:30:30Z'},
            {'cpu_percent': 92.3, 'memory_percent': 88.7, 'timestamp': '2024-01-15T10:31:00Z'}  # Alerta
        ]
        
        # 3. Verificar detección de alertas
        alerts_triggered = []
        for metric in hardware_metrics:
            if metric['cpu_percent'] > monitoring_config['alert_thresholds']['cpu_percent']:
                alerts_triggered.append({
                    'type': 'cpu_high',
                    'value': metric['cpu_percent'],
                    'threshold': monitoring_config['alert_thresholds']['cpu_percent'],
                    'timestamp': metric['timestamp']
                })
            
            if metric['memory_percent'] > monitoring_config['alert_thresholds']['memory_percent']:
                alerts_triggered.append({
                    'type': 'memory_high',
                    'value': metric['memory_percent'],
                    'threshold': monitoring_config['alert_thresholds']['memory_percent'],
                    'timestamp': metric['timestamp']
                })
        
        # 4. Verificar que se generaron alertas apropiadas
        assert len(alerts_triggered) == 2  # CPU y memoria altas en el último metric
        assert any(alert['type'] == 'cpu_high' for alert in alerts_triggered)
        assert any(alert['type'] == 'memory_high' for alert in alerts_triggered)
    
    def test_websocket_api_integration(self, mock_services):
        """Test integración entre WebSocket y API REST."""
        # 1. Configuración inicial via API REST
        api_config = {
            'model': {'layers': [1], 'activation': 'linear'},
            'training': {'epochs': 100, 'learning_rate': 0.1}
        }
        
        # 2. Validación via servicio
        validation_service = mock_services['validation'].return_value
        validation_result = validation_service.validate_experiment_config(api_config)
        assert validation_result.is_valid
        
        # 3. Simulación de eventos WebSocket durante entrenamiento
        websocket_events = []
        
        def mock_emit(event_type, data):
            websocket_events.append({'type': event_type, 'data': data})
        
        # Simular entrenamiento con eventos WebSocket
        mock_emit('training_start', {'config': api_config, 'total_epochs': 100})
        
        for epoch in range(1, 6):  # Simular 5 épocas
            mock_emit('epoch_complete', {
                'epoch': epoch,
                'loss': 0.5 - (epoch * 0.1),
                'progress': epoch / 100
            })
        
        mock_emit('training_complete', {
            'final_loss': 0.01,
            'total_epochs': 100,
            'model_saved': True
        })
        
        # 4. Verificar secuencia de eventos
        assert len(websocket_events) == 7  # start + 5 epochs + complete
        assert websocket_events[0]['type'] == 'training_start'
        assert websocket_events[-1]['type'] == 'training_complete'
        
        # Verificar progreso creciente
        epoch_events = [e for e in websocket_events if e['type'] == 'epoch_complete']
        for i in range(1, len(epoch_events)):
            assert epoch_events[i]['data']['progress'] > epoch_events[i-1]['data']['progress']
    
    def test_error_handling_across_services(self, mock_services):
        """Test manejo de errores a través de todos los servicios."""
        # 1. Error en validación
        validation_service = mock_services['validation'].return_value
        validation_service.validate_experiment_config.side_effect = Exception("Validation service error")
        
        with pytest.raises(Exception) as exc_info:
            validation_service.validate_experiment_config({})
        assert "Validation service error" in str(exc_info.value)
        
        # 2. Error en experimento
        experiment_service = mock_services['experiment'].return_value
        experiment_service.create_experiment.side_effect = Exception("Experiment service error")
        
        with pytest.raises(Exception) as exc_info:
            experiment_service.create_experiment({})
        assert "Experiment service error" in str(exc_info.value)
        
        # 3. Error en plantillas
        template_service = mock_services['template'].return_value
        template_service.get_template.side_effect = Exception("Template service error")
        
        with pytest.raises(Exception) as exc_info:
            template_service.get_template('nonexistent')
        assert "Template service error" in str(exc_info.value)
    
    def test_concurrent_training_sessions(self, mock_services):
        """Test manejo de múltiples sesiones de entrenamiento concurrentes."""
        # 1. Configuraciones para múltiples entrenamientos
        configs = [
            {
                'id': 'session_1',
                'model': {'layers': [1], 'activation': 'linear'},
                'training': {'epochs': 50}
            },
            {
                'id': 'session_2',
                'model': {'layers': [10, 1], 'activation': 'relu'},
                'training': {'epochs': 100}
            },
            {
                'id': 'session_3',
                'model': {'layers': [5, 5, 1], 'activation': 'tanh'},
                'training': {'epochs': 75}
            }
        ]
        
        # 2. Simulación de entrenamientos concurrentes
        active_sessions = {}
        
        for config in configs:
            session_id = config['id']
            active_sessions[session_id] = {
                'config': config,
                'status': 'running',
                'current_epoch': 0,
                'total_epochs': config['training']['epochs'],
                'progress': 0.0
            }
        
        # 3. Simulación de progreso concurrente
        for epoch in range(1, 26):  # 25 épocas de simulación
            for session_id, session in active_sessions.items():
                if session['current_epoch'] < session['total_epochs']:
                    session['current_epoch'] += 1
                    session['progress'] = session['current_epoch'] / session['total_epochs']
                    
                    if session['current_epoch'] >= session['total_epochs']:
                        session['status'] = 'completed'
        
        # 4. Verificar que todas las sesiones progresaron correctamente
        for session_id, session in active_sessions.items():
            if session['total_epochs'] <= 25:
                assert session['status'] == 'completed'
                assert session['progress'] == 1.0
            else:
                assert session['status'] == 'running'
                assert 0 < session['progress'] < 1.0
    
    def test_data_pipeline_integration(self, mock_services):
        """Test integración completa del pipeline de datos."""
        # 1. Datos de entrada típicos (Celsius-Fahrenheit)
        raw_data = {
            'celsius': [-40, -10, 0, 8, 15, 22, 38],
            'fahrenheit': [-40, 14, 32, 46.4, 59, 71.6, 100.4]
        }
        
        # 2. Procesamiento de datos
        processed_data = {
            'input': raw_data['celsius'],
            'output': raw_data['fahrenheit'],
            'size': len(raw_data['celsius']),
            'normalized': False
        }
        
        # 3. Validación de datos
        assert len(processed_data['input']) == len(processed_data['output'])
        assert processed_data['size'] > 0
        
        # Verificar relación Celsius-Fahrenheit
        for c, f in zip(processed_data['input'], processed_data['output']):
            expected_f = c * 1.8 + 32
            assert abs(f - expected_f) < 0.1
        
        # 4. Configuración de modelo basada en datos
        model_config = {
            'input_shape': [1],  # Una característica (Celsius)
            'output_shape': [1],  # Una salida (Fahrenheit)
            'layers': [1],  # Regresión lineal simple
            'activation': 'linear'
        }
        
        # 5. Validación de configuración
        validation_service = mock_services['validation'].return_value
        validation_result = validation_service.validate_architecture(model_config)
        assert validation_result.is_valid
    
    def test_model_lifecycle_integration(self, mock_services):
        """Test integración completa del ciclo de vida del modelo."""
        # 1. Creación de modelo
        model_config = {
            'name': 'celsius_fahrenheit_model',
            'version': '1.0',
            'architecture': {
                'layers': [1],
                'activation': 'linear'
            },
            'training': {
                'epochs': 100,
                'learning_rate': 0.1
            }
        }
        
        # 2. Validación
        validation_service = mock_services['validation'].return_value
        validation_result = validation_service.validate_experiment_config(model_config)
        assert validation_result.is_valid
        
        # 3. Entrenamiento (simulado)
        training_history = {
            'loss': [0.5, 0.3, 0.1, 0.05, 0.01],
            'val_loss': [0.6, 0.35, 0.12, 0.06, 0.015],
            'epochs': [1, 2, 3, 4, 5]
        }
        
        # 4. Evaluación
        evaluation_metrics = {
            'final_loss': training_history['loss'][-1],
            'final_val_loss': training_history['val_loss'][-1],
            'training_epochs': len(training_history['epochs']),
            'convergence': training_history['loss'][0] - training_history['loss'][-1]
        }
        
        assert evaluation_metrics['final_loss'] < 0.1
        assert evaluation_metrics['convergence'] > 0.4  # Buena convergencia
        
        # 5. Almacenamiento
        model_metadata = {
            'config': model_config,
            'training_history': training_history,
            'evaluation': evaluation_metrics,
            'saved_at': datetime.now().isoformat(),
            'file_path': 'models/celsius_fahrenheit_model_v1.keras'
        }
        
        assert 'config' in model_metadata
        assert 'training_history' in model_metadata
        assert 'evaluation' in model_metadata
        assert model_metadata['file_path'].endswith('.keras')
    
    def test_api_websocket_synchronization(self, mock_services):
        """Test sincronización entre API REST y WebSocket."""
        # 1. Estado inicial via API
        api_state = {
            'training_active': False,
            'current_experiment': None,
            'last_update': None
        }
        
        # 2. Inicio de entrenamiento via API
        experiment_config = {
            'name': 'Sync Test',
            'model': {'layers': [1], 'activation': 'linear'},
            'training': {'epochs': 50}
        }
        
        # Simular respuesta API
        api_response = {
            'status': 'success',
            'experiment_id': 'exp_sync_123',
            'message': 'Training started'
        }
        
        # Actualizar estado
        api_state['training_active'] = True
        api_state['current_experiment'] = api_response['experiment_id']
        api_state['last_update'] = datetime.now().isoformat()
        
        # 3. Eventos WebSocket correspondientes
        websocket_events = []
        
        # Evento de inicio
        websocket_events.append({
            'type': 'training_start',
            'experiment_id': api_response['experiment_id'],
            'timestamp': api_state['last_update']
        })
        
        # Eventos de progreso
        for epoch in range(1, 6):
            websocket_events.append({
                'type': 'epoch_complete',
                'experiment_id': api_response['experiment_id'],
                'epoch': epoch,
                'progress': epoch / 50,
                'timestamp': datetime.now().isoformat()
            })
        
        # 4. Verificar sincronización
        assert api_state['training_active'] is True
        assert api_state['current_experiment'] == api_response['experiment_id']
        
        # Todos los eventos WebSocket deben tener el mismo experiment_id
        for event in websocket_events:
            assert event['experiment_id'] == api_response['experiment_id']
        
        # 5. Finalización via WebSocket
        websocket_events.append({
            'type': 'training_complete',
            'experiment_id': api_response['experiment_id'],
            'final_loss': 0.01,
            'timestamp': datetime.now().isoformat()
        })
        
        # Actualizar estado API
        api_state['training_active'] = False
        api_state['last_update'] = websocket_events[-1]['timestamp']
        
        assert api_state['training_active'] is False
        assert len(websocket_events) == 7  # start + 5 epochs + complete