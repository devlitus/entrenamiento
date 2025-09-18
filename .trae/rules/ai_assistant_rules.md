# Reglas para Asistente de IA - Neural Network Trainer

## COMPORTAMIENTO OBLIGATORIO DEL ASISTENTE

### 1. ANÁLISIS PREVIO SIEMPRE REQUERIDO
Antes de cualquier modificación de código, el asistente DEBE:

```markdown
1. **Buscar dependencias**: Usar search_codebase para encontrar todas las referencias
2. **Analizar impacto**: Identificar qué funcionalidades pueden verse afectadas
3. **Verificar tests**: Revisar si existen tests para el código a modificar
4. **Evaluar arquitectura**: Confirmar que el cambio respeta la arquitectura modular
```

### 2. PRINCIPIO DE MÍNIMA MODIFICACIÓN
- **NUNCA** modificar más archivos de los estrictamente necesarios
- **NUNCA** refactorizar código no relacionado con el problema actual
- **NUNCA** agregar funcionalidades no solicitadas
- **SIEMPRE** preservar funcionalidades existentes

### 3. VALIDACIÓN OBLIGATORIA
Después de cada cambio, el asistente DEBE:
```bash
# Verificar que el código funciona
cd backend && python verify_architecture.py
cd backend && python -m pytest

# Verificar que el frontend compila
cd frontend && npm run build
```

## PATRONES DE CÓDIGO OBLIGATORIOS

### Backend (Python)
```python
# ✅ PATRÓN CORRECTO - Servicio modular
class NewService:
    """Servicio para nueva funcionalidad."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger()
    
    def execute_operation(self, params: dict) -> dict:
        """Ejecuta operación específica."""
        try:
            # Lógica del servicio
            result = self._process_data(params)
            self.logger.info(f"Operación exitosa: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error en operación: {e}")
            raise

# ❌ PATRÓN INCORRECTO - Función monolítica
def do_everything(param1, param2, param3, param4, param5, param6):
    # 100+ líneas de código mezclado
    pass
```

### Frontend (TypeScript)
```typescript
// ✅ PATRÓN CORRECTO - Hook personalizado
export function useNewFeature() {
  const [state, setState] = useState<FeatureState>();
  
  const executeAction = useCallback(async (params: ActionParams) => {
    try {
      const result = await api.executeAction(params);
      setState(result);
      return result;
    } catch (error) {
      console.error('Error en acción:', error);
      throw error;
    }
  }, []);
  
  return { state, executeAction };
}

// ✅ PATRÓN CORRECTO - Componente atómico
interface NewComponentProps {
  data: ComponentData;
  onAction: (params: ActionParams) => void;
}

export function NewComponent({ data, onAction }: NewComponentProps) {
  return (
    <div className="component-container">
      {/* UI específica del componente */}
    </div>
  );
}
```

## REGLAS DE MODIFICACIÓN ESPECÍFICAS

### Al Modificar Servicios Existentes
1. **NUNCA** cambiar la signature de métodos públicos
2. **SIEMPRE** mantener compatibilidad hacia atrás
3. **AGREGAR** nuevos métodos en lugar de modificar existentes
4. **PRESERVAR** el comportamiento original

```python
# ✅ CORRECTO - Agregar nuevo método
class ExistingService:
    def existing_method(self, params):
        # NO MODIFICAR este método
        pass
    
    def new_method(self, params):
        # Agregar nueva funcionalidad aquí
        pass

# ❌ INCORRECTO - Modificar método existente
class ExistingService:
    def existing_method(self, params, new_param):  # ❌ Cambió signature
        # Modificó comportamiento existente
        pass
```

### Al Modificar Componentes Existentes
1. **PRESERVAR** props existentes
2. **MANTENER** comportamiento de renderizado
3. **AGREGAR** nuevas props como opcionales
4. **NO ROMPER** componentes padre

```typescript
// ✅ CORRECTO - Agregar prop opcional
interface ExistingComponentProps {
  existingProp: string;        // Mantener existente
  newProp?: string;           // Agregar como opcional
}

export function ExistingComponent({ 
  existingProp, 
  newProp 
}: ExistingComponentProps) {
  // Preservar lógica existente
  // Agregar nueva funcionalidad condicionalmente
  return (
    <div>
      {/* Mantener estructura existente */}
      {newProp && <div>{newProp}</div>}
    </div>
  );
}
```

## ESTRUCTURA DE RESPUESTA OBLIGATORIA

### Para Nuevas Features
```markdown
## Análisis de Impacto
- Archivos que se modificarán: [lista]
- Funcionalidades afectadas: [lista]
- Tests existentes: [estado]
- Dependencias: [lista]

## Plan de Implementación
1. Crear nuevo servicio/componente
2. Implementar interfaces
3. Agregar tests
4. Integrar gradualmente
5. Verificar funcionalidad

## Validación
- [ ] Tests pasan
- [ ] Funcionalidades existentes intactas
- [ ] Arquitectura respetada
- [ ] Performance mantenida
```

### Para Corrección de Bugs
```markdown
## Análisis del Bug
- Ubicación del problema: [archivo:línea]
- Causa raíz: [descripción]
- Impacto: [funcionalidades afectadas]

## Solución Propuesta
- Cambios mínimos necesarios
- Preservación de funcionalidad existente
- Tests para prevenir regresión

## Verificación
- [ ] Bug corregido
- [ ] No hay regresiones
- [ ] Tests actualizados
```

## COMANDOS DE VERIFICACIÓN OBLIGATORIOS

### Antes de Cualquier Cambio
```bash
# Buscar dependencias
search_codebase("función_a_modificar")
search_by_regex("función_a_modificar")

# Verificar tests existentes
search_codebase("test función_a_modificar")
```

### Después de Cada Cambio
```bash
# Backend
cd backend
python verify_architecture.py
python -m pytest -v
python run_complete_test.py

# Frontend
cd frontend
npm test
npm run build
npm run type-check
```

## MANEJO DE ERRORES OBLIGATORIO

### Si Algo Se Rompe
1. **REVERTIR** cambios inmediatamente
2. **ANALIZAR** causa del problema
3. **REPLANTEAR** solución
4. **IMPLEMENTAR** con más cuidado

### Si Tests Fallan
1. **NO IGNORAR** tests fallidos
2. **INVESTIGAR** causa del fallo
3. **CORREGIR** el problema
4. **VERIFICAR** que todos los tests pasan
5. **SI FALLA** no modificar el código modificar el test
5. **SI FALLA** en más de 3 intentos, **REPORTAR** al equipo de desarrollo y **PONERLO EN SKIP**


## LÍMITES ESTRICTOS

### Líneas de Código
- **Máximo 100 líneas por archivo**
- **Máximo 20 líneas por función**
- **Máximo 5 parámetros por función**

### Complejidad
- **Máximo 3 niveles de anidación**
- **Máximo 10 condiciones por función**
- **Máximo 5 dependencias por módulo**

### Performance
- **APIs < 200ms response time**
- **Frontend bundle < 2MB**
- **Memory usage < 80%**

## DOCUMENTACIÓN OBLIGATORIA

### Para Cambios Complejos
```markdown
# Cambio Realizado

## Descripción
Breve descripción del cambio y por qué fue necesario.

## Archivos Modificados
- `archivo1.py`: Descripción del cambio
- `archivo2.ts`: Descripción del cambio

## Impacto
- Funcionalidades afectadas: [lista]
- Breaking changes: [ninguno/lista]
- Performance impact: [descripción]

## Testing
- Tests agregados: [lista]
- Tests modificados: [lista]
- Cobertura: [porcentaje]

## Verificación
- [ ] Todos los tests pasan
- [ ] Funcionalidades existentes intactas
- [ ] Performance mantenida
- [ ] Documentación actualizada
```

---

**IMPORTANTE**: Estas reglas son OBLIGATORIAS para el asistente de IA. Su violación puede resultar en funcionalidades rotas y pérdida de estabilidad del sistema.