#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def extract_zip(folder_path):
    for zip_path in Path(folder_path).rglob("*.zip"):
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(folder_path)
        except Exception as e:
            print(f"[WARN] No se pudo extraer {zip_path}: {e}")


def ingest_folder(folder_path: str, vector_dir: str):
    extract_zip(folder_path)
    embeddings = OllamaEmbeddings(model="llama3")
    docs = []
    for file_path in Path(folder_path).rglob("*"):
        ext = file_path.suffix.lower()
        if ext in ['.pdf', '.docx', '.txt', '.md', '.csv', '.pptx', '.html', '.json', '.png', '.jpg', '.jpeg', '.tiff']:
            try:
                loader = UnstructuredFileLoader(str(file_path))
                docs.extend(loader.load())
            except Exception as e:
                print(f"[WARN] Falló cargar {file_path}: {e}")
    db = Chroma.from_documents(docs, embeddings)
    db.save_local(vector_dir)
    print(f"[INFO] Ingestión completada. {len(docs)} documentos indexados.")

if __name__ == '__main__':
    ingest_folder('data', 'vectorstore')
