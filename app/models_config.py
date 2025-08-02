# Configuración de modelos disponibles
# Formato: nombre_modelo = "modelo_ollama"

MODELS = {
    # Modelos ultra-ligeros (1-2GB RAM)
    "tinyllama": {
        "model": "tinyllama",
        "name": "TinyLlama 1.1B",
        "size": "1.1B",
        "ram": "~1-2 GB",
        "description": "Modelo más rápido, ideal para desarrollo y pruebas"
    },
    
    # Modelos ligeros (2-4GB RAM)
    "gemma2:2b": {
        "model": "gemma2:2b", 
        "name": "Gemma 2 2B",
        "size": "2B",
        "ram": "~2-3 GB",
        "description": "Optimizado para CPU, muy eficiente"
    },
    
    "qwen2:1.5b": {
        "model": "qwen2:1.5b",
        "name": "Qwen2 1.5B", 
        "size": "1.5B",
        "ram": "~2-3 GB",
        "description": "Modelo ligero con buen rendimiento"
    },
    
    # Modelos medianos (3-6GB RAM)
    "llama3.2:3b": {
        "model": "llama3.2:3b",
        "name": "Llama 3.2 3B",
        "size": "3B", 
        "ram": "~4-6 GB",
        "description": "Equilibrio entre velocidad y calidad"
    },
    
    "phi3:3.8b": {
        "model": "phi3:3.8b",
        "name": "Phi-3 3.8B",
        "size": "3.8B",
        "ram": "~4-6 GB", 
        "description": "Modelo de Microsoft, optimizado"
    },
    
    # Modelos grandes (6-8GB RAM)
    "llama3.1:8b": {
        "model": "llama3.1:8b",
        "name": "Llama 3.1 8B",
        "size": "8B",
        "ram": "~8 GB",
        "description": "Alta calidad, más lento"
    },
    
    "mistral:7b": {
        "model": "mistral:7b", 
        "name": "Mistral 7B",
        "size": "7B",
        "ram": "~8 GB",
        "description": "Modelo de alta calidad de Mistral"
    }
}

DEFAULT_MODEL = "tinyllama"
