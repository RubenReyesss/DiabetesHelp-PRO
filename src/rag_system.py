"""
Sistema RAG (Retrieval Augmented Generation) para DiabetesHelp PRO
Busca documentos relevantes y los contextualiza al LLM
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import re

class RAGSystem:
    """Sistema de búsqueda y recuperación de documentos médicos"""
    
    def __init__(self, documents_dir: str = "rag_documents"):
        """Inicializa el sistema RAG"""
        self.documents_dir = documents_dir
        self.documents = {}
        self.chunks = []
        self.load_documents()
    
    def load_documents(self):
        """Carga todos los documentos .md del directorio"""
        if not os.path.exists(self.documents_dir):
            print(f"⚠️ Directorio {self.documents_dir} no encontrado")
            return
        
        for file in os.listdir(self.documents_dir):
            if file.endswith(".md"):
                filepath = os.path.join(self.documents_dir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.documents[file] = content
                        self._chunk_document(file, content)
                except Exception as e:
                    print(f"Error cargando {file}: {e}")
    
    def _chunk_document(self, filename: str, content: str, chunk_size: int = 500):
        """Divide documento en chunks para búsqueda eficiente"""
        # Dividir por secciones (##)
        sections = re.split(r'\n## ', content)
        
        for i, section in enumerate(sections):
            section = "## " + section if i > 0 else section
            # Si la sección es muy larga, dividirla
            if len(section) > chunk_size:
                words = section.split()
                chunk = []
                chunk_text = ""
                for word in words:
                    chunk_text += word + " "
                    if len(chunk_text) > chunk_size:
                        if chunk_text.strip():
                            self.chunks.append({
                                'filename': filename,
                                'content': chunk_text.strip(),
                                'section': section[:100]
                            })
                        chunk_text = ""
                if chunk_text.strip():
                    self.chunks.append({
                        'filename': filename,
                        'content': chunk_text.strip(),
                        'section': section[:100]
                    })
            else:
                self.chunks.append({
                    'filename': filename,
                    'content': section,
                    'section': section[:100]
                })
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Busca chunks relevantes basado en similitud de palabras clave
        """
        query_lower = query.lower()
        query_words = set(word for word in query_lower.split() if len(word) > 3)
        
        scores = []
        for chunk in self.chunks:
            content_lower = chunk['content'].lower()
            # Contar palabras coincidentes
            matches = sum(1 for word in query_words if word in content_lower)
            if matches > 0:
                # Bonus si la palabra aparece en título
                title_bonus = 2 if any(word in chunk['section'].lower() for word in query_words) else 0
                score = matches + title_bonus
                scores.append((score, chunk))
        
        # Ordenar por score descendente
        scores.sort(reverse=True, key=lambda x: x[0])
        return [chunk for _, chunk in scores[:top_k]]
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """
        Obtiene contexto de RAG para incluir en prompt del LLM
        """
        results = self.search(query, top_k)
        
        if not results:
            return ""
        
        context = "📚 CONTEXTO MÉDICO RELEVANTE:\n"
        context += "=" * 50 + "\n"
        
        for i, result in enumerate(results, 1):
            context += f"\n[Fuente {i}: {result['filename']}]\n"
            context += f"{result['content'][:400]}...\n"
        
        context += "\n" + "=" * 50 + "\n"
        return context
    
    def get_specific_document(self, doc_type: str) -> str:
        """
        Obtiene documento específico para contexto profundo
        Mapeo: tipo_diabetes -> archivo_recomendado
        """
        mapping = {
            'tipo1': '01_diabetes_tipo_1.md',
            'tipo2': '02_diabetes_tipo_2.md',
            'nutricion': '03_nutricion_carbohidratos.md',
            'monitoreo': '04_monitoreo_glucosa.md',
            'insulina': '01_diabetes_tipo_1.md',
            'carbohidratos': '03_nutricion_carbohidratos.md',
            'glucosa': '04_monitoreo_glucosa.md',
            'hipoglucemia': '04_monitoreo_glucosa.md',
            'hiperglucemia': '04_monitoreo_glucosa.md',
        }
        
        filename = mapping.get(doc_type.lower())
        if filename and filename in self.documents:
            return self.documents[filename]
        return ""
    
    def generate_context_prompt(self, user_profile: Dict, query: str) -> str:
        """
        Genera prompt aumentado con RAG para el LLM
        """
        # Búsqueda general
        general_context = self.get_context(query, top_k=2)
        
        # Contexto específico por tipo diabetes
        specific_context = ""
        diabetes_type = user_profile.get('diabetes_type', 'tipo2')
        specific_doc = self.get_specific_document(diabetes_type)
        
        if specific_doc:
            specific_context = f"\n\n📋 GUÍA ESPECÍFICA PARA {diabetes_type.upper()}:\n"
            specific_context += specific_doc[:1000] + "...\n"
        
        return general_context + specific_context
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del sistema RAG"""
        return {
            'documentos_cargados': len(self.documents),
            'chunks_totales': len(self.chunks),
            'tamaño_total_caracteres': sum(len(doc) for doc in self.documents.values()),
            'documentos': list(self.documents.keys())
        }


# Inicialización global (se carga una sola vez)
try:
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    rag = RAGSystem(str(project_root / "rag_documents"))
except Exception as e:
    print(f"⚠️ Error inicializando RAG: {e}")
    rag = None
