import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { DashboardContent } from '../components/dashboard/DashboardContent';

// Componentes de p?gina placeholder (se pueden crear m?s adelante)
const AnalysisPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">An?lisis</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">P?gina de an?lisis de datos y m?tricas.</p>
  </div>
);

const TrainingPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">Entrenamiento</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">Configuraci?n y monitoreo de entrenamientos.</p>
  </div>
);

const ModelsPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">Modelos</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">Gesti?n de modelos de machine learning.</p>
  </div>
);

const PredictionsPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">Predicciones</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">Realizar y visualizar predicciones.</p>
  </div>
);

const ExperimentsPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">Experimentos</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">Gesti?n de experimentos de ML.</p>
  </div>
);

const ConfigPage: React.FC = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">Configuraci?n</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">Configuraci?n del sistema y preferencias.</p>
  </div>
);

const NotFoundPage: React.FC = () => (
  <div className="p-6 text-center">
    <h1 className="text-2xl font-bold text-[rgb(var(--color-text-primary))] mb-4">404 - P?gina no encontrada</h1>
    <p className="text-[rgb(var(--color-text-secondary))]">La p?gina que buscas no existe.</p>
  </div>
);

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <DashboardLayout>
        <Routes>
          {/* Ruta por defecto redirige al dashboard */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          
          {/* Rutas principales */}
          <Route path="/dashboard" element={<DashboardContent />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/training" element={<TrainingPage />} />
          <Route path="/models" element={<ModelsPage />} />
          <Route path="/predictions" element={<PredictionsPage />} />
          <Route path="/experiments" element={<ExperimentsPage />} />
          <Route path="/config" element={<ConfigPage />} />
          
          {/* Ruta 404 */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </DashboardLayout>
    </BrowserRouter>
  );
};

export default AppRouter;