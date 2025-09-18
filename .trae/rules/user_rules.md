# 🤖 Reglas Personalizadas para IA - Sistema de Entrenamiento ML

## 📋 Contexto del Proyecto

Este proyecto es un **sistema de entrenamiento de modelos de Machine Learning** que combina:
- **Backend Python**: API REST con FastAPI, manejo de datasets, entrenamiento de modelos
- **Frontend React 19**: Dashboard interactivo para configuración y monitoreo
- **Integración ML**: PyTorch, scikit-learn, visualización de métricas

## 🎯 Instrucciones Específicas para la IA

### Comportamiento General
1. **Siempre responde en español** - El usuario prefiere comunicación en español
2. **Enfoque en Data Science** - Prioriza soluciones orientadas a ML y análisis de datos
3. **Clean Code obligatorio** - Aplica principios de código limpio en cada implementación
4. **Documentación clara** - Incluye docstrings y comentarios explicativos
5. **Seguridad primero** - Nunca expongas credenciales o información sensible

### Stack Tecnológico Preferido

#### Python (Backend/ML)
- **Framework**: Flask para APIs REST (configurado actualmente)
- **Entorno**: Miniconda3 con entorno `neural-trainer` (Python 3.9)
- **ML Libraries**: TensorFlow (principal), scikit-learn, pandas, numpy
- **Visualización**: matplotlib, plotly, seaborn
- **Testing**: pytest con coverage mínimo del 80%
- **Formato**: black + isort + flake8 + mypy

#### TypeScript/React (Frontend)
- **Framework**: React 19 con Server Components
- **Estado**: Zustand para estado global
- **Estilos**: Tailwind CSS v4 (estricto)
- **Testing**: Vitest + React Testing Library
- **Tipos**: TypeScript estricto con configuración completa

### Patrones de Implementación

#### Para Funcionalidades ML
```python
# ✅ SIEMPRE incluir este patrón para ML
from typing import Dict, List, Optional, Tuple
import logging
import numpy as np
import tensorflow as tf

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Entrenador de modelos con logging y manejo de errores."""
    
    def __init__(self, config: TrainingConfig) -> None:
        self.config = config
        self.model: Optional[tf.keras.Model] = None
        self.metrics: Dict[str, float] = {}
    
    def train(self, data: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        """Entrena el modelo y retorna métricas."""
        try:
            logger.info(f"Iniciando entrenamiento con {len(data)} muestras")
            # Implementación del entrenamiento
            return self.metrics
        except Exception as e:
            logger.error(f"Error en entrenamiento: {e}")
            raise
```

#### Para Componentes React
```typescript
// ✅ SIEMPRE incluir este patrón para React
'use client'; // Solo si necesita interactividad

import { useState, useCallback } from 'react';
import { useTrainingStore } from '@/store/trainingStore';
import type { FC } from 'react';

interface ComponentProps {
  data: TrainingData;
  onUpdate: (data: TrainingData) => void;
}

const TrainingComponent: FC<ComponentProps> = ({ data, onUpdate }) => {
  // Implementación con tipos estrictos
};

export default TrainingComponent;
```

### Reglas de Implementación Específicas

#### 🔬 Para Análisis de Datos
1. **Siempre valida los datos** antes de procesarlos
2. **Incluye visualizaciones** para insights importantes
3. **Maneja valores faltantes** explícitamente
4. **Documenta las transformaciones** aplicadas a los datos
5. **Guarda checkpoints** en entrenamientos largos

#### ⚛️ Para Interfaces de Usuario
1. **Componentes accesibles** (WCAG 2.1 AA)
2. **Estados de carga** para operaciones ML
3. **Manejo de errores** con mensajes claros
4. **Responsive design** mobile-first
5. **Optimización de performance** con memoización

#### 🔧 Para APIs y Servicios
1. **Validación de entrada** con Pydantic
2. **Respuestas consistentes** con formato estándar
3. **Logging estructurado** para debugging
4. **Rate limiting** para endpoints costosos
5. **Documentación automática** con OpenAPI

### Flujo de Trabajo Recomendado

#### Al Crear Nuevas Funcionalidades
1. **Analiza el contexto** - Revisa código existente para mantener consistencia
2. **Define tipos primero** - Crea interfaces/tipos antes de implementar
3. **Implementa con tests** - TDD cuando sea posible
4. **Documenta la funcionalidad** - README, docstrings, comentarios
5. **Verifica calidad** - Ejecuta linters y tests antes de finalizar

#### Al Debuggear Problemas
1. **Revisa logs primero** - Busca errores en logs del sistema
2. **Reproduce el error** - Crea caso de prueba mínimo
3. **Verifica tipos** - Confirma que los tipos coinciden
4. **Valida datos** - Asegúrate que los datos son correctos
5. **Propón solución robusta** - No solo fixes temporales

### Comandos Útiles del Proyecto

#### Backend
```bash
# Desarrollo (usando Miniconda3)
cd backend
# Activar entorno neural-trainer
call activate_env.bat
python server.py

# Testing
pytest --cov=app --cov-report=html

# Linting
black . && isort . && flake8 . && mypy .
```

#### Frontend
```bash
# Desarrollo
cd frontend
npm run dev

# Testing
npm run test
npm run test:coverage

# Linting
npm run lint
npm run type-check
```

### Mensajes de Error Comunes

#### Python/ML
- **"CUDA out of memory"** → Reducir batch_size o usar gradient checkpointing
- **"Module not found"** → Verificar PYTHONPATH y virtual environment
- **"Shape mismatch"** → Validar dimensiones de tensores/arrays

#### TypeScript/React
- **"Property does not exist"** → Verificar tipos e interfaces
- **"Hook called conditionally"** → Mover hooks al top level
- **"Hydration mismatch"** → Verificar SSR vs client rendering

### Optimizaciones Específicas

#### Para Modelos ML
- Usar `tf.keras.utils.model_to_dot` para visualizar arquitecturas
- Implementar early stopping para evitar overfitting
- Cachear datasets procesados con `joblib` o `pickle`
- Usar `tf.data.Dataset` para batching eficiente y pipelines de datos

#### Para Frontend
- Lazy loading de componentes pesados
- Memoización con `React.memo` y `useMemo`
- Virtualización para listas largas
- Code splitting por rutas

## 🚨 Recordatorios Importantes

1. **Nunca hardcodees credenciales** - Usa variables de entorno
2. **Siempre valida inputs** - Tanto en frontend como backend
3. **Maneja errores gracefully** - UX no debe romperse por errores
4. **Optimiza para producción** - Considera performance desde el diseño
5. **Mantén consistencia** - Sigue los patrones establecidos en el proyecto

## 📚 Recursos de Referencia

- **Python**: [PEP 8](https://pep8.org/), [Clean Code Python](https://github.com/zedr/clean-code-python)
- **TypeScript**: [Handbook](https://www.typescriptlang.org/docs/), [React 19 Docs](https://react.dev/)
- **ML**: [TensorFlow Docs](https://www.tensorflow.org/guide), [Scikit-learn Guide](https://scikit-learn.org/stable/), [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Testing**: [pytest](https://docs.pytest.org/), [Vitest](https://vitest.dev/)

---

*Estas reglas están diseñadas para mantener la consistencia y calidad del código en el proyecto de entrenamiento ML. Actualiza este documento según evolucionen las necesidades del proyecto.*