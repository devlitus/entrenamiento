/**
 * Interfaces base para la API del Neural Trainer
 * Alineadas con las especificaciones del Swagger API
 */

/**
 * Respuesta base estándar de la API
 */
export interface BaseApiResponse {
  status: string;
  message: string;
}

/**
 * Respuesta de error de la API
 */
export interface ApiErrorResponse extends BaseApiResponse {
  error?: string;
  details?: ApiErrorDetails;
}

/**
 * Detalles específicos de errores de validación
 */
export interface ApiErrorDetails {
  field?: string;
  code?: string;
  value?: unknown;
  [key: string]: unknown;
}

/**
 * Configuración para requests HTTP
 */
export interface RequestConfig {
  headers?: Record<string, string>;
  timeout?: number;
  signal?: AbortSignal;
}

/**
 * Respuesta paginada genérica
 */
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Estados posibles de operaciones asíncronas
 */
export type OperationStatus = 'idle' | 'loading' | 'success' | 'error';

/**
 * Resultado de operación con estado
 */
export interface OperationResult<T = unknown> {
  status: OperationStatus;
  data?: T;
  error?: string;
  loading?: boolean;
}