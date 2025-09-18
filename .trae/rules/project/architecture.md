# Arquitectura del Proyecto - Neural Network Trainer

## Visión General

**Modo de Desarrollo Neural Network Trainer** optimizado para proyecto dual de entrenamiento de redes neuronales con arquitectura modular Flask web app + CLI tool.

## Arquitectura Principal

### Separación de Responsabilidades
- **Backend**: Flask con Flask-SocketIO para API REST y WebSockets
- **Frontend**: React 19 + TypeScript para interfaz de usuario
- **CLI**: Herramienta de línea de comandos independiente
- **Comunicación**: Server-Sent Events para progreso en tiempo real

### Stack Tecnológico

#### Backend (Python)
- **Framework**: Flask con Flask-SocketIO
- **ML/DL**: TensorFlow/Keras para regresión Celsius-Fahrenheit
- **Datos**: NumPy, Pandas con normalización de datos
- **Monitoreo**: psutil, GPUtil para métricas de hardware
- **Storage**: SQLite para métricas históricas
- **Testing**: pytest con cobertura completa

#### Frontend (React + TypeScript)
- **Framework**: React 19 con TypeScript
- **Estado**: Zustand para gestión de estado
- **Comunicación**: Socket.IO para tiempo real, Axios para HTTP
- **Visualización**: Chart.js, Recharts para gráficos
- **Estilos**: TailwindCSS v4 (sin tailwind.config)
- **Animaciones**: Framer Motion

## Patrones de Diseño

### Modularidad
- **Arquitectura modular**: Componentes independientes pero complementarios
- **Puntos de entrada dual**: run_web.py / run_cli.py
- **Servicios inyectados**: Patrón Factory para Flask app
- **Separación clara**: Componentes CLI y web independientes

### Comunicación
- **API REST**: Para operaciones CRUD y configuración
- **WebSockets**: Para streaming de progreso de entrenamiento
- **Server-Sent Events**: Para actualizaciones en tiempo real
- **JSON**: Formato estándar para intercambio de datos

### Persistencia
- **Modelos**: Archivos .keras para modelos entrenados
- **Métricas**: Base de datos SQLite para historial
- **Configuración**: Archivos JSON para configuraciones
- **Logs**: Sistema de logging estructurado

## Restricciones Específicas

### Compatibilidad
- Mantener compatibilidad con puntos de entrada dual
- Preservar formato de eventos de progreso para frontend
- No modificar seeds de reproducibilidad (seed=42)
- Seguir convenciones de registro de rutas Flask existentes

### Rendimiento
- Optimización de redes neuronales (single/multi-layer)
- Streaming eficiente de datos de entrenamiento
- Procesamiento y normalización optimizada de datasets
- Manejo de memoria para entrenamientos largos

### Escalabilidad
- Diseño para soportar múltiples entrenamientos simultáneos
- Estructura de importes Python escalable
- Gestión eficiente de rutas y endpoints
- Componentes reutilizables y modulares

## Flujo de Datos

### Entrenamiento
1. **Configuración**: Frontend envía parámetros via API
2. **Inicialización**: Backend prepara modelo y datos
3. **Entrenamiento**: TensorFlow ejecuta con callbacks
4. **Streaming**: Métricas enviadas via WebSocket
5. **Almacenamiento**: Resultados guardados en DB y archivos

### Monitoreo
1. **Hardware**: Monitor continuo de CPU/GPU/Memoria
2. **Métricas**: Cálculo en tiempo real de rendimiento
3. **Alertas**: Sistema automático de notificaciones
4. **Visualización**: Gráficos interactivos en frontend

## Principios de Diseño

### Mantenibilidad
- Código auto-documentado y legible
- Separación clara de responsabilidades
- Interfaces bien definidas entre componentes
- Testing automatizado y validación continua

### Reproducibilidad
- Seeds fijos para resultados consistentes
- Configuraciones versionadas
- Logs detallados de experimentos
- Trazabilidad completa de entrenamientos

### Extensibilidad
- Arquitectura plugin-ready
- Interfaces abstractas para nuevos algoritmos
- Sistema de configuración flexible
- Hooks para personalización