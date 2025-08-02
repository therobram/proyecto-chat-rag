# 🚀 Guía Rápida - Chat RAG

## Comandos Esenciales

### Inicio Rápido
```bash
# 1. Clonar proyecto
git clone <repo> && cd proyecto-chat-rag

# 2. Ejecutar (modelo por defecto: tinyllama)
docker-compose up --build

# 3. Abrir navegador
open http://localhost:8000
```

### Cambio de Modelo
```bash
# Modelos recomendados por velocidad
./change-model.sh tinyllama      # ⚡⚡⚡ Ultra rápido (1GB)
./change-model.sh gemma2:2b      # ⚡⚡ Muy rápido (2GB)
./change-model.sh llama3.2:3b    # ⚡ Equilibrado (4GB)
./change-model.sh mistral:7b     # 🐌 Lento pero preciso (8GB)
```

### Solución de Problemas
```bash
# Ver logs
docker-compose logs -f

# Reinicio limpio
docker-compose down -v && docker-compose up --build

# Estado de Ollama
curl http://localhost:11434/api/tags
```

## Recursos por Modelo

| Modelo | RAM | CPU | Disco | Tiempo Respuesta |
|--------|-----|-----|-------|------------------|
| tinyllama | 1-2GB | Bajo | ~700MB | 1-2s |
| gemma2:2b | 2-3GB | Medio | ~1.4GB | 2-4s |
| llama3.2:3b | 4-6GB | Medio | ~2GB | 3-6s |
| mistral:7b | 8GB+ | Alto | ~4GB | 5-10s |

## Archivos Soportados

✅ **Soportados**: PDF, TXT, DOCX, MD  
❌ **No soportados**: ZIP, imágenes, audio  
🔄 **Procesamiento**: Automático al cargar

## URLs Importantes

- **Chat**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/model/current
- **Ollama**: http://localhost:11434

---
💡 **Tip**: Usa `tinyllama` para desarrollo y `gemma2:2b` para producción ligera.
