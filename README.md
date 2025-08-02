# 🏥 Proyecto Chat RAG - Sistema de Consulta Médica

Sistema de chat inteligente con Retrieval Augmented Generation (RAG) especializado en documentos médicos, construido con FastAPI, LangChain y Ollama.

## ✨ Características

- 🤖 **Chat inteligente en español** con modelos locales de Ollama
- 📄 **Procesamiento de documentos** médicos (PDF, DOCX, TXT)
- 🧠 **RAG profesional** con memoria conversacional
- 🔍 **Búsqueda semántica** en base de datos vectorial
- 🎯 **Modelos configurables** desde ultra-ligeros hasta alta calidad
- 🐳 **Containerizado** con Docker Compose
- 🌐 **Interfaz web** moderna y responsiva

## 🚀 Inicio Rápido

### Prerequisitos
- Docker y Docker Compose
- Git

### Instalación

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd proyecto-chat-rag

# Configurar variables de entorno
cp .env.example .env

# Iniciar el sistema
docker-compose up --build
```

### Acceso
- **Aplicación web**: http://localhost:8000
- **API Ollama**: http://localhost:11434

## ⚙️ Configuración

### Modelos Disponibles

| Modelo | Tamaño | RAM | Velocidad | Uso Recomendado |
|--------|--------|-----|-----------|-----------------|
| `tinyllama` | 1.1B | 1-2GB | ⚡⚡⚡ | Desarrollo/Testing |
| `gemma2:2b` | 2B | 2-3GB | ⚡⚡ | Producción ligera |
| `llama3.2:3b` | 3B | 4-6GB | ⚡ | Equilibrado |
| `mistral:7b` | 7B | 8GB | 🐌 | Alta calidad |

### Cambiar Modelo

```bash
# Opción 1: Editar .env
OLLAMA_MODEL=gemma2:2b

# Opción 2: Variable de entorno
OLLAMA_MODEL=mistral:7b docker-compose up --build
```

### Variables de Entorno (.env)

```env
# Modelo de IA
OLLAMA_MODEL=tinyllama
OLLAMA_HOST=http://ollama:11434

# Configuración de la aplicación
APP_HOST=0.0.0.0
APP_PORT=8000
DATA_DIR=data
VECTOR_DIR=vectorstore

# Configuración RAG
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_K_DOCUMENTS=3
```

## 📊 Uso

### 1. Cargar Documentos
- Accede a http://localhost:8000
- Usa la sección "Cargar Archivos" 
- Soporta: PDF, DOCX, TXT
- Los documentos se procesan automáticamente

### 2. Hacer Consultas
- Escribe tu pregunta en el chat
- El sistema responde basándose en los documentos cargados
- Incluye citas de las fuentes utilizadas
- Mantiene contexto conversacional

### 3. API Endpoints

```bash
# Información de modelos
GET /api/models

# Chat
POST /chat
Content-Type: application/x-www-form-urlencoded
message=¿Qué es la diabetes?

# Subir documentos
POST /upload
Content-Type: multipart/form-data

# Limpiar conversación
POST /chat/clear

# Estado de documentos
GET /api/documents
```

## 🏗️ Arquitectura

```
proyecto-chat-rag/
├── app/
│   ├── main.py              # FastAPI + RAG logic
│   ├── static/              # CSS, JS, assets
│   └── templates/           # HTML templates
├── data/                    # Documentos (local)
├── vectorstore/             # Base datos vectorial (local)
├── docker-compose.yml       # Orquestación
├── Dockerfile              # Imagen de la app
├── requirements.txt        # Dependencias Python
└── .env                    # Configuración
```

### Componentes

- **FastAPI**: API REST y servidor web
- **LangChain**: Framework RAG y procesamiento
- **Ollama**: Modelos de IA locales
- **ChromaDB**: Base de datos vectorial
- **Docker**: Containerización

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
# Con logs detallados
docker-compose up --build

# Solo la aplicación (Ollama en background)
docker-compose up app

# Reconstruir solo la app
docker-compose build app && docker-compose up app
```

### Logs y debugging

```bash
# Ver logs
docker-compose logs -f app
docker-compose logs -f ollama

# Acceder al contenedor
docker-compose exec app bash
```

## 🛠️ Solución de Problemas

### Problemas Comunes

**Error: "Collection expecting embedding with dimension"**
```bash
# Limpiar vectorstore
docker-compose down
docker volume rm proyecto-chat-rag_ollama_models
docker-compose up --build
```

**Respuestas lentas**
- Usar modelo más ligero: `tinyllama` o `gemma2:2b`
- Verificar recursos disponibles
- Reducir `RAG_K_DOCUMENTS` en `.env`

**Error de archivos PDF**
- Verificar que el PDF no esté corrupto
- Probar con formato TXT primero
- Revisar logs: `docker-compose logs app`

**Puerto ocupado**
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8001:8000"  # App
  - "11435:11434"  # Ollama
```

## 📋 Requisitos del Sistema

### Mínimos
- RAM: 4GB
- CPU: 2 cores
- Disco: 2GB libre
- Docker: 20.x+

### Recomendado
- RAM: 8GB+
- CPU: 4+ cores
- Disco: 5GB libre
- SSD para mejor rendimiento

## 📝 Notas

- Los documentos se procesan localmente (privacidad)
- Los modelos se descargan automáticamente la primera vez
- La base vectorial se crea automáticamente
- Soporta conversaciones con contexto
- Respuestas especializadas en español

## 🔒 Privacidad

- ✅ Todo funciona localmente
- ✅ No se envían datos a servicios externos
- ✅ Documentos médicos permanecen en tu máquina
- ✅ Modelos de IA ejecutan offline

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**Desarrollado con ❤️ para la comunidad médica**

