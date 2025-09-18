import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ModelPerformanceDashboard } from "./pages/ModelPerformanceDashboard";
import { ModelArchitecture } from "./pages/ModelArchitecture";
import { DatasetPage } from "./pages/DatasetPage";
import { ExperimentsPage } from "./pages/ExperimentsPage";
import { DashboardLayout } from "./components/layout/DashboardLayout";
import { useTrainingStore } from './store/trainingStore';

export function App() {
  const { connect, disconnect } = useTrainingStore();

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); 

  return (
    <Router>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<ModelPerformanceDashboard />} />
          <Route path="/models" element={<ModelArchitecture />} />
          <Route path="/dataset" element={<DatasetPage />} />
          <Route path="/experiments" element={<ExperimentsPage />} />
        </Routes>
      </DashboardLayout>
    </Router>
  );
}
