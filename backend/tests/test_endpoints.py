# backend/tests/test_endpoints.py
"""
Tests completos para todos los endpoints de la API REST.
"""

import pytest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask
from routes import register_all_routes

class TestAPIEndpoints:
    """Tests para todos los endpoints de la API."""
    
    @pytest.fixture
    def app(self):
        """Fixture que crea una aplicación Flask de prueba."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Mock de servicios
        with patch('services.validation.ModelValidationService'), \
             patch('services.experiments.ExperimentService'), \
             patch('services.templates.TemplateService'), \
             patch('services.statistics_service.StatisticsService'):
            
            # Crear servicios mock
            services = {
                'training_service': None,
                'statistics_service': None
            }
            
            # Registrar rutas modularizadas
            register_all_routes(app, services)
            
            yield app
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba para hacer requests."""
        return app.test_client()
    
    # Tests de endpoints básicos
    def test_status_endpoint(self, client):
        """Test del endpoint de estado."""
        response = client.get('/api/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
    
    def test_model_info_endpoint(self, client):
        """Test del endpoint de información del modelo."""
        with patch('flask.current_app') as mock_app:
            mock_app.model = Mock()
            mock_app.model.summary = Mock(return_value="Model summary")
            
            response = client.get('/api/model/info')
            assert response.status_code == 200
    
    def test_predict_endpoint(self, client):
        """Test del endpoint de predicción."""
        response = client.get('/api/predict?celsius=25')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'fahrenheit' in data
        assert 'celsius' in data
    
    def test_training_data_endpoint(self, client):
        """Test del endpoint de datos de entrenamiento."""
        response = client.get('/api/training-data')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'celsius' in data
        assert 'fahrenheit' in data
        assert 'count' in data
    
    def test_dataset_endpoint(self, client):
        """Test del endpoint de dataset."""
        response = client.get('/api/dataset')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'name' in data
        assert 'size' in data
        assert 'features' in data
        assert 'target' in data
    
    # Tests de arquitectura del modelo
    def test_get_model_architecture(self, client):
        """Test para obtener arquitectura del modelo."""
        response = client.get('/api/model/architecture')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'layers' in data
        assert 'optimizer' in data
        assert 'loss' in data
    
    def test_set_model_architecture(self, client):
        """Test para establecer arquitectura del modelo."""
        architecture = {
            'layers': [1],
            'activation': 'linear',
            'optimizer': 'adam',
            'loss': 'mse'
        }
        
        response = client.post('/api/model/architecture', 
                             json=architecture,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_validate_model_architecture(self, client):
        """Test para validar arquitectura del modelo."""
        architecture = {
            'layers': [1],
            'activation': 'linear'
        }
        
        response = client.post('/api/model/architecture/validate',
                             json=architecture,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'valid' in data
    
    # Tests de predicciones
    def test_predict_single(self, client):
        """Test de predicción individual."""
        with patch('flask.current_app') as mock_app:
            mock_app.model = Mock()
            mock_app.model.predict = Mock(return_value=[[77.0]])
            
            prediction_data = {'celsius': 25}
            response = client.post('/api/experiments/predict',
                                 json=prediction_data,
                                 content_type='application/json')
            assert response.status_code == 200
    
    def test_predict_batch(self, client):
        """Test de predicción en lote."""
        with patch('flask.current_app') as mock_app:
            mock_app.model = Mock()
            mock_app.model.predict = Mock(return_value=[[32.0], [77.0], [212.0]])
            
            batch_data = {'celsius_values': [0, 25, 100]}
            response = client.post('/api/experiments/predict-batch',
                                 json=batch_data,
                                 content_type='application/json')
            assert response.status_code == 200
    
    def test_model_status(self, client):
        """Test del estado del modelo."""
        response = client.get('/api/experiments/model-status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'model_loaded' in data


class TestTemplateEndpoints:
    """Tests para endpoints de plantillas."""
    
    @pytest.fixture
    def app(self):
        """Fixture que crea una aplicación Flask de prueba."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Importar y registrar blueprint de plantillas refactorizado
        from api.templates import create_template_blueprint
        template_bp = create_template_blueprint()
        app.register_blueprint(template_bp)
        
        yield app
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba."""
        return app.test_client()
    
    @patch('api.templates.template_service.TemplateService')
    def test_list_templates(self, mock_service, client):
        """Test para listar plantillas."""
        mock_service.return_value.list_templates.return_value = [
            {'id': '1', 'name': 'Simple Regression'},
            {'id': '2', 'name': 'Multi Layer'}
        ]
        
        response = client.get('/api/templates')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'templates' in data
        assert len(data['templates']) == 2
    
    @patch('api.templates.template_service.TemplateService')
    def test_get_template(self, mock_service, client):
        """Test para obtener una plantilla específica."""
        mock_service.return_value.get_template.return_value = {
            'id': '1',
            'name': 'Simple Regression',
            'layers': [1]
        }
        
        response = client.get('/api/templates/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == '1'
    
    @patch('api.templates.template_service.TemplateService')
    def test_recommend_templates(self, mock_service, client):
        """Test para recomendaciones de plantillas."""
        mock_service.return_value.recommend_templates.return_value = [
            {'id': '1', 'name': 'Recommended Template', 'score': 0.95}
        ]
        
        requirements = {'use_case': 'regression', 'complexity': 'beginner'}
        response = client.post('/api/templates/recommend',
                             json={'requirements': requirements},
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'recommendations' in data
    
    def test_get_complexity_levels(self, client):
        """Test para obtener niveles de complejidad."""
        response = client.get('/api/templates/complexity-levels')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'complexity_levels' in data
        assert len(data['complexity_levels']) == 3
    
    def test_get_use_cases(self, client):
        """Test para obtener casos de uso."""
        response = client.get('/api/templates/use-cases')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'use_cases' in data
        assert len(data['use_cases']) == 4


class TestExperimentEndpoints:
    """Tests para endpoints de experimentos."""
    
    @pytest.fixture
    def app(self):
        """Fixture que crea una aplicación Flask de prueba."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Importar y registrar blueprint de experimentos
        from api.experiments import create_experiment_blueprint
        experiment_bp = create_experiment_blueprint()
        app.register_blueprint(experiment_bp)
        
        yield app
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba."""
        return app.test_client()
    
    @patch('src.api.experiments.experiment_service.ExperimentService')
    def test_list_experiments(self, mock_service, client):
        """Test para listar experimentos."""
        mock_service.return_value.list_experiments.return_value = [
            {'id': 'exp1', 'name': 'Test Experiment 1'},
            {'id': 'exp2', 'name': 'Test Experiment 2'}
        ]
        
        response = client.get('/api/experiments')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'experiments' in data
        assert data['total'] == 2
    
    @patch('src.api.experiments.experiment_service.ExperimentService')
    def test_get_experiment(self, mock_service, client):
        """Test para obtener un experimento específico."""
        mock_service.return_value.get_experiment.return_value = {
            'id': 'exp1',
            'name': 'Test Experiment',
            'status': 'completed'
        }
        
        response = client.get('/api/experiments/exp1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'experiment' in data
        assert data['experiment']['id'] == 'exp1'
    
    @patch('src.api.experiments.experiment_service.ExperimentService')
    def test_create_run(self, mock_service, client):
        """Test para crear una nueva ejecución."""
        mock_service.return_value.create_run.return_value = {
            'id': 'run1',
            'experiment_id': 'exp1',
            'status': 'created'
        }
        
        run_data = {'parameters': {'epochs': 100}}
        response = client.post('/api/experiments/exp1/runs',
                             json=run_data,
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'run' in data


class TestValidationEndpoints:
    """Tests para endpoints de validación."""
    
    @pytest.fixture
    def app(self):
        """Fixture que crea una aplicación Flask de prueba."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Importar y registrar blueprint de validación refactorizado
        from api.validation.batch_validation import batch_bp
        app.register_blueprint(batch_bp)
        
        yield app
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba."""
        return app.test_client()
    
    @patch('services.validation.batch_validation_service.BatchValidationService')
    def test_validate_architecture(self, mock_service, client):
        """Test para validar arquitectura."""
        mock_validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'summary': {'total': 1, 'valid': 1, 'invalid': 0}
        }
        
        mock_service.return_value.validate_batch.return_value = mock_validation_result
        
        architecture = {'layers': [1], 'activation': 'linear'}
        response = client.post('/batch',
                             json={'items': [architecture]},
                             content_type='application/json')
        assert response.status_code == 200


class TestAdvancedConfigEndpoints:
    """Tests para endpoints de configuración avanzada."""
    
    @pytest.fixture
    def app(self):
        """Fixture que crea una aplicación Flask de prueba."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Importar y registrar blueprint de configuración avanzada
        from api.config import create_config_blueprint
        config_bp = create_config_blueprint()
        app.register_blueprint(config_bp)
        
        yield app
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba."""
        return app.test_client()
    
    def test_get_full_config(self, client):
        """Test para obtener configuración completa."""
        response = client.get('/api/config')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'config' in data
        assert 'training' in data['config']
        assert 'model' in data['config']
    
    def test_get_config_section(self, client):
        """Test para obtener sección específica."""
        response = client.get('/api/config/section/training')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['section'] == 'training'
        assert 'config' in data
    
    def test_update_config_section(self, client):
        """Test para actualizar sección de configuración."""
        config_data = {
            'default_epochs': 1000,
            'default_learning_rate': 0.01
        }
        
        response = client.put('/api/config/section/training',
                            json=config_data,
                            content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])