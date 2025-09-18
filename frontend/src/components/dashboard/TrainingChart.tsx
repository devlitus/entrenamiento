import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { useTraining } from '../../hooks/useTraining';

interface TrainingChartProps {
  title: string;
  height?: string;
}

export const TrainingChart: React.FC<TrainingChartProps> = ({ title, height = 'h-64' }) => {
  const { metrics, trainingStatus, logs } = useTraining();

  const renderProgressChart = () => {
    if (!trainingStatus || !metrics) {
      return (
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto text-[rgb(var(--color-text-muted))] mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p className="text-[rgb(var(--color-text-muted))]">Esperando datos de entrenamiento...</p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {/* Barra de progreso */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-[rgb(var(--color-text-secondary))]">Progreso del Entrenamiento</span>
            <span className="text-[rgb(var(--color-text-primary))] font-medium">
              {trainingStatus.progress?.toFixed(1) || 0}%
            </span>
          </div>
          <div className="w-full bg-[rgb(var(--color-surface))] rounded-full h-2">
            <div 
              className="bg-[rgb(var(--color-primary))] h-2 rounded-full transition-all duration-300"
              style={{ width: `${trainingStatus.progress || 0}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-[rgb(var(--color-text-muted))]">
            <span>Época {trainingStatus.current_epoch || 0}</span>
            <span>de {trainingStatus.total_epochs || 0}</span>
          </div>
        </div>

        {/* Métricas actuales */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">Precisión</p>
            <p className="text-lg font-semibold text-[rgb(var(--color-success))]">
              {metrics.accuracy ? (metrics.accuracy * 100).toFixed(2) : '0.00'}%
            </p>
          </div>
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-1">Pérdida</p>
            <p className="text-lg font-semibold text-[rgb(var(--color-error))]">
              {metrics.loss?.toFixed(4) || '0.0000'}
            </p>
          </div>
        </div>

        {/* Logs recientes */}
        {logs && logs.length > 0 && (
          <div className="bg-[rgb(var(--color-surface))] p-3 rounded-lg">
            <p className="text-xs text-[rgb(var(--color-text-secondary))] mb-2">Logs Recientes</p>
            <div className="space-y-1 max-h-20 overflow-y-auto">
              {logs.slice(-3).map((log, index) => (
                <p key={index} className="text-xs text-[rgb(var(--color-text-primary))] font-mono">
                  {log.message}
                </p>
              ))}
            </div>
          </div>
        )}
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
          {renderProgressChart()}
        </div>
      </CardContent>
    </Card>
  );
};