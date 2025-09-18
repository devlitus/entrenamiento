# Screenshot - Estado Actual del Backend para Entrenamiento de Modelos

## 🧠 **Arquitectura del Backend para Entrenamiento de Modelos**

### **1. Servicio Principal de Entrenamiento**

El corazón del sistema es `training_service.py`, que actúa como **orquestador principal**:

#### **Características Clave:**
- **Gestión de hilos**: Ejecuta entrenamientos en hilos separados para no bloquear la aplicación
- **Control de estado**: Maneja inicio, pausa, reanudación y detención de entrenamientos
- **Comunicación en tiempo real**: Integrado con WebSockets para streaming de métricas
- **Manejo de errores robusto**: Captura y reporta errores durante el entrenamiento

#### **Flujo de Entrenamiento:**
1. **Inicialización**: Configura parámetros y resetea estado
2. **Generación de datos**: Crea datasets sintéticos
3. **Construcción del modelo**: Arquitecturas personalizables
4. **Entrenamiento**: Con callbacks avanzados para monitoreo
5. **Guardado**: Persiste el modelo entrenado

### **2. Arquitectura Modular**

El sistema está dividido en componentes especializados en `src/services/training/`:

#### **🏗️ ModelBuilder** (`model_builder.py`)
- **Arquitecturas personalizables**: Permite definir capas ocultas, neuronas y activaciones
- **Configuración automática**: Arquitectura por defecto si no se especifica
- **Compilación inteligente**: Optimizador Adam, loss MSE, métricas MAE
- **Logging detallado**: Registra la construcción del modelo paso a paso

```python
# Ejemplo de arquitectura personalizada
architecture = {
    'inputLayer': {'shape': [1]},
    'hiddenLayers': [
        {'neurons': 64, 'activation': 'relu'},
        {'neurons': 32, 'activation': 'relu'}
    ],
    'outputLayer': {'neurons': 1, 'activation': 'linear'}
}
```

#### **📊 DataGenerator** (`data_generator.py`)
- **Datos sintéticos**: Genera datasets para regresión lineal
- **División automática**: Train/validation split (80/20)
- **Reproducibilidad**: Seeds fijos para resultados consistentes
- **Escalabilidad**: Tamaño de dataset configurable

#### **📡 EventEmitter** 
- **Streaming en tiempo real**: Emite métricas vía WebSockets
- **Múltiples tipos de eventos**: Progreso, logs, errores, completado
- **Integración con frontend**: Comunicación bidireccional

#### **🔍 AdvancedTrainingCallback**
- **Monitoreo de hardware**: CPU, GPU, memoria en tiempo real
- **Detección de problemas**: Overfitting, underfitting automático
- **Análisis de learning rate**: Optimización dinámica
- **Ejemplos de predicción**: Muestra predicciones durante entrenamiento

### **3. Configuración Centralizada**

El sistema utiliza una **configuración unificada** en `config.py` (archivo único, sin duplicados) que define parámetros por defecto:

```python
# Parámetros de entrenamiento
DEFAULT_EPOCHS = 20
DEFAULT_BATCH_SIZE = 32  
DEFAULT_LEARNING_RATE = 0.01

# Rutas de almacenamiento
MODEL_PATH = 'models/temperature_model.keras'
TRAINING_DATA_PATH = 'data/training_results.json'
```

### **4. API REST Completa**

El sistema expone endpoints especializados a través de `routes.py`:

#### **Endpoints de Entrenamiento:**
- `POST /api/training/start` - Iniciar entrenamiento
- `POST /api/training/stop` - Detener entrenamiento  
- `POST /api/training/pause` - Pausar entrenamiento
- `GET /api/training/status` - Estado actual

#### **Endpoints de Modelos:**
- `GET /api/models/info` - Información del modelo
- `POST /api/predictions/predict` - Realizar predicciones
- `GET /api/predictions/training-data` - Datos de entrenamiento

#### **Endpoints de Estadísticas:**
- `GET /api/statistics/summary` - Resumen de entrenamientos
- `GET /api/statistics/metrics` - Métricas históricas

### **5. Almacenamiento y Persistencia**

#### **Base de Datos SQLite:**
- **Sesiones de entrenamiento**: Metadatos, hiperparámetros, resultados
- **Métricas históricas**: Evolución de loss, accuracy, tiempo
- **Gestión de experimentos**: Comparación entre entrenamientos

#### **Archivos del Sistema:**
- **Modelos entrenados**: Formato Keras (.keras)
- **Logs estructurados**: Registro detallado de eventos
- **Datos temporales**: Cache de métricas en tiempo real

### **6. Comunicación en Tiempo Real**

#### **WebSockets Integration:**
- **Eventos de progreso**: Época actual, loss, métricas
- **Monitoreo de hardware**: CPU%, GPU%, memoria
- **Logs en vivo**: Mensajes del entrenamiento
- **Alertas automáticas**: Problemas detectados

### **7. Características Avanzadas**

#### **🔄 Gestión de Estado:**
- **Thread-safe**: Manejo seguro de concurrencia
- **Estados múltiples**: Entrenando, pausado, detenido
- **Recuperación de errores**: Reinicio automático tras fallos

#### **📈 Monitoreo Inteligente:**
- **Detección de overfitting**: Comparación train vs validation loss
- **Early stopping**: Detención automática si no mejora
- **Learning rate scheduling**: Reducción dinámica del learning rate

#### **🎯 Flexibilidad de Arquitecturas:**
- **Single-layer**: Modelo simple con una capa densa
- **Multi-layer**: Arquitecturas profundas personalizables
- **Activaciones**: ReLU, sigmoid, tanh, linear
- **Optimizadores**: Adam, SGD, RMSprop

### **8. Integración con Frontend**

El backend está completamente preparado para:
- **Dashboard en tiempo real**: Métricas streaming
- **Control interactivo**: Botones de start/stop/pause
- **Visualizaciones**: Gráficos de loss, accuracy, hardware
- **Configuración dinámica**: Ajuste de hiperparámetros desde UI

## **🚀 Estado Actual**

El backend está **completamente funcional** y preparado para:

✅ **Entrenar modelos de regresión** con TensorFlow/Keras
✅ **Arquitecturas personalizables** (single/multi-layer)
✅ **Monitoreo en tiempo real** con WebSockets
✅ **Almacenamiento persistente** de experimentos
✅ **API REST completa** para integración frontend
✅ **Manejo robusto de errores** y estados
✅ **Logging detallado** y debugging

## **📁 Estructura de Archivos Clave**

```
backend/
├── src/
│   ├── services/
│   │   ├── training_service.py          # Orquestador principal
│   │   └── training/
│   │       ├── model_builder.py         # Constructor de modelos
│   │       ├── data_generator.py        # Generador de datos
│   │       ├── event_emitter.py         # Emisor de eventos
│   │       └── advanced_callbacks.py    # Callbacks avanzados
│   ├── api/
│   │   ├── training_routes.py           # Rutas de entrenamiento
│   │   ├── predictions/                 # Predicciones
│   │   ├── statistics_routes.py         # Estadísticas
│   │   └── websocket_handlers.py        # WebSocket handlers
│   └── routes.py                        # Registro de rutas
├── config.py                            # Configuración central
└── server.py                            # Servidor Flask
```

## **🔧 Tecnologías Utilizadas**

- **Framework**: Flask + Flask-SocketIO
- **Machine Learning**: TensorFlow/Keras
- **Base de Datos**: SQLite
- **Comunicación**: WebSockets (Server-Sent Events)
- **Logging**: Python logging con configuración personalizada
- **Threading**: Hilos para entrenamientos no bloqueantes

## **📊 Métricas y Monitoreo**

### **Métricas Básicas (Cada Época):**
- Loss de entrenamiento y validación
- MAE (Mean Absolute Error)
- Tiempo por época
- Progreso del entrenamiento

### **Métricas Avanzadas (Tiempo Real):**
- Uso de CPU y memoria
- Detección de overfitting/underfitting
- Análisis de learning rate
- Ejemplos de predicción en vivo

## **🎯 Capacidades del Sistema**

1. **Entrenamiento Asíncrono**: No bloquea la interfaz de usuario
2. **Control Granular**: Inicio, pausa, reanudación, detención
3. **Arquitecturas Flexibles**: Desde modelos simples hasta redes profundas
4. **Monitoreo Completo**: Hardware, métricas, logs en tiempo real
5. **Persistencia Robusta**: Modelos, experimentos, métricas históricas
6. **API Extensible**: Endpoints RESTful bien documentados
7. **Integración Frontend**: WebSockets para comunicación bidireccional

El sistema sigue una **arquitectura modular** que permite fácil extensión y mantenimiento, cumpliendo con los estándares establecidos en las reglas del proyecto y manteniendo retrocompatibilidad completa.

---

**Documento generado el: 2025-01-18**
**Última actualización: Eliminación de archivos duplicados de configuración**