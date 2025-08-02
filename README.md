# 🤖 Chat RAG - Sistema de Conversación con Documentos

Un sistema RAG (Retrieval-Augmented Generation) moderno que permite conversar con tus documentos usando modelos de lenguaje local con Ollama.

## ✨ Características

- 🚀 **Modelos configurables**: 7 opciones desde ultra-ligero (1GB RAM) hasta alta calidad (8GB RAM)
- 📄 **Múltiples formatos**: PDF, TXT, DOCX y más
- 💬 **Chat inteligente**: Memoria conversacional y contexto persistente
- 🐳 **Docker**: Configuración completa con Docker Compose
- ⚡ **Optimizado**: Arquitectura ligera y eficiente
- 🎨 **Interfaz moderna**: UI responsiva con información del modelo

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose
- Al menos 2GB de RAM libre (según modelo)

### 1. Clonar y configurar
```bash
git clone <tu-repo>
cd proyecto-chat-rag
```

### 2. Configurar modelo (opcional)
```bash
# Editar .env para cambiar modelo
OLLAMA_MODEL=tinyllama  # Modelo por defecto (ultra-rápido)
```

### 3. Ejecutar
```bash
docker-compose up --build
```

### 4. Usar
- **Web UI**: http://localhost:8000
- **API**: http://localhost:8000/docs

## 🎛️ Configuración de Modelos

### Modelos Disponibles

| Modelo | Tamaño | RAM | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----|-----------|---------|-----------------|
| `tinyllama` | 1.1B | 1-2GB | ⚡⚡⚡ | ⭐⭐ | Desarrollo/Testing |
| `gemma2:2b` | 2B | 2-3GB | ⚡⚡ | ⭐⭐⭐ | Producción ligera |
| `qwen2:1.5b` | 1.5B | 2-3GB | ⚡⚡ | ⭐⭐⭐ | Equilibrio ligero |
| `llama3.2:3b` | 3B | 4-6GB | ⚡ | ⭐⭐⭐⭐ | Equilibrado |
| `phi3:3.8b` | 3.8B | 4-6GB | ⚡ | ⭐⭐⭐⭐ | Optimizado |
| `llama3.1:8b` | 8B | 8GB | 🐌 | ⭐⭐⭐⭐⭐ | Alta calidad |
| `mistral:7b` | 7B | 8GB | 🐌 | ⭐⭐⭐⭐⭐ | Mistral AI |

### Cambiar Modelo

#### Opción 1: Script automático (Recomendado)
```bash
./change-model.sh tinyllama      # Ultra rápido
./change-model.sh gemma2:2b      # Muy eficiente  
./change-model.sh llama3.2:3b    # Equilibrado
./change-model.sh mistral:7b     # Alta calidad
```

#### Opción 2: Variable de entorno
```bash
OLLAMA_MODEL=gemma2:2b docker-compose up --build
```

#### Opción 3: Editar .env
```env
OLLAMA_MODEL=tinyllama  # Cambiar por el modelo deseado
```

## 📁 Estructura del Proyecto

```
proyecto-chat-rag/
├── app/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models_config.py     # Configuración de modelos
│   ├── static/              # Archivos estáticos
│   │   ├── css/style.css    # Estilos
│   │   └── js/chat.js       # JavaScript del chat
│   └── templates/
│       └── chat.html        # Interfaz web
├── data/                    # Documentos cargados
├── vectorstore/            # Base de datos vectorial
├── .env                    # Variables de entorno
├── docker-compose.yml      # Configuración Docker
├── Dockerfile             # Imagen de la aplicación
├── requirements.txt       # Dependencias Python
├── change-model.sh        # Script cambio de modelo
└── README.md             # Esta documentación
```

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

```env
# Modelo de IA
OLLAMA_MODEL=tinyllama
OLLAMA_HOST=http://ollama:11434

# Aplicación
APP_HOST=0.0.0.0
APP_PORT=8000
DATA_DIR=data
VECTOR_DIR=vectorstore

# RAG
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_K_DOCUMENTS=3
```

### Personalizar Docker Compose

```yaml
services:
  app:
    environment:
      - OLLAMA_MODEL=${OLLAMA_MODEL:-tinyllama}
    volumes:
      - ./custom-data:/app/data  # Directorio personalizado
  
  ollama:
    environment:
      - OLLAMA_KEEP_ALIVE=24h    # Mantener modelo en memoria
```

## 📡 API Endpoints

### Principales
- `GET /` - Interfaz web
- `POST /upload` - Cargar documentos
- `POST /chat` - Enviar mensaje al chat

### Información
- `GET /api/models` - Listar modelos disponibles
- `GET /api/model/current` - Información del modelo actual
- `GET /docs` - Documentación Swagger

### Ejemplos de API

```bash
# Información del modelo actual
curl http://localhost:8000/api/model/current

# Cargar documento
curl -X POST -F "files=@documento.pdf" http://localhost:8000/upload

# Enviar mensaje
curl -X POST -F "message=¿Qué dice el documento?" http://localhost:8000/chat
```

## 💡 Uso

### 1. Cargar Documentos
- Usa la interfaz web o API
- Formatos soportados: PDF, TXT, DOCX
- Los documentos se procesan automáticamente

### 2. Hacer Preguntas
- El chat mantiene contexto de la conversación
- Las respuestas incluyen información de los documentos
- Soporta preguntas de seguimiento

### 3. Gestionar Modelos
- Cambiar modelo sin perder datos
- Información en tiempo real del modelo usado
- Optimización automática según recursos

## 🛠️ Desarrollo

### Estructura del Código

```python
# app/main.py - Aplicación principal
from fastapi import FastAPI
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuración dinámica de modelos
MODEL_NAME = os.getenv("OLLAMA_MODEL", "tinyllama")
llm = OllamaLLM(model=MODELS[MODEL_NAME]["model"])
```

### Agregar Nuevo Modelo

1. Editar `app/models_config.py`:
```python
MODELS = {
    "nuevo_modelo": {
        "model": "nuevo_modelo:version",
        "name": "Nuevo Modelo",
        "size": "XB",
        "ram": "~X GB",
        "description": "Descripción del modelo"
    }
}
```

2. Actualizar `change-model.sh` con el nuevo modelo

### Testing Local

```bash
# Desarrollo sin Docker
pip install -r requirements.txt
uvicorn app.main:app --reload

# Testing con modelo específico
OLLAMA_MODEL=tinyllama python -m uvicorn app.main:app --reload
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### Error: "model not found"
```bash
# Verificar modelo disponible
docker exec -it proyecto-chat-rag-ollama-1 ollama list

# Descargar modelo manualmente
docker exec -it proyecto-chat-rag-ollama-1 ollama pull tinyllama
```

#### RAM insuficiente
```bash
# Usar modelo más ligero
./change-model.sh tinyllama

# O configurar directamente
OLLAMA_MODEL=tinyllama docker-compose up --build
```

#### Contenedor no inicia
```bash
# Ver logs
docker-compose logs app
docker-compose logs ollama

# Reiniciar limpio
docker-compose down -v
docker-compose up --build
```

### Logs y Debugging

```bash
# Ver logs en tiempo real
docker-compose logs -f app

# Acceder al contenedor
docker exec -it proyecto-chat-rag-app-1 bash

# Estado de Ollama
curl http://localhost:11434/api/tags
```

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- [Ollama](https://ollama.ai/) - Modelos de lenguaje local
- [LangChain](https://langchain.com/) - Framework RAG
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Chroma](https://www.trychroma.com/) - Base de datos vectorial

---

**¿Preguntas?** Abre un [Issue](../../issues) o consulta la [documentación de la API](http://localhost:8000/docs).cto Chat RAG Local

Servidor local RAG (Retrieval-Augmented Generation) con:
- FastAPI + Uvicorn
- LangChain + Ollama
- Ingestión automática de archivos (PDF, DOCX, TXT, CSV, MD, PPTX, HTML, JSON, imágenes y videos)
- Filtrado ZIP y subdirectorios

## Despliegue con Docker

1. Construir y levantar contenedores:

   ```bash
   docker-compose up --build
   ```

2. Abrir en el navegador:

   http://localhost:8000

## Estructura del Proyecto

```
proyecto-chat-rag/
├── app/                 # Código del servidor FastAPI
│   └── main.py
├── data/                # Documentos de usuario (subdirectorios permitidos)
├── scripts/             # Scripts auxiliares (ingestión de datos)
│   └── ingest.py
├── vectorstore/         # Índice vectorial guardado
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Formatos soportados

- Texto: .txt, .md, .csv, .json, .html
- Office: .pdf, .docx, .pptx
- Imágenes: .png, .jpg, .jpeg, .tiff (OCR con Tesseract)
- Videos: .mp4, .avi (transcripción con Whisper)

