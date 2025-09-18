"""Servicio de plantillas para el módulo API."""

from typing import Dict, Any, List, Optional
from src.services.templates.template_service import TemplateService as BaseTemplateService
import logging

logger = logging.getLogger(__name__)

class TemplateService:
    """Wrapper del servicio de plantillas para compatibilidad con API."""
    
    def __init__(self):
        """Inicializa el servicio usando el servicio base."""
        self._base_service = BaseTemplateService()
        
    def _load_default_templates(self):
        """Cargar plantillas por defecto."""
        # Plantillas básicas para diferentes casos de uso
        default_templates = {
            'simple_regression': {
                'id': 'simple_regression',
                'name': 'Regresión Simple',
                'category': 'regression',
                'complexity': 'basic',
                'use_case': 'prediction',
                'description': 'Plantilla básica para regresión lineal',
                'architecture': {
                    'layers': [
                        {'type': 'dense', 'units': 64, 'activation': 'relu'},
                        {'type': 'dense', 'units': 1, 'activation': 'linear'}
                    ]
                },
                'training_params': {
                    'optimizer': 'adam',
                    'loss': 'mse',
                    'metrics': ['mae'],
                    'epochs': 100,
                    'batch_size': 32
                }
            },
            'multi_layer_regression': {
                'id': 'multi_layer_regression',
                'name': 'Regresión Multi-Capa',
                'category': 'regression',
                'complexity': 'intermediate',
                'use_case': 'prediction',
                'description': 'Plantilla avanzada para regresión con múltiples capas',
                'architecture': {
                    'layers': [
                        {'type': 'dense', 'units': 128, 'activation': 'relu'},
                        {'type': 'dropout', 'rate': 0.2},
                        {'type': 'dense', 'units': 64, 'activation': 'relu'},
                        {'type': 'dropout', 'rate': 0.2},
                        {'type': 'dense', 'units': 32, 'activation': 'relu'},
                        {'type': 'dense', 'units': 1, 'activation': 'linear'}
                    ]
                },
                'training_params': {
                    'optimizer': 'adam',
                    'loss': 'mse',
                    'metrics': ['mae'],
                    'epochs': 200,
                    'batch_size': 64
                }
            }
        }
        
        self.templates.update(default_templates)
        
    def list_templates(self, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Listar plantillas con filtros opcionales."""
        templates = list(self.templates.values())
        
        if filters:
            if 'category' in filters:
                templates = [t for t in templates if t.get('category') == filters['category']]
            if 'complexity' in filters:
                templates = [t for t in templates if t.get('complexity') == filters['complexity']]
            if 'use_case' in filters:
                templates = [t for t in templates if t.get('use_case') == filters['use_case']]
                
        return templates
        
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Obtener plantilla por ID."""
        return self.templates.get(template_id)
        
    def customize_template(self, template_id: str, customizations: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Personalizar plantilla con parámetros específicos."""
        template = self.get_template(template_id)
        if not template:
            return None
            
        # Crear copia personalizada
        customized = template.copy()
        
        # Aplicar personalizaciones
        if 'architecture' in customizations:
            customized['architecture'].update(customizations['architecture'])
        if 'training_params' in customizations:
            customized['training_params'].update(customizations['training_params'])
        if 'name' in customizations:
            customized['name'] = customizations['name']
        if 'description' in customizations:
            customized['description'] = customizations['description']
            
        return customized
        
    def recommend_templates(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recomendar plantillas basadas en requerimientos."""
        templates = list(self.templates.values())
        recommendations = []
        
        # Filtrar por requerimientos
        problem_type = requirements.get('problem_type')
        complexity = requirements.get('complexity')
        dataset_size = requirements.get('dataset_size')
        
        for template in templates:
            score = 0
            
            # Puntuación por tipo de problema
            if problem_type and template.get('category') == problem_type:
                score += 3
                
            # Puntuación por complejidad
            if complexity and template.get('complexity') == complexity:
                score += 2
                
            # Puntuación por tamaño de dataset
            if dataset_size:
                if dataset_size == 'small' and template.get('complexity') == 'basic':
                    score += 1
                elif dataset_size == 'large' and template.get('complexity') in ['intermediate', 'advanced']:
                    score += 1
                    
            if score > 0:
                template_with_score = template.copy()
                template_with_score['recommendation_score'] = score
                recommendations.append(template_with_score)
                
        # Ordenar por puntuación
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations
        
    def compare_templates(self, template_ids: List[str]) -> Dict[str, Any]:
        """Comparar múltiples plantillas."""
        templates = []
        for template_id in template_ids:
            template = self.get_template(template_id)
            if template:
                templates.append(template)
                
        if not templates:
            return {'error': 'No valid templates found'}
            
        comparison = {
            'templates': templates,
            'comparison_matrix': self._create_comparison_matrix(templates),
            'summary': self._create_comparison_summary(templates)
        }
        
        return comparison
        
    def _create_comparison_matrix(self, templates: List[Dict]) -> Dict[str, Any]:
        """Crear matriz de comparación."""
        matrix = {}
        
        # Comparar características clave
        for key in ['complexity', 'category', 'use_case']:
            matrix[key] = [t.get(key, 'N/A') for t in templates]
            
        # Comparar parámetros de arquitectura
        matrix['layer_count'] = []
        for template in templates:
            layers = template.get('architecture', {}).get('layers', [])
            matrix['layer_count'].append(len(layers))
            
        return matrix
        
    def _create_comparison_summary(self, templates: List[Dict]) -> Dict[str, Any]:
        """Crear resumen de comparación."""
        summary = {
            'total_templates': len(templates),
            'categories': list(set(t.get('category', 'unknown') for t in templates)),
            'complexity_levels': list(set(t.get('complexity', 'unknown') for t in templates)),
            'avg_layer_count': 0
        }
        
        # Calcular promedio de capas
        total_layers = 0
        for template in templates:
            layers = template.get('architecture', {}).get('layers', [])
            total_layers += len(layers)
            
        if templates:
            summary['avg_layer_count'] = total_layers / len(templates)
            
        return summary