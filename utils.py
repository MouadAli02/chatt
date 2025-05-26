import os
import logging
import json
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from langchain_community.vectorstores import Chroma
from config import (
    DATA_DIR, VECTOR_DB_DIR, KNOWLEDGE_SOURCES,
    EMBEDDING_MODEL, EMBEDDING_DEPLOYMENT_ID
)
from embedding_model import AzureOpenAIEmbeddings

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_documents() -> List[Dict[str, Any]]:
    """Charge tous les documents des sources de connaissances"""
    documents = []
    
    # Parcourir chaque source de connaissances
    for source_name, source_dir in KNOWLEDGE_SOURCES.items():
        logger.info(f"Chargement des documents depuis {source_dir}")
        
        if not os.path.exists(source_dir):
            logger.warning(f"Le répertoire {source_dir} n'existe pas")
            continue
            
        # Parcourir tous les fichiers du répertoire
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            
            # Ignorer les fichiers cachés et les répertoires
            if filename.startswith('.') or os.path.isdir(file_path):
                continue
                
            try:
                # Charger le document en fonction de son extension
                if filename.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                elif filename.endswith('.pdf'):
                    loader = PDFMinerLoader(file_path)
                elif filename.endswith('.docx'):
                    loader = Docx2txtLoader(file_path)
                elif filename.endswith('.md'):
                    loader = UnstructuredMarkdownLoader(file_path)
                else:
                    logger.warning(f"Format de fichier non supporté: {filename}")
                    continue
                    
                # Charger le contenu
                doc = loader.load()
                
                # Ajouter les métadonnées
                for page in doc:
                    page.metadata.update({
                        'source': source_name,
                        'filename': filename,
                        'file_path': file_path,
                        'content_type': 'text'
                    })
                    
                documents.extend(doc)
                logger.info(f"Document chargé: {filename}")
                
            except Exception as e:
                logger.error(f"Erreur lors du chargement de {filename}: {str(e)}")
                continue
                
    logger.info(f"Total des documents chargés: {len(documents)}")
    return documents

def split_documents(documents: List[Dict[str, Any]], chunk_size: int = 500, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
    """Découpe les documents en chunks plus petits"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""]
    )
    
    split_docs = text_splitter.split_documents(documents)
    logger.info(f"Documents découpés en {len(split_docs)} chunks")
    return split_docs

def categorize_and_index_documents(documents: List[Dict[str, Any]], embeddings: AzureOpenAIEmbeddings) -> None:
    """Catégorise et indexe les documents dans les vector stores appropriées"""
    if not documents:
        logger.warning("Aucun document à indexer")
        return
        
    # Découper les documents en chunks
    split_docs = split_documents(documents)
    
    # Grouper les documents par source
    docs_by_source = {}
    for doc in split_docs:
        source = doc.metadata.get('source', 'unknown')
        if source not in docs_by_source:
            docs_by_source[source] = []
        docs_by_source[source].append(doc)
    
    # Créer ou mettre à jour les vector stores pour chaque source
    for source_name, source_docs in docs_by_source.items():
        try:
            # Chemin vers la vector store
            persist_directory = os.path.join(VECTOR_DB_DIR, source_name)
            os.makedirs(persist_directory, exist_ok=True)
            
            logger.info(f"Indexation de {len(source_docs)} documents pour {source_name}")
            
            # Créer ou charger la vector store
            vector_store = Chroma.from_documents(
                documents=source_docs,
                embedding=embeddings,
                persist_directory=persist_directory
            )
            
            # Sauvegarder la vector store
            vector_store.persist()
            
            logger.info(f"Vector store mise à jour pour {source_name}: {len(source_docs)} documents")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'indexation des documents pour {source_name}: {str(e)}")
            continue 