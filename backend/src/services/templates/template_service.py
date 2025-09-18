# backend/src/services/templates/template_service.py
"""
Servicio principal para gestión de plantillas de modelos ML.
"""

from typing import Dict, Any, List, Optional
import logging
import copy

from .model_templates import ModelTemplates, ModelTemplate
from ..validation.model_validation_service import ModelValidationService
from src.schemas.model_schemas import ValidationResult

logger = logging.getLogger(__name__)

class TemplateService:
    """Servicio para gestión de plantillas de modelos con personalización."""
    
    def __init__(self, validator: ModelValidationService = None):
        """
        Inicializa el servicio de plantillas.
        
        Args:
            validator: Instancia de validador (opcional)
        """
        self.validator = validator or ModelValidationService()
        self.logger = logger
    
    def list_templates(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Lista todas las plantillas disponibles con filtros opcionales.
        
        Args:
            filters: Filtros opcionales para las plantillas
            
        Returns:
            Lista de plantillas que coinciden con los filtros
        """
        try:
            all_templates = self.get_available_templates()
            
            if not filters:
                return list(all_templates.values())
            
            filtered_templates = []
            for template_data in all_templates.values():
                if self._matches_filters(template_data, filters):
                    filtered_templates.append(template_data)
            
            return filtered_templates
            
        except Exception as e:
            self.logger.error(f"Error listando plantillas: {e}")
            return []

    def recommend_templates(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Recomienda plantillas basadas en requerimientos del usuario.
        
        Args:
            requirements: Requerimientos del usuario
            
        Returns:
            Lista de plantillas recomendadas con puntuaciones
        """
        try:
            recommendations_data = self.get_template_recommendations(requirements)
            return recommendations_data.get('recommendations', [])
            
        except Exception as e:
            self.logger.error(f"Error recomendando plantillas: {e}")
            return []

    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtiene todas las plantillas disponibles con información resumida.
        
        Returns:
            Diccionario con plantillas y sus metadatos
        """
        try:
            all_templates = ModelTemplates.get_all_templates()
            
            result = {}
            for name, template in all_templates.items():
                result[name] = {
                    'name': template.name,
                    'description': template.description,
                    'complexity': template.complexity,
                    'estimated_training_time': template.estimated_training_time,
                    'use_cases': template.use_cases,
                    'architecture_summary': self._get_architecture_summary(template.architecture),
                    'training_summary': self._get_training_summary(template.training_params)
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error obteniendo plantillas: {e}")
            return {}
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una plantilla específica con configuración completa.
        
        Args:
            template_name: Nombre de la plantilla
            
        Returns:
            Diccionario con configuración completa de la plantilla
        """
        try:
            all_templates = ModelTemplates.get_all_templates()
            
            if template_name not in all_templates:
                self.logger.warning(f"Plantilla no encontrada: {template_name}")
                return None
            
            template = all_templates[template_name]
            
            return {
                'name': template.name,
                'description': template.description,
                'architecture': template.architecture,
                'training_params': template.training_params,
                'use_cases': template.use_cases,
                'complexity': template.complexity,
                'estimated_training_time': template.estimated_training_time
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo plantilla {template_name}: {e}")
            return None
    
    def customize_template(self, template_name: str, 
                          customizations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Personaliza una plantilla con modificaciones específicas.
        
        Args:
            template_name: Nombre de la plantilla base
            customizations: Modificaciones a aplicar
            
        Returns:
            Diccionario con plantilla personalizada y resultado de validación
        """
        try:
            base_template = self.get_template(template_name)
            if not base_template:
                return {
                    'error': f'Plantilla {template_name} no encontrada',
                    'customized_config': None,
                    'validation': ValidationResult(is_valid=False, errors=['Plantilla no encontrada'], warnings=[], suggestions=[])
                }
            
            # Crear copia profunda para personalización
            customized_config = copy.deepcopy(base_template)
            
            # Aplicar personalizaciones
            self._apply_customizations(customized_config, customizations)
            
            # Validar configuración personalizada
            experiment_config = {
                'name': f"custom_{template_name}",
                'description': f"Plantilla {template_name} personalizada",
                'architecture': customized_config['architecture'],
                'training_params': customized_config['training_params'],
                'dataset_size': customizations.get('dataset_size', 1000),
                'tags': ['custom', 'template', template_name]
            }
            
            validation = self.validator.validate_experiment_config(experiment_config)
            
            return {
                'customized_config': customized_config,
                'validation': validation,
                'changes_applied': self._get_changes_summary(base_template, customized_config)
            }
            
        except Exception as e:
            self.logger.error(f"Error personalizando plantilla {template_name}: {e}")
            return {
                'error': str(e),
                'customized_config': None,
                'validation': ValidationResult(is_valid=False, errors=[str(e)], warnings=[], suggestions=[])
            }
    
    def get_template_recommendations(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtiene recomendaciones de plantillas basadas en requerimientos.
        
        Args:
            requirements: Requerimientos del usuario
            
        Returns:
            Diccionario con recomendaciones y justificaciones
        """
        try:
            recommended_names = ModelTemplates.get_template_recommendations(requirements)
            
            recommendations = []
            for name in recommended_names:
                template_info = self.get_template(name)
                if template_info:
                    recommendations.append({
                        'name': name,
                        'template': template_info,
                        'match_score': self._calculate_match_score(template_info, requirements),
                        'justification': self._get_recommendation_justification(template_info, requirements)
                    })
            
            # Ordenar por match_score de mayor a menor
            recommendations.sort(key=lambda x: x['match_score'], reverse=True)
            
            return {
                'recommendations': recommendations,
                'total_available': len(ModelTemplates.get_all_templates()),
                'requirements_analyzed': requirements
            }
            
        except Exception as e:
            self.logger.error(f"Error generando recomendaciones: {e}")
            return {'error': str(e), 'recommendations': []}
    
    def filter_templates(self, filters: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Filtra plantillas según criterios específicos.
        
        Args:
            filters: Criterios de filtrado
            
        Returns:
            Diccionario con plantillas filtradas
        """
        try:
            all_templates = self.get_available_templates()
            filtered = {}
            
            for name, template in all_templates.items():
                if self._matches_filters(template, filters):
                    filtered[name] = template
            
            return filtered
            
        except Exception as e:
            self.logger.error(f"Error filtrando plantillas: {e}")
            return {}
    
    def compare_templates(self, template_names: List[str]) -> Dict[str, Any]:
        """
        Compara múltiples plantillas lado a lado.
        
        Args:
            template_names: Lista de nombres de plantillas a comparar
            
        Returns:
            Diccionario con comparación detallada
        """
        try:
            if len(template_names) < 2:
                return {'error': 'Se necesitan al menos 2 plantillas para comparar'}
            
            templates = {}
            for name in template_names:
                template = self.get_template(name)
                if template:
                    templates[name] = template
            
            if len(templates) < 2:
                return {'error': 'No se encontraron suficientes plantillas válidas'}
            
            comparison = {
                'templates': templates,
                'complexity_comparison': self._compare_complexity(templates),
                'architecture_comparison': self._compare_architectures(templates),
                'training_comparison': self._compare_training_params(templates),
                'use_case_overlap': self._analyze_use_case_overlap(templates)
            }
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error comparando plantillas: {e}")
            return {'error': str(e)}
    
    def _apply_customizations(self, config: Dict[str, Any], customizations: Dict[str, Any]):
        """Aplica personalizaciones a la configuración."""
        # Personalizar arquitectura
        if 'architecture' in customizations:
            arch_custom = customizations['architecture']
            for key, value in arch_custom.items():
                if key in config['architecture']:
                    config['architecture'][key] = value
        
        # Personalizar parámetros de entrenamiento
        if 'training_params' in customizations:
            training_custom = customizations['training_params']
            for key, value in training_custom.items():
                if key in config['training_params']:
                    config['training_params'][key] = value
        
        # Personalizar metadatos
        if 'description' in customizations:
            config['description'] = customizations['description']
    
    def _get_changes_summary(self, original: Dict[str, Any], 
                           customized: Dict[str, Any]) -> List[str]:
        """Genera resumen de cambios aplicados."""
        changes = []
        
        # Comparar arquitectura
        orig_arch = original['architecture']
        cust_arch = customized['architecture']
        
        for key in orig_arch:
            if key in cust_arch and orig_arch[key] != cust_arch[key]:
                changes.append(f"Arquitectura.{key}: {orig_arch[key]} → {cust_arch[key]}")
        
        # Comparar parámetros de entrenamiento
        orig_training = original['training_params']
        cust_training = customized['training_params']
        
        for key in orig_training:
            if key in cust_training and orig_training[key] != cust_training[key]:
                changes.append(f"Entrenamiento.{key}: {orig_training[key]} → {cust_training[key]}")
        
        return changes
    
    def _calculate_match_score(self, template: Dict[str, Any], 
                              requirements: Dict[str, Any]) -> float:
        """Calcula puntuación de coincidencia entre plantilla y requerimientos."""
        score = 0.0
        
        # Puntuación por complejidad
        req_complexity = requirements.get('complexity', 'medium')
        if template['complexity'] == req_complexity:
            score += 0.3
        
        # Puntuación por tiempo de entrenamiento
        req_time = requirements.get('max_training_time', 'medium')
        template_time = template['estimated_training_time']
        
        if req_time == 'fast' and '< 1 minuto' in template_time:
            score += 0.3
        elif req_time == 'medium' and any(x in template_time for x in ['1-2', '3-5']):
            score += 0.3
        elif req_time == 'long' and any(x in template_time for x in ['8-12', '4-6']):
            score += 0.3
        
        # Puntuación por casos de uso
        req_use_cases = requirements.get('use_cases', [])
        if req_use_cases:
            template_use_cases = [uc.lower() for uc in template['use_cases']]
            matches = sum(1 for req_uc in req_use_cases 
                         if any(req_uc.lower() in tuc for tuc in template_use_cases))
            score += (matches / len(req_use_cases)) * 0.4
        
        return min(score, 1.0)
    
    def _get_recommendation_justification(self, template: Dict[str, Any], 
                                        requirements: Dict[str, Any]) -> str:
        """Genera justificación para la recomendación."""
        reasons = []
        
        if requirements.get('complexity') == template['complexity']:
            reasons.append(f"Coincide con complejidad requerida ({template['complexity']})")
        
        if requirements.get('objective') == 'production' and 'production' in template['name']:
            reasons.append("Optimizada para entornos de producción")
        
        if requirements.get('max_training_time') == 'fast' and '< 1 minuto' in template['estimated_training_time']:
            reasons.append("Entrenamiento rápido")
        
        if not reasons:
            reasons.append("Configuración balanceada y versátil")
        
        return "; ".join(reasons)
    
    def _matches_filters(self, template: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Verifica si una plantilla coincide con los filtros."""
        if 'complexity' in filters and template['complexity'] != filters['complexity']:
            return False
        
        if 'max_training_time' in filters:
            time_filter = filters['max_training_time']
            template_time = template['estimated_training_time']
            
            if time_filter == 'fast' and '< 1 minuto' not in template_time:
                return False
            elif time_filter == 'medium' and not any(x in template_time for x in ['1-2', '3-5']):
                return False
        
        return True
    
    def _get_architecture_summary(self, architecture: Dict[str, Any]) -> str:
        """Genera resumen de arquitectura."""
        layers = architecture.get('layers', [])
        activation = architecture.get('activation', 'unknown')
        dropout = architecture.get('dropout_rate', 0)
        
        return f"{len(layers)} capas, activación {activation}, dropout {dropout}"
    
    def _get_training_summary(self, training_params: Dict[str, Any]) -> str:
        """Genera resumen de parámetros de entrenamiento."""
        epochs = training_params.get('epochs', 0)
        lr = training_params.get('learning_rate', 0)
        batch_size = training_params.get('batch_size', 0)
        
        return f"{epochs} épocas, LR {lr}, batch {batch_size}"
    
    def _compare_complexity(self, templates: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compara complejidad entre plantillas."""
        complexity_order = {'simple': 1, 'medium': 2, 'complex': 3}
        
        complexities = {name: template['complexity'] for name, template in templates.items()}
        sorted_by_complexity = sorted(complexities.items(), 
                                    key=lambda x: complexity_order.get(x[1], 2))
        
        return {
            'ranking': sorted_by_complexity,
            'simplest': sorted_by_complexity[0][0],
            'most_complex': sorted_by_complexity[-1][0]
        }
    
    def _compare_architectures(self, templates: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compara arquitecturas entre plantillas."""
        arch_comparison = {}
        
        for name, template in templates.items():
            arch = template['architecture']
            arch_comparison[name] = {
                'total_layers': len(arch.get('layers', [])),
                'total_neurons': sum(arch.get('layers', [])),
                'activation': arch.get('activation'),
                'dropout_rate': arch.get('dropout_rate'),
                'batch_normalization': arch.get('batch_normalization')
            }
        
        return arch_comparison
    
    def _compare_training_params(self, templates: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compara parámetros de entrenamiento entre plantillas."""
        training_comparison = {}
        
        for name, template in templates.items():
            training = template['training_params']
            training_comparison[name] = {
                'epochs': training.get('epochs'),
                'learning_rate': training.get('learning_rate'),
                'batch_size': training.get('batch_size'),
                'early_stopping': training.get('early_stopping'),
                'patience': training.get('patience')
            }
        
        return training_comparison
    
    def _analyze_use_case_overlap(self, templates: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza solapamiento en casos de uso."""
        all_use_cases = set()
        template_use_cases = {}
        
        for name, template in templates.items():
            use_cases = set(uc.lower() for uc in template['use_cases'])
            template_use_cases[name] = use_cases
            all_use_cases.update(use_cases)
        
        overlap_matrix = {}
        for name1 in template_use_cases:
            overlap_matrix[name1] = {}
            for name2 in template_use_cases:
                if name1 != name2:
                    overlap = len(template_use_cases[name1] & template_use_cases[name2])
                    total = len(template_use_cases[name1] | template_use_cases[name2])
                    overlap_matrix[name1][name2] = overlap / total if total > 0 else 0
        
        return {
            'total_unique_use_cases': len(all_use_cases),
            'overlap_matrix': overlap_matrix,
            'common_use_cases': list(all_use_cases)
        }