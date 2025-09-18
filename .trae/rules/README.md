# Sistema de Reglas - Neural Network Trainer

## 🎯 OBJETIVO

Este sistema de reglas está diseñado para **prevenir la rotura de funcionalidades** cuando se añaden nuevas features o se refactoriza código, asegurando que el asistente de IA y todos los desarrolladores sigan los patrones establecidos del proyecto.

## 📁 ESTRUCTURA DE REGLAS

```
.trae/rules/
├── README.md                    # Este archivo - Guía principal
├── project_rules.md            # Reglas arquitectónicas del proyecto
├── user_rules.md              # Reglas específicas del usuario
├── development_rules.md       # Reglas de desarrollo y preservación
├── workflow_rules.md          # Reglas de flujo de trabajo
├── ai_assistant_rules.md      # Reglas específicas para IA
├── code_standards.md          # Estándares de código obligatorios
├── testing_standards.md       # Estándares de testing
└── contribution_guide.md      # Guía completa de contribución
```

## 🚀 INICIO RÁPIDO

### Para Desarrolladores
1. **Leer OBLIGATORIO**: `contribution_guide.md`
2. **Configurar entorno**: Seguir `code_standards.md`
3. **Ejecutar tests**: Usar comandos de `testing_standards.md`

### Para Asistente de IA
1. **Seguir SIEMPRE**: `ai_assistant_rules.md`
2. **Respetar patrones**: `development_rules.md`
3. **Validar cambios**: `workflow_rules.md`

## 🛡️ PRINCIPIOS FUNDAMENTALES

### 1. **Preservación de Funcionalidades**
- ❌ **NUNCA** modificar funciones existentes sin análisis previo
- ✅ **SIEMPRE** extender funcionalidad en lugar de modificar
- ✅ **OBLIGATORIO** ejecutar tests antes de cualquier cambio

### 2. **Arquitectura Modular**
- ✅ Mantener separación clara: Backend ↔ Frontend ↔ CLI
- ✅ Respetar interfaces establecidas entre módulos
- ❌ No crear dependencias circulares

### 3. **Mínima Modificación**
- ✅ Hacer el menor número de cambios posible
- ✅ Preferir composición sobre herencia
- ✅ Documentar razones para cambios significativos

## 📋 CHECKLIST RÁPIDO

### Antes de Cualquier Cambio
```bash
# 1. Verificar funcionalidad existente
pytest tests/ -v
npm test

# 2. Buscar patrones similares
grep -r "función_similar" src/
grep -r "pattern_similar" frontend/src/

# 3. Verificar dependencias
grep -r "import.*módulo" src/
```

### Durante el Desarrollo
- [ ] Seguir patrones de `code_standards.md`
- [ ] Escribir tests según `testing_standards.md`
- [ ] Validar que no se rompe funcionalidad existente
- [ ] Documentar cambios significativos

### Antes de Commit
```bash
# Ejecutar script de verificación completa
./scripts/pre-commit-check.sh
```

## 🎯 PATRONES ESPECÍFICOS DEL PROYECTO

### Backend (Python + Flask)
```python
# ✅ PATRÓN CORRECTO
class TrainingService(BaseService):
    def validate_params(self, params: Dict[str, Any]) -> None:
        """Validación OBLIGATORIA de parámetros."""
        if params.get('epochs', 0) <= 0:
            raise ValidationError("Epochs debe ser mayor a 0")
    
    def new_feature(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Nueva funcionalidad SIN modificar existente."""
        self.validate_params(params)  # Usar validación existente
        return self._extend_functionality(params)
```

### Frontend (React + TypeScript)
```typescript
// ✅ PATRÓN CORRECTO
export const useTraining = (): UseTrainingReturn => {
  const validateParams = useCallback((params: TrainingParams): void => {
    if (params.epochs <= 0) {
      throw new Error('Las épocas deben ser mayor a 0');
    }
  }, []);

  const startTraining = useCallback(async (params: TrainingParams): Promise<void> => {
    validateParams(params); // Validación OBLIGATORIA
    // Lógica de entrenamiento...
  }, [validateParams]);
};
```

## 🧪 TESTING OBLIGATORIO

### Cobertura Mínima
- **Backend**: 80% coverage general, 90% servicios críticos
- **Frontend**: 70% coverage general, 80% hooks y servicios

### Comandos Esenciales
```bash
# Backend
pytest --cov=src --cov-fail-under=80
pytest tests/unit/ -v
pytest tests/integration/ -v

# Frontend
npm run test:coverage
npm test -- --watchAll=false
```

## 🚨 ERRORES COMUNES A EVITAR

### ❌ Modificación Directa
```python
# ❌ MAL - Modificando función existente
def existing_function(params):
    # Cambios que pueden romper funcionalidad
    new_logic()  # ¡PELIGRO!
    return result
```

### ✅ Extensión Correcta
```python
# ✅ BIEN - Extendiendo funcionalidad
def existing_function(params):
    # Código original intacto
    return original_logic(params)

def enhanced_function(params):
    """Nueva funcionalidad que extiende la existente."""
    base_result = existing_function(params)
    return enhance_result(base_result)
```

## 🎯 OBJETIVOS ALCANZADOS

Con este sistema de reglas, hemos logrado:

1. ✅ **Prevenir roturas**: Reglas claras para preservar funcionalidad existente
2. ✅ **Código cohesionado**: Patrones obligatorios para mantener consistencia
3. ✅ **Bajo acoplamiento**: Arquitectura modular con interfaces bien definidas
4. ✅ **Patrones establecidos**: Documentación completa de estándares del proyecto
5. ✅ **Cumplimiento automático**: Herramientas y scripts para verificar reglas

---

**IMPORTANTE**: Este sistema es de cumplimiento **OBLIGATORIO** para mantener la calidad y estabilidad del proyecto Neural Network Trainer.