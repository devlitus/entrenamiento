// Tipos centralizados basados en swagger-api.json
// Este archivo contiene todas las interfaces de la API para evitar duplicación

// ===== TIPOS DE RESPUESTA COMUNES =====
export interface ErrorResponse {
  error: string;
  message: string;
  details?: object;
}

// ===== TIPOS DE PREDICCIÓN =====
export interface PredictionParams {
  input_data: number[];
  model_id?: string;
}

export interface PredictionResponse {
  prediction: number[];
  confidence?: number;
  model_used?: string;
  processing_time?: number;
}

// ===== TIPOS DE ENTRENAMIENTO =====
export interface TrainingParams {
  epochs: number;
  learning_rate: number;
  batch_size?: number;
  architecture?: object;
}

export interface TrainingResponse {
  status: string;
  message: string;
  training_id?: string;
}

// ===== TIPOS DE ESTADO DE ENTRENAMIENTO =====
export interface MetricsResponse {
  loss: number;
  epoch: number;
  accuracy?: number;
  training_time?: number;
  validation_loss?: number;
}

export interface TrainingStatusResponse {
  status: string;
  is_training: boolean;
  current_epoch?: number;
  total_epochs?: number;
  metrics?: MetricsResponse;
}

// ===== TIPOS DE DASHBOARD =====
export interface DashboardResponse {
  total_trainings: number;
  active_trainings?: number;
  completed_trainings?: number;
  average_accuracy?: number;
}

// ===== TIPOS EXTENDIDOS PARA WEBSOCKET =====
export interface TrainingConfig {
  name: string;
  epochs: number;
  learning_rate: number;
  batch_size: number;
  validation_split?: number;
  early_stopping?: boolean;
  patience?: number;
  architecture?: object;
  optimizer?: string;
  loss_function?: string;
  metrics?: string[];
}

export interface TrainingMetrics {
  epoch: number;
  total_epochs: number;
  loss: number;
  accuracy?: number;
  val_loss?: number;
  val_accuracy?: number;
  learning_rate: number;
  batch: number;
  total_batches: number;
  elapsed_time: number;
  estimated_time_remaining?: number;
  timestamp: string;
}

export interface TrainingStatus {
  is_training: boolean;
  is_paused: boolean;
  current_epoch: number;
  total_epochs: number;
  progress_percentage: number;
  start_time?: string;
  elapsed_time: number;
  status_message: string;
  model_name?: string;
}

export interface TrainingLog {
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  timestamp: string;
  epoch?: number;
  batch?: number;
  component?: string;
}

export interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  gpu_usage?: number;
  gpu_memory?: number;
  disk_usage?: number;
  timestamp: string;
}

export type WebSocketEventCallback<T = any> = (data: T) => void;