import { useState, useEffect, useCallback, useRef } from 'react';
import { websocketService, type SupportedEvent, type TrainingEvent, type MetricsEvent, type SystemEvent } from '@/services/websocket';
import { ApiService } from '@/services/api';

// Tipos para el estado del hook
interface RealTimeDataState {
  isConnected: boolean;
  connectionState: 'connecting' | 'connected' | 'disconnected';
  trainingData: TrainingData | null;
  metrics: MetricsData | null;
  systemStats: SystemStats | null;
  logs: LogEntry[];
  error: string | null;
}

interface TrainingData {
  training_id: string;
  status: 'idle' | 'training' | 'paused' | 'completed' | 'error';
  epoch: number;
  total_epochs: number;
  batch?: number;
  total_batches?: number;
  loss?: number;
  accuracy?: number;
  val_loss?: number;
  val_accuracy?: number;
  elapsed_time?: string;
  estimated_time_remaining?: string;
  progress: number;
}

interface MetricsData {
  model_id?: string;
  metrics: Record<string, number>;
  timestamp: string;
  history: Array<{
    epoch: number;
    metrics: Record<string, number>;
    timestamp: string;
  }>;
}

interface SystemStats {
  cpu_usage: number;
  memory_usage: number;
  gpu_usage?: number;
  disk_usage: number;
  timestamp: string;
}

interface LogEntry {
  id: string;
  message: string;
  level: 'info' | 'warning' | 'error' | 'debug';
  timestamp: string;
  source?: string;
}

interface UseRealTimeDataOptions {
  autoConnect?: boolean;
  maxLogs?: number;
  enableSystemStats?: boolean;
  reconnectOnError?: boolean;
}

interface UseRealTimeDataReturn extends RealTimeDataState {
  connect: () => void;
  disconnect: () => void;
  clearLogs: () => void;
  refreshData: () => Promise<void>;
}

export const useRealTimeData = (options: UseRealTimeDataOptions = {}): UseRealTimeDataReturn => {
  const {
    autoConnect = true,
    maxLogs = 100,
    enableSystemStats = true,
    reconnectOnError = true
  } = options;

  // Estado principal
  const [state, setState] = useState<RealTimeDataState>({
    isConnected: false,
    connectionState: 'disconnected',
    trainingData: null,
    metrics: null,
    systemStats: null,
    logs: [],
    error: null
  });

  // Referencias para cleanup
  const unsubscribeRefs = useRef<Array<() => void>>([]);
  const logIdCounter = useRef(0);

  // Función para agregar logs
  const addLog = useCallback((message: string, level: LogEntry['level'] = 'info', source?: string) => {
    const logEntry: LogEntry = {
      id: `log_${++logIdCounter.current}`,
      message,
      level,
      timestamp: new Date().toISOString(),
      source
    };

    setState(prev => ({
      ...prev,
      logs: [...prev.logs.slice(-(maxLogs - 1)), logEntry]
    }));
  }, [maxLogs]);

  // Manejadores de eventos
  const handleConnectionEvent = useCallback((event: SupportedEvent) => {
    if (event.type === 'connection') {
      setState(prev => ({
        ...prev,
        isConnected: true,
        connectionState: 'connected',
        error: null
      }));
      addLog('Conectado al servidor en tiempo real', 'info', 'websocket');
    } else if (event.type === 'disconnection') {
      setState(prev => ({
        ...prev,
        isConnected: false,
        connectionState: 'disconnected'
      }));
      addLog('Desconectado del servidor', 'warning', 'websocket');
    }
  }, [addLog]);

  const handleTrainingEvent = useCallback((event: TrainingEvent) => {
    const { data } = event;
    
    setState(prev => ({
      ...prev,
      trainingData: {
        training_id: data.training_id,
        status: (data.status as TrainingData['status']) || 'idle',
        epoch: data.epoch || 0,
        total_epochs: data.total_epochs || 0,
        batch: data.batch,
        total_batches: data.total_batches,
        loss: data.loss,
        accuracy: data.accuracy,
        val_loss: data.val_loss,
        val_accuracy: data.val_accuracy,
        elapsed_time: data.elapsed_time,
        estimated_time_remaining: data.estimated_time_remaining,
        progress: data.total_epochs ? (data.epoch || 0) / data.total_epochs * 100 : 0
      }
    }));

    // Agregar log según el tipo de evento
    switch (event.type) {
      case 'training_started':
        addLog(`Entrenamiento iniciado: ${data.training_id}`, 'info', 'training');
        break;
      case 'training_progress':
        if (data.epoch && data.total_epochs) {
          addLog(`Época ${data.epoch}/${data.total_epochs} - Loss: ${data.loss?.toFixed(4) || 'N/A'}`, 'info', 'training');
        }
        break;
      case 'training_complete':
        addLog(`Entrenamiento completado: ${data.training_id}`, 'info', 'training');
        break;
      case 'training_error':
        addLog(`Error en entrenamiento: ${data.error || 'Error desconocido'}`, 'error', 'training');
        break;
    }
  }, [addLog]);

  const handleMetricsEvent = useCallback((event: MetricsEvent) => {
    const { data } = event;
    
    setState(prev => ({
      ...prev,
      metrics: {
        model_id: data.model_id,
        metrics: data.metrics,
        timestamp: data.timestamp,
        history: prev.metrics?.history || []
      }
    }));

    addLog('Métricas actualizadas', 'debug', 'metrics');
  }, [addLog]);

  const handleSystemEvent = useCallback((event: SystemEvent) => {
    if (!enableSystemStats) return;

    const { data } = event;
    
    setState(prev => ({
      ...prev,
      systemStats: {
        cpu_usage: data.cpu_usage,
        memory_usage: data.memory_usage,
        gpu_usage: data.gpu_usage,
        disk_usage: data.disk_usage,
        timestamp: data.timestamp
      }
    }));
  }, [enableSystemStats]);

  // Función para conectar
  const connect = useCallback(() => {
    if (websocketService.isConnected) {
      return;
    }

    setState(prev => ({ ...prev, connectionState: 'connecting', error: null }));
    
    // Limpiar suscripciones anteriores
    unsubscribeRefs.current.forEach(unsubscribe => unsubscribe());
    unsubscribeRefs.current = [];

    // Suscribirse a eventos
    unsubscribeRefs.current.push(
      websocketService.on('connection', handleConnectionEvent),
      websocketService.on('disconnection', handleConnectionEvent),
      websocketService.on('training_progress', handleTrainingEvent),
      websocketService.on('training_complete', handleTrainingEvent),
      websocketService.on('training_error', handleTrainingEvent),
      websocketService.on('training_started', handleTrainingEvent),
      websocketService.on('metrics_update', handleMetricsEvent),
      websocketService.on('system_stats', handleSystemEvent)
    );

    // Conectar usando Server-Sent Events
    websocketService.connectSSE();
    addLog('Iniciando conexión en tiempo real...', 'info', 'websocket');
  }, [handleConnectionEvent, handleTrainingEvent, handleMetricsEvent, handleSystemEvent, addLog]);

  // Función para desconectar
  const disconnect = useCallback(() => {
    websocketService.disconnect();
    
    // Limpiar suscripciones
    unsubscribeRefs.current.forEach(unsubscribe => unsubscribe());
    unsubscribeRefs.current = [];
    
    setState(prev => ({
      ...prev,
      isConnected: false,
      connectionState: 'disconnected'
    }));
    
    addLog('Desconectado manualmente', 'info', 'websocket');
  }, [addLog]);

  // Función para limpiar logs
  const clearLogs = useCallback(() => {
    setState(prev => ({ ...prev, logs: [] }));
  }, []);

  // Función para refrescar datos
  const refreshData = useCallback(async () => {
    try {
      // Obtener datos del dashboard
      const dashboardData = await ApiService.getDashboardData();
      
      setState(prev => ({
        ...prev,
        metrics: dashboardData.metrics || prev.metrics,
        systemStats: dashboardData.systemStats || prev.systemStats,
        error: null
      }));
      
      addLog('Datos actualizados desde el servidor', 'info', 'api');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
      setState(prev => ({ ...prev, error: errorMessage }));
      addLog(`Error al actualizar datos: ${errorMessage}`, 'error', 'api');
    }
  }, [addLog]);

  // Efecto para auto-conectar
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Cleanup al desmontar
    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  // Efecto para manejar reconexión en errores
  useEffect(() => {
    if (reconnectOnError && state.error && !state.isConnected) {
      const timer = setTimeout(() => {
        addLog('Intentando reconectar...', 'info', 'websocket');
        connect();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [reconnectOnError, state.error, state.isConnected, connect, addLog]);

  return {
    ...state,
    connect,
    disconnect,
    clearLogs,
    refreshData
  };
};

// Hook especializado para entrenamiento
export const useTrainingData = () => {
  const { trainingData, isConnected, logs, connect, disconnect } = useRealTimeData({
    autoConnect: true,
    enableSystemStats: false
  });

  return {
    trainingData,
    isConnected,
    logs: logs.filter(log => log.source === 'training'),
    connect,
    disconnect
  };
};

// Hook especializado para métricas
export const useMetricsData = () => {
  const { metrics, isConnected, refreshData } = useRealTimeData({
    autoConnect: true,
    enableSystemStats: false
  });

  return {
    metrics,
    isConnected,
    refreshData
  };
};

// Hook especializado para estadísticas del sistema
export const useSystemStats = () => {
  const { systemStats, isConnected } = useRealTimeData({
    autoConnect: true,
    enableSystemStats: true
  });

  return {
    systemStats,
    isConnected
  };
};