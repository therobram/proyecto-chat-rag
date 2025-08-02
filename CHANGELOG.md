# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2.0.0] - 2025-08-02

### 🚀 Agregado
- **Sistema de modelos configurables**: 7 modelos disponibles desde ultra-ligero hasta alta calidad
- **Script de cambio automático**: `change-model.sh` para cambiar modelos fácilmente
- **Variables de entorno**: Configuración completa via `.env`
- **API de información**: Endpoints para consultar modelos disponibles y actual
- **Interfaz mejorada**: Muestra información del modelo actual en la UI
- **Configuración de RAG**: Variables para chunk_size, overlap y documentos
- **Documentación completa**: README.md detallado con guías de uso

### 🎛️ Modelos Soportados
- `tinyllama` - TinyLlama 1.1B (ultra-rápido, 1-2GB RAM)
- `gemma2:2b` - Gemma 2 2B (muy eficiente, 2-3GB RAM)
- `qwen2:1.5b` - Qwen2 1.5B (ligero, 2-3GB RAM)
- `llama3.2:3b` - Llama 3.2 3B (equilibrado, 4-6GB RAM)
- `phi3:3.8b` - Phi-3 3.8B (optimizado, 4-6GB RAM)
- `llama3.1:8b` - Llama 3.1 8B (alta calidad, 8GB RAM)
- `mistral:7b` - Mistral 7B (alta calidad, 8GB RAM)

### 🔧 Mejorado
- **Dockerfile optimizado**: Imagen ~50% más pequeña, mejor cache
- **Docker Compose robusto**: Healthchecks y dependencias mejoradas
- **Gestión de errores**: Fallbacks y manejo de excepciones
- **CSS responsivo**: Diseño mejorado con información de modelo
- **JavaScript interactivo**: Chat más fluido y feedback visual

### 🐛 Corregido
- Problema con `Chroma.load_local()` - migrado a `persist_directory`
- Advertencias de deprecación de LangChain - actualizadas las importaciones
- Error de directorio `static` no encontrado - estructura corregida
- Problemas de conexión con Ollama - configuración de red mejorada

## [1.0.0] - 2025-08-01

### 🚀 Agregado
- **Sistema RAG básico**: Conversación con documentos PDF, TXT, DOCX
- **Integración con Ollama**: Soporte para modelos locales
- **Interfaz web**: Chat básico con FastAPI y HTML
- **Docker Compose**: Configuración para desarrollo
- **Memoria conversacional**: Contexto persistente en chats
- **Carga de archivos**: Upload múltiple de documentos
- **Base vectorial**: Almacenamiento con Chroma

### 🎯 Funcionalidades Iniciales
- Chat básico con modelo llama3:8b
- Carga de documentos via web
- Búsqueda semántica en documentos
- Respuestas basadas en contexto
- Interfaz HTML simple

### 🔧 Tecnologías
- **Backend**: FastAPI + LangChain
- **Frontend**: HTML + CSS + JavaScript vanilla
- **IA**: Ollama + Llama3
- **Vectores**: Chroma DB
- **Contenedores**: Docker + Docker Compose

## [Próximas Versiones]

### 🎯 Roadmap v2.1.0
- [ ] **Selector de modelo en UI**: Cambio de modelo desde la interfaz
- [ ] **Historial de conversaciones**: Guardar y recuperar chats
- [ ] **Múltiples formatos**: Soporte para más tipos de archivo
- [ ] **Análisis de documentos**: Estadísticas y resúmenes automáticos
- [ ] **API completa**: REST API documentada

### 🎯 Roadmap v3.0.0
- [ ] **Autenticación**: Sistema de usuarios
- [ ] **Múltiples bases**: Separación por usuario/proyecto
- [ ] **Streaming**: Respuestas en tiempo real
- [ ] **Plugins**: Sistema extensible
- [ ] **Métricas**: Dashboard de uso y rendimiento

---

## Tipos de Cambios

- 🚀 **Agregado** para nuevas funcionalidades
- 🔧 **Mejorado** para cambios en funcionalidades existentes
- 🐛 **Corregido** para corrección de bugs
- ⚡ **Optimizado** para mejoras de rendimiento
- 🔒 **Seguridad** para vulnerabilidades
- 💥 **Breaking** para cambios incompatibles
- 🗑️ **Obsoleto** para funcionalidades que serán removidas

## Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs compatibles
