import React from 'react';
import { NavigationItem } from './Navigation';

// Iconos SVG como componentes React
export const DashboardIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"
    }),
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"
    })
  )
);

export const AnalysisIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
    })
  )
);

export const TrainingIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M13 10V3L4 14h7v7l9-11h-7z"
    })
  )
);

export const ModelsIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
    })
  )
);

export const ConfigIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
    }),
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M15 12a3 3 0 11-6 0 3 3 0 016 0z"
    })
  )
);

export const PredictionsIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
    })
  )
);

export const ExperimentsIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  React.createElement('svg', {
    className,
    fill: "none",
    stroke: "currentColor",
    viewBox: "0 0 24 24"
  },
    React.createElement('path', {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      strokeWidth: 2,
      d: "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
    })
  )
);

// Configuración de navegación principal
export const createNavigationItems = (currentPath: string = ''): NavigationItem[] => [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: React.createElement(DashboardIcon),
    path: '/dashboard',
    active: currentPath === '/dashboard' || currentPath === '/'
  },
  {
    id: 'analysis',
    label: 'Análisis',
    icon: React.createElement(AnalysisIcon),
    path: '/analysis',
    active: currentPath === '/analysis'
  },
  {
    id: 'training',
    label: 'Entrenamiento',
    icon: React.createElement(TrainingIcon),
    path: '/training',
    active: currentPath === '/training'
  },
  {
    id: 'models',
    label: 'Modelos',
    icon: React.createElement(ModelsIcon),
    path: '/models',
    active: currentPath === '/models'
  },
  {
    id: 'predictions',
    label: 'Predicciones',
    icon: React.createElement(PredictionsIcon),
    path: '/predictions',
    active: currentPath === '/predictions'
  },
  {
    id: 'experiments',
    label: 'Experimentos',
    icon: React.createElement(ExperimentsIcon),
    path: '/experiments',
    active: currentPath === '/experiments'
  },
  {
    id: 'config',
    label: 'Configuración',
    icon: React.createElement(ConfigIcon),
    path: '/config',
    active: currentPath === '/config'
  }
];

export default createNavigationItems;