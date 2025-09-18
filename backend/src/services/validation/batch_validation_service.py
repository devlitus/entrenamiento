"""
Servicio de validación en lote.

Maneja la lógica de negocio para validaciones en lote.
"""

from typing import Dict, Any, List
from datetime import datetime
from .model_validation_service import ModelValidationService
from utils.logger import setup_logger

logger = setup_logger()


class BatchValidationService:
    """Servicio para validaciones en lote."""
    
    def __init__(self, validation_service: ModelValidationService = None):
        """
        Inicializa el servicio de validación en lote.
        
        Args:
            validation_service: Instancia del servicio de validación
        """
        self.validation_service = validation_service or ModelValidationService()
        self.logger = logger
    
    def validate_batch(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida múltiples configuraciones en lote.
        
        Args:
            items: Lista de elementos a validar
            
        Returns:
            Diccionario con resultados de validación
        """
        results = []
        
        for i, item in enumerate(items):
            try:
                result = self._validate_single_item(item)
                results.append({
                    'index': i,
                    'valid': result.is_valid,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'suggestions': result.suggestions
                })
            except Exception as e:
                self.logger.error(f"Error validating item {i}: {str(e)}")
                results.append({
                    'index': i,
                    'valid': False,
                    'errors': [f"Validation error: {str(e)}"],
                    'warnings': [],
                    'suggestions': []
                })
        
        return self._build_batch_response(results)
    
    def _validate_single_item(self, item: Dict[str, Any]):
        """
        Valida un elemento individual determinando su tipo.
        
        Args:
            item: Elemento a validar
            
        Returns:
            Resultado de validación
        """
        # Determinar tipo de validación basado en contenido
        if 'model' in item and 'training' in item:
            return self.validation_service.validate_experiment_config(item)
        elif 'epochs' in item or 'learning_rate' in item:
            return self.validation_service.validate_training_params(item)
        elif 'layers' in item or 'activation' in item:
            return self.validation_service.validate_architecture(item)
        else:
            # Para elementos que no coinciden con ningún patrón, usar validación de arquitectura por defecto
            return self.validation_service.validate_architecture(item)
    
    def _build_batch_response(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Construye la respuesta del lote con estadísticas.
        
        Args:
            results: Lista de resultados de validación
            
        Returns:
            Respuesta completa del lote
        """
        total_items = len(results)
        valid_items = sum(1 for r in results if r['valid'])
        
        return {
            'batch_results': results,
            'summary': {
                'total_items': total_items,
                'valid_items': valid_items,
                'invalid_items': total_items - valid_items,
                'success_rate': (valid_items / total_items) * 100 if total_items > 0 else 0
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Realiza un health check del servicio de validación en lote.
        
        Returns:
            Estado del servicio
        """
        try:
            # Lote de prueba simple
            test_items = [
                {'epochs': 100, 'learning_rate': 0.01},
                {'layers': [1], 'activation': 'linear'}
            ]
            
            test_results = []
            for item in test_items:
                if 'epochs' in item:
                    result = self.validation_service.validate_training_params(item)
                else:
                    result = self.validation_service.validate_architecture(item)
                test_results.append(result.is_valid)
            
            return {
                'status': 'healthy',
                'service': 'batch_validation',
                'test_batch_size': len(test_items),
                'test_success_rate': (sum(test_results) / len(test_results)) * 100,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Batch health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'service': 'batch_validation',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }