export interface PredictionResponse {
  prediction: number[];           
  confidence?: number;            
  model_used?: string;           
  processing_time?: number;      
}