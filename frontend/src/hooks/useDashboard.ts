import { useState, useEffect, useCallback } from 'react';

interface DashboardOverview {
  system_status: string;
  timestamp: string;
  period_days: number;
  total_trainings: number;
  success_rate: number;
  average_training_time: number;
  total_training_time: number;
}

interface TrainingMetrics {
  loss_history: Array<{ epoch: number; loss: number; val_loss: number }>;
  accuracy_history: Array<{ epoch: number; accuracy: number; val_accuracy: number }>;
}

interface SystemMetrics {
  cpu_usage: Array<{ timestamp: number; value: number }>;
  memory_usage: Array<{ timestamp: number; value: number }>;
  gpu_usage: Array<{ timestamp: number; value: number }>;
}

interface DashboardMetrics {
  timestamp: string;
  metrics: {
    training?: TrainingMetrics;
    system?: SystemMetrics;
  };
}

interface TrainingSession {
  id: string;
  name: string;
  start_time: string;
  end_time: string;
  status: 'completed' | 'failed' | 'running';
  duration_seconds: number;
  total_epochs: number;
  final_metrics: {
    train_loss: number;
    val_loss: number;
    train_mae: number;
    val_mae: number;
  };
  hyperparameters: {
    learning_rate: number;
    batch_size: number;
    epochs: number;
  };
}

interface TrainingSessions {
  timestamp: string;
  sessions: TrainingSession[];
}

interface UseDashboardState {
  overview: DashboardOverview | null;
  metrics: DashboardMetrics | null;
  sessions: TrainingSessions | null;
  isLoading: boolean;
  error: string | null;
}

interface UseDashboardActions {
  refreshOverview: () => Promise<void>;
  refreshMetrics: (type?: string, limit?: number) => Promise<void>;
  refreshSessions: (limit?: number) => Promise<void>;
  refreshAll: () => Promise<void>;
  clearError: () => void;
}

export interface UseDashboardReturn extends UseDashboardState, UseDashboardActions {}

/**
 * Hook personalizado para manejar datos del dashboard
 */
export const useDashboard = (): UseDashboardReturn => {
  const [state, setState] = useState<UseDashboardState>({
    overview: null,
    metrics: null,
    sessions: null,
    isLoading: false,
    error: null,
  });

  /**
   * Obtiene el resumen general del dashboard
   */
  const refreshOverview = useCallback(async (days: number = 30): Promise<void> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(`http://localhost:5000/api/dashboard/overview?days=${days}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: DashboardOverview = await response.json();

      setState(prev => ({
        ...prev,
        overview: data,
        error: null,
      }));

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error obteniendo overview del dashboard';
      setState(prev => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  /**
   * Obtiene métricas detalladas del dashboard
   */
  const refreshMetrics = useCallback(async (type: string = 'all', limit: number = 50): Promise<void> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(`http://localhost:5000/api/dashboard/metrics?type=${type}&limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: DashboardMetrics = await response.json();

      setState(prev => ({
        ...prev,
        metrics: data,
        error: null,
      }));

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error obteniendo métricas del dashboard';
      setState(prev => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  /**
   * Obtiene sesiones de entrenamiento recientes
   */
  const refreshSessions = useCallback(async (limit: number = 10): Promise<void> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(`http://localhost:5000/api/dashboard/training-sessions?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: TrainingSessions = await response.json();

      setState(prev => ({
        ...prev,
        sessions: data,
        error: null,
      }));

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error obteniendo sesiones de entrenamiento';
      setState(prev => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  /**
   * Refresca todos los datos del dashboard
   */
  const refreshAll = useCallback(async (): Promise<void> => {
    await Promise.all([
      refreshOverview(),
      refreshMetrics(),
      refreshSessions(),
    ]);
  }, [refreshOverview, refreshMetrics, refreshSessions]);

  /**
   * Limpia el error actual
   */
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Carga inicial de datos
  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  // Actualización periódica cada 30 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      refreshAll();
    }, 30000);

    return () => clearInterval(interval);
  }, [refreshAll]);

  return {
    ...state,
    refreshOverview,
    refreshMetrics,
    refreshSessions,
    refreshAll,
    clearError,
  };
};

export default useDashboard;