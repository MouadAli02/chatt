import logging
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ResponseStyle(Enum):
    CONCISE = "concise"  # Réponses courtes et directes
    NORMAL = "normal"    # Réponses standard
    DETAILED = "detailed" # Réponses détaillées

class ConversationManager:
    def __init__(self):
        self.conversations = {}  # Stockage en mémoire des conversations
        self.default_conversation_length = 20  # Augmentation de la limite par défaut
        self.backup_file = "conversations_backup.json"
        self.load_conversations()  # Chargement automatique au démarrage
        
    def is_message_complete(self, content: str) -> bool:
        """Vérifie si un message est complet
        
        Args:
            content: Le contenu du message à vérifier
            
        Returns:
            bool: True si le message semble complet, False sinon
        """
        # Vérifie si le message se termine par une ponctuation finale
        if not content.strip():
            return False
            
        # Liste des ponctuations finales courantes
        final_punctuations = ['.', '!', '?', ':', ';']
        
        # Vérifie si le message se termine par une ponctuation finale
        last_char = content.strip()[-1]
        if last_char in final_punctuations:
            return True
            
        # Vérifie si le message contient des balises HTML ou Markdown non fermées
        open_tags = ['<', '```', '`', '*', '_', '[']
        close_tags = ['>', '```', '`', '*', '_', ']']
        
        for open_tag, close_tag in zip(open_tags, close_tags):
            if content.count(open_tag) != content.count(close_tag):
                return False
                
        return True
        
    def add_message(self, conv_id: str, role: str, content: str, max_history: int = None, is_complete: bool = None) -> str:
        """Ajoute un message à la conversation et retourne l'ID du message"""
        if conv_id not in self.conversations:
            self.create_conversation(conv_id)
            
        max_history = max_history or self.default_conversation_length
        
        # Generate a unique message ID
        message_id = str(uuid.uuid4())
        
        # Détermine si le message est complet si non spécifié
        if is_complete is None:
            is_complete = self.is_message_complete(content)
        
        self.conversations[conv_id]['messages'].append({
            'id': message_id,
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'feedback': None,
            'is_complete': is_complete
        })
        
        # Limiter la taille de l'historique
        if len(self.conversations[conv_id]['messages']) > max_history * 2:
            self.conversations[conv_id]['messages'] = self.conversations[conv_id]['messages'][-max_history * 2:]
            
        # Mettre à jour le timestamp de la conversation
        self.conversations[conv_id]['timestamp'] = datetime.now().isoformat()
        
        # Sauvegarde automatique après chaque message
        self.save_conversations()
        
        return message_id
    
    def create_conversation(self, conv_id: str = None, title: str = "New Chat", language: str = "fr", response_style: ResponseStyle = ResponseStyle.CONCISE) -> str:
        """Crée une nouvelle conversation
        
        Args:
            conv_id: ID de la conversation (optionnel)
            title: Titre de la conversation
            language: Langue de la conversation (par défaut: 'fr' pour français)
            response_style: Style de réponse souhaité (par défaut: CONCISE)
        """
        if not conv_id:
            conv_id = str(uuid.uuid4())
            
        self.conversations[conv_id] = {
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'messages': [],
            'metadata': {
                'topic_classification': None,
                'language': language,
                'response_style': response_style.value
            }
        }
        return conv_id
    
    def get_conversation(self, conv_id: str) -> Dict:
        """Récupère une conversation par son ID"""
        return self.conversations.get(conv_id, None)
    
    def get_all_conversations(self) -> List[Dict]:
        """Récupère toutes les conversations"""
        return [
            {
                'id': conv_id,
                'title': conv['title'],
                'timestamp': conv['timestamp'],
                'messages': len(conv['messages'])
            }
            for conv_id, conv in self.conversations.items()
        ]
    
    def delete_conversation(self, conv_id: str) -> bool:
        """Supprime une conversation"""
        if conv_id in self.conversations:
            del self.conversations[conv_id]
            return True
        return False
    
    def rename_conversation(self, conv_id: str, new_title: str) -> bool:
        """Renomme une conversation"""
        if conv_id in self.conversations:
            self.conversations[conv_id]['title'] = new_title
            return True
        return False
    
    def get_conversation_history(self, conv_id: str, max_length: int = None) -> List[Dict]:
        """Récupère l'historique d'une conversation"""
        if conv_id not in self.conversations:
            return []
            
        max_length = max_length or self.default_conversation_length
        messages = self.conversations[conv_id]['messages']
        
        # Limiter le nombre de messages retournés
        if len(messages) > max_length * 2:
            return messages[-max_length * 2:]
        return messages
    
    def format_history_for_prompt(self, conv_id: str, max_length: int = None) -> str:
        """Formate l'historique de conversation pour le prompt"""
        messages = self.get_conversation_history(conv_id, max_length)
        formatted_history = []
        
        for msg in messages:
            role_prefix = "User" if msg['role'] == 'user' else "Assistant"
            formatted_history.append(f"{role_prefix}: {msg['content']}")
            
        return "\n\n".join(formatted_history)
    
    def add_feedback_to_message(self, conv_id: str, message_id: str, feedback: Dict) -> bool:
        """Ajoute un feedback à un message spécifique"""
        if conv_id not in self.conversations:
            return False
            
        # Add timestamp if not present
        if 'timestamp' not in feedback:
            feedback['timestamp'] = datetime.now().isoformat()
        
        # Find the message with the given ID
        for message in self.conversations[conv_id]['messages']:
            if message.get('id') == message_id:
                message['feedback'] = feedback
                return True
                
        return False
        
    def get_message(self, conv_id: str, message_id: str) -> Optional[Dict]:
        """Récupère un message spécifique par son ID"""
        if conv_id not in self.conversations:
            return None
            
        for message in self.conversations[conv_id]['messages']:
            if message.get('id') == message_id:
                return message
                
        return None
        
    def classify_conversation_topic(self, conv_id: str, topic: str) -> bool:
        """Classifie le sujet d'une conversation"""
        if conv_id not in self.conversations:
            return False
            
        self.conversations[conv_id]['metadata']['topic_classification'] = topic
        return True
    
    def save_conversations(self, filename: str = None) -> bool:
        """Sauvegarde toutes les conversations dans un fichier JSON"""
        try:
            filename = filename or self.backup_file
            # S'assurer que le répertoire existe
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving conversations: {str(e)}")
            return False
    
    def load_conversations(self, filename: str = None) -> bool:
        """Charge les conversations depuis un fichier JSON"""
        try:
            filename = filename or self.backup_file
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
                    
                    # Add message IDs to existing messages if they don't have one
                    for conv_id, conv in conversations.items():
                        for message in conv.get('messages', []):
                            if 'id' not in message:
                                message['id'] = str(uuid.uuid4())
                            if 'feedback' not in message:
                                message['feedback'] = None
                            if 'is_complete' not in message:
                                message['is_complete'] = True
                    
                    self.conversations = conversations
                return True
            else:
                # Si le fichier n'existe pas, on crée un fichier vide
                logger.info(f"Le fichier {filename} n'existe pas. Création d'un nouveau fichier.")
                self.conversations = {}
                self.save_conversations(filename)
                return True
        except Exception as e:
            logger.error(f"Error loading conversations: {str(e)}")
            # En cas d'erreur, on initialise avec un dictionnaire vide
            self.conversations = {}
            return False
    
    def get_all_feedback(self) -> List[Dict]:
        """Récupère tous les feedbacks de tous les messages"""
        all_feedback = []
        
        for conv_id, conv in self.conversations.items():
            for message in conv.get('messages', []):
                if message.get('feedback'):
                    feedback = message['feedback'].copy()
                    feedback['conversation_id'] = conv_id
                    feedback['message_id'] = message.get('id')
                    feedback['message_content'] = message.get('content')
                    feedback['message_role'] = message.get('role')
                    all_feedback.append(feedback)
                    
        return all_feedback

    def set_conversation_language(self, conv_id: str, language: str) -> bool:
        """Change la langue d'une conversation existante
        
        Args:
            conv_id: ID de la conversation
            language: Nouvelle langue (ex: 'fr' pour français, 'en' pour anglais)
            
        Returns:
            bool: True si la modification a réussi, False sinon
        """
        if conv_id not in self.conversations:
            return False
            
        self.conversations[conv_id]['metadata']['language'] = language
        return True

    def get_conversation_language(self, conv_id: str) -> Optional[str]:
        """Récupère la langue d'une conversation
        
        Args:
            conv_id: ID de la conversation
            
        Returns:
            str: La langue de la conversation ou None si la conversation n'existe pas
        """
        if conv_id not in self.conversations:
            return None
            
        return self.conversations[conv_id]['metadata'].get('language')

    def get_incomplete_messages(self, conv_id: str) -> List[Dict]:
        """Récupère tous les messages incomplets d'une conversation
        
        Args:
            conv_id: ID de la conversation
            
        Returns:
            List[Dict]: Liste des messages incomplets
        """
        if conv_id not in self.conversations:
            return []
            
        return [
            message for message in self.conversations[conv_id]['messages']
            if not message.get('is_complete', True)
        ]

    def update_message_content(self, conv_id: str, message_id: str, new_content: str) -> bool:
        """Met à jour le contenu d'un message existant
        
        Args:
            conv_id: ID de la conversation
            message_id: ID du message à mettre à jour
            new_content: Nouveau contenu du message
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if conv_id not in self.conversations:
            return False
            
        for message in self.conversations[conv_id]['messages']:
            if message.get('id') == message_id:
                message['content'] = new_content
                message['is_complete'] = self.is_message_complete(new_content)
                return True
                
        return False

    def set_response_style(self, conv_id: str, style: ResponseStyle) -> bool:
        """Change le style de réponse d'une conversation
        
        Args:
            conv_id: ID de la conversation
            style: Nouveau style de réponse (CONCISE, NORMAL, ou DETAILED)
            
        Returns:
            bool: True si la modification a réussi, False sinon
        """
        if conv_id not in self.conversations:
            return False
            
        self.conversations[conv_id]['metadata']['response_style'] = style.value
        return True

    def get_response_style(self, conv_id: str) -> Optional[ResponseStyle]:
        """Récupère le style de réponse actuel d'une conversation
        
        Args:
            conv_id: ID de la conversation
            
        Returns:
            ResponseStyle: Le style de réponse actuel ou None si la conversation n'existe pas
        """
        if conv_id not in self.conversations:
            return None
            
        style_value = self.conversations[conv_id]['metadata'].get('response_style')
        return ResponseStyle(style_value) if style_value else None

    def get_response_guidelines(self, conv_id: str) -> Dict:
        """Récupère les directives de réponse pour une conversation
        
        Args:
            conv_id: ID de la conversation
            
        Returns:
            Dict: Directives de réponse basées sur le style actuel
        """
        style = self.get_response_style(conv_id) or ResponseStyle.CONCISE
        
        guidelines = {
            ResponseStyle.CONCISE: {
                'max_length': 100,  # Caractères
                'max_sentences': 2,
                'include_examples': False,
                'include_explanations': False
            },
            ResponseStyle.NORMAL: {
                'max_length': 300,
                'max_sentences': 4,
                'include_examples': True,
                'include_explanations': True
            },
            ResponseStyle.DETAILED: {
                'max_length': 1000,
                'max_sentences': 8,
                'include_examples': True,
                'include_explanations': True
            }
        }
        
        return guidelines[style]
