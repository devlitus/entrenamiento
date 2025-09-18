# Plantillas de Prompts Automatizados - Neural Network Trainer

## Plantilla 1: Diagnóstico de Bugs UI/Frontend

```
🐛 DIAGNÓSTICO UI/FRONTEND AUTOMÁTICO

PROBLEMA: [DESCRIBE EL PROBLEMA ESPECÍFICO]
COMPONENTE: [frontend/src/components/NombreComponente.tsx]
COMPORTAMIENTO ESPERADO: [QUÉ DEBERÍA PASAR]
COMPORTAMIENTO ACTUAL: [QUÉ ESTÁ PASANDO]

CONTEXTO AUTOMÁTICO:
- Stack: React 19 + TypeScript + Zustand + TailwindCSS v4
- Comunicación: Socket.IO + Axios
- Visualización: Chart.js + Recharts + Framer Motion

EJECUCIÓN AUTOMÁTICA:
1. 🔍 Analizar componente React + hooks relacionados
2. 🔗 Verificar conexión con Zustand store
3. 🎨 Revisar estilos TailwindCSS + animaciones
4. 🔧 Implementar solución mínima
5. ✅ Validar con tests + mostrar preview

REGLAS: .trae/rules/contribution_guide.md + code_standards.md
RESULTADO: Solución funcional con preview visual
```

## Plantilla 2: Problemas de Backend/API

```
⚙️ DIAGNÓSTICO BACKEND AUTOMÁTICO

PROBLEMA: [DESCRIBE EL ISSUE DEL SERVIDOR]
ENDPOINT/SERVICIO: [backend/src/routes.py o backend/src/services/]
ERROR OBSERVADO: [LOGS O COMPORTAMIENTO ANÓMALO]

CONTEXTO AUTOMÁTICO:
- Stack: Flask + SocketIO + TensorFlow/Keras
- Datos: NumPy + Pandas con normalización
- Storage: SQLite + archivos .keras
- Monitoreo: psutil + GPUtil

EJECUCIÓN AUTOMÁTICA:
1. 🔍 Analizar Flask routes + SocketIO handlers
2. 🧠 Verificar servicios ML/TensorFlow
3. 📊 Comprobar procesamiento de datos
4. 🔧 Implementar fix preservando arquitectura
5. ✅ Ejecutar pytest + validar funcionalidades

REGLAS: Mantener seeds (seed=42) + arquitectura modular
RESULTADO: Backend funcional con tests pasando
```

## Plantilla 3: Comunicación Tiempo Real (WebSockets)

```
🔄 DIAGNÓSTICO COMUNICACIÓN TIEMPO REAL

PROBLEMA: [ISSUE CON WEBSOCKETS/SERVER-SENT EVENTS]
FLUJO AFECTADO: [Frontend ↔ Backend communication]
SÍNTOMAS: [Sin updates, conexión perdida, datos no llegan]

CONTEXTO AUTOMÁTICO:
- Backend: Flask-SocketIO para streaming
- Frontend: Socket.IO client + event listeners
- Datos: Progreso de entrenamiento + métricas hardware

EJECUCIÓN AUTOMÁTICA:
1. 🔍 Verificar configuración SocketIO backend/src/sockets.py
2. 🔗 Analizar client connection en frontend/src/services/
3. 📡 Comprobar emisión/recepción de eventos
4. 🔧 Corregir comunicación bidireccional
5. ✅ Validar streaming en tiempo real

REGLAS: Preservar formato eventos + arquitectura modular
RESULTADO: Comunicación tiempo real funcional
```

## Plantilla 4: Optimización de Modelos ML

```
🧠 OPTIMIZACIÓN MODELOS ML AUTOMÁTICA

OBJETIVO: [MEJORAR RENDIMIENTO/PRECISIÓN/VELOCIDAD]
MODELO ACTUAL: [TensorFlow/Keras architecture]
MÉTRICAS OBJETIVO: [Loss, accuracy, tiempo entrenamiento]

CONTEXTO AUTOMÁTICO:
- ML Stack: TensorFlow + Keras + NumPy + Pandas
- Arquitecturas: Single/Multi-layer neural networks
- Dataset: Regresión Celsius-Fahrenheit normalizado
- Reproducibilidad: seed=42 obligatorio

EJECUCIÓN AUTOMÁTICA:
1. 🔍 Analizar arquitectura actual del modelo
2. 📊 Evaluar métricas de rendimiento
3. ⚡ Optimizar hiperparámetros + arquitectura
4. 🔧 Implementar mejoras incrementales
5. ✅ Validar con tests + comparar métricas

REGLAS: NO modificar seeds + mantener compatibilidad
RESULTADO: Modelo optimizado con métricas mejoradas
```

## Plantilla 5: Nuevas Features

```
✨ IMPLEMENTACIÓN NUEVA FEATURE

FEATURE: [DESCRIBE LA NUEVA FUNCIONALIDAD]
ALCANCE: [Frontend, Backend, o Full-stack]
REQUISITOS: [FUNCIONALIDADES ESPECÍFICAS NECESARIAS]

CONTEXTO AUTOMÁTICO:
- Arquitectura: Flask backend + React frontend modular
- Comunicación: API REST + WebSockets según necesidad
- Testing: pytest (backend) + jest/vitest (frontend)

EJECUCIÓN AUTOMÁTICA:
1. 🔍 Analizar impacto en arquitectura existente
2. 📋 Planificar implementación incremental
3. 🔧 Desarrollar backend + frontend coordinadamente
4. 🧪 Implementar tests automáticos
5. ✅ Validar integración + mostrar preview

REGLAS: Extensión sin modificación + arquitectura modular
RESULTADO: Feature funcional integrada con tests
```