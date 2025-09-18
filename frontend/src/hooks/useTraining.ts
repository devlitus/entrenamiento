import { useState, useEffect, useCallback, useRef } from 'react';
import { websocketService } from '@/services/websocket';
import type { TrainingConfig, TrainingMetrics, TrainingStatus, TrainingLog } from '@/types/training';

interface UseTrainingState {
  isConnected: boolean;
  isTraining: boolean;
  currentEpoch: number;
  totalEpochs: number;
  metrics: TrainingMetrics | null;
  status: TrainingStatus | null;
  logs: TrainingLog[];
  error: string | null;
  progress: number;
}

interface UseTrainingActions {
  connect: () => Promise<void>;
  disconnect: () => void;
  startTraining: (config: TrainingConfig) => Promise<void>;
  stopTraining: () => void;
  pauseTraining: () => void;
  resumeTraining: () => void;
  getStatus: () => void;
  clearLogs: () => void;
  clearError: () => void;
}

export interface UseTrainingReturn extends UseTrainingState, UseTrainingActions {}

/**
 * Hook personalizado para manejar el entrenamiento de modelos ML en tiempo real
 * Gestiona la conexión WebSocket, estado del entrenamiento y eventos en tiempo real
 */
export const useTraining = (): UseTrainingReturn => {
  // Estado del hook
  const [state, setState] = useState<UseTrainingState>({
    isConnected: false,
    isTraining: false,
    currentEpoch: 0,
    totalEpochs: 0,
    metrics: null,
    status: null,
    logs: [],
    error: null,
    progress: 0,
  });

  // Referencias para evitar re-renders innecesarios
  const isConnectingRef = useRef(false);
  const maxLogsRef = useRef(100); // Límite de logs para evitar memory leaks

  /**
   * Conecta al servidor WebSocket
   */
  const connect = useCallback(async (): Promise<void> => {
    if (isConnectingRef.current || websocketService.getConnectionStatus()) {
      return;
    }

    try {
      isConnectingRef.current = true;
      setState(prev => ({ ...prev, error: null }));

      await websocketService.connect();
      
      setState(prev => ({ ...prev, isConnected: true }));
      console.log('✅ Hook useTraining: Conectado al WebSocket');

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error de conexión desconocido';
      setState(prev => ({ 
        ...prev, 
        isConnected: false, 
        error: errorMessage 
      }));
      console.error('❌ Hook useTraining: Error de conexión:', errorMessage);
    } finally {
      isConnectingRef.current = false;
    }
  }, []);

  /**
   * Desconecta del servidor WebSocket
   */
  const disconnect = useCallback((): void => {
    websocketService.disconnect();
    setState(prev => ({ 
      ...prev, 
      isConnected: false,
      isTraining: false,
      error: null
    }));
    console.log('🔌 Hook useTraining: Desconectado del WebSocket');
  }, []);

  /**
   * Inicia el entrenamiento con la configuración especificada
   */
  const startTraining = useCallback(async (config: TrainingConfig): Promise<void> => {
    try {
      if (!websocketService.getConnectionStatus()) {
        await connect();
      }

      websocketService.startTraining(config);
      
      setState(prev => ({ 
        ...prev, 
        isTraining: true,
        totalEpochs: config.epochs || 100,
        currentEpoch: 0,
        progress: 0,
        error: null,
        logs: []
      }));

      console.log('🚀 Hook useTraining: Entrenamiento iniciado', config);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error al iniciar entrenamiento';
      setState(prev => ({ ...prev, error: errorMessage }));
      console.error('❌ Hook useTraining: Error al iniciar entrenamiento:', errorMessage);
    }
  }, [connect]);

  /**
   * Detiene el entrenamiento actual
   */
  const stopTraining = useCallback((): void => {
    try {
      websocketService.stopTraining();
      setState(prev => ({ 
        ...prev, 
        isTraining: false,
        progress: 0,
        error: null
      }));
      console.log('⏹️ Hook useTraining: Entrenamiento detenido');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error al detener entrenamiento';
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, []);

  /**
   * Pausa el entrenamiento actual
   */
  const pauseTraining = useCallback((): void => {
    try {
      websocketService.pauseTraining();
      console.log('⏸️ Hook useTraining: Entrenamiento pausado');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error al pausar entrenamiento';
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, []);

  /**
   * Reanuda el entrenamiento pausado
   */
  const resumeTraining = useCallback((): void => {
    try {
      websocketService.resumeTraining();
      console.log('▶️ Hook useTraining: Entrenamiento reanudado');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error al reanudar entrenamiento';
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, []);

  /**
   * Solicita el estado actual del entrenamiento
   */
  const getStatus = useCallback((): void => {
    try {
      websocketService.getTrainingStatus();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error al obtener estado';
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, []);

  /**
   * Limpia los logs acumulados
   */
  const clearLogs = useCallback((): void => {
    setState(prev => ({ ...prev, logs: [] }));
  }, []);

  /**
   * Limpia el error actual
   */
  const clearError = useCallback((): void => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Configurar listeners de WebSocket al montar el componente
  useEffect(() => {
    // Handler para actualizaciones de métricas de entrenamiento
    const handleTrainingUpdate = (metrics: TrainingMetrics) => {
      setState(prev => {
        const newEpoch = metrics.epoch || prev.currentEpoch;
        const progress = prev.totalEpochs > 0 ? Math.round((newEpoch / prev.totalEpochs) * 100) : 0;
        
        return {
          ...prev,
          metrics,
          currentEpoch: newEpoch,
          progress,
          isTraining: true
        };
      });
    };

    // Handler para logs de entrenamiento
    const handleTrainingLog = (log: TrainingLog) => {
      setState(prev => {
        const newLogs = [...prev.logs, log];
        // Mantener solo los últimos N logs para evitar memory leaks
        if (newLogs.length > maxLogsRef.current) {
          newLogs.splice(0, newLogs.length - maxLogsRef.current);
        }
        return { ...prev, logs: newLogs };
      });
    };

    // Handler para errores de entrenamiento
    const handleTrainingError = (errorData: { error: string }) => {
      setState(prev => ({ 
        ...prev, 
        error: errorData.error,
        isTraining: false
      }));
    };

    // Handler para estado del entrenamiento
    const handleTrainingStatus = (status: TrainingStatus) => {
      setState(prev => ({ 
        ...prev, 
        status,
        isTraining: status.is_training || false
      }));
    };

    // Handler para entrenamiento completado
    const handleTrainingComplete = (data: any) => {
      setState(prev => ({ 
        ...prev, 
        isTraining: false,
        progress: 100
      }));
      console.log('🎉 Hook useTraining: Entrenamiento completado', data);
    };

    // Registrar listeners
    websocketService.onTrainingUpdate(handleTrainingUpdate);
    websocketService.onTrainingLog(handleTrainingLog);
    websocketService.onTrainingError(handleTrainingError);
    websocketService.onTrainingStatus(handleTrainingStatus);
    websocketService.onTrainingComplete(handleTrainingComplete);

    // Cleanup al desmontar
    return () => {
      websocketService.removeAllListeners();
    };
  }, []);

  // Verificar estado de conexión periódicamente
  useEffect(() => {
    const checkConnection = () => {
      const isConnected = websocketService.getConnectionStatus();
      setState(prev => {
        if (prev.isConnected !== isConnected) {
          return { ...prev, isConnected };
        }
        return prev;
      });
    };

    const interval = setInterval(checkConnection, 2000);
    return () => clearInterval(interval);
  }, []);

  return {
    // Estado
    ...state,
    // Acciones
    connect,
    disconnect,
    startTraining,
    stopTraining,
    pauseTraining,
    resumeTraining,
    getStatus,
    clearLogs,
    clearError,
  };
};

export default useTraining;