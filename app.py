from flask import Flask, request, jsonify, render_template
import os
import logging
from datetime import datetime, timedelta
import jwt
import hashlib
from dotenv import load_dotenv

# Import custom modules
from utils import load_documents, categorize_and_index_documents
from config import (
    API_KEY, API_BASE, DEPLOYMENT_ID, MODEL_NAME,
    EMBEDDING_MODEL, DATA_DIR, VECTOR_DB_DIR, KNOWLEDGE_SOURCES,
    MAX_HISTORY_LENGTH
)
from embedding_model import AzureOpenAIEmbeddings
from conversation_manager import ConversationManager
from hybrid_rag import HybridRAG
from api_manager import AzureOpenAIManager

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate API key
if not API_KEY or not API_BASE or not DEPLOYMENT_ID:
    raise ValueError("Azure OpenAI configuration is missing. Please set API_KEY, API_BASE, and DEPLOYMENT_ID in the .env file.")

# Configuration de l'application Flask
app = Flask(__name__)

# Variables globales
documents = []
conversation_manager = ConversationManager()
api_manager = None
embedding_model = None
is_initialized = False

def initialize_app():
    """Initialise l'application et ses composants"""
    global api_manager, embedding_model, is_initialized
    
    try:
        # Vérifier les variables d'environnement requises
        if not all([API_KEY, API_BASE, DEPLOYMENT_ID]):
            raise ValueError("Variables d'environnement manquantes")
            
        # Créer les répertoires nécessaires
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)
        for source_dir in KNOWLEDGE_SOURCES.values():
            os.makedirs(source_dir, exist_ok=True)
            
        # Initialiser le modèle d'embedding
        embedding_model = AzureOpenAIEmbeddings()
        
        # Initialiser le gestionnaire d'API Azure OpenAI
        api_manager = AzureOpenAIManager(
            api_key=API_KEY,
            api_base=API_BASE,
            deployment_id=DEPLOYMENT_ID
        )
        
        # Vérifier si la base vectorielle existe et est valide
        vector_db_exists = os.path.exists(VECTOR_DB_DIR) and any(
            os.path.exists(os.path.join(VECTOR_DB_DIR, source)) and 
            os.listdir(os.path.join(VECTOR_DB_DIR, source))
            for source in KNOWLEDGE_SOURCES.keys()
        )
        
        if not vector_db_exists:
            logger.info("Base vectorielle non trouvée ou vide, création en cours...")
            from create_vectorstore import create_vectorstore
            if not create_vectorstore():
                raise Exception("Échec de la création de la base vectorielle")
            logger.info("Base vectorielle créée avec succès")
        else:
            # Charger et indexer les documents
            documents = load_documents()
            if documents:
                categorize_and_index_documents(documents, embedding_model)
                logger.info(f"Documents chargés et indexés: {len(documents)}")
            else:
                logger.warning("Aucun document trouvé à charger")
            
        is_initialized = True
        logger.info("Application initialisée avec succès")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {str(e)}")
        return False

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    return jsonify(conversation_manager.get_all_conversations())

@app.route('/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    conv_id = conversation_manager.create_conversation()
    return jsonify({'id': conv_id, 'title': 'New Chat'})

@app.route('/conversations/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    """Get a specific conversation"""
    conversation = conversation_manager.get_conversation(conv_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    return jsonify(conversation)

@app.route('/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    """Delete a conversation"""
    if not conversation_manager.delete_conversation(conv_id):
        return jsonify({'error': 'Conversation not found'}), 404
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour le chat"""
    try:
        # Vérifier l'initialisation
        if not all([api_manager, embedding_model]):
            logger.error("Application non initialisée correctement")
            return jsonify({
                'error': 'Erreur d\'initialisation',
                'details': 'L\'application n\'a pas pu être initialisée correctement'
            }), 500
        
        # Récupérer les paramètres de la requête
        data = request.get_json()
        
        if not data:
            logger.error("Aucune donnée reçue dans la requête")
            return jsonify({'error': 'Données manquantes'}), 400
        
        # Accepter soit 'message' soit 'question'
        user_message = data.get('message', data.get('question', '')).strip()
        conv_id = data.get('conversation_id')
        
        if not user_message:
            logger.error("Message vide reçu")
            return jsonify({'error': 'Message vide'}), 400
            
        # Créer une nouvelle conversation si nécessaire
        if not conv_id:
            conv_id = conversation_manager.create_conversation()
            
        # Ajouter le message de l'utilisateur à l'historique
        message_id = conversation_manager.add_message(conv_id, 'user', user_message)
        
        # Récupérer l'historique de la conversation
        conversation_history = conversation_manager.get_conversation_history(conv_id)
        
        # Générer la réponse
        try:
            response = api_manager.generate_response(
                user_message,
                conversation_history
            )
            
            # Ajouter la réponse de l'assistant à l'historique
            assistant_message_id = conversation_manager.add_message(
                conv_id,
                'assistant',
                response['response']
            )
            
            # Ajouter les IDs de message à la réponse
            response['message_id'] = message_id
            response['assistant_message_id'] = assistant_message_id
            response['conversation_id'] = conv_id
            
            return jsonify(response)
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse: {str(e)}")
            return jsonify({
                'error': 'Erreur lors de la génération de la réponse',
                'details': str(e)
            }), 500
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la requête: {str(e)}")
        return jsonify({
            'error': 'Erreur interne',
            'details': str(e)
        }), 500

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Endpoint pour vérifier l'état du système"""
    status = {
        "status": "ok" if is_initialized else "initializing",
        "documents_count": len(documents) if documents else 0,
        "conversations_count": len(conversation_manager.conversations)
    }
    return jsonify(status)

if __name__ == '__main__':
    if initialize_app():
        app.run(debug=False)
    else:
        logger.error("Impossible de démarrer l'application")