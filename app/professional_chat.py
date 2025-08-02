"""
Sistema de chat profesional para RAG
Optimizado para respuestas coherentes y precisas
"""

from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging

logger = logging.getLogger(__name__)

class ProfessionalRAGChat:
    """Sistema de chat RAG profesional"""
    
    def __init__(self, llm, retriever, memory_window: int = 10):
        self.llm = llm
        self.retriever = retriever
        
        # Memoria con ventana deslizante para mantener contexto relevante
        self.memory = ConversationBufferWindowMemory(
            k=memory_window,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Prompt profesional optimizado
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""Eres un asistente especializado en análisis de documentos. Tu tarea es proporcionar respuestas precisas, coherentes y útiles basadas ÚNICAMENTE en la información de los documentos proporcionados.

CONTEXTO DE DOCUMENTOS:
{context}

HISTORIAL DE CONVERSACIÓN:
{chat_history}

INSTRUCCIONES:
1. Basa tu respuesta EXCLUSIVAMENTE en la información de los documentos del contexto
2. Si la información no está en los documentos, di claramente: "No encuentro esa información en los documentos proporcionados"
3. Cita específicamente qué documento o sección respalda tu respuesta
4. Mantén un tono profesional y preciso
5. Estructura tu respuesta de manera clara y organizada
6. Si hay múltiples perspectivas en los documentos, méncionalas todas

PREGUNTA: {question}

RESPUESTA PROFESIONAL:"""
        )
        
        # Chain para generar respuestas
        self.qa_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=True
        )
    
    def get_response(self, question: str) -> Dict[str, Any]:
        """Generar respuesta profesional basada en documentos"""
        
        try:
            # 1. Obtener documentos relevantes
            logger.info(f"🔍 Buscando información para: {question}")
            relevant_docs = self.retriever.get_relevant_documents(question)
            
            if not relevant_docs:
                return {
                    "answer": "No encontré documentos relevantes para responder tu pregunta. Por favor, asegúrate de haber cargado documentos relacionados con el tema.",
                    "sources": [],
                    "confidence": "low",
                    "documents_found": 0
                }
            
            # 2. Preparar contexto con información de fuentes
            context_parts = []
            sources = []
            
            for i, doc in enumerate(relevant_docs, 1):
                filename = doc.metadata.get('filename', 'Documento desconocido')
                content = doc.page_content.strip()
                
                context_parts.append(f"[DOCUMENTO {i}: {filename}]\n{content}")
                sources.append({
                    'filename': filename,
                    'preview': content[:200] + "..." if len(content) > 200 else content
                })
            
            context = "\n\n".join(context_parts)
            
            # 3. Obtener historial para contexto
            chat_history = self._format_chat_history()
            
            # 4. Generar respuesta
            logger.info(f"🤖 Generando respuesta con {len(relevant_docs)} documentos")
            
            response = self.qa_chain.run(
                context=context,
                question=question,
                chat_history=chat_history
            )
            
            # 5. Evaluar confianza de la respuesta
            confidence = self._evaluate_confidence(response, relevant_docs)
            
            return {
                "answer": response.strip(),
                "sources": sources,
                "confidence": confidence,
                "documents_found": len(relevant_docs),
                "context_length": len(context)
            }
            
        except Exception as e:
            logger.error(f"❌ Error generando respuesta: {str(e)}")
            return {
                "answer": f"Disculpa, ocurrió un error al procesar tu pregunta: {str(e)}",
                "sources": [],
                "confidence": "error",
                "documents_found": 0
            }
    
    def _format_chat_history(self) -> str:
        """Formatear historial de chat para el prompt"""
        if not hasattr(self.memory, 'chat_memory') or not self.memory.chat_memory.messages:
            return "No hay conversación previa."
        
        history_parts = []
        for message in self.memory.chat_memory.messages[-6:]:  # Últimos 3 intercambios
            if isinstance(message, HumanMessage):
                history_parts.append(f"Usuario: {message.content}")
            elif isinstance(message, AIMessage):
                history_parts.append(f"Asistente: {message.content}")
        
        return "\n".join(history_parts) if history_parts else "No hay conversación previa."
    
    def _evaluate_confidence(self, response: str, docs: List) -> str:
        """Evaluar confianza en la respuesta"""
        
        # Indicadores de baja confianza
        low_confidence_phrases = [
            "no encuentro", "no está disponible", "no puedo determinar",
            "no está claro", "información insuficiente"
        ]
        
        response_lower = response.lower()
        
        if any(phrase in response_lower for phrase in low_confidence_phrases):
            return "low"
        elif len(docs) >= 3 and len(response) > 200:
            return "high"
        elif len(docs) >= 2:
            return "medium"
        else:
            return "low"
    
    def clear_memory(self):
        """Limpiar memoria de conversación"""
        self.memory.clear()
        logger.info("🧹 Memoria de conversación limpiada")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Obtener resumen de la conversación actual"""
        messages = self.memory.chat_memory.messages if hasattr(self.memory, 'chat_memory') else []
        
        return {
            "total_messages": len(messages),
            "user_questions": len([m for m in messages if isinstance(m, HumanMessage)]),
            "ai_responses": len([m for m in messages if isinstance(m, AIMessage)]),
            "last_activity": messages[-1].content[:100] + "..." if messages else "Sin actividad"
        }
