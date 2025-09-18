// Servicios principales
export { ApiService, ApiError } from './api';
export { WebSocketService, websocketService } from './websocket';

// Tipos de servicios
export type { 
  HealthResponse, 
  ServerConfigResponse 
} from './api';

export type { 
  WebSocketEvent, 
  TrainingEvent, 
  MetricsEvent, 
  SystemEvent, 
  SupportedEvent 
} from './websocket';