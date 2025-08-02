#!/usr/bin/env python3
"""
Script de inicialización para limpiar vectorstore incompatible
"""
import os
import shutil
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_incompatible_vectorstore():
    """Limpiar vectorstore si existe y puede ser incompatible"""
    vectorstore_dir = "/app/vectorstore"
    
    if os.path.exists(vectorstore_dir) and os.listdir(vectorstore_dir):
        logger.info("🧹 Detectado vectorstore existente")
        
        # Verificar si hay archivos de ChromaDB
        chroma_files = [f for f in os.listdir(vectorstore_dir) if f.endswith('.sqlite3') or f.startswith('chroma')]
        
        if chroma_files:
            logger.warning("⚠️ Limpiando vectorstore para evitar incompatibilidades de dimensiones...")
            try:
                # Crear backup si es necesario
                backup_dir = f"{vectorstore_dir}_backup"
                if not os.path.exists(backup_dir):
                    shutil.copytree(vectorstore_dir, backup_dir)
                    logger.info(f"📦 Backup creado en: {backup_dir}")
                
                # Limpiar directorio
                for item in os.listdir(vectorstore_dir):
                    item_path = os.path.join(vectorstore_dir, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except Exception as e:
                        logger.warning(f"No se pudo eliminar {item}: {e}")
                
                logger.info("✅ Vectorstore limpiado correctamente")
                
            except Exception as e:
                logger.error(f"❌ Error limpiando vectorstore: {e}")
    else:
        logger.info("📂 No hay vectorstore existente")

if __name__ == "__main__":
    clean_incompatible_vectorstore()
