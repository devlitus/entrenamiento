# 🏗️ Arquitectura de Componentes - Dashboard ML Training

## 📋 **Índice**
- [Visión General](#visión-general)
- [Principios de Diseño](#principios-de-diseño)
- [Estructura de Componentes](#estructura-de-componentes)
- [Componentes Base (UI)](#componentes-base-ui)
- [Componentes de Funcionalidad](#componentes-de-funcionalidad)
- [Hooks Personalizados](#hooks-personalizados)
- [Servicios y Estado](#servicios-y-estado)
- [Patrones de Comunicación](#patrones-de-comunicación)
- [Flujo de Datos](#flujo-de-datos)
- [Optimización y Performance](#optimización-y-performance)

---

## 🎯 **Visión General**

La arquitectura de componentes del Dashboard ML Training está diseñada siguiendo principios de **Clean Architecture** y **Component-Driven Development**, proporcionando una base sólida, escalable y mantenible para aplicaciones de machine learning.

### **Objetivos Principales**
- ✅ **Reutilización**: Componentes modulares y reutilizables
- ✅ **Mantenibilidad**: Código limpio y bien estructurado
- ✅ **Escalabilidad**: Fácil extensión y modificación
- ✅ **Performance**: Optimización desde el diseño
- ✅ **Accesibilidad**: Cumplimiento WCAG 2.1 AA
- ✅ **Experiencia de Usuario**: Interfaz intuitiva y educativa

---

## 🎨 **Principios de Diseño**

### **1. Atomic Design**
```
Átomos → Moléculas → Organismos → Templates → Páginas
```

### **2. Single Responsibility Principle**
Cada componente tiene una única responsabilidad bien definida.

### **3. Composition over Inheritance**
Uso de composición para crear componentes complejos.

### **4. Props Interface Design**
Interfaces claras y tipadas para todas las props.

---

## 🏛️ **Estructura de Componentes**

```
src/
├── components/
│   ├── ui/                    # Componentes Base (Átomos)
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Card/
│   │   ├── MetricCard/
│   │   ├── ProgressBar/
│   │   └── Tooltip/
│   │
│   ├── features/              # Componentes de Funcionalidad (Moléculas)
│   │   ├── TrainingControls/
│   │   ├── MetricsDisplay/
│   │   ├── ConfigurationForm/
│   │   ├── ProgressSummary/
│   │   └── LogsViewer/
│   │
│   ├── layout/                # Componentes de Layout (Organismos)
│   │   ├── Header/
│   │   ├── Sidebar/
│   │   ├── MainContent/
│   │   └── Footer/
│   │
│   └── TrainingDashboard.tsx  # Componente Principal (Template)
│
├── hooks/                     # Custom Hooks
│   ├── useWebSocket.ts
│   ├── useTraining.ts
│   └── useMetrics.ts
│
├── services/                  # Servicios
│   ├── api.ts
│   ├── websocket.ts
│   └── training.ts
│
├── store/                     # Estado Global
│   ├── trainingStore.ts
│   └── uiStore.ts
│
└── types/                     # Definiciones de Tipos
    ├── training.ts
    ├── metrics.ts
    └── ui.ts
```

---

## 🧱 **Componentes Base (UI)**

### **Button Component**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  children: ReactNode;
  onClick?: () => void;
  'aria-label'?: string;
}

const Button: FC<ButtonProps> = ({ 
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon,
  children,
  onClick,
  'aria-label': ariaLabel,
  ...props 
}) => {
  // Implementación con estados visuales y accesibilidad
};
```

### **MetricCard Component**
```typescript
interface MetricCardProps {
  title: string;
  description: string;
  explanation: string;
  value: number;
  status: 'excellent' | 'good' | 'warning' | 'poor';
  format: 'decimal' | 'percentage' | 'integer';
  trend?: {
    direction: 'up' | 'down' | 'stable';
    value: string;
  };
  icon?: ReactNode;
}

const MetricCard: FC<MetricCardProps> = ({
  title,
  description,
  explanation,
  value,
  status,
  format,
  trend,
  icon
}) => {
  // Implementación con tooltip explicativo y estados visuales
};
```

### **ProgressBar Component**
```typescript
interface ProgressBarProps {
  value: number;
  max: number;
  variant: 'primary' | 'success' | 'warning' | 'error';
  size: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  animated?: boolean;
  striped?: boolean;
}
```

---

## 🔧 **Componentes de Funcionalidad**

### **TrainingControls Component**
```typescript
interface TrainingControlsProps {
  isTraining: boolean;
  isConnected: boolean;
  onStart: (config: TrainingConfig) => void;
  onPause: () => void;
  onResume: () => void;
  onStop: () => void;
  config: TrainingConfig;
  onConfigChange: (config: TrainingConfig) => void;
}

const TrainingControls: FC<TrainingControlsProps> = ({
  isTraining,
  isConnected,
  onStart,
  onPause,
  onResume,
  onStop,
  config,
  onConfigChange
}) => {
  // Lógica de controles de entrenamiento
  // Validación de configuración
  // Estados de UI según el estado del entrenamiento
};
```

### **ProgressSummary Component**
```typescript
interface ProgressSummaryProps {
  currentEpoch: number;
  totalEpochs: number;
  loss: number;
  validationLoss: number;
  isTraining: boolean;
  estimatedTimeRemaining?: string;
}

const ProgressSummary: FC<ProgressSummaryProps> = ({
  currentEpoch,
  totalEpochs,
  loss,
  validationLoss,
  isTraining,
  estimatedTimeRemaining
}) => {
  // Cálculo de progreso
  // Interpretación de métricas
  // Detección de sobreajuste
  // Consejos personalizados
};
```

### **MetricsDisplay Component**
```typescript
interface MetricsDisplayProps {
  metrics: ModelMetrics | null;
  isTraining: boolean;
}

const MetricsDisplay: FC<MetricsDisplayProps> = ({
  metrics,
  isTraining
}) => {
  // Grid de métricas con explicaciones
  // Estados visuales según rendimiento
  // Comparación de métricas de entrenamiento vs validación
};
```

---

## 🎣 **Hooks Personalizados**

### **useWebSocket Hook**
```typescript
interface UseWebSocketReturn {
  isConnected: boolean;
  trainingStatus: TrainingStatus | null;
  metrics: ModelMetrics | null;
  logs: string[];
  startTraining: (config: TrainingConfig) => void;
  stopTraining: () => void;
  pauseTraining: () => void;
  resumeTraining: () => void;
  clearLogs: () => void;
}

const useWebSocket = (): UseWebSocketReturn => {
  // Gestión de conexión WebSocket
  // Manejo de mensajes en tiempo real
  // Reconexión automática
  // Estado de conexión
};
```

### **useTraining Hook**
```typescript
interface UseTrainingReturn {
  config: TrainingConfig;
  updateConfig: (updates: Partial<TrainingConfig>) => void;
  validateConfig: () => ValidationResult;
  resetConfig: () => void;
  saveConfig: () => void;
  loadConfig: (configId: string) => void;
}

const useTraining = (): UseTrainingReturn => {
  // Gestión de configuración de entrenamiento
  // Validación de parámetros
  // Persistencia de configuración
};
```

### **useMetrics Hook**
```typescript
interface UseMetricsReturn {
  processedMetrics: ProcessedMetrics;
  getMetricStatus: (value: number, type: MetricType) => MetricStatus;
  getPerformanceInsights: () => PerformanceInsight[];
  getRecommendations: () => Recommendation[];
}

const useMetrics = (metrics: ModelMetrics | null): UseMetricsReturn => {
  // Procesamiento de métricas
  // Análisis de rendimiento
  // Generación de insights
  // Recomendaciones automáticas
};
```

---

## 🏪 **Servicios y Estado**

### **Training Store (Zustand)**
```typescript
interface TrainingStore {
  // Estado
  config: TrainingConfig;
  status: TrainingStatus;
  metrics: ModelMetrics | null;
  logs: string[];
  experiments: Experiment[];
  
  // Acciones
  setConfig: (config: TrainingConfig) => void;
  updateStatus: (status: TrainingStatus) => void;
  updateMetrics: (metrics: ModelMetrics) => void;
  addLog: (log: string) => void;
  clearLogs: () => void;
  saveExperiment: (experiment: Experiment) => void;
  
  // Selectores computados
  isTraining: () => boolean;
  progress: () => number;
  currentPerformance: () => PerformanceLevel;
}

const useTrainingStore = create<TrainingStore>((set, get) => ({
  // Implementación del store
}));
```

### **API Service**
```typescript
class TrainingAPIService {
  private baseURL: string;
  private httpClient: AxiosInstance;
  
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
    this.httpClient = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
    });
  }
  
  async startTraining(config: TrainingConfig): Promise<TrainingResponse> {
    // Implementación de inicio de entrenamiento
  }
  
  async getTrainingStatus(trainingId: string): Promise<TrainingStatus> {
    // Implementación de consulta de estado
  }
  
  async getMetrics(trainingId: string): Promise<ModelMetrics> {
    // Implementación de obtención de métricas
  }
}
```

---

## 🔄 **Patrones de Comunicación**

### **1. Props Drilling Prevention**
```typescript
// ❌ EVITAR: Props drilling excesivo
<Dashboard>
  <Header user={user} />
  <MainContent>
    <TrainingSection user={user} config={config} />
    <MetricsSection user={user} metrics={metrics} />
  </MainContent>
</Dashboard>

// ✅ PREFERIR: Context o Store global
const TrainingProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const store = useTrainingStore();
  return (
    <TrainingContext.Provider value={store}>
      {children}
    </TrainingContext.Provider>
  );
};
```

### **2. Event Handling Pattern**
```typescript
// Patrón de eventos tipados
type TrainingEvent = 
  | { type: 'START_TRAINING'; payload: TrainingConfig }
  | { type: 'PAUSE_TRAINING' }
  | { type: 'RESUME_TRAINING' }
  | { type: 'STOP_TRAINING' }
  | { type: 'UPDATE_METRICS'; payload: ModelMetrics };

const useTrainingEvents = () => {
  const dispatch = useTrainingStore(state => state.dispatch);
  
  const handleEvent = useCallback((event: TrainingEvent) => {
    dispatch(event);
  }, [dispatch]);
  
  return { handleEvent };
};
```

### **3. Error Boundary Pattern**
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class TrainingErrorBoundary extends Component<
  { children: ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Training Dashboard Error:', error, errorInfo);
    // Enviar error a servicio de monitoreo
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    
    return this.props.children;
  }
}
```

---

## 📊 **Flujo de Datos**

### **Arquitectura de Datos**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WebSocket     │───▶│   Training       │───▶│   Components    │
│   Connection    │    │   Store          │    │   (UI Layer)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Real-time     │    │   State          │    │   User          │
│   Updates       │    │   Management     │    │   Interactions  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Flujo de Entrenamiento**
```typescript
// 1. Usuario configura parámetros
const handleConfigChange = (newConfig: TrainingConfig) => {
  // Validación inmediata
  const validation = validateConfig(newConfig);
  if (!validation.isValid) {
    showValidationErrors(validation.errors);
    return;
  }
  
  // Actualización del store
  updateConfig(newConfig);
};

// 2. Inicio de entrenamiento
const handleStartTraining = async () => {
  try {
    // Validación final
    const validation = validateConfig(config);
    if (!validation.isValid) throw new Error('Invalid config');
    
    // Llamada a API
    const response = await trainingAPI.startTraining(config);
    
    // Actualización de estado
    updateTrainingStatus({ isTraining: true, id: response.trainingId });
    
    // Inicio de monitoreo en tiempo real
    startWebSocketConnection(response.trainingId);
    
  } catch (error) {
    handleTrainingError(error);
  }
};

// 3. Actualización en tiempo real
const handleWebSocketMessage = (message: WebSocketMessage) => {
  switch (message.type) {
    case 'METRICS_UPDATE':
      updateMetrics(message.payload);
      break;
    case 'STATUS_UPDATE':
      updateTrainingStatus(message.payload);
      break;
    case 'LOG_MESSAGE':
      addLog(message.payload);
      break;
    case 'TRAINING_COMPLETE':
      handleTrainingComplete(message.payload);
      break;
  }
};
```

---

## ⚡ **Optimización y Performance**

### **1. Code Splitting**
```typescript
// Lazy loading de componentes pesados
const TrainingDashboard = lazy(() => import('./TrainingDashboard'));
const MetricsAnalysis = lazy(() => import('./MetricsAnalysis'));
const ExperimentHistory = lazy(() => import('./ExperimentHistory'));

// Suspense boundaries
const App: FC = () => (
  <Suspense fallback={<LoadingSpinner />}>
    <Router>
      <Routes>
        <Route path="/dashboard" element={<TrainingDashboard />} />
        <Route path="/analysis" element={<MetricsAnalysis />} />
        <Route path="/history" element={<ExperimentHistory />} />
      </Routes>
    </Router>
  </Suspense>
);
```

### **2. Memoization Strategy**
```typescript
// Memoización de componentes costosos
const MetricCard = memo<MetricCardProps>(({ 
  title, 
  value, 
  status, 
  explanation 
}) => {
  // Componente memoizado
}, (prevProps, nextProps) => {
  // Comparación personalizada
  return (
    prevProps.value === nextProps.value &&
    prevProps.status === nextProps.status
  );
});

// Memoización de cálculos costosos
const useProcessedMetrics = (metrics: ModelMetrics | null) => {
  return useMemo(() => {
    if (!metrics) return null;
    
    return {
      performance: calculatePerformance(metrics),
      insights: generateInsights(metrics),
      recommendations: generateRecommendations(metrics)
    };
  }, [metrics]);
};
```

### **3. Virtual Scrolling**
```typescript
// Para listas largas de logs o experimentos
const VirtualizedLogsList: FC<{ logs: string[] }> = ({ logs }) => {
  return (
    <FixedSizeList
      height={300}
      itemCount={logs.length}
      itemSize={40}
      itemData={logs}
    >
      {LogItem}
    </FixedSizeList>
  );
};
```

### **4. Debouncing y Throttling**
```typescript
// Debouncing para inputs de configuración
const useConfigDebounce = (config: TrainingConfig, delay: number = 500) => {
  const [debouncedConfig, setDebouncedConfig] = useState(config);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedConfig(config);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [config, delay]);
  
  return debouncedConfig;
};

// Throttling para actualizaciones de métricas
const useThrottledMetrics = (metrics: ModelMetrics | null, delay: number = 100) => {
  const [throttledMetrics, setThrottledMetrics] = useState(metrics);
  const lastUpdate = useRef(0);
  
  useEffect(() => {
    const now = Date.now();
    if (now - lastUpdate.current >= delay) {
      setThrottledMetrics(metrics);
      lastUpdate.current = now;
    }
  }, [metrics, delay]);
  
  return throttledMetrics;
};
```

---

## 🧪 **Testing Strategy**

### **Component Testing**
```typescript
// Test de componente MetricCard
describe('MetricCard', () => {
  const defaultProps: MetricCardProps = {
    title: 'Test Metric',
    description: 'Test Description',
    explanation: 'Test Explanation',
    value: 0.85,
    status: 'good',
    format: 'decimal'
  };
  
  it('renders metric information correctly', () => {
    render(<MetricCard {...defaultProps} />);
    
    expect(screen.getByText('Test Metric')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('0.85')).toBeInTheDocument();
  });
  
  it('shows tooltip on hover', async () => {
    render(<MetricCard {...defaultProps} />);
    
    const infoButton = screen.getByRole('button', { name: /más información/i });
    fireEvent.mouseEnter(infoButton);
    
    await waitFor(() => {
      expect(screen.getByText('Test Explanation')).toBeVisible();
    });
  });
  
  it('applies correct status styling', () => {
    render(<MetricCard {...defaultProps} status="excellent" />);
    
    const card = screen.getByTestId('metric-card');
    expect(card).toHaveClass('metric-card--excellent');
  });
});
```

### **Hook Testing**
```typescript
// Test de custom hook useWebSocket
describe('useWebSocket', () => {
  it('establishes connection and handles messages', async () => {
    const { result } = renderHook(() => useWebSocket());
    
    // Verificar estado inicial
    expect(result.current.isConnected).toBe(false);
    expect(result.current.metrics).toBe(null);
    
    // Simular conexión
    act(() => {
      mockWebSocket.connect();
    });
    
    await waitFor(() => {
      expect(result.current.isConnected).toBe(true);
    });
    
    // Simular mensaje de métricas
    act(() => {
      mockWebSocket.sendMessage({
        type: 'METRICS_UPDATE',
        payload: mockMetrics
      });
    });
    
    expect(result.current.metrics).toEqual(mockMetrics);
  });
});
```

---

## 📚 **Documentación de Componentes**

### **Storybook Integration**
```typescript
// MetricCard.stories.tsx
export default {
  title: 'Components/MetricCard',
  component: MetricCard,
  parameters: {
    docs: {
      description: {
        component: 'Tarjeta de métrica con explicaciones educativas para usuarios no técnicos.'
      }
    }
  },
  argTypes: {
    status: {
      control: { type: 'select' },
      options: ['excellent', 'good', 'warning', 'poor']
    },
    format: {
      control: { type: 'select' },
      options: ['decimal', 'percentage', 'integer']
    }
  }
} as Meta<MetricCardProps>;

export const Default: Story<MetricCardProps> = {
  args: {
    title: 'Error de Entrenamiento',
    description: 'Qué tan bien aprende el modelo',
    explanation: 'Este valor indica qué tan lejos están las predicciones...',
    value: 0.045,
    status: 'good',
    format: 'decimal'
  }
};

export const Excellent: Story<MetricCardProps> = {
  args: {
    ...Default.args,
    value: 0.02,
    status: 'excellent'
  }
};

export const WithTrend: Story<MetricCardProps> = {
  args: {
    ...Default.args,
    trend: {
      direction: 'down',
      value: '12%'
    }
  }
};
```

---

## 🔮 **Roadmap y Extensibilidad**

### **Próximas Funcionalidades**
- 📊 **Gráficos Interactivos**: Integración con Chart.js/D3.js
- 🤖 **IA Explicativa**: Explicaciones automáticas generadas por IA
- 📱 **PWA Support**: Aplicación web progresiva
- 🌐 **Internacionalización**: Soporte multi-idioma
- 🎨 **Temas Personalizables**: Sistema de temas dinámico
- 📈 **Analytics Avanzados**: Métricas de uso y rendimiento

### **Extensión de Componentes**
```typescript
// Ejemplo de extensión para nuevos tipos de métricas
interface CustomMetricCardProps extends MetricCardProps {
  customRenderer?: (value: number) => ReactNode;
  comparisonValue?: number;
  benchmark?: number;
}

const CustomMetricCard: FC<CustomMetricCardProps> = ({
  customRenderer,
  comparisonValue,
  benchmark,
  ...baseProps
}) => {
  // Implementación extendida
};
```

---

## 📝 **Conclusión**

Esta arquitectura de componentes proporciona una base sólida y escalable para el Dashboard ML Training, priorizando:

- **🎯 Experiencia de Usuario**: Interfaz intuitiva y educativa
- **🔧 Mantenibilidad**: Código limpio y bien estructurado
- **⚡ Performance**: Optimización desde el diseño
- **🧪 Testabilidad**: Cobertura completa de tests
- **📈 Escalabilidad**: Fácil extensión y modificación

La arquitectura está diseñada para evolucionar con las necesidades del proyecto, manteniendo siempre los principios de calidad y usabilidad que caracterizan a las mejores aplicaciones de machine learning.