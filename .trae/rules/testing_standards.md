# Estándares de Testing - Neural Network Trainer

## ESTRUCTURA DE TESTING OBLIGATORIA

### Backend (Python)
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Configuración pytest
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── test_training_service.py
│   │   │   ├── test_model_builder.py
│   │   │   └── test_metrics_service.py
│   │   ├── routes/
│   │   │   ├── test_api_routes.py
│   │   │   └── test_websocket_routes.py
│   │   └── utils/
│   │       ├── test_logger.py
│   │       └── test_validators.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_training_flow.py
│   │   ├── test_api_integration.py
│   │   └── test_websocket_integration.py
│   └── e2e/
│       ├── __init__.py
│       └── test_complete_training.py
└── pytest.ini                        # Configuración pytest
```

### Frontend (TypeScript)
```
frontend/src/
├── components/
│   ├── training/
│   │   ├── TrainingForm.tsx
│   │   └── __tests__/
│   │       └── TrainingForm.test.tsx
│   └── common/
│       ├── Button.tsx
│       └── __tests__/
│           └── Button.test.tsx
├── hooks/
│   ├── useTraining.ts
│   └── __tests__/
│       └── useTraining.test.ts
├── services/
│   ├── trainingService.ts
│   └── __tests__/
│       └── trainingService.test.ts
└── stores/
    ├── trainingStore.ts
    └── __tests__/
        └── trainingStore.test.ts
```

## CONFIGURACIÓN DE TESTING

### Backend - pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
```

### Backend - conftest.py
```python
"""Configuración global para tests."""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from src.config import Config
from src.services.training.model_builder import ModelBuilder

@pytest.fixture
def test_config():
    """Configuración de prueba."""
    return Config(
        DEBUG=True,
        TESTING=True,
        DATABASE_URL='sqlite:///:memory:',
        SECRET_KEY='test-secret-key'
    )

@pytest.fixture
def mock_model():
    """Mock de modelo TensorFlow."""
    model = Mock()
    model.fit.return_value = Mock()
    model.evaluate.return_value = [0.1, 0.95]  # loss, accuracy
    model.predict.return_value = [[0.5], [1.0], [1.5]]
    model.count_params.return_value = 100
    return model

@pytest.fixture
def temp_model_file():
    """Archivo temporal para modelo."""
    with tempfile.NamedTemporaryFile(suffix='.keras', delete=False) as f:
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def sample_training_params():
    """Parámetros de entrenamiento de ejemplo."""
    return {
        'epochs': 10,
        'learningRate': 0.01,
        'batchSize': 32,
        'datasetSize': 100,
        'architecture': {
            'inputLayer': {'shape': [1]},
            'hiddenLayers': [
                {'neurons': 8, 'activation': 'relu'}
            ],
            'outputLayer': {'neurons': 1, 'activation': 'linear'}
        }
    }

@pytest.fixture
def mock_socketio():
    """Mock de SocketIO."""
    return Mock()
```

### Frontend - jest.config.js
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/main.tsx',
    '!src/vite-env.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
    '<rootDir>/src/**/*.{test,spec}.{ts,tsx}',
  ],
};
```

## PATRONES DE TESTING

### Backend - Unit Tests
```python
"""Tests unitarios para TrainingService."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.training.training_service import TrainingService
from src.services.training.exceptions import ValidationError, TrainingError

class TestTrainingService:
    """Tests para TrainingService."""
    
    def test_init_service(self, test_config):
        """Test inicialización del servicio."""
        service = TrainingService(test_config)
        
        assert service.config == test_config
        assert service.logger is not None
        assert service.model_builder is not None
    
    def test_validate_params_valid(self, test_config, sample_training_params):
        """Test validación de parámetros válidos."""
        service = TrainingService(test_config)
        
        # No debe lanzar excepción
        service._validate_params(sample_training_params)
    
    def test_validate_params_invalid_epochs(self, test_config):
        """Test validación con épocas inválidas."""
        service = TrainingService(test_config)
        params = {'epochs': 0, 'learningRate': 0.01}
        
        with pytest.raises(ValidationError, match="Epochs debe ser mayor a 0"):
            service._validate_params(params)
    
    def test_validate_params_invalid_learning_rate(self, test_config):
        """Test validación con learning rate inválido."""
        service = TrainingService(test_config)
        params = {'epochs': 10, 'learningRate': 0}
        
        with pytest.raises(ValidationError, match="Learning rate debe ser mayor a 0"):
            service._validate_params(params)
    
    @patch('src.services.training.training_service.ModelBuilder')
    def test_create_model(self, mock_model_builder, test_config, sample_training_params):
        """Test creación de modelo."""
        mock_model = Mock()
        mock_model_builder.return_value.create_model.return_value = mock_model
        
        service = TrainingService(test_config)
        result = service._create_model(sample_training_params)
        
        assert result == mock_model
        mock_model_builder.return_value.create_model.assert_called_once_with(
            learning_rate=sample_training_params['learningRate'],
            architecture=sample_training_params['architecture']
        )
    
    @patch('src.services.training.training_service.TrainingService._execute_training')
    @patch('src.services.training.training_service.TrainingService._create_model')
    def test_start_training_success(self, mock_create_model, mock_execute_training, 
                                  test_config, sample_training_params, mock_model):
        """Test entrenamiento exitoso."""
        mock_create_model.return_value = mock_model
        expected_result = {'status': 'completed', 'metrics': {'loss': 0.1}}
        mock_execute_training.return_value = expected_result
        
        service = TrainingService(test_config)
        result = service.start_training(sample_training_params)
        
        assert result == expected_result
        mock_create_model.assert_called_once_with(sample_training_params)
        mock_execute_training.assert_called_once_with(mock_model, sample_training_params)
    
    def test_start_training_validation_error(self, test_config):
        """Test entrenamiento con error de validación."""
        invalid_params = {'epochs': 0, 'learningRate': 0.01}
        
        service = TrainingService(test_config)
        
        with pytest.raises(ValidationError):
            service.start_training(invalid_params)

@pytest.mark.integration
class TestTrainingServiceIntegration:
    """Tests de integración para TrainingService."""
    
    def test_full_training_flow(self, test_config, sample_training_params):
        """Test flujo completo de entrenamiento."""
        service = TrainingService(test_config)
        
        # Este test requiere TensorFlow real
        with patch('tensorflow.keras.models.Sequential') as mock_sequential:
            mock_model = Mock()
            mock_sequential.return_value = mock_model
            mock_model.fit.return_value.history = {'loss': [0.5, 0.3, 0.1]}
            
            result = service.start_training(sample_training_params)
            
            assert result is not None
            assert 'status' in result
```

### Frontend - Component Tests
```typescript
/**
 * Tests para TrainingForm component.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TrainingForm } from '../TrainingForm';
import type { TrainingParams } from '../../types/training';

describe('TrainingForm', () => {
  const defaultProps = {
    onSubmit: jest.fn(),
    disabled: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(<TrainingForm {...defaultProps} />);
    
    expect(screen.getByLabelText(/épocas/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/tasa de aprendizaje/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /iniciar entrenamiento/i })).toBeInTheDocument();
  });

  it('displays initial values correctly', () => {
    const initialValues = {
      epochs: 50,
      learningRate: 0.001,
    };

    render(<TrainingForm {...defaultProps} initialValues={initialValues} />);
    
    expect(screen.getByDisplayValue('50')).toBeInTheDocument();
    expect(screen.getByDisplayValue('0.001')).toBeInTheDocument();
  });

  it('updates form values when user types', async () => {
    const user = userEvent.setup();
    render(<TrainingForm {...defaultProps} />);
    
    const epochsInput = screen.getByLabelText(/épocas/i);
    
    await user.clear(epochsInput);
    await user.type(epochsInput, '200');
    
    expect(epochsInput).toHaveValue(200);
  });

  it('calls onSubmit with correct params when form is submitted', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = jest.fn();
    
    render(<TrainingForm {...defaultProps} onSubmit={mockOnSubmit} />);
    
    const epochsInput = screen.getByLabelText(/épocas/i);
    const submitButton = screen.getByRole('button', { name: /iniciar entrenamiento/i });
    
    await user.clear(epochsInput);
    await user.type(epochsInput, '150');
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        epochs: 150,
        learningRate: 0.01, // valor por defecto
        batchSize: 32, // valor por defecto
      })
    );
  });

  it('prevents submission with invalid epochs', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = jest.fn();
    
    render(<TrainingForm {...defaultProps} onSubmit={mockOnSubmit} />);
    
    const epochsInput = screen.getByLabelText(/épocas/i);
    const submitButton = screen.getByRole('button', { name: /iniciar entrenamiento/i });
    
    await user.clear(epochsInput);
    await user.type(epochsInput, '0');
    await user.click(submitButton);
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('disables form when disabled prop is true', () => {
    render(<TrainingForm {...defaultProps} disabled={true} />);
    
    expect(screen.getByLabelText(/épocas/i)).toBeDisabled();
    expect(screen.getByLabelText(/tasa de aprendizaje/i)).toBeDisabled();
    expect(screen.getByRole('button', { name: /entrenando.../i })).toBeDisabled();
  });
});
```

### Frontend - Hook Tests
```typescript
/**
 * Tests para useTraining hook.
 */

import { renderHook, act } from '@testing-library/react';
import { useTraining } from '../useTraining';
import { trainingService } from '../../services/trainingService';

// Mock del servicio
jest.mock('../../services/trainingService');
const mockTrainingService = trainingService as jest.Mocked<typeof trainingService>;

// Mock del toast
jest.mock('../useToast', () => ({
  useToast: () => ({
    showToast: jest.fn(),
  }),
}));

describe('useTraining', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('initializes with correct default state', () => {
    const { result } = renderHook(() => useTraining());
    
    expect(result.current.state.isActive).toBe(false);
    expect(result.current.state.progress).toBe(0);
    expect(result.current.state.metrics).toBeNull();
    expect(result.current.state.error).toBeNull();
    expect(result.current.isTraining).toBe(false);
  });

  it('starts training successfully', async () => {
    const mockResult = {
      status: 'completed',
      metrics: { loss: 0.1, accuracy: 0.95 },
    };
    mockTrainingService.startTraining.mockResolvedValue(mockResult);

    const { result } = renderHook(() => useTraining());
    
    const params = {
      epochs: 100,
      learningRate: 0.01,
      batchSize: 32,
    };

    await act(async () => {
      await result.current.startTraining(params);
    });

    expect(mockTrainingService.startTraining).toHaveBeenCalledWith(params);
    expect(result.current.state.isActive).toBe(false);
    expect(result.current.state.metrics).toEqual(mockResult.metrics);
    expect(result.current.state.error).toBeNull();
  });

  it('handles training error correctly', async () => {
    const mockError = new Error('Training failed');
    mockTrainingService.startTraining.mockRejectedValue(mockError);

    const { result } = renderHook(() => useTraining());
    
    const params = {
      epochs: 100,
      learningRate: 0.01,
      batchSize: 32,
    };

    await act(async () => {
      await result.current.startTraining(params);
    });

    expect(result.current.state.isActive).toBe(false);
    expect(result.current.state.error).toBe('Training failed');
    expect(result.current.state.metrics).toBeNull();
  });

  it('stops training correctly', () => {
    const { result } = renderHook(() => useTraining());
    
    act(() => {
      result.current.stopTraining();
    });

    expect(mockTrainingService.stopTraining).toHaveBeenCalled();
    expect(result.current.state.isActive).toBe(false);
  });
});
```

## COMANDOS DE TESTING

### Backend
```bash
# Ejecutar todos los tests
pytest

# Tests unitarios solamente
pytest tests/unit/

# Tests con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/services/test_training_service.py

# Tests con marcadores
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Tests en paralelo
pytest -n auto

# Tests con output detallado
pytest -v -s
```

### Frontend
```bash
# Ejecutar todos los tests
npm test

# Tests en modo watch
npm run test:watch

# Tests con coverage
npm run test:coverage

# Tests específicos
npm test -- TrainingForm.test.tsx

# Tests en modo CI
npm run test:ci
```

## COVERAGE REQUIREMENTS

### Mínimos Obligatorios
- **Backend**: 80% coverage general, 90% para servicios críticos
- **Frontend**: 70% coverage general, 80% para hooks y servicios

### Exclusiones Permitidas
```python
# Backend - .coveragerc
[run]
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */config.py
    */wsgi.py
```

```javascript
// Frontend - jest.config.js
collectCoverageFrom: [
  'src/**/*.{ts,tsx}',
  '!src/**/*.d.ts',
  '!src/main.tsx',
  '!src/vite-env.d.ts',
  '!src/**/*.stories.{ts,tsx}',
],
```

## TESTING CHECKLIST

### Antes de Commit
- [ ] Todos los tests pasan
- [ ] Coverage mínimo alcanzado
- [ ] No hay tests skipped sin justificación
- [ ] Tests nuevos para funcionalidades nuevas
- [ ] Tests de regresión para bugs corregidos

### Para Nuevas Features
- [ ] Unit tests para lógica de negocio
- [ ] Integration tests para comunicación entre módulos
- [ ] Component tests para UI
- [ ] E2E tests para flujos críticos
- [ ] Tests de error y edge cases

### Para Bug Fixes
- [ ] Test que reproduce el bug
- [ ] Test que verifica la corrección
- [ ] Tests de regresión relacionados
- [ ] Verificación de no romper funcionalidad existente

---

**IMPORTANTE**: Los tests son OBLIGATORIOS para todo código nuevo y modificado. No se acepta código sin tests apropiados.