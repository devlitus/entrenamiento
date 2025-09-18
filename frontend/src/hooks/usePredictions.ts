import { useState, useCallback } from 'react';

interface PredictionRequest {
  input_data: number[];
  model_type?: string;
}

interface PredictionResponse {
  prediction: number[];
  confidence: number;
  model_used: string;
  processing_time: number;
}

interface UsePredictionsState {
  isLoading: boolean;
  prediction: PredictionResponse | null;
  error: string | null;
  history: PredictionResponse[];
}

interface UsePredictionsActions {
  predict: (data: PredictionRequest) => Promise<void>;
  clearPrediction: () => void;
  clearError: () => void;
  clearHistory: () => void;
}

export interface UsePredictionsReturn extends UsePredictionsState, UsePredictionsActions {}

/**
 * Hook personalizado para manejar predicciones del modelo ML
 */
export const usePredictions = (): UsePredictionsReturn => {
  const [state, setState] = useState<UsePredictionsState>({
    isLoading: false,
    prediction: null,
    error: null,
    history: [],
  });

  /**
   * Realiza una predicción con el modelo entrenado
   */
  const predict = useCallback(async (data: PredictionRequest): Promise<void> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch('http://localhost:5000/api/prediction/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result: PredictionResponse = await response.json();

      setState(prev => ({
        ...prev,
        isLoading: false,
        prediction: result,
        error: null,
        history: [result, ...prev.history].slice(0, 10), // Mantener últimas 10 predicciones
      }));

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido en predicción';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, []);

  /**
   * Limpia la predicción actual
   */
  const clearPrediction = useCallback(() => {
    setState(prev => ({ ...prev, prediction: null }));
  }, []);

  /**
   * Limpia el error actual
   */
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  /**
   * Limpia el historial de predicciones
   */
  const clearHistory = useCallback(() => {
    setState(prev => ({ ...prev, history: [] }));
  }, []);

  return {
    ...state,
    predict,
    clearPrediction,
    clearError,
    clearHistory,
  };
};

export default usePredictions;