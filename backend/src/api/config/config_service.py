"""
Servicio para manejo de configuraciones avanzadas del sistema.

Este servicio encapsula toda la lógica relacionada con la gestión,
validación y persistencia de configuraciones del sistema.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class ConfigService:
    """Servicio para manejo de configuraciones del sistema."""
    
    def __init__(self):
        """Inicializa el servicio de configuración."""
        self.logger = logger
        self.default_config = self._get_default_config()
    
    def get_full_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa del sistema."""
        try:
            return {
                'config': self.default_config,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo configuración: {e}")
            raise
    
    def update_full_config(self, new_config: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza la configuración completa del sistema."""
        try:
            validation_result = self.validate_config(new_config)
            if not validation_result['valid']:
                raise ValueError(f"Configuración inválida: {validation_result['errors']}")
            
            # En un sistema real, aquí se persistiría la configuración
            self.logger.info("Configuración actualizada exitosamente")
            return {
                'message': 'Configuración actualizada exitosamente',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error actualizando configuración: {e}")
            raise
    
    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """Obtiene una sección específica de la configuración."""
        try:
            if section_name not in self.default_config:
                raise ValueError(f"Sección '{section_name}' no encontrada")
            
            return {
                'section': section_name,
                'config': self.default_config[section_name],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo sección {section_name}: {e}")
            raise
    
    def update_config_section(self, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una sección específica de la configuración."""
        try:
            if section_name not in self.default_config:
                raise ValueError(f"Sección '{section_name}' no encontrada")
            
            validation_result = self._validate_config_section(section_name, section_config)
            if not validation_result['valid']:
                raise ValueError(f"Configuración de sección inválida: {validation_result['errors']}")
            
            self.logger.info(f"Sección {section_name} actualizada exitosamente")
            return {
                'message': f'Sección {section_name} actualizada exitosamente',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error actualizando sección {section_name}: {e}")
            raise
    
    def reset_config(self) -> Dict[str, Any]:
        """Resetea la configuración a valores por defecto."""
        try:
            self.logger.info("Configuración reseteada a valores por defecto")
            return {
                'message': 'Configuración reseteada exitosamente',
                'config': self.default_config,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error reseteando configuración: {e}")
            raise
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Valida una configuración completa."""
        try:
            errors = []
            warnings = []
            
            # Validaciones básicas
            if not isinstance(config, dict):
                errors.append("La configuración debe ser un objeto JSON")
                return {'valid': False, 'errors': errors, 'warnings': warnings}
            
            # Validar secciones requeridas
            required_sections = ['training', 'model', 'data']
            for section in required_sections:
                if section not in config:
                    errors.append(f"Sección requerida '{section}' no encontrada")
            
            # Obtener advertencias y sugerencias
            warnings.extend(self._get_config_warnings(config))
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'suggestions': self._get_config_suggestions(config)
            }
        except Exception as e:
            self.logger.error(f"Error validando configuración: {e}")
            raise
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Obtiene la configuración por defecto del sistema."""
        return {
            'training': {
                'default_epochs': 500,
                'default_learning_rate': 0.1,
                'default_batch_size': 32,
                'early_stopping_patience': 50,
                'reduce_lr_patience': 25,
                'min_learning_rate': 0.0001
            },
            'model': {
                'default_activation': 'linear',
                'max_layers': 10,
                'max_neurons_per_layer': 1000,
                'default_dropout_rate': 0.0,
                'enable_batch_normalization': False
            },
            'data': {
                'validation_split': 0.2,
                'shuffle_data': True,
                'normalize_features': False,
                'random_seed': 42
            }
        }
    
    def _validate_config_section(self, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Valida una sección específica de configuración."""
        errors = []
        
        if section_name == 'training':
            if 'default_epochs' in section_config and section_config['default_epochs'] <= 0:
                errors.append("default_epochs debe ser mayor a 0")
            if 'default_learning_rate' in section_config and section_config['default_learning_rate'] <= 0:
                errors.append("default_learning_rate debe ser mayor a 0")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def _get_config_warnings(self, config: Dict[str, Any]) -> List[str]:
        """Obtiene advertencias sobre la configuración."""
        warnings = []
        
        if 'training' in config:
            training = config['training']
            if training.get('default_learning_rate', 0) > 1.0:
                warnings.append("Learning rate muy alto, puede causar inestabilidad")
        
        return warnings
    
    def _get_config_suggestions(self, config: Dict[str, Any]) -> List[str]:
        """Obtiene sugerencias para mejorar la configuración."""
        suggestions = []
        
        if 'model' in config:
            model = config['model']
            if not model.get('enable_batch_normalization', False):
                suggestions.append("Considerar habilitar batch normalization para mejor convergencia")
        
        return suggestions