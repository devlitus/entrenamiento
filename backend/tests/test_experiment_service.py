# backend/tests/test_experiment_service.py
"""
Tests exhaustivos para ExperimentService.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import sys
import json
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.experiments.experiment_service import ExperimentService
from services.experiments.experiment_storage import ExperimentStorage
from services.validation.model_validation_service import ModelValidationService
from schemas.model_schemas import ValidationResult

class TestExperimentService:
    """Tests para ExperimentService."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Fixture para base de datos temporal."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        yield db_path
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def mock_validator(self):
        """Fixture para validador mock."""
        validator = Mock(spec=ModelValidationService)
        validator.validate_experiment_config.return_value = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[],
            suggestions=[]
        )
        return validator
    
    @pytest.fixture
    def experiment_service(self, temp_db_path, mock_validator):
        """Fixture para servicio de experimentos."""
        storage = ExperimentStorage(temp_db_path)
        return ExperimentService(storage, mock_validator)
    
    @pytest.fixture
    def sample_experiment_config(self):
        """Fixture para configuración de experimento de muestra."""
        return {
            'name': 'test_experiment',
            'description': 'Experimento de prueba',
            'architecture': {
                'layers': [64, 32, 1],
                'activation': 'relu',
                'dropout_rate': 0.2,
                'batch_normalization': False
            },
            'training_params': {
                'epochs': 100,
                'learning_rate': 0.001,
                'batch_size': 32,
                'early_stopping': True,
                'patience': 10,
                'validation_split': 0.2
            },
            'dataset_size': 1000,
            'tags': ['test', 'regression']
        }
    
    def test_create_experiment_valid(self, experiment_service, sample_experiment_config):
        """Test creación de experimento válido."""
        result = experiment_service.create_experiment(sample_experiment_config)
        
        assert 'experiment_id' in result
        assert result['validation']['is_valid']
        assert 'created_at' in result
        assert result['status'] == 'created'
    
    def test_create_experiment_invalid(self, experiment_service, mock_validator):
        """Test creación de experimento inválido."""
        mock_validator.validate_experiment_config.return_value = ValidationResult(
            is_valid=False,
            errors=['Error de validación'],
            warnings=[],
            suggestions=[]
        )
        
        invalid_config = {
            'name': '',  # Nombre vacío
            'description': 'Test',
            'architecture': {'layers': []},  # Sin capas
            'training_params': {'epochs': 0},  # Épocas inválidas
            'dataset_size': 0,  # Dataset vacío
            'tags': []
        }
        
        result = experiment_service.create_experiment(invalid_config)
        
        assert not result['validation']['is_valid']
        assert len(result['validation']['errors']) > 0
        assert 'experiment_id' not in result
    
    def test_get_experiment_existing(self, experiment_service, sample_experiment_config):
        """Test obtener experimento existente."""
        # Crear experimento
        create_result = experiment_service.create_experiment(sample_experiment_config)
        experiment_id = create_result['experiment_id']
        
        # Obtener experimento
        result = experiment_service.get_experiment(experiment_id)
        
        assert result is not None
        assert result['id'] == experiment_id
        assert result['name'] == sample_experiment_config['name']
        assert result['status'] == 'created'
    
    def test_get_experiment_nonexistent(self, experiment_service):
        """Test obtener experimento inexistente."""
        result = experiment_service.get_experiment('nonexistent_id')
        
        assert result is None
    
    def test_list_experiments_empty(self, experiment_service):
        """Test listar experimentos cuando no hay ninguno."""
        result = experiment_service.list_experiments()
        
        assert result['experiments'] == []
        assert result['total'] == 0
        assert result['page'] == 1
        assert result['per_page'] == 50
    
    def test_list_experiments_with_data(self, experiment_service, sample_experiment_config):
        """Test listar experimentos con datos."""
        # Crear varios experimentos
        configs = []
        for i in range(3):
            config = sample_experiment_config.copy()
            config['name'] = f'experiment_{i}'
            configs.append(config)
            experiment_service.create_experiment(config)
        
        result = experiment_service.list_experiments()
        
        assert len(result['experiments']) == 3
        assert result['total'] == 3
        assert all(exp['name'].startswith('experiment_') for exp in result['experiments'])
    
    def test_list_experiments_with_filters(self, experiment_service, sample_experiment_config):
        """Test listar experimentos con filtros."""
        # Crear experimentos con diferentes tags
        config1 = sample_experiment_config.copy()
        config1['name'] = 'exp1'
        config1['tags'] = ['regression', 'simple']
        
        config2 = sample_experiment_config.copy()
        config2['name'] = 'exp2'
        config2['tags'] = ['classification', 'complex']
        
        experiment_service.create_experiment(config1)
        experiment_service.create_experiment(config2)
        
        # Filtrar por tag
        result = experiment_service.list_experiments(filters={'tags': ['regression']})
        
        assert len(result['experiments']) == 1
        assert result['experiments'][0]['name'] == 'exp1'
    
    def test_list_experiments_pagination(self, experiment_service, sample_experiment_config):
        """Test paginación en listado de experimentos."""
        # Crear 5 experimentos
        for i in range(5):
            config = sample_experiment_config.copy()
            config['name'] = f'experiment_{i:02d}'
            experiment_service.create_experiment(config)
        
        # Primera página (2 elementos)
        result = experiment_service.list_experiments(page=1, per_page=2)
        
        assert len(result['experiments']) == 2
        assert result['total'] == 5
        assert result['page'] == 1
        assert result['per_page'] == 2
        
        # Segunda página
        result = experiment_service.list_experiments(page=2, per_page=2)
        
        assert len(result['experiments']) == 2
        assert result['page'] == 2
    
    def test_update_experiment_status(self, experiment_service, sample_experiment_config):
        """Test actualización de estado de experimento."""
        # Crear experimento
        create_result = experiment_service.create_experiment(sample_experiment_config)
        experiment_id = create_result['experiment_id']
        
        # Actualizar estado
        result = experiment_service.update_experiment_status(experiment_id, 'running')
        
        assert result['success']
        assert result['new_status'] == 'running'
        
        # Verificar actualización
        experiment = experiment_service.get_experiment(experiment_id)
        assert experiment['status'] == 'running'
    
    def test_update_experiment_status_invalid(self, experiment_service):
        """Test actualización de estado con experimento inexistente."""
        result = experiment_service.update_experiment_status('nonexistent', 'running')
        
        assert not result['success']
        assert 'error' in result
    
    def test_compare_experiments(self, experiment_service, sample_experiment_config):
        """Test comparación de experimentos."""
        # Crear dos experimentos diferentes
        config1 = sample_experiment_config.copy()
        config1['name'] = 'exp1'
        config1['architecture']['layers'] = [32, 16, 1]
        
        config2 = sample_experiment_config.copy()
        config2['name'] = 'exp2'
        config2['architecture']['layers'] = [64, 32, 1]
        config2['training_params']['learning_rate'] = 0.01
        
        exp1_result = experiment_service.create_experiment(config1)
        exp2_result = experiment_service.create_experiment(config2)
        
        # Comparar experimentos
        comparison = experiment_service.compare_experiments([
            exp1_result['experiment_id'],
            exp2_result['experiment_id']
        ])
        
        assert 'experiments' in comparison
        assert len(comparison['experiments']) == 2
        assert 'architecture_comparison' in comparison
        assert 'training_comparison' in comparison
        assert 'differences' in comparison
    
    def test_compare_experiments_insufficient(self, experiment_service):
        """Test comparación con experimentos insuficientes."""
        comparison = experiment_service.compare_experiments(['single_id'])
        
        assert 'error' in comparison
        assert 'al menos 2' in comparison['error'].lower()
    
    def test_get_experiment_insights(self, experiment_service, sample_experiment_config):
        """Test obtención de insights de experimento."""
        # Crear experimento
        create_result = experiment_service.create_experiment(sample_experiment_config)
        experiment_id = create_result['experiment_id']
        
        # Obtener insights
        insights = experiment_service.get_experiment_insights(experiment_id)
        
        assert 'complexity_analysis' in insights
        assert 'training_analysis' in insights
        assert 'recommendations' in insights
        assert 'potential_issues' in insights
    
    def test_get_experiment_insights_nonexistent(self, experiment_service):
        """Test insights para experimento inexistente."""
        insights = experiment_service.get_experiment_insights('nonexistent')
        
        assert 'error' in insights
    
    def test_delete_experiment(self, experiment_service, sample_experiment_config):
        """Test eliminación de experimento."""
        # Crear experimento
        create_result = experiment_service.create_experiment(sample_experiment_config)
        experiment_id = create_result['experiment_id']
        
        # Verificar que existe
        experiment = experiment_service.get_experiment(experiment_id)
        assert experiment is not None
        
        # Eliminar experimento
        result = experiment_service.delete_experiment(experiment_id)
        
        assert result['success']
        
        # Verificar que ya no existe
        experiment = experiment_service.get_experiment(experiment_id)
        assert experiment is None
    
    def test_delete_experiment_nonexistent(self, experiment_service):
        """Test eliminación de experimento inexistente."""
        result = experiment_service.delete_experiment('nonexistent')
        
        assert not result['success']
        assert 'error' in result
    
    def test_search_experiments(self, experiment_service, sample_experiment_config):
        """Test búsqueda de experimentos."""
        # Crear experimentos con diferentes nombres y descripciones
        configs = [
            {'name': 'regression_simple', 'description': 'Simple regression model'},
            {'name': 'regression_complex', 'description': 'Complex deep regression'},
            {'name': 'classification_test', 'description': 'Classification experiment'}
        ]
        
        for config_data in configs:
            config = sample_experiment_config.copy()
            config.update(config_data)
            experiment_service.create_experiment(config)
        
        # Buscar por término
        results = experiment_service.search_experiments('regression')
        
        assert len(results['experiments']) == 2
        assert all('regression' in exp['name'].lower() or 'regression' in exp['description'].lower() 
                  for exp in results['experiments'])
    
    def test_get_experiment_statistics(self, experiment_service, sample_experiment_config):
        """Test estadísticas de experimentos."""
        # Crear experimentos con diferentes estados
        for i in range(3):
            config = sample_experiment_config.copy()
            config['name'] = f'exp_{i}'
            result = experiment_service.create_experiment(config)
            
            # Cambiar algunos estados
            if i == 1:
                experiment_service.update_experiment_status(result['experiment_id'], 'running')
            elif i == 2:
                experiment_service.update_experiment_status(result['experiment_id'], 'completed')
        
        stats = experiment_service.get_experiment_statistics()
        
        assert 'total_experiments' in stats
        assert 'status_distribution' in stats
        assert 'recent_activity' in stats
        assert stats['total_experiments'] == 3
    
    def test_export_experiment_config(self, experiment_service, sample_experiment_config):
        """Test exportación de configuración de experimento."""
        # Crear experimento
        create_result = experiment_service.create_experiment(sample_experiment_config)
        experiment_id = create_result['experiment_id']
        
        # Exportar configuración
        exported = experiment_service.export_experiment_config(experiment_id)
        
        assert 'config' in exported
        assert 'metadata' in exported
        assert exported['config']['name'] == sample_experiment_config['name']
        assert exported['config']['architecture'] == sample_experiment_config['architecture']
    
    def test_import_experiment_config(self, experiment_service, sample_experiment_config):
        """Test importación de configuración de experimento."""
        # Preparar configuración para importar
        import_data = {
            'config': sample_experiment_config,
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
        
        # Importar configuración
        result = experiment_service.import_experiment_config(import_data)
        
        assert result['success']
        assert 'experiment_id' in result
        
        # Verificar que se creó correctamente
        experiment = experiment_service.get_experiment(result['experiment_id'])
        assert experiment['name'] == sample_experiment_config['name']
    
    def test_validate_experiment_config_integration(self, experiment_service, mock_validator):
        """Test integración con validador."""
        # Configurar validador para retornar warnings
        mock_validator.validate_experiment_config.return_value = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=['Warning de prueba'],
            suggestions=['Sugerencia de prueba']
        )
        
        config = {
            'name': 'test_with_warnings',
            'description': 'Test',
            'architecture': {'layers': [64, 1], 'activation': 'relu', 'dropout_rate': 0.0, 'batch_normalization': False},
            'training_params': {'epochs': 100, 'learning_rate': 0.001, 'batch_size': 32, 'early_stopping': True, 'patience': 10, 'validation_split': 0.2},
            'dataset_size': 1000,
            'tags': ['test']
        }
        
        result = experiment_service.create_experiment(config)
        
        assert result['validation']['is_valid']
        assert len(result['validation']['warnings']) > 0
        assert len(result['validation']['suggestions']) > 0
    
    def test_concurrent_experiment_creation(self, experiment_service, sample_experiment_config):
        """Test creación concurrente de experimentos."""
        import threading
        import time
        
        results = []
        
        def create_experiment(i):
            config = sample_experiment_config.copy()
            config['name'] = f'concurrent_exp_{i}'
            result = experiment_service.create_experiment(config)
            results.append(result)
        
        # Crear múltiples threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_experiment, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Esperar a que terminen
        for thread in threads:
            thread.join()
        
        # Verificar resultados
        assert len(results) == 5
        assert all('experiment_id' in result for result in results)
        
        # Verificar que todos los experimentos se crearon
        all_experiments = experiment_service.list_experiments()
        assert all_experiments['total'] == 5