#!/bin/bash

# Script para remover backup accidental del repositorio

echo "🗑️ Removiendo backup accidental del repositorio..."

# Remover el backup del índice de git pero mantenerlo localmente
git rm --cached -r data_backup_20250802_045709/ 2>/dev/null || echo "ℹ️ El backup no estaba en el repositorio"

# Remover cualquier otro backup que pueda estar
git rm --cached -r data_backup_*/ 2>/dev/null || echo "ℹ️ No hay otros backups en el repositorio"

# Agregar el .gitignore actualizado
git add .gitignore

echo "📋 Verificando cambios..."
git status

echo ""
echo "¿Deseas continuar con el commit para remover el backup? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    # Commit de los cambios
    git commit -m "🗑️ Remover backup accidental del repositorio y actualizar .gitignore

- Removido data_backup_20250802_045709/ del repositorio
- Agregadas exclusiones para futuros backups en .gitignore
- Los backups se mantienen localmente pero no se suben al repo"

    echo "✅ Backup removido del repositorio"
    echo ""
    echo "🚀 Para aplicar al repositorio remoto, ejecuta:"
    echo "   git push origin main"
else
    echo "❌ Operación cancelada"
    exit 1
fi

echo ""
echo "📁 El backup se mantiene localmente"
echo "🔒 Futuros backups no se subirán al repositorio"