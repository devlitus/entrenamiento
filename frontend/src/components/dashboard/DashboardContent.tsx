import React, { useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { useTraining } from '../../hooks/useTraining';
import { useSystemMetrics } from '../../hooks/useSystemMetrics';
import { useDashboard } from '../../hooks/useDashboard';
import { TrainingChart } from './TrainingChart';
import { SystemMetricsChart } from './SystemMetricsChart';

interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: React.ReactNode;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, change, changeType, icon }) => {
  const changeColors = {
    positive: 'text-[rgb(var(--color-success))]',
    negative: 'text-[rgb(var(--color-error))]',
    neutral: 'text-[rgb(var(--color-text-muted))]'
  };

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-[rgb(var(--color-text-secondary))]">{title}</p>
            <p className="text-2xl font-bold text-[rgb(var(--color-text-primary))]">{value}</p>
            <p className={`text-sm ${changeColors[changeType]}`}>
              {changeType === 'positive' && '↗'} 
              {changeType === 'negative' && '↘'} 
              {change}
            </p>
          </div>
          <div className="p-3 bg-[rgb(var(--color-surface))] rounded-lg">
            {icon}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const ChartPlaceholder: React.FC<{ title: string; height?: string }> = ({ title, height = 'h-64' }) => (
  <Card>
    <CardHeader>
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <div className={`${height} bg-[rgb(var(--color-surface))] rounded-lg flex items-center justify-center border-2 border-dashed border-[rgb(var(--color-border))]`}>
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto text-[rgb(var(--color-text-muted))] mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p className="text-[rgb(var(--color-text-muted))]">Gráfico: {title}</p>
        </div>
      </div>
    </CardContent>
  </Card>
);

export const DashboardContent: React.FC = () => {
  const { 
    trainingStatus, 
    metrics, 
    logs, 
    isConnected, 
    startTraining, 
    stopTraining 
  } = useTraining();
  
  const { 
    systemMetrics, 
    isSystemConnected 
  } = useSystemMetrics();

  const {
    overview,
    metrics: dashboardMetrics,
    sessions,
    isLoading: isDashboardLoading,
    error: dashboardError,
    refreshAll,
    clearError
  } = useDashboard();

  useEffect(() => {
    // Conectar automáticamente al montar el componente
    console.log('Dashboard montado, conexiones WebSocket:', { isConnected, isSystemConnected });
  }, [isConnected, isSystemConnected]);

  // Datos dinámicos basados en el estado real y datos del dashboard
  const dynamicMetrics = [
    {
      title: 'Total de Entrenamientos',
      value: overview?.total_trainings?.toString() || '0',
      change: overview?.success_rate ? `${(overview.success_rate * 100).toFixed(1)}% éxito` : 'Sin datos',
      changeType: (overview?.success_rate && overview.success_rate > 0.8 ? 'positive' : 'neutral') as const,
      icon: (
        <svg className="w-6 h-6 text-[rgb(var(--color-primary))]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      )
    },
    {
      title: 'Estado del Sistema',
      value: overview?.system_status || 'Desconocido',
      change: trainingStatus?.status || 'Inactivo',
      changeType: (overview?.system_status === 'healthy' ? 'positive' : 'negative') as const,
      icon: (
        <svg className="w-6 h-6 text-[rgb(var(--color-success))]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      title: 'Tiempo Promedio',
      value: overview?.average_training_time ? `${Math.floor(overview.average_training_time / 60)}m` : 'N/A',
      change: overview?.total_training_time ? `Total: ${Math.floor(overview.total_training_time / 3600)}h` : 'Sin datos',
      changeType: 'neutral' as const,
      icon: (
        <svg className="w-6 h-6 text-[rgb(var(--color-warning))]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      title: 'Uso de CPU',
      value: systemMetrics?.cpu_percent ? `${systemMetrics.cpu_percent.toFixed(1)}%` : 'N/A',
      change: systemMetrics?.memory_percent ? `RAM: ${systemMetrics.memory_percent.toFixed(1)}%` : 'Sin datos',
      changeType: (systemMetrics?.cpu_percent && systemMetrics.cpu_percent > 80 ? 'negative' : 'positive') as const,
      icon: (
        <svg className="w-6 h-6 text-[rgb(var(--color-info))]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      )
    }
  ];

  const handleStartTraining = async () => {
    const config = {
      model_name: 'test_model',
      epochs: 10,
      learning_rate: 0.001,
      batch_size: 32,
      architecture: {
        layers: [64, 32, 1],
        activation: 'relu'
      }
    };
    
    try {
      await startTraining(config);
      // Refrescar datos del dashboard después de iniciar entrenamiento
      setTimeout(() => refreshAll(), 1000);
    } catch (error) {
      console.error('Error al iniciar entrenamiento:', error);
    }
  };

  // Usar datos reales de sesiones de entrenamiento si están disponibles
  const recentExperiments = sessions?.sessions?.slice(0, 4).map(session => ({
    name: session.name,
    status: session.status === 'completed' ? 'Completado' : 
            session.status === 'failed' ? 'Fallido' : 
            session.status === 'running' ? 'En progreso' : 'Desconocido',
    accuracy: session.final_metrics?.val_mae ? `MAE: ${session.final_metrics.val_mae.toFixed(3)}` : 'N/A',
    time: `${Math.floor(session.duration_seconds / 60)}m ${session.duration_seconds % 60}s`
  })) || [
    {
      name: trainingStatus?.model_name || 'Modelo Actual',
      status: trainingStatus?.status || 'Inactivo',
      accuracy: metrics?.accuracy ? `${(metrics.accuracy * 100).toFixed(1)}%` : 'N/A',
      time: trainingStatus?.elapsed_time ? `${Math.floor(trainingStatus.elapsed_time / 60)}m ${Math.floor(trainingStatus.elapsed_time % 60)}s` : 'N/A'
    },
    { name: 'LSTM Predicción', status: 'Completado', accuracy: '89.1%', time: '45m' },
    { name: 'Random Forest', status: 'Fallido', accuracy: '82.7%', time: '1h 30m' },
    { name: 'SVM Optimizado', status: 'Completado', accuracy: '91.8%', time: '3h 20m' }
  ];

  return (
    <div className="space-y-6 min-w-0">
      {/* Header con acciones */}
      <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] truncate">
            Dashboard de Entrenamiento
          </h1>
          <p className="mt-1 text-sm text-[rgb(var(--color-text-secondary))] break-words">
            Monitorea el progreso de tus modelos de machine learning
            {overview && (
              <span className="ml-2 text-xs bg-[rgb(var(--color-surface))] px-2 py-1 rounded whitespace-nowrap">
                Últimos {overview.period_days} días
              </span>
            )}
          </p>
        </div>
        <div className="flex flex-wrap gap-2 sm:gap-3 sm:flex-nowrap">
          <Button 
            variant="outline" 
            size="sm"
            onClick={refreshAll}
            disabled={isDashboardLoading}
            className="flex-shrink-0"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span className="hidden sm:inline">{isDashboardLoading ? 'Actualizando...' : 'Actualizar'}</span>
            <span className="sm:hidden">↻</span>
          </Button>
          <Button variant="outline" size="sm" className="flex-shrink-0">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span className="hidden sm:inline">Exportar</span>
            <span className="sm:hidden">↓</span>
          </Button>
          <Button 
            variant="primary" 
            size="sm"
            onClick={handleStartTraining}
            disabled={trainingStatus?.status === 'training'}
            className="flex-shrink-0"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="hidden sm:inline">{trainingStatus?.status === 'training' ? 'Entrenando...' : 'Nuevo Experimento'}</span>
            <span className="sm:hidden">+</span>
          </Button>
          {trainingStatus?.status === 'training' && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={stopTraining}
              className="flex-shrink-0"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span className="hidden sm:inline">Detener</span>
              <span className="sm:hidden">×</span>
            </Button>
          )}
        </div>
      </div>

      {/* Error del dashboard */}
      {dashboardError && (
        <Card className="border-[rgb(var(--color-error))] bg-[rgb(var(--color-error))]/5">
          <CardContent className="p-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start min-w-0 flex-1">
                <svg className="w-5 h-5 text-[rgb(var(--color-error))] mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm text-[rgb(var(--color-error))] break-words">Error cargando datos: {dashboardError}</span>
              </div>
              <Button variant="outline" size="sm" onClick={clearError} className="flex-shrink-0">
                Cerrar
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Métricas principales */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        {dynamicMetrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {/* Gráficos principales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <TrainingChart title="Progreso de Entrenamiento" />
        <SystemMetricsChart title="Métricas del Sistema" />
      </div>

      {/* Sección de experimentos recientes */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 sm:gap-6">
        <div className="xl:col-span-2 min-w-0">
          <ChartPlaceholder title="Historial de Experimentos" height="h-80" />
        </div>
        
        <Card className="min-w-0">
          <CardHeader>
            <CardTitle>Experimentos Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentExperiments.map((experiment, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-[rgb(var(--color-surface))] rounded-lg gap-3 min-w-0">
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-[rgb(var(--color-text-primary))] truncate">{experiment.name}</p>
                    <p className="text-sm text-[rgb(var(--color-text-secondary))] truncate">
                      {experiment.accuracy} • {experiment.time}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full whitespace-nowrap flex-shrink-0 ${
                    experiment.status === 'Completado' || experiment.status === 'completed'
                      ? 'bg-[rgb(var(--color-success))]/10 text-[rgb(var(--color-success))]'
                      : experiment.status === 'En progreso' || experiment.status === 'training'
                      ? 'bg-[rgb(var(--color-warning))]/10 text-[rgb(var(--color-warning))]'
                      : experiment.status === 'Inactivo' || experiment.status === 'idle'
                      ? 'bg-[rgb(var(--color-text-muted))]/10 text-[rgb(var(--color-text-muted))]'
                      : 'bg-[rgb(var(--color-error))]/10 text-[rgb(var(--color-error))]'
                  }`}>
                    {experiment.status}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};