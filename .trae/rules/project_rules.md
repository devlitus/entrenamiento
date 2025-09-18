# Reglas de Codificación del Proyecto - Neural Trainer

## 🐍 Reglas para Python (Backend)

### Principios Fundamentales
- **PEP 8**: Seguir estrictamente las convenciones de estilo de Python
- **PEP 20**: Aplicar "The Zen of Python" en el diseño
- **Clean Code**: Código limpio, legible y mantenible
- **SOLID**: Principios de diseño orientado a objetos
- **DRY**: Don't Repeat Yourself


### Estructura y Organización

#### Estructura de Archivos
```python
# ✅ CORRECTO: Estructura modular clara
backend/
├── src/
│   ├── api/           # Endpoints REST
│   ├── services/      # Lógica de negocio
│   ├── schemas/       # Validación con Pydantic
│   └── utils/         # Utilidades compartidas
├── tests/             # Tests unitarios e integración
├── config.py          # Configuración centralizada
└── server.py          # Punto de entrada
```

#### Imports y Dependencias
```python
# ✅ CORRECTO: Orden de imports según PEP 8
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

from config import Config
from src.services.training_service import TrainingService
from utils.logger import setup_logger
```

### Convenciones de Nomenclatura

#### Clases
```python
# ✅ CORRECTO: PascalCase para clases
class TrainingService:
    """Servicio principal para entrenamiento de modelos ML."""
    
class ModelValidationService:
    """Servicio de validación robusta para configuraciones."""
```

#### Funciones y Variables
```python
# ✅ CORRECTO: snake_case para funciones y variables
def calculate_training_metrics(model_data: Dict[str, Any]) -> Dict[str, float]:
    """Calcula métricas de entrenamiento del modelo."""
    training_accuracy = model_data.get('accuracy', 0.0)
    validation_loss = model_data.get('val_loss', float('inf'))
    return {'accuracy': training_accuracy, 'val_loss': validation_loss}

# Variables
model_config = {'epochs': 100, 'batch_size': 32}
learning_rate = 0.001
```

#### Constantes
```python
# ✅ CORRECTO: UPPER_CASE para constantes
DEFAULT_EPOCHS = 100
MAX_BATCH_SIZE = 512
MODEL_SAVE_PATH = Path('models/trained_model.keras')
```

### Documentación y Comentarios
**Documentación**: Util para los endpoint de la API REST http://localhost:5000/api/docs/

#### Docstrings
```python
# ✅ CORRECTO: Docstrings detallados estilo Google
class ExperimentService:
    """Servicio para gestión de experimentos de ML.
    
    Este servicio encapsula toda la lógica relacionada con la creación,
    ejecución y análisis de experimentos de machine learning.
    
    Attributes:
        storage: Gestor de almacenamiento de experimentos.
        validator: Servicio de validación de configuraciones.
    """
    
    def create_experiment(self, config: Dict[str, Any]) -> str:
        """Crea un nuevo experimento de ML.
        
        Args:
            config: Configuración del experimento incluyendo arquitectura,
                   parámetros de entrenamiento y configuración del dataset.
                   
        Returns:
            ID único del experimento creado.
            
        Raises:
            ValidationError: Si la configuración no es válida.
            StorageError: Si hay problemas al guardar el experimento.
            
        Example:
            >>> service = ExperimentService()
            >>> config = {'name': 'test', 'epochs': 100}
            >>> experiment_id = service.create_experiment(config)
        """
```

#### Comentarios en Código
```python
# ✅ CORRECTO: Comentarios explicativos cuando sea necesario
def train_model(self, config: TrainingConfig) -> TrainingResult:
    """Entrena el modelo con la configuración especificada."""
    
    # Validar configuración antes del entrenamiento
    validation_result = self.validator.validate_config(config)
    if not validation_result.is_valid:
        raise ValidationError(validation_result.errors)
    
    # Construir modelo con arquitectura especificada
    model = self.model_builder.build_model(config.architecture)
    
    # Configurar callbacks para monitoreo avanzado
    callbacks = self._setup_training_callbacks(config)
    
    return self._execute_training(model, config, callbacks)
```

### Type Hints y Validación

#### Type Hints Obligatorios
```python
# ✅ CORRECTO: Type hints en todas las funciones públicas
from typing import Dict, List, Optional, Union, Tuple, Any
from pathlib import Path

def process_training_data(
    data_path: Path,
    batch_size: int = 32,
    validation_split: float = 0.2
) -> Tuple[np.ndarray, np.ndarray]:
    """Procesa datos de entrenamiento."""
    pass

class TrainingParams(BaseModel):
    """Parámetros de entrenamiento validados con Pydantic."""
    epochs: int = Field(gt=0, le=1000)
    learning_rate: float = Field(gt=0.0, le=1.0)
    batch_size: int = Field(gt=1, le=512)
    early_stopping: bool = True
```

### Manejo de Errores

#### Excepciones Específicas
```python
# ✅ CORRECTO: Excepciones específicas y manejo robusto
class TrainingError(Exception):
    """Excepción base para errores de entrenamiento."""
    pass

class ModelValidationError(TrainingError):
    """Error en validación de modelo."""
    pass

def validate_model_architecture(architecture: Dict[str, Any]) -> None:
    """Valida la arquitectura del modelo."""
    try:
        required_fields = ['layers', 'activation']
        for field in required_fields:
            if field not in architecture:
                raise ModelValidationError(f"Campo requerido '{field}' no encontrado")
                
        if not isinstance(architecture['layers'], list):
            raise ModelValidationError("'layers' debe ser una lista")
            
    except KeyError as e:
        logger.error(f"Error de configuración: {e}")
        raise ModelValidationError(f"Configuración inválida: {e}")
    except Exception as e:
        logger.error(f"Error inesperado en validación: {e}")
        raise
```

### Logging y Monitoreo

#### Configuración de Logging
```python
# ✅ CORRECTO: Logging estructurado y consistente
import logging
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TrainingService:
    """Servicio de entrenamiento con logging completo."""
    
    def __init__(self):
        self.logger = logger
        
    def start_training(self, config: TrainingConfig) -> str:
        """Inicia el entrenamiento del modelo."""
        self.logger.info(f"Iniciando entrenamiento con configuración: {config.name}")
        
        try:
            # Validar configuración
            self.logger.debug("Validando configuración de entrenamiento")
            validation_result = self._validate_config(config)
            
            if not validation_result.is_valid:
                self.logger.error(f"Configuración inválida: {validation_result.errors}")
                raise ValidationError("Configuración de entrenamiento inválida")
                
            # Ejecutar entrenamiento
            self.logger.info("Configuración válida, iniciando entrenamiento")
            training_id = self._execute_training(config)
            
            self.logger.info(f"Entrenamiento iniciado exitosamente: {training_id}")
            return training_id
            
        except Exception as e:
            self.logger.error(f"Error al iniciar entrenamiento: {e}", exc_info=True)
            raise
```

### Testing

#### Estructura de Tests
```python
# ✅ CORRECTO: Tests completos y organizados
import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
from pathlib import Path

from src.services.training_service import TrainingService
from src.schemas.model_schemas import TrainingConfig, ValidationResult

class TestTrainingService:
    """Tests para TrainingService."""
    
    @pytest.fixture
    def mock_validator(self):
        """Mock del validador de modelos."""
        validator = Mock()
        validator.validate_config.return_value = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[]
        )
        return validator
    
    @pytest.fixture
    def training_service(self, mock_validator):
        """Fixture del servicio de entrenamiento."""
        return TrainingService(validator=mock_validator)
    
    @pytest.fixture
    def sample_config(self):
        """Configuración de muestra para tests."""
        return TrainingConfig(
            name="test_training",
            epochs=10,
            learning_rate=0.001,
            batch_size=32
        )
    
    def test_start_training_success(self, training_service, sample_config):
        """Test de entrenamiento exitoso."""
        # Arrange
        expected_training_id = "training_123"
        
        # Act
        with patch.object(training_service, '_execute_training') as mock_execute:
            mock_execute.return_value = expected_training_id
            result = training_service.start_training(sample_config)
        
        # Assert
        assert result == expected_training_id
        mock_execute.assert_called_once_with(sample_config)
    
    def test_start_training_invalid_config(self, training_service, sample_config):
        """Test con configuración inválida."""
        # Arrange
        training_service.validator.validate_config.return_value = ValidationResult(
            is_valid=False,
            errors=["Epochs debe ser mayor a 0"],
            warnings=[]
        )
        
        # Act & Assert
        with pytest.raises(ValidationError):
            training_service.start_training(sample_config)
```

### Performance y Optimización

#### Código Eficiente
```python
# ✅ CORRECTO: Código optimizado y eficiente
import numpy as np
from typing import Generator
from functools import lru_cache

class DataProcessor:
    """Procesador de datos optimizado."""
    
    @lru_cache(maxsize=128)
    def get_cached_model_config(self, model_type: str) -> Dict[str, Any]:
        """Obtiene configuración de modelo con cache."""
        return self._load_model_config(model_type)
    
    def process_batch_data(self, data: np.ndarray, batch_size: int = 32) -> Generator[np.ndarray, None, None]:
        """Procesa datos en lotes para eficiencia de memoria."""
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]
    
    def calculate_metrics_vectorized(self, predictions: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Calcula métricas usando operaciones vectorizadas."""
        # Usar operaciones NumPy vectorizadas para mejor performance
        mse = np.mean((predictions - targets) ** 2)
        mae = np.mean(np.abs(predictions - targets))
        
        return {
            'mse': float(mse),
            'mae': float(mae),
            'rmse': float(np.sqrt(mse))
        }
```

### Seguridad

#### Validación de Entrada
```python
# ✅ CORRECTO: Validación robusta de entrada
from pydantic import BaseModel, Field, validator
import os
from pathlib import Path

class SecureTrainingConfig(BaseModel):
    """Configuración de entrenamiento con validación de seguridad."""
    
    model_name: str = Field(..., regex=r'^[a-zA-Z0-9_-]+$', max_length=100)
    data_path: Path = Field(...)
    epochs: int = Field(gt=0, le=1000)
    
    @validator('data_path')
    def validate_data_path(cls, v):
        """Valida que el path de datos sea seguro."""
        # Prevenir path traversal
        if '..' in str(v) or str(v).startswith('/'):
            raise ValueError("Path de datos no seguro")
        
        # Verificar que existe y es accesible
        if not v.exists():
            raise ValueError(f"Path de datos no existe: {v}")
            
        return v
    
    @validator('model_name')
    def validate_model_name(cls, v):
        """Valida el nombre del modelo."""
        # Prevenir nombres maliciosos
        forbidden_names = ['system', 'admin', 'root']
        if v.lower() in forbidden_names:
            raise ValueError(f"Nombre de modelo no permitido: {v}")
            
        return v

# Nunca exponer información sensible en logs
def safe_log_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Crea versión segura de configuración para logging."""
    safe_config = config.copy()
    
    # Remover información sensible
    sensitive_keys = ['api_key', 'password', 'token', 'secret']
    for key in sensitive_keys:
        if key in safe_config:
            safe_config[key] = '***REDACTED***'
    
    return safe_config
```

## 🚫 Anti-patrones a Evitar

### ❌ INCORRECTO
```python
# Nombres no descriptivos
def f(x, y):
    return x + y

# Sin type hints
def process_data(data):
    pass

# Funciones muy largas (>50 líneas)
def giant_function():
    # ... 100+ líneas de código

# Imports desordenados
from flask import Flask
import os
from src.services import TrainingService
import sys

# Sin manejo de errores
def risky_operation():
    result = some_operation()  # Puede fallar
    return result.value  # Sin verificar si result existe

# Hardcoded values
model = create_model(layers=[64, 32, 1], lr=0.001)  # ❌

# Sin logging
def important_operation():
    # Operación crítica sin logging
    pass
```

### ✅ CORRECTO
```python
# Nombres descriptivos
def calculate_model_accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
    return np.mean(predictions == targets)

# Con type hints
def process_training_data(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    pass

# Funciones pequeñas y enfocadas
def validate_model_config(config: Dict[str, Any]) -> ValidationResult:
    """Valida configuración de modelo (una sola responsabilidad)."""
    pass

# Imports ordenados
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask

from config import Config
from src.services import TrainingService

# Manejo robusto de errores
def safe_operation() -> Optional[ModelResult]:
    try:
        result = some_operation()
        if result is None:
            logger.warning("Operación retornó None")
            return None
        return result.value
    except Exception as e:
        logger.error(f"Error en operación: {e}")
        return None

# Configuración centralizada
model = create_model(
    layers=Config.DEFAULT_LAYERS,
    learning_rate=Config.DEFAULT_LEARNING_RATE
)

# Con logging apropiado
def important_operation() -> bool:
    logger.info("Iniciando operación crítica")
    try:
        # ... lógica de operación
        logger.info("Operación completada exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error en operación crítica: {e}")
        return False
```

---

## ⚛️ Reglas para TypeScript y React 19 (Frontend)

### Principios Fundamentales
- **TypeScript Strict Mode**: Configuración estricta habilitada
- **React 19 Features**: Uso de Server Components y nuevas APIs
- **Clean Architecture**: Separación clara de responsabilidades
- **Performance First**: Optimización desde el diseño
- **Accessibility**: WCAG 2.1 AA compliance

### Estructura y Organización

#### Estructura de Archivos
```typescript
// ✅ CORRECTO: Estructura modular clara
frontend/
├── src/
│   ├── components/        # Componentes reutilizables
│   │   ├── ui/           # Componentes base (Button, Input, etc.)
│   │   └── features/     # Componentes específicos de funcionalidad
│   ├── pages/            # Páginas/rutas principales
│   ├── hooks/            # Custom hooks
│   ├── services/         # Servicios API y lógica de negocio
│   ├── store/            # Estado global (Zustand)
│   ├── types/            # Definiciones de tipos TypeScript
│   ├── utils/            # Utilidades y helpers
│   └── styles/           # Estilos globales y temas
├── public/               # Assets estáticos
└── tests/                # Tests unitarios e integración
```

#### Imports y Dependencias
```typescript
// ✅ CORRECTO: Orden de imports optimizado
import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';

import { Button } from '@/components/ui/Button';
import { TrainingService } from '@/services/training';
import { useTrainingStore } from '@/store/trainingStore';
import { TrainingConfig, ModelMetrics } from '@/types/training';

import type { FC, ReactNode } from 'react';
```

### Convenciones de Nomenclatura

#### Componentes
```typescript
// ✅ CORRECTO: PascalCase para componentes
interface TrainingDashboardProps {
  initialConfig?: TrainingConfig;
  onConfigChange?: (config: TrainingConfig) => void;
}

const TrainingDashboard: FC<TrainingDashboardProps> = ({ 
  initialConfig, 
  onConfigChange 
}) => {
  // Implementación del componente
};

export default TrainingDashboard;
```

#### Hooks Personalizados
```typescript
// ✅ CORRECTO: Prefijo 'use' para hooks
interface UseTrainingReturn {
  isTraining: boolean;
  metrics: ModelMetrics | null;
  startTraining: (config: TrainingConfig) => Promise<void>;
  stopTraining: () => Promise<void>;
  error: string | null;
}

const useTraining = (): UseTrainingReturn => {
  const [isTraining, setIsTraining] = useState(false);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startTraining = useCallback(async (config: TrainingConfig) => {
    try {
      setIsTraining(true);
      setError(null);
      
      const result = await TrainingService.startTraining(config);
      setMetrics(result.metrics);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsTraining(false);
    }
  }, []);

  return { isTraining, metrics, startTraining, stopTraining, error };
};
```

#### Variables y Funciones
```typescript
// ✅ CORRECTO: camelCase para variables y funciones
const trainingConfig: TrainingConfig = {
  modelName: 'neural_network_v1',
  epochs: 100,
  learningRate: 0.001,
  batchSize: 32
};

const calculateTrainingProgress = (currentEpoch: number, totalEpochs: number): number => {
  return Math.round((currentEpoch / totalEpochs) * 100);
};
```

### TypeScript y Tipado

#### Definición de Tipos
```typescript
// ✅ CORRECTO: Tipos bien definidos y documentados
/**
 * Configuración completa para entrenamiento de modelos ML
 */
interface TrainingConfig {
  /** Nombre único del modelo */
  modelName: string;
  /** Arquitectura de la red neuronal */
  architecture: {
    layers: number[];
    activation: 'relu' | 'sigmoid' | 'tanh';
    dropoutRate?: number;
  };
  /** Parámetros de entrenamiento */
  trainingParams: {
    epochs: number;
    learningRate: number;
    batchSize: number;
    validationSplit: number;
  };
  /** Configuración del dataset */
  datasetConfig?: {
    size: number;
    features: string[];
    target: string;
  };
}

// Union types para estados específicos
type TrainingStatus = 'idle' | 'preparing' | 'training' | 'completed' | 'error';

// Utility types para flexibilidad
type PartialTrainingConfig = Partial<TrainingConfig>;
type RequiredTrainingParams = Required<Pick<TrainingConfig, 'modelName' | 'architecture'>>;
```

#### Generics y Tipos Avanzados
```typescript
// ✅ CORRECTO: Uso de generics para reutilización
interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
  message?: string;
  timestamp: string;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    hasNext: boolean;
  };
}

// Hook genérico para API calls
const useApiCall = <T, P = void>(
  apiFunction: (params: P) => Promise<ApiResponse<T>>
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (params: P) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiFunction(params);
      
      if (response.status === 'success') {
        setData(response.data);
      } else {
        setError(response.message || 'Error en la API');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  }, [apiFunction]);

  return { data, loading, error, execute };
};
```

### React 19 - Server Components y Client Components

#### Server Components
```typescript
// ✅ CORRECTO: Server Component para data fetching
// No necesita "use client" - se ejecuta en el servidor
interface TrainingHistoryPageProps {
  searchParams: { page?: string; limit?: string };
}

const TrainingHistoryPage = async ({ searchParams }: TrainingHistoryPageProps) => {
  // Data fetching en el servidor
  const page = Number(searchParams.page) || 1;
  const limit = Number(searchParams.limit) || 10;
  
  const trainingHistory = await TrainingService.getHistory({ page, limit });
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Historial de Entrenamientos</h1>
      
      {/* Server Component puede renderizar Client Components */}
      <TrainingHistoryList 
        initialData={trainingHistory.data}
        pagination={trainingHistory.pagination}
      />
    </div>
  );
};

export default TrainingHistoryPage;
```

#### Client Components
```typescript
// ✅ CORRECTO: Client Component para interactividad
'use client';

import { useState, useEffect } from 'react';
import { useTrainingStore } from '@/store/trainingStore';

interface TrainingControlPanelProps {
  initialConfig: TrainingConfig;
}

const TrainingControlPanel: FC<TrainingControlPanelProps> = ({ initialConfig }) => {
  const [config, setConfig] = useState(initialConfig);
  const { startTraining, stopTraining, isTraining } = useTrainingStore();
  
  // Client-side effects y event handlers
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isTraining) {
        stopTraining();
      }
    };
    
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isTraining, stopTraining]);
  
  const handleStartTraining = async () => {
    try {
      await startTraining(config);
    } catch (error) {
      console.error('Error al iniciar entrenamiento:', error);
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Panel de Control</h2>
      
      <ConfigurationForm 
        config={config}
        onChange={setConfig}
        disabled={isTraining}
      />
      
      <div className="flex gap-4 mt-6">
        <Button
          onClick={handleStartTraining}
          disabled={isTraining}
          className="bg-blue-600 hover:bg-blue-700"
        >
          {isTraining ? 'Entrenando...' : 'Iniciar Entrenamiento'}
        </Button>
        
        {isTraining && (
          <Button
            onClick={stopTraining}
            variant="outline"
            className="border-red-500 text-red-500 hover:bg-red-50"
          >
            Detener
          </Button>
        )}
      </div>
    </div>
  );
};

export default TrainingControlPanel;
```

#### Server Actions
```typescript
// ✅ CORRECTO: Server Actions para mutations
'use server';

import { revalidatePath } from 'next/cache';
import { TrainingService } from '@/services/training';
import { TrainingConfig } from '@/types/training';

export async function createTrainingSession(
  formData: FormData
): Promise<{ success: boolean; error?: string; sessionId?: string }> {
  try {
    // Validar y parsear datos del formulario
    const config: TrainingConfig = {
      modelName: formData.get('modelName') as string,
      architecture: JSON.parse(formData.get('architecture') as string),
      trainingParams: JSON.parse(formData.get('trainingParams') as string),
    };
    
    // Validación del lado del servidor
    if (!config.modelName || config.modelName.length < 3) {
      return { success: false, error: 'Nombre del modelo debe tener al menos 3 caracteres' };
    }
    
    // Crear sesión de entrenamiento
    const session = await TrainingService.createSession(config);
    
    // Revalidar cache de la página
    revalidatePath('/training');
    
    return { success: true, sessionId: session.id };
  } catch (error) {
    console.error('Error creando sesión de entrenamiento:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Error desconocido' 
    };
  }
}
```

### Estado Global con Zustand

#### Store Configuration
```typescript
// ✅ CORRECTO: Store bien estructurado con Zustand
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface TrainingState {
  // Estado
  sessions: TrainingSession[];
  currentSession: TrainingSession | null;
  isLoading: boolean;
  error: string | null;
  
  // Acciones
  setSessions: (sessions: TrainingSession[]) => void;
  addSession: (session: TrainingSession) => void;
  updateSession: (id: string, updates: Partial<TrainingSession>) => void;
  removeSession: (id: string) => void;
  setCurrentSession: (session: TrainingSession | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Acciones async
  fetchSessions: () => Promise<void>;
  createSession: (config: TrainingConfig) => Promise<TrainingSession>;
}

export const useTrainingStore = create<TrainingState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Estado inicial
        sessions: [],
        currentSession: null,
        isLoading: false,
        error: null,
        
        // Acciones síncronas
        setSessions: (sessions) => set({ sessions }),
        
        addSession: (session) => set((state) => {
          state.sessions.push(session);
        }),
        
        updateSession: (id, updates) => set((state) => {
          const index = state.sessions.findIndex(s => s.id === id);
          if (index !== -1) {
            Object.assign(state.sessions[index], updates);
          }
        }),
        
        removeSession: (id) => set((state) => {
          state.sessions = state.sessions.filter(s => s.id !== id);
        }),
        
        setCurrentSession: (session) => set({ currentSession: session }),
        setLoading: (loading) => set({ isLoading: loading }),
        setError: (error) => set({ error }),
        
        // Acciones asíncronas
        fetchSessions: async () => {
          try {
            set({ isLoading: true, error: null });
            const response = await TrainingService.getSessions();
            set({ sessions: response.data, isLoading: false });
          } catch (error) {
            set({ 
              error: error instanceof Error ? error.message : 'Error desconocido',
              isLoading: false 
            });
          }
        },
        
        createSession: async (config) => {
          try {
            set({ isLoading: true, error: null });
            const session = await TrainingService.createSession(config);
            
            set((state) => {
              state.sessions.push(session);
              state.currentSession = session;
              state.isLoading = false;
            });
            
            return session;
          } catch (error) {
            set({ 
              error: error instanceof Error ? error.message : 'Error creando sesión',
              isLoading: false 
            });
            throw error;
          }
        },
      })),
      {
        name: 'training-store',
        partialize: (state) => ({ 
          sessions: state.sessions,
          currentSession: state.currentSession 
        }),
      }
    ),
    { name: 'TrainingStore' }
  )
);
```

### Tailwind CSS v4 y Estilos

#### Configuración de Tailwind v4
```typescript
// ✅ CORRECTO: Uso de Tailwind v4 con CSS-in-JS cuando sea necesario
import { cn } from '@/utils/cn'; // Utility para combinar clases

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button: FC<ButtonProps> = ({ 
  className, 
  variant = 'primary', 
  size = 'md',
  isLoading = false,
  children,
  disabled,
  ...props 
}) => {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        
        // Variant styles
        {
          'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500': 
            variant === 'primary',
          'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500': 
            variant === 'secondary',
          'border border-gray-300 bg-transparent hover:bg-gray-50 focus-visible:ring-gray-500': 
            variant === 'outline',
          'hover:bg-gray-100 focus-visible:ring-gray-500': 
            variant === 'ghost',
        },
        
        // Size styles
        {
          'h-8 px-3 text-sm': size === 'sm',
          'h-10 px-4 text-base': size === 'md',
          'h-12 px-6 text-lg': size === 'lg',
        },
        
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg 
          className="mr-2 h-4 w-4 animate-spin" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  );
};

export default Button;
```

### Performance y Optimización

#### Memoización y Optimización
```typescript
// ✅ CORRECTO: Uso apropiado de React.memo y hooks de optimización
import { memo, useMemo, useCallback } from 'react';

interface TrainingMetricsChartProps {
  metrics: ModelMetrics[];
  timeRange: TimeRange;
  onTimeRangeChange: (range: TimeRange) => void;
}

const TrainingMetricsChart = memo<TrainingMetricsChartProps>(({ 
  metrics, 
  timeRange, 
  onTimeRangeChange 
}) => {
  // Memoizar cálculos costosos
  const chartData = useMemo(() => {
    return metrics
      .filter(metric => isWithinTimeRange(metric.timestamp, timeRange))
      .map(metric => ({
        x: metric.timestamp,
        accuracy: metric.accuracy,
        loss: metric.loss,
      }));
  }, [metrics, timeRange]);
  
  // Memoizar callbacks para evitar re-renders
  const handleTimeRangeChange = useCallback((newRange: TimeRange) => {
    onTimeRangeChange(newRange);
  }, [onTimeRangeChange]);
  
  // Early return si no hay datos
  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        No hay datos de métricas disponibles
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Métricas de Entrenamiento</h3>
        <TimeRangeSelector 
          value={timeRange}
          onChange={handleTimeRangeChange}
        />
      </div>
      
      <ResponsiveChart data={chartData} />
    </div>
  );
});

TrainingMetricsChart.displayName = 'TrainingMetricsChart';

export default TrainingMetricsChart;
```

#### Lazy Loading y Code Splitting
```typescript
// ✅ CORRECTO: Lazy loading de componentes pesados
import { lazy, Suspense } from 'react';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

// Lazy load de componentes pesados
const TrainingVisualization = lazy(() => import('@/components/TrainingVisualization'));
const ModelArchitectureEditor = lazy(() => import('@/components/ModelArchitectureEditor'));

const TrainingDashboard: FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'visualization' | 'editor'>('overview');
  
  return (
    <div className="container mx-auto px-4 py-8">
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
      
      <div className="mt-6">
        {activeTab === 'overview' && <TrainingOverview />}
        
        {activeTab === 'visualization' && (
          <ErrorBoundary fallback={<div>Error cargando visualización</div>}>
            <Suspense fallback={<LoadingSpinner />}>
              <TrainingVisualization />
            </Suspense>
          </ErrorBoundary>
        )}
        
        {activeTab === 'editor' && (
          <ErrorBoundary fallback={<div>Error cargando editor</div>}>
            <Suspense fallback={<LoadingSpinner />}>
              <ModelArchitectureEditor />
            </Suspense>
          </ErrorBoundary>
        )}
      </div>
    </div>
  );
};
```

### Testing

#### Testing con Vitest y React Testing Library
```typescript
// ✅ CORRECTO: Tests completos y bien estructurados
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TrainingControlPanel } from '@/components/TrainingControlPanel';
import { useTrainingStore } from '@/store/trainingStore';

// Mock del store
vi.mock('@/store/trainingStore');

const mockUseTrainingStore = vi.mocked(useTrainingStore);

describe('TrainingControlPanel', () => {
  const mockStartTraining = vi.fn();
  const mockStopTraining = vi.fn();
  
  const defaultStoreState = {
    isTraining: false,
    startTraining: mockStartTraining,
    stopTraining: mockStopTraining,
    error: null,
  };
  
  beforeEach(() => {
    vi.clearAllMocks();
    mockUseTrainingStore.mockReturnValue(defaultStoreState);
  });
  
  const defaultProps = {
    initialConfig: {
      modelName: 'test-model',
      architecture: { layers: [64, 32, 1], activation: 'relu' as const },
      trainingParams: {
        epochs: 100,
        learningRate: 0.001,
        batchSize: 32,
        validationSplit: 0.2,
      },
    },
  };
  
  it('renderiza correctamente el estado inicial', () => {
    render(<TrainingControlPanel {...defaultProps} />);
    
    expect(screen.getByText('Panel de Control')).toBeInTheDocument();
    expect(screen.getByText('Iniciar Entrenamiento')).toBeInTheDocument();
    expect(screen.queryByText('Detener')).not.toBeInTheDocument();
  });
  
  it('inicia el entrenamiento cuando se hace clic en el botón', async () => {
    const user = userEvent.setup();
    render(<TrainingControlPanel {...defaultProps} />);
    
    const startButton = screen.getByText('Iniciar Entrenamiento');
    await user.click(startButton);
    
    expect(mockStartTraining).toHaveBeenCalledWith(defaultProps.initialConfig);
  });
  
  it('muestra el botón de detener cuando está entrenando', () => {
    mockUseTrainingStore.mockReturnValue({
      ...defaultStoreState,
      isTraining: true,
    });
    
    render(<TrainingControlPanel {...defaultProps} />);
    
    expect(screen.getByText('Entrenando...')).toBeInTheDocument();
    expect(screen.getByText('Detener')).toBeInTheDocument();
  });
  
  it('maneja errores de entrenamiento correctamente', async () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    mockStartTraining.mockRejectedValue(new Error('Error de entrenamiento'));
    
    const user = userEvent.setup();
    render(<TrainingControlPanel {...defaultProps} />);
    
    const startButton = screen.getByText('Iniciar Entrenamiento');
    await user.click(startButton);
    
    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error al iniciar entrenamiento:',
        expect.any(Error)
      );
    });
    
    consoleErrorSpy.mockRestore();
  });
  
  it('detiene el entrenamiento con la tecla Escape', async () => {
    mockUseTrainingStore.mockReturnValue({
      ...defaultStoreState,
      isTraining: true,
    });
    
    render(<TrainingControlPanel {...defaultProps} />);
    
    fireEvent.keyDown(window, { key: 'Escape' });
    
    expect(mockStopTraining).toHaveBeenCalled();
  });
});
```

### Accesibilidad

#### Implementación de WCAG 2.1
```typescript
// ✅ CORRECTO: Componente accesible
interface ProgressBarProps {
  value: number;
  max: number;
  label: string;
  description?: string;
}

const ProgressBar: FC<ProgressBarProps> = ({ value, max, label, description }) => {
  const percentage = Math.round((value / max) * 100);
  
  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <label 
          id={`progress-label-${label}`}
          className="text-sm font-medium text-gray-700"
        >
          {label}
        </label>
        <span 
          className="text-sm text-gray-500"
          aria-label={`${percentage} por ciento completado`}
        >
          {percentage}%
        </span>
      </div>
      
      <div 
        className="w-full bg-gray-200 rounded-full h-2"
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-labelledby={`progress-label-${label}`}
        aria-describedby={description ? `progress-desc-${label}` : undefined}
      >
        <div 
          className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
      
      {description && (
        <p 
          id={`progress-desc-${label}`}
          className="text-xs text-gray-500 mt-1"
        >
          {description}
        </p>
      )}
    </div>
  );
};
```

## 🚫 Anti-patrones a Evitar en Frontend

### ❌ INCORRECTO
```typescript
// Componente sin tipos
const BadComponent = ({ data, onClick }) => {
  return <div onClick={onClick}>{data}</div>;
};

// Mutación directa del estado
const [state, setState] = useState({ items: [] });
state.items.push(newItem); // ❌ Mutación directa

// Efectos sin dependencias correctas
useEffect(() => {
  fetchData(userId);
}, []); // ❌ Falta userId en dependencias

// Props drilling excesivo
<ComponentA>
  <ComponentB data={data} onUpdate={onUpdate}>
    <ComponentC data={data} onUpdate={onUpdate}>
      <ComponentD data={data} onUpdate={onUpdate} />
    </ComponentC>
  </ComponentB>
</ComponentA>

// Inline styles en lugar de Tailwind
<div style={{ backgroundColor: 'blue', padding: '16px' }}>
  Content
</div>
```

### ✅ CORRECTO
```typescript
// Componente con tipos completos
interface GoodComponentProps {
  data: string;
  onClick: () => void;
}

const GoodComponent: FC<GoodComponentProps> = ({ data, onClick }) => {
  return (
    <button 
      onClick={onClick}
      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
    >
      {data}
    </button>
  );
};

// Actualización inmutable del estado
const [state, setState] = useState({ items: [] });
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));

// Efectos con dependencias correctas
useEffect(() => {
  fetchData(userId);
}, [userId]);

// Uso de contexto/store para evitar props drilling
const { data, onUpdate } = useTrainingStore();
<ComponentA>
  <ComponentB>
    <ComponentC>
      <ComponentD />
    </ComponentC>
  </ComponentB>
</ComponentA>

// Uso de Tailwind CSS
<div className="bg-blue-500 p-4 rounded-lg shadow-md">
  Content
</div>
```