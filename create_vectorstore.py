import os
import logging
import shutil
from config import DATA_DIR, VECTOR_DB_DIR, KNOWLEDGE_SOURCES
from embedding_model import AzureOpenAIEmbeddings
from utils import load_documents, categorize_and_index_documents

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vectorstore():
    """Create vector stores from documents"""
    
    # Supprimer l'ancienne base vectorielle si elle existe
    if os.path.exists(VECTOR_DB_DIR):
        logger.info(f"Suppression de l'ancienne base vectorielle dans {VECTOR_DB_DIR}")
        shutil.rmtree(VECTOR_DB_DIR)
    
    # Créer les répertoires nécessaires
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    for source_dir in KNOWLEDGE_SOURCES.values():
        os.makedirs(source_dir, exist_ok=True)
    
    # Initialiser le modèle d'embedding
    try:
        embeddings = AzureOpenAIEmbeddings()
        logger.info("Modèle d'embedding initialisé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du modèle d'embedding: {str(e)}")
        return False
    
    # Charger les documents
    documents = load_documents()
    logger.info(f"Chargement de {len(documents)} documents")
    
    if not documents:
        logger.warning("Aucun document trouvé à indexer")
        return False
    
    # Catégoriser et indexer les documents
    try:
        categorize_and_index_documents(documents, embeddings)
        logger.info("Documents catégorisés et indexés avec succès")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'indexation des documents: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Démarrage de la création de la base vectorielle...")
    if create_vectorstore():
        logger.info("Base vectorielle créée avec succès!")
    else:
        logger.error("Échec de la création de la base vectorielle")
