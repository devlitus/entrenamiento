import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { useSystemMetrics } from '../../hooks/useSystemMetrics';

interface SystemMetricsChartProps {
  title: string;
  height?: string;
}

export const SystemMetricsChart: React.FC<SystemMetricsChartProps> = ({ title, height = 'h-64' }) => {
  const { systemMetrics, isSystemConnected } = useSystemMetrics();

  const renderSystemMetrics = () => {
    if (!isSystemConnected || !systemMetrics) {
      return (
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto text-[rgb(var(--color-text-muted))] mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
          </svg>
          <p className="text-[rgb(var(--color-text-muted))]">Esperando métricas del sistema...</p>
        </div>
      );
    }

    const getCpuColor = (percent: number) => {
      if (percent > 80) return 'rgb(var(--color-error))';
      if (percent > 60) return 'rgb(var(--color-warning))';
      return 'rgb(var(--color-success))';
    };

    const getMemoryColor = (percent: number) => {
      if (percent > 85) return 'rgb(var(--color-error))';
      if (percent > 70) return 'rgb(var(--color-warning))';
      return 'rgb(var(--color-info))';
    };

    return (
      <div className="space-y-4">
        {/* CPU Usage */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-[rgb(var(--color-text-secondary))]">Uso de CPU</span>
            <span className="text-[rgb(var(--color-text-primary))] font-medium">
              {systemMetrics.cpu_stats?.usage_percent?.toFixed(1) || 0}%
            </span>
          </div>
          <div className="w-full bg-[rgb(var(--color-surface))] rounded-full h-2">
            <div 
              className="h-2 rounded-full transition-all duration-300"
              style={{ 
                width: `${systemMetrics.cpu_stats?.usage_percent || 0}%`,
                backgroundColor: getCpuColor(systemMetrics.cpu_stats?.usage_percent || 0)
              }}
            />
          </div>
        </div>

        {/* Memory Usage */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-[rgb(var(--color-text-secondary))]">Uso de Memoria</span>
            <span className="text-[rgb(var(--color-text-primary))] font-medium">
              {systemMetrics.memory_stats?.usage_percent?.toFixed(1) || 0}%
            </span>
          </div>
          <div className="w-full bg-[rgb(var(--color-surface))] rounded-full h-2">
            <div 
              className="h-2 rounded-full transition-all duration-300"
              style={{ 
                width: `${systemMetrics.memory_stats?.usage_percent || 0}%`,
                backgroundColor: getMemoryColor(systemMetrics.memory_stats?.usage_percent || 0)
              }}
            />
          </div>
        </div>

        {/* GPU and Disk metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">GPU</p>
            <p className="text-sm font-semibold text-[rgb(var(--color-text-primary))]">
              {systemMetrics.gpu_stats?.usage_percent?.toFixed(1) || 0}%
            </p>
          </div>
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">Disco</p>
            <p className="text-sm font-semibold text-[rgb(var(--color-text-primary))]">
              {systemMetrics.disk_stats?.usage_percent?.toFixed(1) || 0}%
            </p>
          </div>
        </div>

        {/* Detailed metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">Memoria Total</p>
            <p className="text-sm font-semibold text-[rgb(var(--color-text-primary))]">
              {systemMetrics.memory_stats?.total_gb ? `${systemMetrics.memory_stats.total_gb.toFixed(1)} GB` : 'N/A'}
            </p>
          </div>
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">Memoria Usada</p>
            <p className="text-sm font-semibold text-[rgb(var(--color-text-primary))]">
              {systemMetrics.memory_stats?.used_gb ? `${systemMetrics.memory_stats.used_gb.toFixed(1)} GB` : 'N/A'}
            </p>
          </div>
        </div>

        {/* GPU info if available */}
        {systemMetrics.gpu_stats && (
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-2">GPU</p>
            <div className="space-y-1">
              <p className="text-xs text-[rgb(var(--color-text-primary))]">
                Nombre: {systemMetrics.gpu_stats.name || 'N/A'}
              </p>
              <p className="text-xs text-[rgb(var(--color-text-primary))]">
                Memoria: {systemMetrics.gpu_stats.memory_usage_percent?.toFixed(1) || 0}%
              </p>
              <p className="text-xs text-[rgb(var(--color-text-primary))]">
                Utilización: {systemMetrics.gpu_stats.usage_percent?.toFixed(1) || 0}%
              </p>
              {systemMetrics.gpu_stats.temperature && (
                <p className="text-xs text-[rgb(var(--color-text-primary))]">
                  Temperatura: {systemMetrics.gpu_stats.temperature.toFixed(1)}°C
                </p>
              )}
            </div>
          </div>
        )}

        {/* Connection status */}
        <div className="flex items-center justify-center pt-2">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isSystemConnected ? 'bg-[rgb(var(--color-success))] animate-pulse' : 'bg-[rgb(var(--color-error))]'}`}></div>
            <span className="text-xs text-[rgb(var(--color-text-secondary))]">
              {isSystemConnected ? 'Conectado' : 'Desconectado'}
            </span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className={`${height} flex items-center justify-center`}>
          {renderSystemMetrics()}
        </div>
      </CardContent>
    </Card>
  );
};