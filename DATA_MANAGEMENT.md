# 🗂️ Gestión de Carpetas Sensibles

## Problema
Las carpetas `data/` y `vectorstore/` no deberían estar en el repositorio porque:
- Contienen archivos grandes (documentos médicos, bases de datos vectoriales)
- Son específicos de cada instalación local
- Pueden contener información sensible

## Solución Implementada

### 1. ✅ `.gitignore` actualizado
Se agregaron exclusiones para:
- `data/` - Documentos subidos por usuarios
- `vectorstore/` - Base de datos vectorial de Chroma
- Archivos de Python (`__pycache__/`, `*.pyc`)
- Archivos de entorno (`.env`)
- Archivos de IDE (`.vscode/`, `.idea/`)
- Archivos del sistema (`.DS_Store`)

### 2. 🛠️ Script de limpieza
El script `remove_data_from_repo.sh`:
- Crea backup de las carpetas locales
- Las remueve del repositorio remoto
- Las mantiene funcionando localmente
- Commit automático con mensaje descriptivo

## Uso

### Para ejecutar la limpieza:
```bash
# Hacer el script ejecutable
chmod +x remove_data_from_repo.sh

# Ejecutar el script
./remove_data_from_repo.sh

# Subir cambios al repositorio remoto
git push origin main
```

### Resultado:
- ✅ Carpetas removidas del repositorio remoto
- ✅ Carpetas mantenidas localmente
- ✅ Aplicación funciona normalmente
- ✅ Futuras modificaciones no se suben

## Estructura después de la limpieza:

```
proyecto-chat-rag/
├── .gitignore          # ✅ Excluye archivos sensibles
├── data/               # 🔒 Solo local, no en repo
├── vectorstore/        # 🔒 Solo local, no en repo
├── app/
├── docker-compose.yml
└── ...                 # ✅ Resto del código en repo
```

## Notas importantes:
- Las carpetas `data/` y `vectorstore/` se crean automáticamente al ejecutar la aplicación
- Cada desarrollador tendrá sus propios documentos locales
- La configuración en `.env` tampoco se sube al repositorio