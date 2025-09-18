# Guía de Contribución - Neural Network Trainer

## INTRODUCCIÓN

Esta guía establece los patrones, procesos y estándares que **TODOS** los desarrolladores (incluido el asistente de IA) deben seguir para mantener la integridad y calidad del proyecto.

## PRINCIPIOS FUNDAMENTALES

### 1. Preservación de Funcionalidades
- **NUNCA** modificar funciones existentes sin análisis previo
- **SIEMPRE** verificar que los cambios no rompen funcionalidad existente
- **OBLIGATORIO** ejecutar tests antes de cualquier commit

### 2. Arquitectura Modular
- Mantener separación clara entre backend, frontend y CLI
- Respetar interfaces establecidas entre módulos
- No crear dependencias circulares

### 3. Mínima Modificación
- Hacer el menor número de cambios posible
- Preferir extensión sobre modificación
- Documentar razones para cambios significativos

## FLUJO DE DESARROLLO OBLIGATORIO

### Para Nuevas Features

#### 1. Análisis Previo (OBLIGATORIO)
```bash
# Buscar funcionalidad similar existente
grep -r "función_similar" src/
grep -r "pattern_similar" frontend/src/

# Verificar dependencias
grep -r "import.*módulo" src/
grep -r "from.*módulo" src/

# Revisar tests existentes
find tests/ -name "*related*.py"
```

#### 2. Planificación
- [ ] Identificar módulos afectados
- [ ] Definir interfaces necesarias
- [ ] Planificar tests requeridos
- [ ] Verificar compatibilidad con arquitectura existente

#### 3. Implementación Incremental
```python
# ✅ CORRECTO: Extensión sin modificación
class TrainingService:
    def __init__(self):
        self.existing_method = self._preserve_existing()
    
    def new_feature(self):
        """Nueva funcionalidad sin tocar código existente."""
        return self._extend_functionality()
    
    def _preserve_existing(self):
        """Método existente - NO MODIFICAR."""
        pass

# ❌ INCORRECTO: Modificación directa
class TrainingService:
    def existing_method(self):  # ¡PELIGRO! Modificando existente
        # Cambios que pueden romper funcionalidad
        pass
```

#### 4. Validación Continua
```bash
# Ejecutar después de cada cambio
pytest tests/unit/
pytest tests/integration/
npm test

# Verificar coverage
pytest --cov=src --cov-fail-under=80
npm run test:coverage
```

### Para Refactoring

#### 1. Antes del Refactoring
- [ ] Ejecutar todos los tests (deben pasar 100%)
- [ ] Documentar funcionalidad actual
- [ ] Identificar todos los puntos de uso
- [ ] Crear tests de regresión adicionales

#### 2. Durante el Refactoring
- [ ] Cambios pequeños e incrementales
- [ ] Tests después de cada cambio
- [ ] Mantener interfaces públicas
- [ ] Preservar comportamiento observable

#### 3. Después del Refactoring
- [ ] Todos los tests pasan
- [ ] Coverage mantenido o mejorado
- [ ] Documentación actualizada
- [ ] Revisión de código completa

## PATRONES DE CÓDIGO OBLIGATORIOS

### Backend (Python)

#### Estructura de Servicios
```python
"""
Patrón obligatorio para servicios.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

class BaseService(ABC):
    """Clase base para todos los servicios."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> None:
        """Validar parámetros de entrada."""
        pass
    
    def _log_operation(self, operation: str, params: Dict[str, Any]) -> None:
        """Log estandarizado de operaciones."""
        self.logger.info(f"Executing {operation}", extra={'params': params})

class TrainingService(BaseService):
    """Servicio de entrenamiento siguiendo patrón establecido."""
    
    def validate_params(self, params: Dict[str, Any]) -> None:
        """Implementación específica de validación."""
        required_fields = ['epochs', 'learningRate', 'batchSize']
        
        for field in required_fields:
            if field not in params:
                raise ValueError(f"Campo requerido: {field}")
        
        if params['epochs'] <= 0:
            raise ValueError("Epochs debe ser mayor a 0")
        
        if params['learningRate'] <= 0:
            raise ValueError("Learning rate debe ser mayor a 0")
    
    def start_training(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Iniciar entrenamiento con validación obligatoria."""
        self._log_operation("start_training", params)
        
        # Validación OBLIGATORIA
        self.validate_params(params)
        
        try:
            # Lógica de entrenamiento
            result = self._execute_training(params)
            return result
        except Exception as e:
            self.logger.error(f"Error en entrenamiento: {str(e)}")
            raise
```

#### Manejo de Errores Estandarizado
```python
"""
Patrón obligatorio para manejo de errores.
"""

class TrainingError(Exception):
    """Error base para entrenamiento."""
    pass

class ValidationError(TrainingError):
    """Error de validación de parámetros."""
    pass

class ModelError(TrainingError):
    """Error relacionado con el modelo."""
    pass

def handle_training_error(func):
    """Decorator para manejo estandarizado de errores."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Error de validación: {str(e)}")
            return {'error': 'validation', 'message': str(e)}
        except ModelError as e:
            logger.error(f"Error de modelo: {str(e)}")
            return {'error': 'model', 'message': str(e)}
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return {'error': 'unexpected', 'message': 'Error interno del servidor'}
    
    return wrapper
```

### Frontend (TypeScript)

#### Estructura de Hooks
```typescript
/**
 * Patrón obligatorio para hooks personalizados.
 */

import { useState, useCallback, useEffect } from 'react';
import { useToast } from './useToast';
import type { TrainingParams, TrainingState, TrainingResult } from '../types/training';

interface UseTrainingReturn {
  state: TrainingState;
  startTraining: (params: TrainingParams) => Promise<void>;
  stopTraining: () => void;
  resetTraining: () => void;
  isTraining: boolean;
}

export const useTraining = (): UseTrainingReturn => {
  const [state, setState] = useState<TrainingState>({
    isActive: false,
    progress: 0,
    metrics: null,
    error: null,
  });

  const { showToast } = useToast();

  // Validación OBLIGATORIA de parámetros
  const validateParams = useCallback((params: TrainingParams): void => {
    if (params.epochs <= 0) {
      throw new Error('Las épocas deben ser mayor a 0');
    }
    
    if (params.learningRate <= 0) {
      throw new Error('La tasa de aprendizaje debe ser mayor a 0');
    }
    
    if (params.batchSize <= 0) {
      throw new Error('El batch size debe ser mayor a 0');
    }
  }, []);

  const startTraining = useCallback(async (params: TrainingParams): Promise<void> => {
    try {
      // Validación OBLIGATORIA
      validateParams(params);
      
      setState(prev => ({
        ...prev,
        isActive: true,
        error: null,
      }));

      const result = await trainingService.startTraining(params);
      
      setState(prev => ({
        ...prev,
        isActive: false,
        metrics: result.metrics,
      }));

      showToast('Entrenamiento completado exitosamente', 'success');
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
      
      setState(prev => ({
        ...prev,
        isActive: false,
        error: errorMessage,
      }));

      showToast(`Error en entrenamiento: ${errorMessage}`, 'error');
    }
  }, [validateParams, showToast]);

  const stopTraining = useCallback((): void => {
    trainingService.stopTraining();
    setState(prev => ({
      ...prev,
      isActive: false,
    }));
  }, []);

  const resetTraining = useCallback((): void => {
    setState({
      isActive: false,
      progress: 0,
      metrics: null,
      error: null,
    });
  }, []);

  const isTraining = state.isActive;

  return {
    state,
    startTraining,
    stopTraining,
    resetTraining,
    isTraining,
  };
};
```

#### Estructura de Componentes
```typescript
/**
 * Patrón obligatorio para componentes.
 */

import React, { memo } from 'react';
import type { TrainingParams } from '../types/training';

interface TrainingFormProps {
  onSubmit: (params: TrainingParams) => void;
  disabled?: boolean;
  initialValues?: Partial<TrainingParams>;
}

export const TrainingForm = memo<TrainingFormProps>(({
  onSubmit,
  disabled = false,
  initialValues = {},
}) => {
  // Valores por defecto OBLIGATORIOS
  const defaultValues: TrainingParams = {
    epochs: 100,
    learningRate: 0.01,
    batchSize: 32,
    datasetSize: 1000,
    ...initialValues,
  };

  const [formData, setFormData] = useState<TrainingParams>(defaultValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Validación OBLIGATORIA
  const validateForm = useCallback((data: TrainingParams): Record<string, string> => {
    const newErrors: Record<string, string> = {};

    if (data.epochs <= 0) {
      newErrors.epochs = 'Las épocas deben ser mayor a 0';
    }

    if (data.learningRate <= 0 || data.learningRate >= 1) {
      newErrors.learningRate = 'La tasa de aprendizaje debe estar entre 0 y 1';
    }

    if (data.batchSize <= 0) {
      newErrors.batchSize = 'El batch size debe ser mayor a 0';
    }

    return newErrors;
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    
    // Validación OBLIGATORIA antes de envío
    const formErrors = validateForm(formData);
    setErrors(formErrors);

    if (Object.keys(formErrors).length === 0) {
      onSubmit(formData);
    }
  }, [formData, validateForm, onSubmit]);

  // Resto del componente...
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Campos del formulario */}
    </form>
  );
});

TrainingForm.displayName = 'TrainingForm';
```

## COMUNICACIÓN ENTRE CAPAS

### API REST (Backend ↔ Frontend)
```python
# Backend - Patrón obligatorio para rutas
@app.route('/api/training/start', methods=['POST'])
@handle_training_error
def start_training():
    """Iniciar entrenamiento con validación completa."""
    try:
        # Validación de request OBLIGATORIA
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        params = request.get_json()
        
        # Validación de parámetros OBLIGATORIA
        training_service = TrainingService(current_app.config)
        training_service.validate_params(params)
        
        # Ejecutar entrenamiento
        result = training_service.start_training(params)
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'error': 'validation',
            'message': str(e)
        }), 400
    
    except Exception as e:
        current_app.logger.error(f"Error inesperado: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'internal',
            'message': 'Error interno del servidor'
        }), 500
```

```typescript
// Frontend - Patrón obligatorio para servicios
class TrainingService {
  private readonly baseURL = '/api/training';

  async startTraining(params: TrainingParams): Promise<TrainingResult> {
    try {
      const response = await fetch(`${this.baseURL}/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error en la solicitud');
      }

      if (data.status !== 'success') {
        throw new Error(data.message || 'Error en el servidor');
      }

      return data.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Error de conexión');
    }
  }
}
```

### WebSocket (Tiempo Real)
```python
# Backend - Patrón obligatorio para WebSocket
@socketio.on('training_progress')
def handle_training_progress(data):
    """Manejar progreso de entrenamiento."""
    try:
        # Validación OBLIGATORIA
        if 'session_id' not in data:
            emit('error', {'message': 'session_id requerido'})
            return
        
        session_id = data['session_id']
        
        # Emitir progreso con formato estandarizado
        emit('training_update', {
            'session_id': session_id,
            'progress': data.get('progress', 0),
            'metrics': data.get('metrics', {}),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        emit('error', {
            'message': 'Error procesando progreso',
            'details': str(e)
        })
```

```typescript
// Frontend - Patrón obligatorio para WebSocket
class SocketService {
  private socket: Socket | null = null;

  connect(): void {
    this.socket = io();
    
    this.socket.on('connect', () => {
      console.log('Conectado al servidor');
    });

    this.socket.on('training_update', (data: TrainingUpdate) => {
      // Validación OBLIGATORIA de datos recibidos
      if (!this.isValidTrainingUpdate(data)) {
        console.error('Datos de entrenamiento inválidos:', data);
        return;
      }

      // Procesar actualización
      this.handleTrainingUpdate(data);
    });

    this.socket.on('error', (error: SocketError) => {
      console.error('Error de socket:', error);
      this.handleSocketError(error);
    });
  }

  private isValidTrainingUpdate(data: any): data is TrainingUpdate {
    return (
      typeof data === 'object' &&
      typeof data.session_id === 'string' &&
      typeof data.progress === 'number' &&
      typeof data.metrics === 'object'
    );
  }
}
```

## TESTING OBLIGATORIO

### Para Cada Nueva Función
```python
# Test unitario OBLIGATORIO
def test_new_function():
    """Test para nueva funcionalidad."""
    # Arrange
    service = TrainingService(test_config)
    params = {'epochs': 10, 'learningRate': 0.01}
    
    # Act
    result = service.new_function(params)
    
    # Assert
    assert result is not None
    assert 'status' in result

# Test de integración OBLIGATORIO
def test_new_function_integration():
    """Test de integración para nueva funcionalidad."""
    # Verificar que no rompe funcionalidad existente
    pass

# Test de error OBLIGATORIO
def test_new_function_error_handling():
    """Test manejo de errores."""
    service = TrainingService(test_config)
    
    with pytest.raises(ValidationError):
        service.new_function({'invalid': 'params'})
```

### Para Cada Componente Nuevo
```typescript
// Test de componente OBLIGATORIO
describe('NewComponent', () => {
  it('renders correctly', () => {
    render(<NewComponent />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const mockHandler = jest.fn();
    render(<NewComponent onAction={mockHandler} />);
    
    await userEvent.click(screen.getByRole('button'));
    expect(mockHandler).toHaveBeenCalled();
  });

  it('handles errors gracefully', () => {
    const mockError = jest.fn(() => {
      throw new Error('Test error');
    });
    
    render(<NewComponent onAction={mockError} />);
    // Verificar que el error se maneja correctamente
  });
});
```

## COMANDOS DE VERIFICACIÓN

### Antes de Commit (OBLIGATORIO)
```bash
#!/bin/bash
# pre-commit-check.sh

echo "🔍 Ejecutando verificaciones pre-commit..."

# 1. Tests backend
echo "📋 Ejecutando tests backend..."
cd backend/
python -m pytest tests/ -v --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests backend fallaron"
    exit 1
fi

# 2. Tests frontend
echo "📋 Ejecutando tests frontend..."
cd ../frontend/
npm test -- --watchAll=false
if [ $? -ne 0 ]; then
    echo "❌ Tests frontend fallaron"
    exit 1
fi

# 3. Linting
echo "🔧 Verificando linting..."
cd ../backend/
flake8 src/
if [ $? -ne 0 ]; then
    echo "❌ Linting backend falló"
    exit 1
fi

cd ../frontend/
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Linting frontend falló"
    exit 1
fi

# 4. Type checking
echo "🔍 Verificando tipos..."
cd ../frontend/
npm run type-check
if [ $? -ne 0 ]; then
    echo "❌ Type checking falló"
    exit 1
fi

echo "✅ Todas las verificaciones pasaron"
```

### Verificación de Integridad
```bash
# Verificar que no se rompió funcionalidad existente
pytest tests/integration/ -v

# Verificar coverage mínimo
pytest --cov=src --cov-fail-under=80

# Verificar que todos los endpoints funcionan
python scripts/test_endpoints.py

# Verificar que el frontend compila
npm run build
```

## DOCUMENTACIÓN OBLIGATORIA

### Para Nuevas Features
- [ ] Docstring completo en funciones
- [ ] Comentarios en lógica compleja
- [ ] Actualizar README si es necesario
- [ ] Ejemplos de uso en código

### Para APIs
- [ ] Documentar parámetros de entrada
- [ ] Documentar respuestas posibles
- [ ] Documentar códigos de error
- [ ] Ejemplos de requests/responses

## CHECKLIST DE CONTRIBUCIÓN

### Antes de Empezar
- [ ] Leer esta guía completa
- [ ] Entender la arquitectura del proyecto
- [ ] Configurar entorno de desarrollo
- [ ] Ejecutar tests existentes

### Durante el Desarrollo
- [ ] Seguir patrones establecidos
- [ ] Escribir tests para código nuevo
- [ ] Validar que no se rompe funcionalidad existente
- [ ] Documentar cambios significativos

### Antes de Commit
- [ ] Ejecutar script de verificación
- [ ] Revisar que todos los tests pasan
- [ ] Verificar coverage mínimo
- [ ] Linting sin errores

### Para Pull Request
- [ ] Descripción clara de cambios
- [ ] Tests que demuestran funcionalidad
- [ ] Documentación actualizada
- [ ] No hay conflictos de merge

---

**IMPORTANTE**: Esta guía es de cumplimiento OBLIGATORIO para mantener la calidad y estabilidad del proyecto. Cualquier código que no siga estos patrones será rechazado.