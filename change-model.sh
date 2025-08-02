#!/bin/bash

# Script para cambiar modelo de LLM
# Uso: ./change-model.sh [modelo]

AVAILABLE_MODELS=(
    "tinyllama"      # 1.1B - Ultra rápido
    "gemma2:2b"      # 2B - Muy eficiente  
    "qwen2:1.5b"     # 1.5B - Ligero
    "llama3.2:3b"    # 3B - Equilibrado
    "phi3:3.8b"      # 3.8B - Optimizado
    "llama3.1:8b"    # 8B - Alta calidad
    "mistral:7b"     # 7B - Mistral
)

show_help() {
    echo "🤖 Chat RAG - Cambio de Modelo"
    echo ""
    echo "Uso: $0 [modelo]"
    echo ""
    echo "📊 Modelos disponibles:"
    echo ""
    echo "🚀 ULTRA RÁPIDOS (1-3GB RAM):"
    echo "  tinyllama     - TinyLlama 1.1B (~1-2GB) - ⚡⚡⚡ Desarrollo/Testing"
    echo "  gemma2:2b     - Gemma 2 2B (~2-3GB) - ⚡⚡ Producción ligera"  
    echo "  qwen2:1.5b    - Qwen2 1.5B (~2-3GB) - ⚡⚡ Equilibrio ligero"
    echo ""
    echo "⚖️ EQUILIBRADOS (4-6GB RAM):"
    echo "  llama3.2:3b   - Llama 3.2 3B (~4-6GB) - ⚡ Uso general"
    echo "  phi3:3.8b     - Phi-3 3.8B (~4-6GB) - ⚡ Microsoft optimizado"
    echo ""
    echo "🎯 ALTA CALIDAD (8GB+ RAM):"
    echo "  llama3.1:8b   - Llama 3.1 8B (~8GB) - 🐌 Máxima calidad"
    echo "  mistral:7b    - Mistral 7B (~8GB) - 🐌 Mistral AI premium"
    echo ""
    echo "💡 Recomendaciones:"
    echo "  • Desarrollo: tinyllama (más rápido)"
    echo "  • Producción ligera: gemma2:2b (equilibrio ideal)"
    echo "  • Producción premium: llama3.2:3b (calidad/velocidad)"
    echo "  • Máxima calidad: mistral:7b (si tienes RAM suficiente)"
    echo ""
    echo "🚀 Ejemplos:"
    echo "  $0 tinyllama      # Inicio rápido"
    echo "  $0 gemma2:2b      # Recomendado para producción"
    echo "  $0 llama3.2:3b    # Equilibrio perfecto"
    echo ""
    echo "📚 Más info: README.md | Changelog: CHANGELOG.md"
}

if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

MODEL=$1

# Validar modelo
if [[ ! " ${AVAILABLE_MODELS[@]} " =~ " ${MODEL} " ]]; then
    echo "❌ Error: Modelo '$MODEL' no disponible"
    echo ""
    show_help
    exit 1
fi

echo "🔄 Cambiando modelo a: $MODEL"

# Actualizar .env
sed -i.bak "s/OLLAMA_MODEL=.*/OLLAMA_MODEL=$MODEL/" .env

echo "✅ Modelo actualizado en .env"
echo "🚀 Reiniciando contenedores..."

# Reiniciar Docker Compose
docker-compose down
docker-compose up --build -d

echo "✅ ¡Listo! El modelo $MODEL se está descargando y configurando."
echo "📱 La aplicación estará disponible en: http://localhost:8000"
echo "⏱️  La primera vez puede tardar unos minutos descargando el modelo."
