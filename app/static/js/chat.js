// JavaScript profesional para Chat RAG
document.addEventListener('DOMContentLoaded', function() {
    const chatDiv = document.getElementById('chat');
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const infoPanel = document.getElementById('info-panel');
    const responseInfo = document.getElementById('response-info');

    // Función para añadir mensajes al chat
    function addMessage(message, isUser = false, metadata = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        if (isUser) {
            messageDiv.innerHTML = `<strong>Tú:</strong><br>${message}`;
        } else {
            let content = `<strong>🤖 Asistente:</strong><br>${message}`;
            
            // Agregar información de fuentes si está disponible
            if (metadata && metadata.sources && metadata.sources.length > 0) {
                content += '<br><br><strong>📚 Fuentes consultadas:</strong><br>';
                metadata.sources.forEach((source, index) => {
                    content += `<small><strong>${index + 1}. ${source.filename}:</strong> ${source.preview}</small><br>`;
                });
            }
            
            // Agregar indicador de confianza
            if (metadata && metadata.confidence) {
                const confidenceEmoji = {
                    'high': '🟢',
                    'medium': '🟡', 
                    'low': '🔴',
                    'error': '❌'
                };
                content += `<br><small>${confidenceEmoji[metadata.confidence]} Confianza: ${metadata.confidence}</small>`;
            }
            
            messageDiv.innerHTML = content;
        }
        
        chatDiv.appendChild(messageDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
        
        // Mostrar información adicional
        if (metadata && !isUser) {
            showResponseInfo(metadata);
        }
    }

    // Función para mostrar información de la respuesta
    function showResponseInfo(metadata) {
        if (!responseInfo) return;
        
        let infoHTML = '<div class="metadata">';
        
        if (metadata.documents_found !== undefined) {
            infoHTML += `<span class="info-item">📄 Documentos: ${metadata.documents_found}</span>`;
        }
        
        if (metadata.confidence) {
            infoHTML += `<span class="info-item">🎯 Confianza: ${metadata.confidence.toUpperCase()}</span>`;
        }
        
        if (metadata.metadata && metadata.metadata.model) {
            infoHTML += `<span class="info-item">🤖 Modelo: ${metadata.metadata.model}</span>`;
        }
        
        infoHTML += '</div>';
        
        responseInfo.innerHTML = infoHTML;
        infoPanel.style.display = 'block';
    }

    // Manejar envío del formulario
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            // Deshabilitar form mientras procesa
            sendBtn.disabled = true;
            sendBtn.textContent = 'Procesando...';
            
            // Añadir mensaje del usuario
            addMessage(message, true);
            messageInput.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message=${encodeURIComponent(message)}`
                });
                
                if (response.ok) {
                    const result = await response.json();
                    
                    // Mostrar respuesta con metadata
                    addMessage(result.response || 'Respuesta recibida', false, {
                        sources: result.sources || [],
                        confidence: result.confidence || 'unknown',
                        documents_found: result.documents_found || 0,
                        metadata: result.metadata || {}
                    });
                } else {
                    const errorData = await response.json();
                    addMessage(`Error: ${errorData.detail || 'Error desconocido'}`, false);
                }
            } catch (error) {
                addMessage(`Error de conexión: ${error.message}`, false);
                console.error('Error:', error);
            } finally {
                // Rehabilitar form
                sendBtn.disabled = false;
                sendBtn.textContent = 'Enviar';
            }
        });
    }

    // Manejar carga de archivos con feedback mejorado
    const uploadForm = document.querySelector('form[action="/upload"]');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(uploadForm);
            const files = formData.getAll('files');
            
            if (files.length === 0 || (files.length === 1 && !files[0].name)) {
                addMessage('Por favor selecciona al menos un archivo.', false);
                return;
            }
            
            addMessage(`📤 Cargando ${files.length} archivo(s)...`, false);
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    
                    let summary = '📁 Resultados de carga:<br>';
                    let successCount = 0;
                    let errorCount = 0;
                    
                    result.results.forEach(fileResult => {
                        if (fileResult.status === 'success') {
                            successCount++;
                            summary += `✅ <strong>${fileResult.filename}</strong>: ${fileResult.message}<br>`;
                        } else {
                            errorCount++;
                            summary += `❌ <strong>${fileResult.filename}</strong>: ${fileResult.message}<br>`;
                        }
                    });
                    
                    summary += `<br>📊 Resumen: ${successCount} exitosos, ${errorCount} errores`;
                    
                    addMessage(summary, false);
                    uploadForm.reset();
                } else {
                    const errorData = await response.json();
                    addMessage(`Error cargando archivos: ${errorData.detail}`, false);
                }
            } catch (error) {
                addMessage(`Error de conexión al cargar archivos: ${error.message}`, false);
                console.error('Error:', error);
            }
        });
    }

    // Cargar información inicial de documentos
    loadDocumentInfo();

    async function loadDocumentInfo() {
        try {
            const response = await fetch('/api/documents');
            if (response.ok) {
                const info = await response.json();
                
                if (info.documents.count > 0) {
                    addMessage(`📚 Base de conocimiento cargada: ${info.documents.count} documentos (${info.documents.total_size_mb} MB) con ${info.vectorstore.chunks} fragmentos indexados.`, false);
                }
            }
        } catch (error) {
            console.log('No se pudo cargar información inicial de documentos');
        }
    }
});
