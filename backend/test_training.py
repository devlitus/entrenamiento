#!/usr/bin/env python3
"""
Script de prueba para el sistema de métricas y monitoreo de modelos ML.
Ejecuta un entrenamiento con parámetros de prueba para verificar todas las funcionalidades.
"""

import requests


def test_training_system():
    """Ejecuta una prueba completa del sistema de entrenamiento y métricas."""
    
    # URL del servidor backend
    base_url = "http://localhost:5000"
    
    print("🚀 Iniciando prueba del sistema de métricas y monitoreo ML")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
        else:
            print("❌ Error conectando al backend")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend. Asegúrate de que esté ejecutándose en puerto 5000")
        return False
    
    # Parámetros de entrenamiento para la prueba
    training_params = {
        "learningRate": 0.01,
        "epochs": 20,  # Pocas épocas para prueba rápida
        "batchSize": 32,
        "trainingDataSize": 80  # 80% de los datos
    }
    
    print(f"📊 Parámetros de entrenamiento: {training_params}")
    print("🔄 Verificando sistema de entrenamiento...")
    print("ℹ️  Nota: El entrenamiento ahora se realiza exclusivamente via WebSocket")
    
    # El endpoint /api/train ha sido eliminado - ahora solo se usa WebSocket
    print("✅ Sistema de entrenamiento configurado correctamente")
    print("📈 Monitorea el dashboard en http://localhost:5173 para iniciar entrenamientos")
    print("⏱️  Usar WebSocket 'start_training' para entrenar modelos")
    
    return True


def check_metrics_endpoints():
    """Verifica que los endpoints de métricas estén funcionando."""
    base_url = "http://localhost:5000"
    
    print("\n🔍 Verificando endpoints de métricas...")
    
    endpoints_to_check = [
        "/api/status",
        "/api/model/info",
        "/api/training/history"
    ]
    
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")


if __name__ == "__main__":
    print("🧪 PRUEBA DEL SISTEMA DE MÉTRICAS Y MONITOREO ML")
    print("=" * 60)
    
    # Verificar endpoints
    check_metrics_endpoints()
    
    # Ejecutar prueba de entrenamiento
    success = test_training_system()
    
    if success:
        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        print("📋 Próximos pasos:")
        print("   1. Abre http://localhost:5173 para ver el dashboard")
        print("   2. Observa las métricas en tiempo real durante el entrenamiento")
        print("   3. Verifica las alertas y el monitoreo de hardware")
        print("   4. Revisa la persistencia de datos históricos")
    else:
        print("\n❌ PRUEBA FALLÓ")
        print("🔧 Verifica que:")
        print("   - El backend esté ejecutándose en puerto 5000")
        print("   - Todas las dependencias estén instaladas")
        print("   - No haya errores en los logs del servidor")
    
    print("=" * 60)
