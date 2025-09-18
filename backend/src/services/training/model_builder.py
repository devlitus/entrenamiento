# c:/dev/entrenamiento/backend/src/services/training/model_builder.py
"""
Constructor de modelos con arquitecturas personalizables.
"""

import tensorflow as tf
from utils.logger import setup_logger

logger = setup_logger()

class ModelBuilder:
    """Constructor de modelos con arquitecturas personalizables."""
    
    @staticmethod
    def create_model(learning_rate, architecture=None):
        """Crea y compila el modelo con arquitectura personalizable."""
        layers = []
        architecture_info = {
            'type': 'custom' if architecture and 'hiddenLayers' in architecture else 'default',
            'layers': [],
            'total_parameters': 0,
            'config_received': architecture is not None
        }
        
        if architecture and 'hiddenLayers' in architecture:
            # Capa de entrada implícita
            input_shape = architecture.get('inputLayer', {}).get('shape', [1])
            architecture_info['input_shape'] = input_shape
            
            logger.info("[BUILD] CREANDO MODELO CON ARQUITECTURA PERSONALIZADA")
            logger.info(f"[CONFIG] Configuración recibida: {architecture}")
            
            # Agregar capas ocultas
            for i, layer_config in enumerate(architecture['hiddenLayers']):
                layer_info = {
                    'type': 'hidden',
                    'index': i,
                    'neurons': layer_config['neurons'],
                    'activation': layer_config['activation']
                }
                architecture_info['layers'].append(layer_info)
                
                if i == 0:
                    # Primera capa oculta necesita input_shape
                    layers.append(tf.keras.layers.Dense(
                        layer_config['neurons'],
                        activation=layer_config['activation'],
                        input_shape=input_shape,
                        name=f'hidden_layer_{i+1}'
                    ))
                    logger.info(f"  ➤ Capa oculta {i+1}: {layer_config['neurons']} neuronas, activación '{layer_config['activation']}'")
                else:
                    layers.append(tf.keras.layers.Dense(
                        layer_config['neurons'],
                        activation=layer_config['activation'],
                        name=f'hidden_layer_{i+1}'
                    ))
                    logger.info(f"  ➤ Capa oculta {i+1}: {layer_config['neurons']} neuronas, activación '{layer_config['activation']}'")
            
            # Capa de salida
            output_config = architecture.get('outputLayer', {'neurons': 1, 'activation': 'linear'})
            output_info = {
                'type': 'output',
                'neurons': output_config['neurons'],
                'activation': output_config['activation']
            }
            architecture_info['layers'].append(output_info)
            
            layers.append(tf.keras.layers.Dense(
                output_config['neurons'],
                activation=output_config['activation'],
                name='output_layer'
            ))
            logger.info(f"  ➤ Capa de salida: {output_config['neurons']} neuronas, activación '{output_config['activation']}'")
            
        else:
            # Arquitectura por defecto (modelo simple)
            logger.info("[BUILD] CREANDO MODELO CON ARQUITECTURA POR DEFECTO")
            logger.info("  ➤ Modelo simple: 1 capa densa con 1 neurona")
            
            layers.append(tf.keras.layers.Dense(1, input_shape=[1], name='output_layer'))
            architecture_info['layers'].append({
                'type': 'output',
                'neurons': 1,
                'activation': 'linear'
            })
        
        model = tf.keras.Sequential(layers)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='mse',
            metrics=['mae']
        )
        
        # Actualizar información de arquitectura
        architecture_info['total_parameters'] = model.count_params()
        
        # Agregar conteo de capas ocultas
        if architecture and 'hiddenLayers' in architecture:
            architecture_info['hidden_layers'] = len(architecture['hiddenLayers'])
        else:
            architecture_info['hidden_layers'] = 0  # Modelo por defecto no tiene capas ocultas
        
        # Log detallado de la arquitectura creada
        logger.info(f"[SUCCESS] MODELO CREADO EXITOSAMENTE")
        logger.info(f"   📈 Tipo: {architecture_info['type']}")
        logger.info(f"   [LAYERS] Total de capas: {len(layers)}")
        logger.info(f"   [PARAMS] Total de parámetros: {architecture_info['total_parameters']}")
        logger.info(f"   [CONFIG] Tasa de aprendizaje: {learning_rate}")
        
        # Guardar información de arquitectura en el modelo para verificación posterior
        model._architecture_info = architecture_info
        
        return model
    
    @staticmethod
    def get_architecture_summary(model):
        """Obtiene un resumen de la arquitectura del modelo para verificación."""
        if hasattr(model, '_architecture_info'):
            return model._architecture_info
        
        # Fallback: extraer información del modelo existente
        layers_info = []
        hidden_layers_count = 0
        
        for i, layer in enumerate(model.layers):
            layer_info = {
                'name': layer.name,
                'type': layer.__class__.__name__,
                'units': getattr(layer, 'units', None),
                'activation': getattr(layer, 'activation', None)
            }
            layers_info.append(layer_info)
            
            # Contar capas ocultas (Dense layers excepto la última que es output)
            if layer.__class__.__name__ == 'Dense' and i < len(model.layers) - 1:
                hidden_layers_count += 1
        
        summary = {
            'type': 'unknown',
            'layers': layers_info,
            'hidden_layers': hidden_layers_count,  # Campo que faltaba
            'total_parameters': model.count_params(),
            'config_received': False
        }
        
        return summary