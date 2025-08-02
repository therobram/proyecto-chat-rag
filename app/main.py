import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import shutil
import logging
from .models_config import MODELS, DEFAULT_MODEL

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Config
MODEL_NAME = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
DATA_DIR = os.getenv("DATA_DIR", "data")
VECTOR_DIR = os.getenv("VECTOR_DIR", "vectorstore")

# Validar que el modelo existe
if MODEL_NAME not in MODELS:
    print(f"⚠️  Modelo '{MODEL_NAME}' no encontrado. Usando modelo por defecto: {DEFAULT_MODEL}")
    MODEL_NAME = DEFAULT_MODEL

CURRENT_MODEL = MODELS[MODEL_NAME]["model"]
print(f"🚀 Usando modelo: {MODELS[MODEL_NAME]['name']} ({CURRENT_MODEL})")
print(f"   RAM estimada: {MODELS[MODEL_NAME]['ram']}")
print(f"   Descripción: {MODELS[MODEL_NAME]['description']}")

# App init
app = FastAPI(title="Chat RAG Profesional", description=f"Sistema RAG optimizado usando {MODELS[MODEL_NAME]['name']}")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Inicialización de modelos
logger.info(f"🚀 Inicializando modelo: {MODELS[MODEL_NAME]['name']}")
llm = OllamaLLM(
    model=MODEL_NAME, 
    base_url=OLLAMA_HOST,
    temperature=0.1,
    system="""Eres un asistente médico especializado que SIEMPRE responde en español. 
    Tu función es ayudar con información médica basada en documentos proporcionados.
    Usa terminología médica apropiada en español y sé preciso en tus respuestas."""
)
embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url=OLLAMA_HOST)

# Crear directorios necesarios
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# Configurar text splitter profesional
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", ", ", " ", ""]
)

# Inicializar base vectorial de forma simple y robusta
def initialize_vectorstore():
    """Inicializar vectorstore de forma robusta"""
    # Siempre crear un vectorstore fresco para evitar problemas de dimensiones
    vectorstore = Chroma(
        persist_directory=VECTOR_DIR, 
        embedding_function=embeddings,
        collection_name=f"docs_{CURRENT_MODEL.replace(':', '_')}"  # Nombre único por modelo
    )
    logger.info(f"✅ Vectorstore inicializado para modelo: {CURRENT_MODEL}")
    return vectorstore

vectorstore = initialize_vectorstore()

def load_document(file_path):
    """Cargar documento según su extensión"""
    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1].lower()
    
    try:
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension in ['.txt', '.md']:
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            # Para otros tipos, intentar como texto
            loader = TextLoader(file_path, encoding='utf-8')
        
        return loader.load()
    except Exception as e:
        logger.error(f"Error cargando {filename}: {e}")
        return []

# Cargar documentos existentes al iniciar
def load_existing_documents():
    """Cargar todos los documentos del directorio data al iniciar"""
    if not os.path.exists(DATA_DIR):
        return
    
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(('.pdf', '.txt', '.docx')):
            file_path = os.path.join(DATA_DIR, filename)
            docs = load_document(file_path)
            
            if docs:
                # Agregar metadata mejorada
                for doc in docs:
                    doc.metadata.update({
                        'filename': filename,
                        'source_path': file_path
                    })
                documents.extend(docs)
                logger.info(f"✅ Cargado: {filename}")
    
    if documents:
        # Dividir en chunks
        chunks = text_splitter.split_documents(documents)
        # Agregar al vectorstore
        vectorstore.add_documents(chunks)
        logger.info(f"📚 {len(chunks)} fragmentos agregados a la base de conocimiento")

# Cargar documentos existentes
load_existing_documents()

# Memoria y chain
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True,
    output_key="answer"
)

# Chain RAG con retriever optimizado y prompt en español
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.7}
)

# Crear un prompt personalizado en español
spanish_prompt = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""Eres un asistente médico especializado que responde ÚNICAMENTE en español.

Contexto de documentos médicos:
{context}

Historial de conversación:
{chat_history}

Pregunta del usuario: {question}

INSTRUCCIONES IMPORTANTES:
- Responde SIEMPRE en español
- Usa terminología médica precisa en español
- Si no tienes información en los documentos, dilo claramente en español
- Sé preciso y profesional
- Cita los documentos relevantes cuando sea posible
- Mantén un tono profesional pero accesible

Respuesta en español:"""
)

# Prompt para condensar preguntas en español
spanish_condense_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""Dada la siguiente conversación y una pregunta de seguimiento, reformula la pregunta de seguimiento para que sea una pregunta independiente, en español.

Historial de Chat:
{chat_history}
Pregunta de seguimiento: {question}
Pregunta independiente en español:"""
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True,
    combine_docs_chain_kwargs={"prompt": spanish_prompt},
    condense_question_prompt=spanish_condense_prompt
)

logger.info("✅ Sistema RAG profesional inicializado correctamente")

@app.get("/", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "current_model": MODELS[MODEL_NAME],
        "available_models": MODELS
    })

@app.get("/api/models")
async def get_models():
    """Obtener información de modelos disponibles"""
    return {
        "current_model": MODEL_NAME,
        "current_model_info": MODELS[MODEL_NAME],
        "available_models": MODELS
    }

@app.get("/api/model/current")
async def get_current_model():
    """Obtener información del modelo actual"""
    return {
        "model_key": MODEL_NAME,
        "model_info": MODELS[MODEL_NAME],
        "ollama_host": OLLAMA_HOST
    }

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    """Cargar y procesar archivos de manera profesional"""
    
    if not files:
        raise HTTPException(status_code=400, detail="No se proporcionaron archivos")
    
    results = []
    
    for file in files:
        try:
            # Validar tipo de archivo
            allowed_extensions = ['.pdf', '.txt', '.docx', '.doc']
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            if file_extension not in allowed_extensions:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": f"Tipo de archivo no soportado: {file_extension}"
                })
                continue
            
            # Guardar archivo
            file_path = os.path.join(DATA_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Cargar y procesar documento
            documents = load_document(file_path)
            
            # Agregar metadata
            for doc in documents:
                doc.metadata.update({
                    'filename': file.filename,
                    'source_path': file_path
                })
            
            # Dividir en chunks
            chunks = text_splitter.split_documents(documents)
            
            # Agregar al vectorstore
            vectorstore.add_documents(chunks)
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "chunks": len(chunks),
                "message": f"Procesado exitosamente ({len(chunks)} fragmentos)"
            })
            
            logger.info(f"📄 Archivo procesado: {file.filename} ({len(chunks)} fragmentos)")
            
        except Exception as e:
            logger.error(f"Error procesando {file.filename}: {e}")
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": f"Error: {str(e)}"
            })
    
    return {"results": results}
    
    for file in files:
        try:
            # Validar tipo de archivo
            allowed_extensions = ['.pdf', '.txt', '.docx', '.doc']
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            if file_extension not in allowed_extensions:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": f"Tipo de archivo no soportado: {file_extension}"
                })
                continue
            
            # Guardar archivo
            file_path = os.path.join(DATA_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Procesar documento
            documents = processor.load_document(file_path)
            
            if not documents:
                results.append({
                    "filename": file.filename,
                    "status": "error", 
                    "message": "No se pudo procesar el documento"
                })
                continue
            
            # Crear chunks
            chunks = processor.process_documents(documents)
            
            if chunks:
                # Agregar a la base vectorial
                vectorstore.add_documents(chunks)
                
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "message": f"Procesado exitosamente: {len(chunks)} fragmentos creados",
                    "chunks": len(chunks),
                    "pages": len(documents)
                })
                
                logger.info(f"✅ Archivo procesado: {file.filename} -> {len(chunks)} chunks")
            else:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "No se pudieron crear fragmentos del documento"
                })
                
        except Exception as e:
            logger.error(f"❌ Error procesando {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": f"Error interno: {str(e)}"
            })
    
    return {"results": results}

@app.post("/chat")
async def chat_endpoint(request: Request):
    """Endpoint de chat profesional en español"""
    form = await request.form()
    question = form.get("message")
    
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Pregunta vacía")
    
    try:
        # Prefijo para reforzar respuesta en español
        spanish_question = f"Responde en español: {question.strip()}"
        
        # Generar respuesta usando el chain
        result = qa_chain({"question": spanish_question})
        
        # Extraer información de fuentes
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append({
                    "filename": doc.metadata.get("filename", "Desconocido"),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
        
        return {
            "response": result["answer"],
            "sources": sources,
            "documents_found": len(sources),
            "metadata": {
                "model": MODELS[MODEL_NAME]["name"],
                "language": "español"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error en chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando pregunta: {str(e)}")

@app.post("/chat/clear")
async def clear_chat():
    """Limpiar historial de conversación"""
    memory.clear()
    return {"message": "Historial de conversación limpiado"}

@app.get("/api/chat/summary")
async def get_chat_summary():
    """Obtener resumen de la conversación actual"""
    chat_history = memory.chat_memory.messages
    if not chat_history:
        return {"summary": "No hay conversación activa", "message_count": 0}
    
    summary = f"Conversación con {len(chat_history)} mensajes"
    return {"summary": summary, "message_count": len(chat_history)}

@app.get("/api/documents")
async def get_documents_info():
    """Obtener información de documentos cargados"""
    
    # Contar documentos en el directorio
    doc_count = 0
    doc_types = {}
    total_size = 0
    
    if os.path.exists(DATA_DIR):
        for file_path in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, file_path)
            if os.path.isfile(full_path):
                doc_count += 1
                ext = os.path.splitext(file_path)[1].lower()
                doc_types[ext] = doc_types.get(ext, 0) + 1
                total_size += os.path.getsize(full_path)
    
    # Información del vectorstore
    vector_info = {"chunks": 0, "status": "empty"}
    try:
        if hasattr(vectorstore, '_collection') and vectorstore._collection:
            vector_info = {
                "chunks": vectorstore._collection.count(),
                "status": "active"
            }
    except Exception as e:
        logger.warning(f"No se pudo obtener info del vectorstore: {e}")
    
    return {
        "documents": {
            "count": doc_count,
            "types": doc_types,
            "total_size_mb": round(total_size / (1024*1024), 2)
        },
        "vectorstore": vector_info,
        "data_directory": DATA_DIR
    }
