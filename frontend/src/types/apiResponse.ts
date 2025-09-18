export interface apiResponse<T> {
  status: 'success' | 'error';
  data: T;
  error?: string;
}