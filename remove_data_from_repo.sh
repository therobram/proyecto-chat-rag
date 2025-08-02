#!/bin/bash

# Script para remover carpeta data del repositorio remoto pero mantenerla local

echo "🗂️  Removiendo carpeta 'data' del repositorio remoto..."

# Hacer backup local de la carpeta data si existe
if [ -d "data" ]; then
    echo "📋 Creando backup de la carpeta data..."
    cp -r data data_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup creado"
fi

# Remover archivos específicos del índice de git pero mantenerlos localmente
echo "🗑️ Removiendo archivos de data/ del índice de git..."
git rm --cached -r data/ 2>/dev/null || echo "ℹ️  Algunos archivos de data/ no estaban en el repositorio"

# Remover la carpeta vectorstore del índice de git (pero mantenerla localmente)
git rm --cached -r vectorstore/ 2>/dev/null || echo "ℹ️  La carpeta 'vectorstore' no estaba en el repositorio"

# Agregar el .gitignore al repositorio
git add .gitignore

# También agregar otros archivos nuevos (scripts y documentación)
git add DATA_MANAGEMENT.md
git add remove_data_from_repo.sh

echo "📋 Verificando archivos que se van a commitear..."
git status

echo ""
echo "¿Deseas continuar con el commit? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    # Commit de los cambios
    git commit -m "🗂️ Agregar .gitignore y remover carpetas data/ y vectorstore/ del repositorio

- Agregado .gitignore completo para excluir archivos sensibles
- Removidas carpetas data/ y vectorstore/ del repositorio remoto
- Las carpetas se mantienen localmente para el funcionamiento de la app
- Agregadas exclusiones para archivos de Python, Docker, IDE, macOS, etc.
- Agregada documentación sobre gestión de carpetas sensibles"

    echo "✅ Cambios aplicados localmente"
    echo ""
    echo "🚀 Para aplicar al repositorio remoto, ejecuta:"
    echo "   git push origin main"
else
    echo "❌ Operación cancelada"
    exit 1
fi

echo ""
echo "📁 Las carpetas 'data' y 'vectorstore' se mantienen localmente"
echo "🔒 Futuras modificaciones a estas carpetas no se subirán al repositorio"