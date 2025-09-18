# backend/tests/test_validation_service.py
"""
Tests exhaustivos para ModelValidationService.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.validation.model_validation_service import ModelValidationService
from schemas.model_schemas import ValidationResult

class TestModelValidationService:
    """Tests para ModelValidationService."""
    
    @pytest.fixture
    def validator(self):
        """Fixture para instancia del validador."""
        return ModelValidationService()
    
    def test_validate_architecture_valid_simple(self, validator):
        """Test validación de arquitectura simple válida."""
        architecture = {
            'layers': [64, 32, 1],
            'activation': 'relu',
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert result.is_valid
        assert len(result.errors) == 0
        assert 'arquitectura simple' in ' '.join(result.suggestions).lower()
    
    def test_validate_architecture_valid_complex(self, validator):
        """Test validación de arquitectura compleja válida."""
        architecture = {
            'layers': [128, 64, 32, 16, 1],
            'activation': 'relu',
            'dropout_rate': 0.3,
            'batch_normalization': True
        }
        
        result = validator.validate_architecture(architecture)
        
        assert result.is_valid
        assert len(result.errors) == 0
        assert any('compleja' in s.lower() for s in result.suggestions)
    
    def test_validate_architecture_invalid_empty_layers(self, validator):
        """Test validación con capas vacías."""
        architecture = {
            'layers': [],
            'activation': 'relu',
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert not result.is_valid
        assert any('al menos una capa' in error.lower() for error in result.errors)
    
    def test_validate_architecture_invalid_negative_neurons(self, validator):
        """Test validación con neuronas negativas."""
        architecture = {
            'layers': [64, -32, 1],
            'activation': 'relu',
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert not result.is_valid
        assert any('positivo' in error.lower() for error in result.errors)
    
    def test_validate_architecture_invalid_activation(self, validator):
        """Test validación con función de activación inválida."""
        architecture = {
            'layers': [64, 32, 1],
            'activation': 'invalid_activation',
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert not result.is_valid
        assert any('activación' in error.lower() for error in result.errors)
    
    def test_validate_architecture_invalid_dropout_rate(self, validator):
        """Test validación con tasa de dropout inválida."""
        architecture = {
            'layers': [64, 32, 1],
            'activation': 'relu',
            'dropout_rate': 1.5,  # > 1.0
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert not result.is_valid
        assert any('dropout' in error.lower() for error in result.errors)
    
    def test_validate_training_params_valid(self, validator):
        """Test validación de parámetros de entrenamiento válidos."""
        params = {
            'epochs': 100,
            'learning_rate': 0.001,
            'batch_size': 32,
            'early_stopping': True,
            'patience': 10,
            'validation_split': 0.2
        }
        
        result = validator.validate_training_params(params)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_validate_training_params_invalid_epochs(self, validator):
        """Test validación con épocas inválidas."""
        params = {
            'epochs': 0,
            'learning_rate': 0.001,
            'batch_size': 32,
            'early_stopping': True,
            'patience': 10,
            'validation_split': 0.2
        }
        
        result = validator.validate_training_params(params)
        
        assert not result.is_valid
        assert any('épocas' in error.lower() for error in result.errors)
    
    def test_validate_training_params_invalid_learning_rate(self, validator):
        """Test validación con learning rate inválido."""
        params = {
            'epochs': 100,
            'learning_rate': 0.0,  # <= 0
            'batch_size': 32,
            'early_stopping': True,
            'patience': 10,
            'validation_split': 0.2
        }
        
        result = validator.validate_training_params(params)
        
        assert not result.is_valid
        assert any('learning rate' in error.lower() for error in result.errors)
    
    def test_validate_training_params_invalid_batch_size(self, validator):
        """Test validación con batch size inválido."""
        params = {
            'epochs': 100,
            'learning_rate': 0.001,
            'batch_size': 0,  # <= 0
            'early_stopping': True,
            'patience': 10,
            'validation_split': 0.2
        }
        
        result = validator.validate_training_params(params)
        
        assert not result.is_valid
        assert any('batch size' in error.lower() for error in result.errors)
    
    def test_validate_training_params_invalid_validation_split(self, validator):
        """Test validación con validation split inválido."""
        params = {
            'epochs': 100,
            'learning_rate': 0.001,
            'batch_size': 32,
            'early_stopping': True,
            'patience': 10,
            'validation_split': 1.5  # > 1.0
        }
        
        result = validator.validate_training_params(params)
        
        assert not result.is_valid
        assert any('validation split' in error.lower() for error in result.errors)
    
    def test_validate_experiment_config_valid(self, validator):
        """Test validación de configuración de experimento válida."""
        config = {
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
        
        result = validator.validate_experiment_config(config)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_validate_experiment_config_invalid_name(self, validator):
        """Test validación con nombre de experimento inválido."""
        config = {
            'name': '',  # Vacío
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
            'tags': ['test']
        }
        
        result = validator.validate_experiment_config(config)
        
        assert not result.is_valid
        assert any('nombre' in error.lower() for error in result.errors)
    
    def test_validate_experiment_config_invalid_dataset_size(self, validator):
        """Test validación con tamaño de dataset inválido."""
        config = {
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
            'dataset_size': 0,  # <= 0
            'tags': ['test']
        }
        
        result = validator.validate_experiment_config(config)
        
        assert not result.is_valid
        assert any('dataset' in error.lower() for error in result.errors)
    
    def test_validate_with_warnings(self, validator):
        """Test validación que genera warnings."""
        architecture = {
            'layers': [1000, 800, 600, 400, 200, 100, 50, 1],  # Muy compleja
            'activation': 'relu',
            'dropout_rate': 0.1,  # Bajo para arquitectura compleja
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert result.is_valid
        assert len(result.warnings) > 0
        assert any('compleja' in warning.lower() for warning in result.warnings)
    
    def test_validate_with_suggestions(self, validator):
        """Test validación que genera sugerencias."""
        params = {
            'epochs': 1000,  # Muchas épocas
            'learning_rate': 0.1,  # Learning rate alto
            'batch_size': 1,  # Batch size muy pequeño
            'early_stopping': False,
            'patience': 5,
            'validation_split': 0.1  # Split pequeño
        }
        
        result = validator.validate_training_params(params)
        
        assert result.is_valid
        assert len(result.suggestions) > 0
    
    def test_edge_case_single_neuron_layer(self, validator):
        """Test caso edge con capa de una sola neurona."""
        architecture = {
            'layers': [1],
            'activation': 'linear',
            'dropout_rate': 0.0,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert result.is_valid
        assert len(result.warnings) > 0
    
    def test_edge_case_very_high_dropout(self, validator):
        """Test caso edge con dropout muy alto."""
        architecture = {
            'layers': [64, 32, 1],
            'activation': 'relu',
            'dropout_rate': 0.9,  # Muy alto pero válido
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        
        assert result.is_valid
        assert len(result.warnings) > 0
        assert any('dropout' in warning.lower() for warning in result.warnings)
    
    def test_regression_compatibility(self, validator):
        """Test compatibilidad con configuraciones de regresión típicas."""
        # Configuración típica para regresión Celsius-Fahrenheit
        architecture = {
            'layers': [1],
            'activation': 'linear',
            'dropout_rate': 0.0,
            'batch_normalization': False
        }
        
        params = {
            'epochs': 500,
            'learning_rate': 0.1,
            'batch_size': 32,
            'early_stopping': True,
            'patience': 50,
            'validation_split': 0.2
        }
        
        arch_result = validator.validate_architecture(architecture)
        params_result = validator.validate_training_params(params)
        
        assert arch_result.is_valid
        assert params_result.is_valid
        
        # Debe sugerir configuraciones apropiadas para regresión
        all_suggestions = arch_result.suggestions + params_result.suggestions
        assert any('regresión' in s.lower() for s in all_suggestions)
    
    @pytest.mark.parametrize("activation", ['relu', 'tanh', 'sigmoid', 'linear', 'swish'])
    def test_all_supported_activations(self, validator, activation):
        """Test todas las funciones de activación soportadas."""
        architecture = {
            'layers': [64, 32, 1],
            'activation': activation,
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        assert result.is_valid
    
    @pytest.mark.parametrize("layers", [
        [1],
        [64, 1],
        [128, 64, 32, 1],
        [256, 128, 64, 32, 16, 8, 1]
    ])
    def test_various_layer_configurations(self, validator, layers):
        """Test varias configuraciones de capas."""
        architecture = {
            'layers': layers,
            'activation': 'relu',
            'dropout_rate': 0.2,
            'batch_normalization': False
        }
        
        result = validator.validate_architecture(architecture)
        assert result.is_valid