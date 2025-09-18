import { io, Socket } from 'socket.io-client';

// Configuración de entrenamiento
export interface TrainingConfig {
  learningRate: number;
  epochs: number;
  batchSize: number;
  trainingDataSize: number;
  modelType?: 'single' | 'multi';
  activation?: string;
}

// Métricas de entrenamiento
export interface TrainingMetrics {
  epoch: number;
  totalEpochs: number;
  progress: number;
  loss: number;
  valLoss?: number;
  accuracy?: number;
  valAccuracy?: number;
  timestamp: string;
}

// Estado del entrenamiento
export interface TrainingStatus {
  isTraining: boolean;
  isPaused: boolean;
  currentEpoch?: number;
  totalEpochs?: number;
  progress?: number;
  startTime?: string;
  elapsedTime?: number;
}

// Logs de entrenamiento
export interface TrainingLog {
  message: string;
  level: 'info' | 'warning' | 'error';
  timestamp?: string;
}

// Callback para eventos WebSocket
export type WebSocketEventCallback<T = any> = (data: T) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private isConnected = false;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  /**
   * Conecta al servidor WebSocket
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.socket = io('http://localhost:5000', {
          transports: ['websocket', 'polling'],
          timeout: 10000,
          reconnection: true,
          reconnectionAttempts: this.maxReconnectAttempts,
          reconnectionDelay: this.reconnectDelay,
        });

        this.socket.on('connect', () => {
          console.log('✅ WebSocket conectado al backend');
          this.isConnected = true;
          this.reconnectAttempts = 0;
          resolve();
        });

        this.socket.on('disconnect', (reason) => {
          console.log('❌ WebSocket desconectado:', reason);
          this.isConnected = false;
        });

        this.socket.on('connect_error', (error) => {
          console.error('❌ Error de conexión WebSocket:', error);
          this.isConnected = false;
          
          if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            reject(new Error(`No se pudo conectar después de ${this.maxReconnectAttempts} intentos`));
          }
          this.reconnectAttempts++;
        });

        this.socket.on('reconnect', (attemptNumber) => {
          console.log(`🔄 WebSocket reconectado después de ${attemptNumber} intentos`);
          this.isConnected = true;
          this.reconnectAttempts = 0;
        });

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Desconecta del servidor WebSocket
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      console.log('🔌 WebSocket desconectado manualmente');
    }
  }

  /**
   * Verifica si está conectado
   */
  getConnectionStatus(): boolean {
    return this.isConnected && this.socket?.connected === true;
  }

  /**
   * Inicia el entrenamiento con la configuración especificada
   */
  startTraining(config: TrainingConfig): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('WebSocket no está conectado');
    }

    console.log('🚀 Iniciando entrenamiento:', config);
    this.socket.emit('start_training', config);
  }

  /**
   * Detiene el entrenamiento actual
   */
  stopTraining(): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('WebSocket no está conectado');
    }

    console.log('⏹️ Deteniendo entrenamiento');
    this.socket.emit('stop_training');
  }

  /**
   * Pausa el entrenamiento actual
   */
  pauseTraining(): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('WebSocket no está conectado');
    }

    console.log('⏸️ Pausando entrenamiento');
    this.socket.emit('pause_training');
  }

  /**
   * Reanuda el entrenamiento pausado
   */
  resumeTraining(): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('WebSocket no está conectado');
    }

    console.log('▶️ Reanudando entrenamiento');
    this.socket.emit('resume_training');
  }

  /**
   * Solicita el estado actual del entrenamiento
   */
  getTrainingStatus(): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('WebSocket no está conectado');
    }

    this.socket.emit('get_training_status');
  }

  /**
   * Registra un callback para actualizaciones de entrenamiento
   */
  onTrainingUpdate(callback: WebSocketEventCallback<TrainingMetrics>): void {
    if (!this.socket) return;
    this.socket.on('training_update', callback);
  }

  /**
   * Registra un callback para logs de entrenamiento
   */
  onTrainingLog(callback: WebSocketEventCallback<TrainingLog>): void {
    if (!this.socket) return;
    this.socket.on('training_log', callback);
  }

  /**
   * Registra un callback para errores de entrenamiento
   */
  onTrainingError(callback: WebSocketEventCallback<{ error: string }>): void {
    if (!this.socket) return;
    this.socket.on('training_error', callback);
  }

  /**
   * Registra un callback para el estado del entrenamiento
   */
  onTrainingStatus(callback: WebSocketEventCallback<TrainingStatus>): void {
    if (!this.socket) return;
    this.socket.on('training_status', callback);
  }

  /**
   * Registra un callback para cuando el entrenamiento se completa
   */
  onTrainingComplete(callback: WebSocketEventCallback<any>): void {
    if (!this.socket) return;
    this.socket.on('training_complete', callback);
  }

  /**
   * Remueve todos los listeners de un evento específico
   */
  removeAllListeners(event?: string): void {
    if (!this.socket) return;
    
    if (event) {
      this.socket.removeAllListeners(event);
    } else {
      // Remover listeners de eventos de entrenamiento
      const trainingEvents = [
        'training_update',
        'training_log', 
        'training_error',
        'training_status',
        'training_complete'
      ];
      
      trainingEvents.forEach(eventName => {
        this.socket?.removeAllListeners(eventName);
      });
    }
  }

  /**
   * Remueve un listener específico
   */
  removeListener(event: string, callback: WebSocketEventCallback): void {
    if (!this.socket) return;
    this.socket.off(event, callback);
  }
}

// Instancia singleton del servicio WebSocket
export const websocketService = new WebSocketService();

export default websocketService;