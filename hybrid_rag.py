import os
import logging
import re
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Dict, Tuple, Set, Any
import math
from functools import lru_cache
import hashlib
from config import VECTOR_DB_DIR, KNOWLEDGE_SOURCES

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cache pour les embeddings
EMBEDDING_CACHE_SIZE = 1000

class HybridRAG:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_stores = {}
        self.initialize_vector_stores()
        self._query_cache = {}
        
    def initialize_vector_stores(self):
        """Initialise les différentes bases vectorielles"""
        for source_name, source_dir in KNOWLEDGE_SOURCES.items():
            try:
                vector_store_path = os.path.join(VECTOR_DB_DIR, source_name)
                if os.path.exists(vector_store_path):
                    try:
                        self.vector_stores[source_name] = Chroma(
                            persist_directory=vector_store_path,
                            embedding_function=self.embeddings
                        )
                        logger.info(f"Loaded vector store for {source_name} from {vector_store_path}")
                    except Exception as e:
                        logger.error(f"Error initializing Chroma for {source_name}: {str(e)}")
                        # Essayer de recréer la base vectorielle
                        try:
                            import shutil
                            shutil.rmtree(vector_store_path)
                            logger.info(f"Removed corrupted vector store for {source_name}")
                        except Exception as rm_error:
                            logger.error(f"Error removing corrupted vector store: {str(rm_error)}")
                else:
                    logger.warning(f"Vector store directory for {source_name} doesn't exist at {vector_store_path}")
            except Exception as e:
                logger.error(f"Error loading vector store for {source_name}: {str(e)}")

    @lru_cache(maxsize=EMBEDDING_CACHE_SIZE)
    def _get_cached_embedding(self, query: str) -> List[float]:
        """Récupère l'embedding depuis le cache ou le calcule"""
        return self.embeddings.embed_query(query)

    def _get_query_hash(self, query: str) -> str:
        """Génère un hash unique pour la requête"""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
        
    def classify_query(self, query: str) -> Dict[str, float]:
        """Classifie la requête pour déterminer quelles sources utiliser"""
        # Implémentation améliorée basée sur des mots clés et patterns
        scores = {
            "documentation": 0.6,  # Augmenté par défaut
            "faqs": 0.6,
            "troubleshooting": 0.6
        }
        
        query_lower = query.lower()
        
        # Patterns pour les FAQs
        faq_patterns = [
            r'\b(how|what|when|where|why|can|do|is|are|comment|quand|où|pourquoi|peut|est|sont)\b',
            r'\?',  # Questions directes
            r'\b(explain|describe|tell me about|décrire|expliquer|parler de)\b'
        ]
        
        # Patterns pour le troubleshooting
        troubleshooting_patterns = [
            r'\b(error|problem|issue|bug|not working|crash|fail|exception|erreur|problème|bug|ne fonctionne pas|plantage|échec)\b',
            r'\b(fix|solve|resolve|corriger|résoudre)\b',
            r'\b(help|aide|support)\b'
        ]
        
        # Patterns pour la documentation
        doc_patterns = [
            r'\b(feature|function|concept|tutorial|guide|explain|help me understand|fonctionnalité|fonction|concept|tutoriel|guide|expliquer|comprendre)\b',
            r'\b(how to|comment faire|guide|tutorial|tutoriel)\b',
            r'\b(overview|introduction|introduction|aperçu)\b'
        ]
        
        # Vérifier les patterns FAQ
        for pattern in faq_patterns:
            if re.search(pattern, query_lower):
                scores["faqs"] += 0.3
                break
                
        # Vérifier les patterns troubleshooting
        for pattern in troubleshooting_patterns:
            if re.search(pattern, query_lower):
                scores["troubleshooting"] += 0.4
                scores["documentation"] -= 0.1
                break
                
        # Vérifier les patterns documentation
        for pattern in doc_patterns:
            if re.search(pattern, query_lower):
                scores["documentation"] += 0.4
                break
                
        # Normaliser les scores pour qu'ils soient entre 0 et 1
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
            
        logger.debug(f"Scores de classification pour '{query}': {scores}")
        return scores
        
    def hybrid_search(self, query: str, k: int = 5) -> List[Tuple[Document, float, str]]:
        """Effectue une recherche hybride dans les différentes sources"""
        query_hash = self._get_query_hash(query)
        
        # Vérifier le cache
        if query_hash in self._query_cache:
            return self._query_cache[query_hash]
            
        source_scores = self.classify_query(query)
        all_results = []
        
        # Rechercher dans toutes les sources disponibles
        for source_name, vector_store in self.vector_stores.items():
            try:
                # Recherche de similarité dans cette source
                source_results = vector_store.similarity_search_with_relevance_scores(
                    query,
                    k=k*2  # Augmenter le nombre de résultats recherchés
                )
                
                # Ajouter la source aux résultats
                for doc, rel_score in source_results:
                    # Ajuster le score en fonction de la source
                    source_score = source_scores.get(source_name, 0.5)
                    adjusted_score = rel_score * (0.5 + 0.5 * source_score)
                    all_results.append((doc, adjusted_score, source_name))
                    
            except Exception as e:
                logger.error(f"Error searching in {source_name}: {str(e)}")
                # Réessayer avec une nouvelle instance de Chroma
                try:
                    vector_store_path = os.path.join(VECTOR_DB_DIR, source_name)
                    self.vector_stores[source_name] = Chroma(
                        persist_directory=vector_store_path,
                        embedding_function=self.embeddings
                    )
                    # Réessayer la recherche
                    source_results = self.vector_stores[source_name].similarity_search_with_relevance_scores(
                        query,
                        k=k*2
                    )
                    for doc, rel_score in source_results:
                        source_score = source_scores.get(source_name, 0.5)
                        adjusted_score = rel_score * (0.5 + 0.5 * source_score)
                        all_results.append((doc, adjusted_score, source_name))
                except Exception as retry_error:
                    logger.error(f"Error in retry search for {source_name}: {str(retry_error)}")
        
        # Trier les résultats par score décroissant
        all_results.sort(key=lambda x: x[1], reverse=True)
        
        # Mettre en cache les résultats
        self._query_cache[query_hash] = all_results[:k]
        
        return all_results[:k]

    def search_and_format_context(self, query: str, k: int = 5) -> Tuple[str, List[str]]:
        """Recherche et formate le contexte pour la requête"""
        logger.debug(f"Recherche de contexte pour la requête: {query}")
        
        # Vérifier si les vector stores sont initialisés
        if not self.vector_stores:
            logger.error("Aucun vector store n'est initialisé")
            return "Je n'ai pas trouvé d'information pertinente dans notre base de connaissances. Pourriez-vous reformuler votre question ou préciser le sujet ?", []
        
        # Rechercher les résultats
        search_results = self.hybrid_search(query, k=k*2)
        logger.debug(f"Nombre de résultats trouvés: {len(search_results)}")
        
        if not search_results:
            logger.warning(f"Aucun résultat trouvé pour la requête: {query}")
            return "Je n'ai pas trouvé d'information pertinente dans notre base de connaissances. Pourriez-vous reformuler votre question ou préciser le sujet ?", []
        
        # Ajuster le seuil de similarité en fonction du score le plus élevé
        max_score = max(score for _, score, _ in search_results)
        similarity_threshold = max(0.01, max_score * 0.1)  # Seuil encore plus bas
        logger.debug(f"Score maximum: {max_score:.2f}, Seuil de similarité: {similarity_threshold:.2f}")
        
        # Filtrer les résultats avec le seuil ajusté
        filtered_results = [(doc, score, source) for doc, score, source in search_results if score > similarity_threshold]
        logger.debug(f"Nombre de résultats après filtrage: {len(filtered_results)}")
        
        if not filtered_results:
            # Si aucun document ne dépasse le seuil, utiliser les 5 meilleurs résultats
            logger.info("Aucun résultat ne dépasse le seuil, utilisation des meilleurs résultats disponibles")
            context_parts = []
            sources = set()
            
            for doc, score, source_type in search_results[:5]:  # Augmenté à 5 résultats
                source = doc.metadata.get('source', 'Unknown')
                sources.add(source)
                context_parts.append(f"From {source_type} (Source: {source}, Relevance: {score:.2f}):\n{doc.page_content}")
            
            context = "\n\n".join(context_parts)
        else:
            # Extraire et trier les contenus par score de pertinence
            context_parts = []
            sources = set()
            
            for doc, score, source_type in filtered_results[:k]:
                source = doc.metadata.get('source', 'Unknown')
                sources.add(source)
                context_parts.append(f"From {source_type} (Source: {source}, Relevance: {score:.2f}):\n{doc.page_content}")
            
            context = "\n\n".join(context_parts)
        
        logger.debug(f"Contexte généré (premiers 200 caractères): {context[:200]}...")
        logger.debug(f"Sources utilisées: {sources}")
        
        return context, list(sources)
