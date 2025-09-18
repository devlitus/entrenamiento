# Estándares de Código - Neural Network Trainer

## ESTÁNDARES PYTHON (BACKEND)

### Estructura de Archivos
```python
"""
Módulo para [descripción breve].

Este módulo implementa [funcionalidad principal] siguiendo los patrones
establecidos del proyecto Neural Network Trainer.
"""

# Imports estándar
import os
import sys
from typing import Dict, List, Optional, Union

# Imports de terceros
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

# Imports locales
from src.config import Config
from src.services.base_service import BaseService
from utils.logger import setup_logger

# Configuración del logger
logger = setup_logger()

# Constantes del módulo
DEFAULT_BATCH_SIZE = 32
MAX_EPOCHS = 1000
```

### Clases y Servicios
```python
class TrainingService(BaseService):
    """Servicio para manejo de entrenamientos de redes neuronales.
    
    Este servicio encapsula toda la lógica relacionada con el entrenamiento
    de modelos, incluyendo configuración, ejecución y monitoreo.
    
    Attributes:
        config: Configuración del servicio
        logger: Logger para el servicio
        model_builder: Constructor de modelos
    """
    
    def __init__(self, config: Config):
        """Inicializa el servicio de entrenamiento.
        
        Args:
            config: Configuración del servicio
        """
        super().__init__(config)
        self.model_builder = ModelBuilder(config)
        self.logger = setup_logger()
    
    def start_training(self, params: TrainingParams) -> TrainingResult:
        """Inicia un proceso de entrenamiento.
        
        Args:
            params: Parámetros de entrenamiento
            
        Returns:
            Resultado del entrenamiento
            
        Raises:
            ValidationError: Si los parámetros no son válidos
            TrainingError: Si ocurre un error durante el entrenamiento
        """
        try:
            self._validate_params(params)
            model = self._create_model(params)
            result = self._execute_training(model, params)
            self.logger.info(f"Entrenamiento completado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error en entrenamiento: {e}")
            raise
    
    def _validate_params(self, params: TrainingParams) -> None:
        """Valida parámetros de entrenamiento."""
        if params.epochs <= 0:
            raise ValidationError("Epochs debe ser mayor a 0")
        if params.learning_rate <= 0:
            raise ValidationError("Learning rate debe ser mayor a 0")
    
    def _create_model(self, params: TrainingParams) -> tf.keras.Model:
        """Crea modelo basado en parámetros."""
        return self.model_builder.create_model(
            learning_rate=params.learning_rate,
            architecture=params.architecture
        )
    
    def _execute_training(self, model: tf.keras.Model, params: TrainingParams) -> TrainingResult:
        """Ejecuta el entrenamiento del modelo."""
        # Implementación específica
        pass
```

### Funciones Utilitarias
```python
def validate_architecture_config(config: Dict) -> bool:
    """Valida configuración de arquitectura de modelo.
    
    Args:
        config: Configuración de arquitectura
        
    Returns:
        True si la configuración es válida
        
    Raises:
        ValidationError: Si la configuración no es válida
    """
    required_fields = ['inputLayer', 'hiddenLayers', 'outputLayer']
    
    for field in required_fields:
        if field not in config:
            raise ValidationError(f"Campo requerido: {field}")
    
    return True

def calculate_model_parameters(layers: List[Dict]) -> int:
    """Calcula número total de parámetros del modelo.
    
    Args:
        layers: Lista de configuraciones de capas
        
    Returns:
        Número total de parámetros
    """
    total_params = 0
    prev_neurons = 1
    
    for layer in layers:
        neurons = layer.get('neurons', 1)
        total_params += (prev_neurons * neurons) + neurons
        prev_neurons = neurons
    
    return total_params
```

### Manejo de Errores
```python
class TrainingError(Exception):
    """Error específico de entrenamiento."""
    pass

class ValidationError(Exception):
    """Error de validación de datos."""
    pass

class ConfigurationError(Exception):
    """Error de configuración."""
    pass

# Uso en servicios
try:
    result = service.execute_operation(params)
    logger.info(f"Operación exitosa: {result}")
    return jsonify(result), 200
except ValidationError as e:
    logger.warning(f"Error de validación: {e}")
    return jsonify({'error': str(e)}), 400
except TrainingError as e:
    logger.error(f"Error de entrenamiento: {e}")
    return jsonify({'error': 'Error en entrenamiento'}), 500
except Exception as e:
    logger.critical(f"Error crítico: {e}")
    return jsonify({'error': 'Error interno del servidor'}), 500
```

## ESTÁNDARES TYPESCRIPT (FRONTEND)

### Estructura de Archivos
```typescript
/**
 * Hook personalizado para manejo de estado de entrenamiento.
 * 
 * Este hook encapsula toda la lógica relacionada con el estado
 * y las operaciones de entrenamiento de modelos.
 */

import { useState, useCallback, useEffect } from 'react';
import type { 
  TrainingParams, 
  TrainingResult, 
  TrainingState 
} from '../types/training';
import { trainingService } from '../services/trainingService';
import { useToast } from './useToast';

// Tipos específicos del hook
interface UseTrainingReturn {
  state: TrainingState;
  startTraining: (params: TrainingParams) => Promise<void>;
  stopTraining: () => void;
  isTraining: boolean;
}

// Estado inicial
const initialState: TrainingState = {
  isActive: false,
  progress: 0,
  metrics: null,
  error: null
};
```

### Hooks Personalizados
```typescript
export function useTraining(): UseTrainingReturn {
  const [state, setState] = useState<TrainingState>(initialState);
  const { showToast } = useToast();
  
  const startTraining = useCallback(async (params: TrainingParams) => {
    try {
      setState(prev => ({ ...prev, isActive: true, error: null }));
      
      const result = await trainingService.startTraining(params);
      
      setState(prev => ({ 
        ...prev, 
        isActive: false, 
        metrics: result.metrics 
      }));
      
      showToast('Entrenamiento completado exitosamente', 'success');
    } catch (error) {
      console.error('Error en entrenamiento:', error);
      setState(prev => ({ 
        ...prev, 
        isActive: false, 
        error: error instanceof Error ? error.message : 'Error desconocido'
      }));
      showToast('Error en entrenamiento', 'error');
    }
  }, [showToast]);
  
  const stopTraining = useCallback(() => {
    trainingService.stopTraining();
    setState(prev => ({ ...prev, isActive: false }));
  }, []);
  
  const isTraining = state.isActive;
  
  return {
    state,
    startTraining,
    stopTraining,
    isTraining
  };
}
```

### Componentes
```typescript
interface TrainingFormProps {
  onSubmit: (params: TrainingParams) => void;
  disabled?: boolean;
  initialValues?: Partial<TrainingParams>;
}

export function TrainingForm({ 
  onSubmit, 
  disabled = false, 
  initialValues = {} 
}: TrainingFormProps) {
  const [params, setParams] = useState<TrainingParams>({
    epochs: 100,
    learningRate: 0.01,
    batchSize: 32,
    ...initialValues
  });
  
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    
    // Validación
    if (params.epochs <= 0) {
      console.error('Epochs debe ser mayor a 0');
      return;
    }
    
    onSubmit(params);
  }, [params, onSubmit]);
  
  const handleChange = useCallback((field: keyof TrainingParams) => 
    (value: number) => {
      setParams(prev => ({ ...prev, [field]: value }));
    }, []
  );
  
  return (
    <form onSubmit={handleSubmit} className="training-form">
      <div className="form-group">
        <label htmlFor="epochs">Épocas</label>
        <input
          id="epochs"
          type="number"
          value={params.epochs}
          onChange={(e) => handleChange('epochs')(Number(e.target.value))}
          disabled={disabled}
          min={1}
          max={1000}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="learningRate">Tasa de Aprendizaje</label>
        <input
          id="learningRate"
          type="number"
          value={params.learningRate}
          onChange={(e) => handleChange('learningRate')(Number(e.target.value))}
          disabled={disabled}
          min={0.0001}
          max={1}
          step={0.0001}
        />
      </div>
      
      <button 
        type="submit" 
        disabled={disabled}
        className="submit-button"
      >
        {disabled ? 'Entrenando...' : 'Iniciar Entrenamiento'}
      </button>
    </form>
  );
}
```

### Servicios
```typescript
class TrainingService {
  private readonly baseUrl = 'http://localhost:5000/api';
  
  async startTraining(params: TrainingParams): Promise<TrainingResult> {
    try {
      const response = await fetch(`${this.baseUrl}/training/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error iniciando entrenamiento:', error);
      throw error;
    }
  }
  
  stopTraining(): void {
    // Implementación para detener entrenamiento
    fetch(`${this.baseUrl}/training/stop`, { method: 'POST' })
      .catch(error => console.error('Error deteniendo entrenamiento:', error));
  }
}

export const trainingService = new TrainingService();
```

### Stores (Zustand)
```typescript
interface TrainingStore {
  // Estado
  currentTraining: TrainingSession | null;
  history: TrainingSession[];
  isLoading: boolean;
  
  // Acciones
  setCurrentTraining: (training: TrainingSession | null) => void;
  addToHistory: (training: TrainingSession) => void;
  clearHistory: () => void;
  setLoading: (loading: boolean) => void;
}

export const useTrainingStore = create<TrainingStore>((set, get) => ({
  // Estado inicial
  currentTraining: null,
  history: [],
  isLoading: false,
  
  // Acciones
  setCurrentTraining: (training) => 
    set({ currentTraining: training }),
  
  addToHistory: (training) => 
    set(state => ({ 
      history: [training, ...state.history].slice(0, 50) // Mantener últimas 50
    })),
  
  clearHistory: () => 
    set({ history: [] }),
  
  setLoading: (loading) => 
    set({ isLoading: loading }),
}));
```

## CONVENCIONES DE NAMING

### Python
```python
# Variables y funciones: snake_case
training_params = {}
def calculate_metrics():
    pass

# Clases: PascalCase
class TrainingService:
    pass

# Constantes: UPPER_SNAKE_CASE
DEFAULT_LEARNING_RATE = 0.01
MAX_EPOCHS = 1000

# Archivos: snake_case
training_service.py
model_builder.py
```

### TypeScript
```typescript
// Variables y funciones: camelCase
const trainingParams = {};
function calculateMetrics() {}

// Interfaces y tipos: PascalCase
interface TrainingParams {}
type TrainingResult = {};

// Componentes: PascalCase
function TrainingForm() {}

// Constantes: UPPER_SNAKE_CASE
const DEFAULT_LEARNING_RATE = 0.01;
const MAX_EPOCHS = 1000;

// Archivos: camelCase
trainingService.ts
modelBuilder.ts
```

## COMENTARIOS Y DOCUMENTACIÓN

### Python - Docstrings
```python
def complex_function(param1: str, param2: int, param3: Optional[Dict] = None) -> Dict:
    """Función compleja que realiza múltiples operaciones.
    
    Esta función toma varios parámetros y realiza operaciones complejas
    sobre ellos, devolviendo un resultado estructurado.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro
        param3: Parámetro opcional con valor por defecto
        
    Returns:
        Diccionario con los resultados de la operación
        
    Raises:
        ValueError: Si param1 está vacío
        TypeError: Si param2 no es un entero
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result['status'])
        'success'
    """
    pass
```

### TypeScript - JSDoc
```typescript
/**
 * Hook personalizado para manejo de estado de entrenamiento.
 * 
 * Este hook encapsula toda la lógica relacionada con el estado
 * y las operaciones de entrenamiento de modelos.
 * 
 * @returns Objeto con estado y funciones de entrenamiento
 * 
 * @example
 * ```tsx
 * function TrainingComponent() {
 *   const { startTraining, isTraining } = useTraining();
 *   
 *   return (
 *     <button onClick={() => startTraining(params)} disabled={isTraining}>
 *       {isTraining ? 'Entrenando...' : 'Entrenar'}
 *     </button>
 *   );
 * }
 * ```
 */
export function useTraining(): UseTrainingReturn {
  // Implementación
}
```

---

**IMPORTANTE**: Estos estándares son OBLIGATORIOS y deben seguirse en todo el código del proyecto para mantener consistencia y calidad.