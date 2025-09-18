import { baseUrl } from '@/constants/baseUrl';
import type { 
  TrainingParams, 
  PredictionParams, 
  TrainingStatusResponse,
  PredictionResponse,
  ErrorResponse 
} from '@/types/training';

// Configuración base para fetch
const defaultHeaders = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// Clase para manejar errores de API
class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: ErrorResponse
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Función helper para manejar respuestas
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorData: ErrorResponse;
    
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        error: `HTTP ${response.status}: ${response.statusText}`,
        message: 'Error de comunicación con el servidor'
      };
    }
    
    throw new ApiError(
      errorData.message || errorData.error || 'Error desconocido',
      response.status,
      errorData
    );
  }
  
  return response.json();
}

// Servicio principal de API
export class ApiService {
  private static baseUrl = baseUrl;

  // Métodos de entrenamiento
  static async startTraining(params: TrainingParams): Promise<{ training_id: string }> {
    const response = await fetch(`${this.baseUrl}/api/training/start`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify(params)
    });
    
    return handleResponse(response);
  }

  static async stopTraining(trainingId: string): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/api/training/stop`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({ training_id: trainingId })
    });
    
    return handleResponse(response);
  }

  static async getTrainingStatus(trainingId: string): Promise<TrainingStatusResponse> {
    const response = await fetch(`${this.baseUrl}/api/training/status/${trainingId}`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  static async getTrainingHistory(): Promise<TrainingStatusResponse[]> {
    const response = await fetch(`${this.baseUrl}/api/training/history`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  // Métodos de predicción
  static async makePrediction(params: PredictionParams): Promise<PredictionResponse> {
    const response = await fetch(`${this.baseUrl}/api/predictions/predict`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify(params)
    });
    
    return handleResponse(response);
  }

  // Métodos de métricas y estadísticas
  static async getModelMetrics(modelId?: string): Promise<any> {
    const url = modelId 
      ? `${this.baseUrl}/api/metrics/model/${modelId}`
      : `${this.baseUrl}/api/metrics/latest`;
      
    const response = await fetch(url, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  static async getSystemStats(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/stats/system`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  static async getDashboardData(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/dashboard/data`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  // Método para verificar conectividad
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }

  // Método para obtener configuración del servidor
  static async getServerConfig(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/config`, {
      method: 'GET',
      headers: defaultHeaders
    });
    
    return handleResponse(response);
  }
}

// Exportar también la clase de error para uso externo
export { ApiError };

// Tipos para respuestas comunes
export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface ServerConfigResponse {
  version: string;
  environment: string;
  features: string[];
}