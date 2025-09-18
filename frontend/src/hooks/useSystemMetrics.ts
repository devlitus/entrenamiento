import { useState, useEffect, useCallback } from 'react';

interface CpuStats {
  usage_percent: number;
  cores: number;
  frequency?: number;
}

interface MemoryStats {
  usage_percent: number;
  total_gb: number;
  available_gb?: number;
  used_gb: number;
}

interface DiskStats {
  usage_percent: number;
  total_gb: number;
  free_gb?: number;
  used_gb: number;
}

interface GpuStats {
  usage_percent: number;
  memory_usage_percent: number;
  temperature: number;
  name: string;
}

interface SystemStatsResponse {
  timestamp: string;
  cpu: CpuStats;
  memory: MemoryStats;
  disk: DiskStats;
  gpu?: GpuStats;
}

interface SystemMetrics {
  cpu: number;
  memory: number;
  gpu: number;
  temperature: number;
  memory_total_gb?: number;
  memory_used_gb?: number;
  gpu_info?: GpuStats;
  disk_usage?: number;
  timestamp?: string;
}

interface UseSystemMetricsState {
  systemMetrics: SystemMetrics;
  isSystemConnected: boolean;
  error: string | null;
}

interface UseSystemMetricsActions {
  refreshMetrics: () => Promise<void>;
  clearError: () => void;
}

export interface UseSystemMetricsReturn extends UseSystemMetricsState, UseSystemMetricsActions {}

/**
 * Hook personalizado para manejar métricas del sistema en tiempo real
 */
export const useSystemMetrics = (): UseSystemMetricsReturn => {
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics>({
    cpu: 0,
    memory: 0,
    gpu: 0,
    temperature: 0,
  });
  const [isSystemConnected, setIsSystemConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSystemMetrics = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/dashboard/system-stats', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data: SystemStatsResponse = await response.json();
        setSystemMetrics({
          cpu: data.cpu.usage_percent,
          memory: data.memory.usage_percent,
          gpu: data.gpu?.usage_percent || 0,
          temperature: data.gpu?.temperature || 0,
          memory_total_gb: data.memory.total_gb,
          memory_used_gb: data.memory.used_gb,
          disk_usage: data.disk.usage_percent,
          timestamp: data.timestamp,
          gpu_info: data.gpu ? {
            usage_percent: data.gpu.usage_percent,
            memory_usage_percent: data.gpu.memory_usage_percent,
            temperature: data.gpu.temperature,
            name: data.gpu.name
          } : undefined
        });
        setIsSystemConnected(true);
        setError(null);
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (err) {
      console.error('Error fetching system metrics:', err);
      setError(err instanceof Error ? err.message : 'Error desconocido');
      setIsSystemConnected(false);
    }
  }, []);

  const refreshMetrics = useCallback(async (): Promise<void> => {
    await fetchSystemMetrics();
  }, [fetchSystemMetrics]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Fetch inicial y polling cada 5 segundos
  useEffect(() => {
    fetchSystemMetrics();
    const interval = setInterval(fetchSystemMetrics, 5000);
    return () => clearInterval(interval);
  }, [fetchSystemMetrics]);

  return {
    systemMetrics,
    isSystemConnected,
    error,
    refreshMetrics,
    clearError,
  };
};

export default useSystemMetrics;