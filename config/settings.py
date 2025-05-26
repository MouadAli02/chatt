import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la base de données
POSTGRES_URI = os.getenv('POSTGRES_URI', 'sqlite:///app.db')

# Configuration de Flask
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Configuration de l'API OpenRouter
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Configuration du RAG
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
CHROMA_PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', './data/chroma')

# Configuration de l'API OpenRouter
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-4-scout:free"

# Configuration des embeddings
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu")

# Configuration de ChromaDB
CHROMA_COLLECTION_NAME = "ebus_documents"

# Configuration des dossiers de données
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

# Configuration du traitement d'images
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Configuration du RAG
MAX_CONTEXT_LENGTH = 2000
MAX_HISTORY_LENGTH = 5
CONFIDENCE_THRESHOLD = 0.7

# Création des dossiers nécessaires
for directory in [DATA_DIR, DOCUMENTS_DIR, UPLOAD_DIR, CHROMA_PERSIST_DIR]:
    os.makedirs(directory, exist_ok=True) 