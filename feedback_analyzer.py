import os
import logging
import json
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FeedbackAnalyzer:
    def __init__(self, conversation_manager, feedback_dir="feedback"):
        """
        Initialise l'analyseur de feedback

        Args:
            conversation_manager: Instance de ConversationManager pour accéder aux feedbacks
            feedback_dir: Répertoire où sont stockés les fichiers de feedback
        """
        self.conversation_manager = conversation_manager
        self.feedback_dir = feedback_dir

    def save_feedback(self, conv_id, message_id, feedback_type, comment=""):
        """
        Sauvegarde un feedback de manière centralisée

        Args:
            conv_id (str): ID de la conversation
            message_id (str): ID du message
            feedback_type (str): Type de feedback ('like' ou 'dislike')
            comment (str, optional): Commentaire optionnel sur le feedback

        Returns:
            tuple: (success, error_message)
        """
        if not conv_id or not message_id or not feedback_type:
            return False, "Missing required parameters"

        feedback = {
            'type': feedback_type,
            'timestamp': datetime.now().isoformat(),
            'comment': comment
        }

        # Ajouter le feedback au message
        if not self.conversation_manager.add_feedback_to_message(conv_id, message_id, feedback):
            return False, "Conversation or message not found"

        # Créer le répertoire feedback s'il n'existe pas
        os.makedirs(self.feedback_dir, exist_ok=True)

        # Chemin du fichier de feedback
        feedback_file = os.path.join(self.feedback_dir, f"{message_id}.json")

        try:
            # Sauvegarder le feedback dans un fichier
            with open(feedback_file, 'w') as f:
                json.dump(feedback, f, indent=2)

            # Sauvegarder les conversations (incluant les feedbacks)
            self.conversation_manager.save_conversations()
            return True, None

        except Exception as e:
            logger.error(f"Error saving feedback: {str(e)}")
            return False, f"Failed to save feedback: {str(e)}"
            
    def adjust_prompt_based_on_feedback(self, base_prompt):
        """
        Analyse les feedbacks récents et ajuste le prompt système en conséquence

        Args:
            base_prompt (str): Le prompt système de base

        Returns:
            str: Le prompt système ajusté en fonction des tendances de feedback
        """
        # Récupérer tous les feedbacks
        all_feedbacks = self.conversation_manager.get_all_feedback()
        
        # Si pas assez de feedbacks, retourner le prompt de base
        if len(all_feedbacks) < 5:
            logger.debug("Not enough feedback data to adjust prompt")
            return base_prompt
            
        # Analyser les tendances des feedbacks
        likes = 0
        dislikes = 0
        recent_comments = []
        
        # Ne prendre que les 20 feedbacks les plus récents pour l'analyse
        for feedback in sorted(all_feedbacks, key=lambda x: x.get('timestamp', ''), reverse=True)[:20]:
            if feedback.get('type') == 'like':
                likes += 1
            elif feedback.get('type') == 'dislike':
                dislikes += 1
                
            # Collecter les commentaires des dislikes
            if feedback.get('type') == 'dislike' and feedback.get('comment'):
                recent_comments.append(feedback.get('comment'))
                
        # Calculer le ratio de satisfaction
        total_feedbacks = likes + dislikes
        satisfaction_ratio = likes / total_feedbacks if total_feedbacks > 0 else 0.5
        
        # Ajuster le prompt en fonction du feedback
        adjusted_prompt = base_prompt
        
        # Si le taux de satisfaction est bas, ajouter des instructions spécifiques
        if satisfaction_ratio < 0.6:
            common_issues = self._identify_common_issues(recent_comments)
            if common_issues:
                adjusted_prompt += "\n\nPay special attention to these aspects based on user feedback:"
                for issue in common_issues:
                    adjusted_prompt += f"\n- {issue}"
        
        logger.info(f"Prompt adjusted based on {total_feedbacks} feedbacks (satisfaction: {satisfaction_ratio:.2f})")
        return adjusted_prompt
        
    def _identify_common_issues(self, comments):
        """
        Identifie les problèmes communs dans les commentaires de feedback négatif
        
        Args:
            comments (list): Liste des commentaires de feedback
            
        Returns:
            list: Liste des problèmes identifiés
        """
        # Mots clés pour rechercher des problèmes spécifiques
        issue_keywords = {
            "trop long": "Be more concise and to the point",
            "pas clair": "Provide clearer explanations",
            "hors sujet": "Stay more focused on the user's specific question",
            "imprécis": "Be more precise in your answers",
            "incorrect": "Double-check information for accuracy",
            "incomplet": "Provide more comprehensive answers",
            "confus": "Structure your responses more clearly"
        }
        
        issues = set()
        
        for comment in comments:
            if not isinstance(comment, str):
                continue
                
            comment_lower = comment.lower()
            for keyword, suggestion in issue_keywords.items():
                if keyword in comment_lower:
                    issues.add(suggestion)
        
        return list(issues)
