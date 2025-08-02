"""
Procesador de documentos profesional para RAG - Versión simplificada
Optimizado para coherencia y precisión
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredWordDocumentLoader
)
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Procesador profesional de documentos para RAG"""
    
    def __init__(self, llm, embeddings, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.llm = llm
        self.embeddings = embeddings
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Splitter optimizado para diferentes tipos de contenido
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",  # Párrafos
                "\n",    # Líneas
                ". ",    # Oraciones
                ", ",    # Cláusulas
                " ",     # Palabras
                ""       # Caracteres
            ]
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Cargar un documento según su tipo"""
        file_path_obj = Path(file_path)
        extension = file_path_obj.suffix.lower()
        
        try:
            if extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif extension == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif extension in ['.docx', '.doc']:
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:
                logger.warning(f"Tipo de archivo no soportado: {extension}")
                return []
            
            documents = loader.load()
            
            # Agregar metadata enriquecida
            for doc in documents:
                doc.metadata.update({
                    'filename': file_path_obj.name,
                    'file_type': extension,
                    'file_size': file_path_obj.stat().st_size,
                    'source_path': str(file_path)
                })
            
            logger.info(f"✅ Cargado: {file_path_obj.name} ({len(documents)} páginas)")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Error cargando {file_path}: {str(e)}")
            return []
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """Cargar todos los documentos de un directorio"""
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.warning(f"Directorio no existe: {directory_path}")
            return documents
        
        # Buscar archivos soportados
        supported_extensions = ['.pdf', '.txt', '.docx', '.doc']
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                docs = self.load_document(str(file_path))
                documents.extend(docs)
        
        logger.info(f"📁 Directorio procesado: {len(documents)} documentos cargados")
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Procesar y dividir documentos en chunks optimizados"""
        if not documents:
            return []
        
        # Limpiar y preparar texto
        processed_docs = []
        for doc in documents:
            # Limpiar texto
            cleaned_text = self._clean_text(doc.page_content)
            
            if len(cleaned_text.strip()) < 50:  # Ignorar chunks muy pequeños
                continue
                
            doc.page_content = cleaned_text
            processed_docs.append(doc)
        
        # Dividir en chunks
        chunks = self.text_splitter.split_documents(processed_docs)
        
        # Enriquecer metadata de chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                'chunk_id': i,
                'chunk_size': len(chunk.page_content),
                'content_preview': chunk.page_content[:100] + "..."
            })
        
        logger.info(f"📝 Documentos procesados: {len(chunks)} chunks creados")
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Limpiar y normalizar texto"""
        import re
        
        # Eliminar caracteres de control
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar líneas muy cortas (probablemente basura)
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return '\n'.join(cleaned_lines).strip()

class OptimizedRetriever:
    """Retriever optimizado para respuestas coherentes - versión simplificada"""
    
    def __init__(self, vectorstore: Chroma, llm, k: int = 5):
        self.vectorstore = vectorstore
        self.llm = llm
        self.k = k
        
        # Retriever base con MMR para diversidad
        self.retriever = vectorstore.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance para diversidad
            search_kwargs={
                "k": k,
                "fetch_k": k * 2,  # Fetch más documentos para seleccionar mejores
                "lambda_mult": 0.7  # Balance relevancia/diversidad
            }
        )
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Obtener documentos relevantes con filtrado optimizado"""
        try:
            docs = self.retriever.get_relevant_documents(query)
            
            # Filtrar y ordenar por relevancia
            filtered_docs = []
            for doc in docs:
                # Solo incluir chunks con contenido sustancial
                if len(doc.page_content.strip()) > 100:
                    filtered_docs.append(doc)
            
            return filtered_docs[:self.k]  # Limitar a k documentos finales
            
        except Exception as e:
            logger.error(f"Error en retrieval: {str(e)}")
            # Fallback a búsqueda simple
            return self.vectorstore.similarity_search(query, k=self.k)

def create_knowledge_base(data_dir: str, vector_dir: str, llm, embeddings) -> tuple:
    """Crear base de conocimiento optimizada"""
    
    processor = DocumentProcessor(llm, embeddings)
    
    # Cargar documentos existentes
    documents = processor.load_directory(data_dir)
    
    if not documents:
        logger.warning("⚠️ No se encontraron documentos en el directorio")
        # Crear vectorstore vacío
        vectorstore = Chroma(
            persist_directory=vector_dir,
            embedding_function=embeddings
        )
        return vectorstore, OptimizedRetriever(vectorstore, llm)
    
    # Procesar documentos
    chunks = processor.process_documents(documents)
    
    if not chunks:
        logger.warning("⚠️ No se pudieron procesar los documentos")
        vectorstore = Chroma(
            persist_directory=vector_dir,
            embedding_function=embeddings
        )
        return vectorstore, OptimizedRetriever(vectorstore, llm)
    
    # Crear o actualizar vectorstore
    if os.path.exists(vector_dir) and os.listdir(vector_dir):
        # Cargar existente y agregar nuevos
        vectorstore = Chroma(
            persist_directory=vector_dir,
            embedding_function=embeddings
        )
        vectorstore.add_documents(chunks)
    else:
        # Crear nuevo
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=vector_dir
        )
    
    logger.info(f"🎯 Base de conocimiento creada: {len(chunks)} chunks indexados")
    
    # Crear retriever optimizado
    retriever = OptimizedRetriever(vectorstore, llm, k=5)
    
    return vectorstore, retriever
