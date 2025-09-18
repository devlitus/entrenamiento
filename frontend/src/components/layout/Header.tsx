import React from 'react';
import { Button } from '../ui/Button';
import { useTraining } from '../../hooks/useTraining';
import { useSystemMetrics } from '../../hooks/useSystemMetrics';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { isConnected, trainingStatus } = useTraining();
  const { isSystemConnected } = useSystemMetrics();
  
  const getSystemStatus = () => {
    if (isConnected && isSystemConnected) {
      return { text: 'Sistema activo', color: 'bg-[rgb(var(--color-success))]' };
    } else if (isConnected || isSystemConnected) {
      return { text: 'Conexión parcial', color: 'bg-[rgb(var(--color-warning))]' };
    } else {
      return { text: 'Sistema inactivo', color: 'bg-[rgb(var(--color-error))]' };
    }
  };

  const systemStatus = getSystemStatus();
  return (
    <header className="sticky top-0 z-40 bg-[rgb(var(--color-surface))]/95 backdrop-blur-sm border-b border-[rgb(var(--color-border))]">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Botón de menú móvil y breadcrumbs */}
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={onMenuClick}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </Button>
          
          {/* Breadcrumbs */}
          <nav className="hidden sm:flex items-center space-x-2 text-sm">
            <span className="text-[rgb(var(--color-text-secondary))]">Dashboard</span>
            <svg className="w-4 h-4 text-[rgb(var(--color-text-muted))]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span className="text-[rgb(var(--color-text-primary))] font-medium">Entrenamiento</span>
          </nav>
        </div>

        {/* Controles del header */}
        <div className="flex items-center space-x-2 sm:space-x-4">
          {/* Indicador de estado */}
          <div className="hidden sm:flex items-center space-x-2">
            <div className={`w-2 h-2 ${systemStatus.color} rounded-full ${isConnected || isSystemConnected ? 'animate-pulse' : ''}`}></div>
            <span className="text-sm text-[rgb(var(--color-text-secondary))]">{systemStatus.text}</span>
            {trainingStatus?.status === 'training' && (
              <span className="text-xs bg-[rgb(var(--color-warning))]/10 text-[rgb(var(--color-warning))] px-2 py-1 rounded-full">
                Entrenando
              </span>
            )}
          </div>

          {/* Notificaciones */}
          <Button variant="ghost" size="sm" className="relative">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM10.07 2.82l3.12 3.12M7.05 5.84l3.12 3.12M4.03 8.86l3.12 3.12M1.01 11.88l3.12 3.12" />
            </svg>
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-[rgb(var(--color-error))] rounded-full text-xs flex items-center justify-center text-white">
              3
            </span>
          </Button>

          {/* Configuración rápida */}
          <Button variant="ghost" size="sm">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </Button>

          {/* Avatar del usuario */}
          <div className="flex items-center space-x-3">
            <div className="hidden sm:block text-right">
              <p className="text-sm font-medium text-[rgb(var(--color-text-primary))]">Usuario</p>
              <p className="text-xs text-[rgb(var(--color-text-secondary))]">ML Engineer</p>
            </div>
            <div className="w-8 h-8 bg-[rgb(var(--color-primary))] rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-white">U</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};