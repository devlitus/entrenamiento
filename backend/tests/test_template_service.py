# backend/tests/test_template_service.py
"""
Tests exhaustivos para TemplateService.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os
import copy

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.templates.template_service import TemplateService
from services.validation.model_validation_service import ModelValidationService
from schemas.model_schemas import ValidationResult

class TestTemplateService:
    """Tests para TemplateService."""
    
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
    def template_service(self, mock_validator):
        """Fixture para servicio de plantillas."""
        return TemplateService(mock_validator)
    
    def test_get_available_templates(self, template_service):
        """Test obtener plantillas disponibles."""
        templates = template_service.get_available_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
        
        # Verificar estructura de cada plantilla
        for name, template in templates.items():
            assert 'name' in template
            assert 'description' in template
            assert 'complexity' in template
            assert 'estimated_training_time' in template
            assert 'use_cases' in template
            assert 'architecture_summary' in template
            assert 'training_summary' in template
    
    def test_get_template_existing(self, template_service):
        """Test obtener plantilla existente."""
        # Obtener lista de plantillas disponibles
        available = template_service.get_available_templates()
        template_name = list(available.keys())[0]
        
        template = template_service.get_template(template_name)
        
        assert template is not None
        assert template['name'] == template_name
        assert 'architecture' in template
        assert 'training_params' in template
        assert 'use_cases' in template
        assert 'complexity' in template
    
    def test_get_template_nonexistent(self, template_service):
        """Test obtener plantilla inexistente."""
        template = template_service.get_template('nonexistent_template')
        
        assert template is None
    
    def test_customize_template_valid(self, template_service):
        """Test personalización válida de plantilla."""
        # Obtener plantilla base
        available = template_service.get_available_templates()
        template_name = list(available.keys())[0]
        
        customizations = {
            'architecture': {
                'dropout_rate': 0.3,
                'batch_normalization': True
            },
            'training_params': {
                'learning_rate': 0.01,
                'epochs': 200
            },
            'description': 'Plantilla personalizada para pruebas'
        }
        
        result = template_service.customize_template(template_name, customizations)
        
        assert 'customized_config' in result
        assert 'validation' in result
        assert 'changes_applied' in result
        assert result['validation'].is_valid
        
        # Verificar que las personalizaciones se aplicaron
        config = result['customized_config']
        assert config['architecture']['dropout_rate'] == 0.3
        assert config['architecture']['batch_normalization'] == True
        assert config['training_params']['learning_rate'] == 0.01
        assert config['training_params']['epochs'] == 200
        assert config['description'] == 'Plantilla personalizada para pruebas'
    
    def test_customize_template_nonexistent(self, template_service):
        """Test personalización de plantilla inexistente."""
        customizations = {'architecture': {'dropout_rate': 0.3}}
        
        result = template_service.customize_template('nonexistent', customizations)
        
        assert 'error' in result
        assert result['customized_config'] is None
        assert not result['validation'].is_valid
    
    def test_customize_template_invalid_config(self, template_service, mock_validator):
        """Test personalización que resulta en configuración inválida."""
        # Configurar validador para retornar error
        mock_validator.validate_experiment_config.return_value = ValidationResult(
            is_valid=False,
            errors=['Configuración inválida'],
            warnings=[],
            suggestions=[]
        )
        
        available = template_service.get_available_templates()
        template_name = list(available.keys())[0]
        
        customizations = {
            'architecture': {'dropout_rate': 1.5}  # Inválido
        }
        
        result = template_service.customize_template(template_name, customizations)
        
        assert not result['validation'].is_valid
        assert len(result['validation'].errors) > 0
    
    def test_get_template_recommendations_basic(self, template_service):
        """Test recomendaciones básicas de plantillas."""
        requirements = {
            'complexity': 'simple',
            'max_training_time': 'fast',
            'use_cases': ['regression']
        }
        
        result = template_service.get_template_recommendations(requirements)
        
        assert 'recommendations' in result
        assert 'total_available' in result
        assert 'requirements_analyzed' in result
        assert isinstance(result['recommendations'], list)
        
        # Verificar estructura de recomendaciones
        if result['recommendations']:
            rec = result['recommendations'][0]
            assert 'name' in rec
            assert 'template' in rec
            assert 'match_score' in rec
            assert 'justification' in rec
            assert 0 <= rec['match_score'] <= 1
    
    def test_get_template_recommendations_complex(self, template_service):
        """Test recomendaciones para requerimientos complejos."""
        requirements = {
            'complexity': 'complex',
            'max_training_time': 'long',
            'use_cases': ['deep_learning', 'production'],
            'objective': 'production'
        }
        
        result = template_service.get_template_recommendations(requirements)
        
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0
        
        # Las recomendaciones deben estar ordenadas por puntuación
        scores = [rec['match_score'] for rec in result['recommendations']]
        assert scores == sorted(scores, reverse=True)
    
    def test_filter_templates_by_complexity(self, template_service):
        """Test filtrado por complejidad."""
        filters = {'complexity': 'simple'}
        
        filtered = template_service.filter_templates(filters)
        
        assert isinstance(filtered, dict)
        
        # Todas las plantillas filtradas deben tener la complejidad especificada
        for template in filtered.values():
            assert template['complexity'] == 'simple'
    
    def test_filter_templates_by_training_time(self, template_service):
        """Test filtrado por tiempo de entrenamiento."""
        filters = {'max_training_time': 'fast'}
        
        filtered = template_service.filter_templates(filters)
        
        assert isinstance(filtered, dict)
        
        # Verificar que las plantillas filtradas tienen tiempo de entrenamiento rápido
        for template in filtered.values():
            assert '< 1 minuto' in template['estimated_training_time']
    
    def test_filter_templates_multiple_criteria(self, template_service):
        """Test filtrado con múltiples criterios."""
        filters = {
            'complexity': 'simple',
            'max_training_time': 'fast'
        }
        
        filtered = template_service.filter_templates(filters)
        
        # Todas las plantillas deben cumplir ambos criterios
        for template in filtered.values():
            assert template['complexity'] == 'simple'
            assert '< 1 minuto' in template['estimated_training_time']
    
    def test_compare_templates_valid(self, template_service):
        """Test comparación válida de plantillas."""
        available = template_service.get_available_templates()
        template_names = list(available.keys())[:2]  # Tomar las primeras 2
        
        if len(template_names) < 2:
            pytest.skip("Se necesitan al menos 2 plantillas para la comparación")
        
        comparison = template_service.compare_templates(template_names)
        
        assert 'templates' in comparison
        assert 'complexity_comparison' in comparison
        assert 'architecture_comparison' in comparison
        assert 'training_comparison' in comparison
        assert 'use_case_overlap' in comparison
        
        assert len(comparison['templates']) == 2
    
    def test_compare_templates_insufficient(self, template_service):
        """Test comparación con plantillas insuficientes."""
        comparison = template_service.compare_templates(['single_template'])
        
        assert 'error' in comparison
        assert 'al menos 2' in comparison['error'].lower()
    
    def test_compare_templates_nonexistent(self, template_service):
        """Test comparación con plantillas inexistentes."""
        comparison = template_service.compare_templates(['nonexistent1', 'nonexistent2'])
        
        assert 'error' in comparison
        assert 'suficientes plantillas válidas' in comparison['error'].lower()
    
    def test_complexity_comparison(self, template_service):
        """Test comparación de complejidad específica."""
        available = template_service.get_available_templates()
        
        # Buscar plantillas con diferentes complejidades
        simple_templates = [name for name, template in available.items() 
                          if template['complexity'] == 'simple']
        complex_templates = [name for name, template in available.items() 
                           if template['complexity'] == 'complex']
        
        if simple_templates and complex_templates:
            template_names = [simple_templates[0], complex_templates[0]]
            comparison = template_service.compare_templates(template_names)
            
            complexity_comp = comparison['complexity_comparison']
            assert 'ranking' in complexity_comp
            assert 'simplest' in complexity_comp
            assert 'most_complex' in complexity_comp
            
            # La plantilla simple debe ser la más simple
            assert complexity_comp['simplest'] == simple_templates[0]
            assert complexity_comp['most_complex'] == complex_templates[0]
    
    def test_architecture_comparison(self, template_service):
        """Test comparación de arquitecturas."""
        available = template_service.get_available_templates()
        template_names = list(available.keys())[:2]
        
        if len(template_names) < 2:
            pytest.skip("Se necesitan al menos 2 plantillas")
        
        comparison = template_service.compare_templates(template_names)
        arch_comp = comparison['architecture_comparison']
        
        for template_name in template_names:
            assert template_name in arch_comp
            template_arch = arch_comp[template_name]
            assert 'total_layers' in template_arch
            assert 'total_neurons' in template_arch
            assert 'activation' in template_arch
            assert 'dropout_rate' in template_arch
    
    def test_use_case_overlap_analysis(self, template_service):
        """Test análisis de solapamiento de casos de uso."""
        available = template_service.get_available_templates()
        template_names = list(available.keys())[:2]
        
        if len(template_names) < 2:
            pytest.skip("Se necesitan al menos 2 plantillas")
        
        comparison = template_service.compare_templates(template_names)
        overlap = comparison['use_case_overlap']
        
        assert 'total_unique_use_cases' in overlap
        assert 'overlap_matrix' in overlap
        assert 'common_use_cases' in overlap
        
        # Verificar matriz de solapamiento
        matrix = overlap['overlap_matrix']
        for name1 in template_names:
            assert name1 in matrix
            for name2 in template_names:
                if name1 != name2:
                    assert name2 in matrix[name1]
                    assert 0 <= matrix[name1][name2] <= 1
    
    def test_match_score_calculation(self, template_service):
        """Test cálculo de puntuación de coincidencia."""
        available = template_service.get_available_templates()
        template_name = list(available.keys())[0]
        template = available[template_name]
        
        # Requerimientos que coinciden exactamente
        requirements = {
            'complexity': template['complexity'],
            'max_training_time': 'fast' if '< 1 minuto' in template['estimated_training_time'] else 'medium',
            'use_cases': template['use_cases'][:1]  # Primer caso de uso
        }
        
        result = template_service.get_template_recommendations(requirements)
        
        # Buscar la plantilla en las recomendaciones
        matching_rec = None
        for rec in result['recommendations']:
            if rec['name'] == template_name:
                matching_rec = rec
                break
        
        if matching_rec:
            # La puntuación debe ser alta para coincidencias exactas
            assert matching_rec['match_score'] > 0.5
    
    def test_recommendation_justification(self, template_service):
        """Test justificación de recomendaciones."""
        requirements = {
            'complexity': 'simple',
            'max_training_time': 'fast'
        }
        
        result = template_service.get_template_recommendations(requirements)
        
        if result['recommendations']:
            rec = result['recommendations'][0]
            justification = rec['justification']
            
            assert isinstance(justification, str)
            assert len(justification) > 0
            
            # Debe mencionar los criterios de coincidencia
            if requirements['complexity'] == 'simple':
                assert 'simple' in justification.lower() or 'complejidad' in justification.lower()
    
    def test_changes_summary(self, template_service):
        """Test resumen de cambios aplicados."""
        available = template_service.get_available_templates()
        template_name = list(available.keys())[0]
        
        customizations = {
            'architecture': {
                'dropout_rate': 0.5
            },
            'training_params': {
                'learning_rate': 0.005,
                'epochs': 150
            }
        }
        
        result = template_service.customize_template(template_name, customizations)
        changes = result['changes_applied']
        
        assert isinstance(changes, list)
        assert len(changes) > 0
        
        # Verificar formato de cambios
        for change in changes:
            assert '→' in change  # Formato "antes → después"
    
    def test_error_handling(self, template_service):
        """Test manejo de errores."""
        # Test con plantilla None
        result = template_service.get_template(None)
        assert result is None
        
        # Test con customizations None
        result = template_service.customize_template('simple_regression', None)
        assert 'customized_config' in result  # Debe manejar gracefully
        
        # Test con requirements vacíos
        result = template_service.get_template_recommendations({})
        assert 'recommendations' in result
    
    def test_template_service_integration(self, template_service):
        """Test integración completa del servicio."""
        # Flujo completo: obtener plantillas → filtrar → personalizar → comparar
        
        # 1. Obtener plantillas disponibles
        available = template_service.get_available_templates()
        assert len(available) > 0
        
        # 2. Filtrar por complejidad
        filtered = template_service.filter_templates({'complexity': 'simple'})
        
        # 3. Personalizar una plantilla
        if filtered:
            template_name = list(filtered.keys())[0]
            customizations = {'architecture': {'dropout_rate': 0.25}}
            
            custom_result = template_service.customize_template(template_name, customizations)
            assert custom_result['validation'].is_valid
        
        # 4. Obtener recomendaciones
        requirements = {'complexity': 'simple', 'use_cases': ['regression']}
        recommendations = template_service.get_template_recommendations(requirements)
        assert 'recommendations' in recommendations
    
    @pytest.mark.parametrize("complexity", ['simple', 'medium', 'complex'])
    def test_all_complexity_levels(self, template_service, complexity):
        """Test todas las complejidades disponibles."""
        filters = {'complexity': complexity}
        filtered = template_service.filter_templates(filters)
        
        # Debe haber al menos una plantilla de cada complejidad
        # (esto depende de las plantillas definidas en ModelTemplates)
        for template in filtered.values():
            assert template['complexity'] == complexity
    
    def test_template_metadata_consistency(self, template_service):
        """Test consistencia de metadatos de plantillas."""
        available = template_service.get_available_templates()
        
        for name, template in available.items():
            # Verificar campos requeridos
            required_fields = ['name', 'description', 'complexity', 
                             'estimated_training_time', 'use_cases']
            for field in required_fields:
                assert field in template, f"Campo {field} faltante en plantilla {name}"
            
            # Verificar tipos
            assert isinstance(template['use_cases'], list)
            assert template['complexity'] in ['simple', 'medium', 'complex']
            assert isinstance(template['estimated_training_time'], str)