# Reglas de Refactorización - Neural Network Trainer

## Proceso de Refactorización

### Análisis Previo
- Analizar el codebase y archivos relacionados para entender el contexto
- Identificar todas las dependencias y posibles impactos en el sistema
- Verificar que el código/archivo no se use en otras partes antes de eliminar
- Crear un plan detallado y específico con pasos numerados

### Planificación
- El plan debe ser específico y detallado, incluyendo los pasos a seguir
- Presentar el plan en formato de lista numerada
- Dividir en sub-pasos si es necesario para mayor claridad
- No comenzar a escribir código hasta que el plan esté completo y aprobado

### Implementación
- Mantener la misma funcionalidad del código refactorizado
- Asegurar que el código refactorizado esté bien integrado con el sistema existente
- Remover archivos o código obsoleto/no utilizado
- Considerar todas las dependencias y posibles impactos

## Reglas Específicas del Proyecto

### Límites de Archivo
- Los archivos nunca deben exceder 100 líneas
- Dividir archivos grandes en módulos más pequeños
- Mantener responsabilidad única por archivo

### Estructura Modular
- Mantener separación clara entre componentes CLI y web
- Preservar formato de eventos de progreso para frontend
- No modificar seeds de reproducibilidad establecidos (seed=42)
- Seguir convenciones de registro de rutas Flask existentes

### Compatibilidad
- Mantener compatibilidad con puntos de entrada dual (run_web.py / run_cli.py)
- Preservar compatibilidad hacia atrás con versiones anteriores
- No modificar la estructura del proyecto sin aprobación explícita
- Evitar agregar nuevas dependencias sin justificación

## Mejores Prácticas

### Documentación
- La documentación debe ser clara, precisa y fácil de entender
- Asegurar que esté actualizada y refleje el estado actual del sistema
- Organizar la documentación de manera fácil de navegar
- Incluir ejemplos claros y concisos

### Testing
- Verificar que todas las pruebas pasen después del refactoring
- Agregar pruebas para nueva funcionalidad
- Mantener cobertura de pruebas existente
- Probar integración completa del sistema

### Minimización de Cambios
- Priorizar claridad y mantenibilidad del código
- Solo realizar cambios en archivos relevantes al problema actual
- Evitar cambios en archivos no relacionados
- No ser proactivo en modificaciones adicionales innecesarias