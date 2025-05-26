import logging
import json
import time
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
from enum import Enum
from langdetect import detect
from openai import AzureOpenAI, APIError
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Language(Enum):
    """Énumération des langues supportées"""
    FRENCH = "fr"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    UNKNOWN = "unknown"

@dataclass
class APIResponse:
    """Structure de données pour les réponses API"""
    content: str
    usage: Dict[str, int]
    sources: List[Dict[str, Any]] = None
    confidence: float = 0.0
    language: Language = Language.UNKNOWN
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la réponse en dictionnaire"""
        return {
            "content": self.content,
            "usage": self.usage,
            "sources": self.sources or [],
            "confidence": self.confidence,
            "language": self.language.value,
            "processing_time": self.processing_time
        }

class PromptManager:
    """Gestionnaire de prompts système multilingues"""
    
    SYSTEM_PROMPTS = {
        Language.FRENCH: """Vous êtes un assistant IA expert intégré dans une base de connaissances d'entreprise. 
Votre mission est de fournir des réponses précises, structurées et utiles basées exclusivement sur le contexte fourni.

## Instructions principales :
- **Langue** : Répondez toujours dans la même langue que la question
- **Sources** : Basez toutes vos réponses uniquement sur le contexte fourni
- **Transparence** : Si l'information n'est pas disponible dans le contexte, indiquez-le clairement
- **Exactitude** : Ne jamais inventer ou extrapoler d'informations

## Structure de réponse :
- Utilisez des paragraphes courts et clairs
- Organisez les informations avec des listes à puces pour les points clés
- Mettez en **gras** les informations cruciales
- Créez des sections bien délimitées avec des titres
- Citez vos sources spécifiques quand disponible""",

        Language.ENGLISH: """You are an expert AI assistant embedded in an enterprise knowledge base. 
Your mission is to provide accurate, structured, and helpful responses based exclusively on the provided context.

## Key Instructions:
- **Language**: Always respond in the same language as the question
- **Sources**: Base all answers only on the provided context
- **Transparency**: If information is not available in the context, clearly state this
- **Accuracy**: Never fabricate or extrapolate information

## Response Structure:
- Use short, clear paragraphs
- Organize information with bullet points for key items
- Use **bold** text for crucial information
- Create well-defined sections with headers
- Cite specific sources when available""",
    }
    
    @classmethod
    def get_system_prompt(cls, language: Language, custom_prompt: str = None) -> str:
        """Retourne le prompt système pour la langue spécifiée"""
        if custom_prompt:
            return custom_prompt
        return cls.SYSTEM_PROMPTS.get(language, cls.SYSTEM_PROMPTS[Language.ENGLISH])

class AzureOpenAIManager:
    """Gestionnaire Azure OpenAI"""
    
    def __init__(self, api_key: str, api_base: str, deployment_id: str):
        """Initialise le client Azure OpenAI"""
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=api_base
        )
        self.deployment_id = deployment_id
        self.prompt_manager = PromptManager()
        
        # Initialiser le modèle d'embeddings
        from embedding_model import AzureOpenAIEmbeddings
        self.embeddings = AzureOpenAIEmbeddings()
        
        # Initialiser HybridRAG
        from hybrid_rag import HybridRAG
        self.hybrid_rag = HybridRAG(embeddings=self.embeddings)
        
        logger.info("Client Azure OpenAI initialisé avec succès")
    
    def generate_response(self, 
                         user_message: str, 
                         conversation_history: List[Dict[str, str]] = None,
                         system_prompt: str = None,
                         use_rag: bool = True,
                         temperature: float = None,
                         max_tokens: int = None) -> Dict:
        """Génère une réponse complète avec RAG optionnel"""
        try:
            # Détecter la langue
            detected_language = self.detect_language(user_message)
            logger.info(f"Langue détectée: {detected_language}")
            
            # Utiliser HybridRAG pour obtenir le contexte et les sources
            context, sources = self.hybrid_rag.search_and_format_context(user_message)
            logger.info(f"Contexte trouvé: {len(sources)} sources")
            
            # Préparer les messages
            messages = []
            
            # Ajouter le prompt système
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": self.prompt_manager.get_system_prompt(detected_language)})
            
            # Ajouter l'historique de conversation
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Préparer le message avec le contexte
            context_prompt = f"""Question de l'utilisateur:
{user_message}

Contexte:
{context}"""

            # Ajouter le message avec contexte
            messages.append({"role": "user", "content": context_prompt})
            
            # Appeler l'API
            response = self.client.chat.completions.create(
                model=self.deployment_id,
                messages=messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens or 2000
            )
            
            # Extraire la réponse
            assistant_message = response.choices[0].message.content
            
            # Préparer la réponse finale
            result = {
                "response": assistant_message,
                "sources": [str(source) for source in sources],
                "confidence": 0.9 if sources else 0.3,
                "language": str(detected_language)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse: {str(e)}", exc_info=True)
            raise

    def detect_language(self, text: str) -> str:
        """Détecte la langue du texte"""
        try:
            detected_language = detect(text)
            if detected_language in ['fr', 'fr-ca', 'fr-fr']:
                detected_language = 'fr'
            elif detected_language.startswith('en'):
                detected_language = 'en'
        except Exception as e:
            logger.warning(f"Erreur lors de la détection de langue: {str(e)}")
            detected_language = 'en'
        
        return detected_language

def create_azure_openai_manager(api_key: str, api_base: str, deployment_id: str) -> AzureOpenAIManager:
    """Factory function pour créer un gestionnaire Azure OpenAI"""
    return AzureOpenAIManager(
        api_key=api_key,
        api_base=api_base,
        deployment_id=deployment_id
    )

if __name__ == "__main__":
    # Test basique
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        manager = create_azure_openai_manager(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_base=os.getenv("AZURE_OPENAI_API_BASE"),
            deployment_id=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
        )
        
        # Test de génération
        response = manager.generate_response("Hello, how are you?")
        print(f"Réponse: {response['response']}")
        print(f"Temps de traitement: {response['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"Erreur lors du test: {str(e)}")