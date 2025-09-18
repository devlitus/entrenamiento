# Configuración del Proyecto - Neural Network Trainer

## Stack Tecnológico Principal

### Backend
- **Python 3**: Lenguaje principal para data science y ML
- **Flask + Flask-SocketIO**: Framework web con WebSockets
- **TensorFlow/Keras**: Deep learning y redes neuronales
- **PyTorch**: Alternativa para deep learning
- **NumPy**: Computación numérica y operaciones con arrays
- **Pandas**: Manipulación y análisis de datos
- **Scikit-learn**: Algoritmos de machine learning
- **pytest**: Testing automatizado

### Frontend
- **React 19**: Framework de interfaz de usuario
- **TypeScript**: Tipado estático para JavaScript
- **TailwindCSS v4**: Framework de estilos (sin tailwind.config)
- **Zustand**: Gestión de estado
- **Socket.IO**: Comunicación en tiempo real
- **Chart.js/Recharts**: Visualización de datos
- **Framer Motion**: Animaciones

### Herramientas de Desarrollo
- **Conda**: Gestión de entornos y paquetes
- **Jupyter**: Desarrollo interactivo y visualización
- **Matplotlib/Seaborn**: Visualización estadística
- **psutil/GPUtil**: Monitoreo de hardware

## Convenciones de Código

### Python
- **Estilo**: PEP 8 con líneas de máximo 100 caracteres
- **Imports**: Organizados por categorías (stdlib, third-party, local)
- **Funciones**: Documentación con docstrings
- **Variables**: snake_case para variables y funciones
- **Clases**: PascalCase para nombres de clases
- **Constantes**: UPPER_CASE para constantes

### TypeScript/React
- **Componentes**: Funcionales con interfaces TypeScript
- **Naming**: camelCase para variables, PascalCase para componentes
- **Exports**: Preferir named exports sobre default exports
- **Directorios**: lowercase con guiones (auth-wizard)
- **Archivos**: Descriptivos con auxiliary verbs (isLoading, hasError)

## Configuración de Entorno

### Variables de Entorno
```bash
# Desarrollo
FLASK_ENV=development
FLASK_DEBUG=True
PYTHONPATH=./backend

# Producción
FLASK_ENV=production
FLASK_DEBUG=False
```

### Estructura de Archivos
```
backend/
├── src/
│   ├── api/          # Endpoints REST y WebSocket
│   ├── services/     # Lógica de negocio
│   ├── utils/        # Utilidades compartidas
│   └── models/       # Modelos de datos
├── tests/            # Pruebas automatizadas
└── config.py         # Configuración de la aplicación

frontend/
├── src/
│   ├── components/   # Componentes React
│   ├── hooks/        # Custom hooks
│   ├── types/        # Definiciones TypeScript
│   └── utils/        # Utilidades frontend
└── public/           # Archivos estáticos
```

## Configuración de Machine Learning

### Reproducibilidad
- **Seed fijo**: np.random.seed(42), tf.random.set_seed(42)
- **Determinismo**: Configurar TensorFlow para resultados consistentes
- **Versionado**: Tracking de experimentos y modelos

### Optimización
- **GPU**: Configuración automática de TensorFlow/PyTorch
- **Memoria**: Gestión eficiente para entrenamientos largos
- **Paralelización**: Uso de múltiples cores cuando sea posible

### Monitoreo
- **Métricas**: Loss, accuracy, val_loss, val_accuracy
- **Hardware**: CPU, GPU, memoria, temperatura
- **Tiempo real**: Streaming via WebSocket al frontend

## Configuración de Comunicación

### API REST
- **Base URL**: http://localhost:5000/api
- **Formato**: JSON para request/response
- **CORS**: Configurado para desarrollo local
- **Autenticación**: Preparado para implementación futura

### WebSockets
- **Namespace**: /training para eventos de entrenamiento
- **Eventos**: progress, metrics, status, error
- **Formato**: JSON estructurado con timestamps
- **Reconexión**: Automática en caso de desconexión

### Base de Datos
- **SQLite**: Para desarrollo y métricas históricas
- **Migraciones**: Automáticas en inicio de aplicación
- **Backup**: Configuración para respaldo periódico

## Configuración de Testing

### Backend (pytest)
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --cov=src --cov-report=html
```

### Frontend (Jest/Vitest)
```json
{
  "test": {
    "environment": "jsdom",
    "setupFiles": ["./src/test/setup.ts"],
    "coverage": {
      "reporter": ["text", "html"]
    }
  }
}
```

## Configuración de Desarrollo

### Hot Reload
- **Backend**: Flask development server con auto-reload
- **Frontend**: Vite con HMR (Hot Module Replacement)
- **Sincronización**: Cambios reflejados inmediatamente

### Debugging
- **Backend**: Python debugger integrado
- **Frontend**: React DevTools + Browser DevTools
- **Network**: Monitoreo de requests/responses
- **WebSocket**: Debug de eventos en tiempo real

### Logging
```python
# Configuración de logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```