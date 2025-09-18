// import { StrictMode } from "react"; // Removido temporalmente para evitar dobles renders
import { createRoot } from "react-dom/client";
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { App } from "./App";
import "./index.css";

// Registrar componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Renderizar la aplicación
const container = document.getElementById("root");

if (container) {
  const root = createRoot(container);

  root.render(
    <App />
  );
} else {
  console.error('No se encontró el elemento con ID "root" en el DOM.');
}
