import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration Azure OpenAI
API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
MODEL_NAME = os.getenv("MODEL_NAME")

# Configuration des embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
EMBEDDING_DEPLOYMENT_ID = os.getenv("EMBEDDING_DEPLOYMENT_ID", "text-embedding-ada-002")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")

# Configuration des dossiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")
FEEDBACK_DIR = os.path.join(DATA_DIR, "feedback")

# Configuration des sources de connaissances
KNOWLEDGE_SOURCES = {
    "documentation": os.path.join(DATA_DIR, "documentation"),
    "faqs": os.path.join(DATA_DIR, "faqs"),
    "troubleshooting": os.path.join(DATA_DIR, "troubleshooting")
}

# Création des dossiers nécessaires
for directory in [DATA_DIR, VECTOR_DB_DIR, FEEDBACK_DIR] + list(KNOWLEDGE_SOURCES.values()):
    os.makedirs(directory, exist_ok=True)

# Configuration du RAG
MAX_CONTEXT_LENGTH = 15000
MAX_HISTORY_LENGTH = 5
CONFIDENCE_THRESHOLD = 0.7

# Application Settings
DEFAULT_CONVERSATION_LENGTH = 5
MAX_SEARCH_RESULTS = 8
APP_PORT = 5000
APP_HOST = "0.0.0.0"
