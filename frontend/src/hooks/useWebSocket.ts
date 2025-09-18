import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { TrainingStatusResponse, MetricsResponse } from '../types/training';

interface UseWebSocketReturn {
  socket: Socket | null;
  isConnected: boolean;
  trainingStatus: TrainingStatusResponse | null;
  metrics: MetricsResponse | null;
  logs: string[];
  startTraining: (config: any) => void;
  stopTraining: () => void;
  pauseTraining: () => void;
  resumeTraining: () => void;
}

export const useWebSocket = (): UseWebSocketReturn => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [trainingStatus, setTrainingStatus] = useState<TrainingStatusResponse | null>(null);
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    // Conectar al servidor WebSocket
    const newSocket = io('http://localhost:5000');
    
    newSocket.on('connect', () => {
      console.log('Conectado al servidor WebSocket');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Desconectado del servidor WebSocket');
      setIsConnected(false);
    });

    // Eventos de entrenamiento
    newSocket.on('training_update', (data: any) => {
      console.log('Métricas recibidas:', data);
      setMetrics(data);
    });

    newSocket.on('advanced_training_update', (data: any) => {
      console.log('Métricas avanzadas recibidas:', data);
      setMetrics(data);
    });

    newSocket.on('training_complete', (data: any) => {
      console.log('Entrenamiento completado:', data);
      setLogs(prev => [...prev.slice(-49), '[INFO] Entrenamiento completado exitosamente']);
    });

    newSocket.on('training_log', (data: { message: string; level: string }) => {
      setLogs(prev => [...prev.slice(-49), `[${data.level.toUpperCase()}] ${data.message}`]);
    });

    newSocket.on('training_error', (data: { error: string }) => {
      setLogs(prev => [...prev.slice(-49), `[ERROR] ${data.error}`]);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const startTraining = (config: any) => {
    if (socket) {
      socket.emit('start_training', config);
    }
  };

  const stopTraining = () => {
    if (socket) {
      socket.emit('stop_training');
    }
  };

  const pauseTraining = () => {
    if (socket) {
      socket.emit('pause_training');
    }
  };

  const resumeTraining = () => {
    if (socket) {
      socket.emit('resume_training');
    }
  };

  return {
    socket,
    isConnected,
    trainingStatus,
    metrics,
    logs,
    startTraining,
    stopTraining,
    pauseTraining,
    resumeTraining
  };
};