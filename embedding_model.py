import time
import logging
import math
import hashlib
from langchain.embeddings.base import Embeddings
from typing import List, Dict, Any, Optional, Tuple
from functools import lru_cache
import asyncio
import concurrent.futures
from sentence_transformers import SentenceTransformer
import torch
import os
from openai import AzureOpenAI
from config import API_KEY, API_BASE, EMBEDDING_DEPLOYMENT_ID

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomOpenSourceEmbeddings(Embeddings):
    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        cache_size: int = 1000,
        device: str = None
    ):
        logger.info(f"Initializing SentenceTransformer with model {model_name}")
        try:
            # Automatically use CUDA if available, otherwise CPU
            if device is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self.device = device
            self.model = SentenceTransformer(model_name, device=device)
            logger.info(f"Model loaded successfully on {device}")
        except Exception as e:
            logger.error(f"Failed to initialize SentenceTransformer: {str(e)}")
            raise
            
        self.model_name = model_name
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        
        # Cache settings
        self._cached_embed_query = lru_cache(maxsize=cache_size)(self._embed_query_implementation)
        self._hash_to_embedding = {}
        
        # Batch settings
        self.batch_size = 32  # Most models can handle this batch size
        
    def _process_text(self, text: str) -> str:
        """Clean and validate text before embedding"""
        if not isinstance(text, str):
            text = str(text)
            
        # Conversion en texte unicode normalisé (gestion des accents)
        import unicodedata
        text = unicodedata.normalize('NFKD', text)
        
        # Remplacer certains caractères spéciaux par des espaces
        import re
        # Remplacer les caractères de ponctuation multiples par un seul
        text = re.sub(r'([.!?])\1+', r'\1', text)
        
        # Remplacer les caractères spéciaux non alphanumériques par des espaces
        # tout en préservant la ponctuation de base et les caractères accentués
        text = re.sub(r'[^\w\s.,!?;:\-\'\"()\[\]{}]', ' ', text)
        
        # Remove excessive whitespace (espaces multiples, tabulations, retours à la ligne)
        text = " ".join(text.split())
        
        # Suppression des espaces autour de la ponctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        return text
    
    def _hash_text(self, text: str) -> str:
        """Create a unique hash for the text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _embed_query_implementation(self, text_hash: str, text: str) -> List[float]:
        """Actual implementation of embed_query without caching"""
        try:
            # Generate embeddings using sentence-transformers
            embedding = self.model.encode(text, convert_to_numpy=True).tolist()
            return embedding
        except Exception as e:
            logger.error(f"Error in embed_query: {str(e)}")
            # Return zeros with correct dimension in case of error
            return [0.0] * self.embedding_dimension
    
    def embed_query(self, text: str) -> List[float]:
        """Cached version of embed_query"""
        processed_text = self._process_text(text)
        text_hash = self._hash_text(processed_text)
        
        # Check if in document cache first (might have been embedded as a document)
        if text_hash in self._hash_to_embedding:
            return self._hash_to_embedding[text_hash]
            
        return self._cached_embed_query(text_hash, processed_text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents with caching and batching"""
        if not texts:
            logger.warning("No texts provided for embedding")
            return []
            
        try:
            logger.info(f"Starting embedding of {len(texts)} documents")
            # Clean and validate texts
            processed_texts = [self._process_text(text) for text in texts]
            
            # Check cache and prepare embedding
            texts_to_embed = []
            text_hashes = []
            embeddings_result = [None] * len(processed_texts)
            
            for i, text in enumerate(processed_texts):
                text_hash = self._hash_text(text)
                text_hashes.append(text_hash)
                
                if text_hash in self._hash_to_embedding:
                    embeddings_result[i] = self._hash_to_embedding[text_hash]
                else:
                    texts_to_embed.append((i, text))
            
            logger.info(f"Found {len(processed_texts) - len(texts_to_embed)} cached embeddings, need to embed {len(texts_to_embed)} texts")
            
            # If all texts are cached, return results
            if not texts_to_embed:
                return embeddings_result
                
            # Process texts not in cache
            indices_to_embed = [i for i, _ in texts_to_embed]
            actual_texts_to_embed = [text for _, text in texts_to_embed]
            
            # Split into batches
            all_batch_results = []
            
            for i in range(0, len(actual_texts_to_embed), self.batch_size):
                batch = actual_texts_to_embed[i:i + self.batch_size]
                logger.info(f"Processing batch {i//self.batch_size + 1}/{(len(actual_texts_to_embed) + self.batch_size - 1)//self.batch_size} with {len(batch)} texts")
                
                try:
                    # Generate embeddings
                    batch_embeddings = self.model.encode(batch, convert_to_numpy=True).tolist()
                    all_batch_results.extend(batch_embeddings)
                    logger.info(f"Successfully embedded batch of {len(batch)} texts")
                    
                except Exception as e:
                    logger.error(f"Error embedding batch: {str(e)}")
                    # Return zeros for this batch
                    all_batch_results.extend([[0.0] * self.embedding_dimension] * len(batch))
            
            # Populate results and update cache
            for idx, embedding in zip(indices_to_embed, all_batch_results):
                embeddings_result[idx] = embedding
                self._hash_to_embedding[text_hashes[idx]] = embedding
            
            logger.info(f"Completed embedding of {len(texts)} documents")
            return embeddings_result
            
        except Exception as e:
            logger.error(f"Error in embed_documents: {str(e)}")
            return [[0.0] * self.embedding_dimension] * len(texts)
    
    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous version of embed_documents"""
        if not texts:
            return []
        
        # Process texts and check cache
        processed_texts = [self._process_text(text) for text in texts]
        texts_to_embed = []
        text_hashes = []
        embeddings_result = [None] * len(processed_texts)
        
        for i, text in enumerate(processed_texts):
            text_hash = self._hash_text(text)
            text_hashes.append(text_hash)
            
            if text_hash in self._hash_to_embedding:
                embeddings_result[i] = self._hash_to_embedding[text_hash]
            else:
                texts_to_embed.append((i, text))
        
        # If all texts are cached, return immediately
        if not texts_to_embed:
            return embeddings_result
            
        # Process uncached texts
        indices_to_embed = [i for i, _ in texts_to_embed]
        actual_texts_to_embed = [text for _, text in texts_to_embed]
        
        # Prepare batches
        batches = []
        for i in range(0, len(actual_texts_to_embed), self.batch_size):
            batch = actual_texts_to_embed[i:i + self.batch_size]
            batches.append(batch)
        
        # Semaphore to limit concurrent processing
        semaphore = asyncio.Semaphore(3)  # Process 3 batches at a time
        batch_results = {}  # Store results by batch index
        
        async def process_batch(batch_idx):
            async with semaphore:
                try:
                    batch = batches[batch_idx]
                    
                    # Use thread pool for CPU-bound embedding operation
                    loop = asyncio.get_event_loop()
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        embeddings = await loop.run_in_executor(
                            executor,
                            lambda: self.model.encode(batch, convert_to_numpy=True).tolist()
                        )
                    
                    # Store results
                    batch_results[batch_idx] = embeddings
                    return True
                    
                except Exception as e:
                    logger.error(f"Error in async batch {batch_idx}: {str(e)}")
                    
                    # Store empty results
                    batch_results[batch_idx] = [[0.0] * self.embedding_dimension] * len(batches[batch_idx])
                    return False
        
        # Create and run tasks
        tasks = [process_batch(i) for i in range(len(batches))]
        await asyncio.gather(*tasks)
        
        # Combine all results in the right order
        all_batch_results = []
        for i in range(len(batches)):
            all_batch_results.extend(batch_results.get(i, [[0.0] * self.embedding_dimension] * len(batches[i])))
        
        # Populate final results and update cache
        for idx, embedding in zip(indices_to_embed, all_batch_results):
            embeddings_result[idx] = embedding
            self._hash_to_embedding[text_hashes[idx]] = embedding
        
        return embeddings_result

class AzureOpenAIEmbeddings(Embeddings):
    """Classe pour gérer les embeddings avec Azure OpenAI"""
    
    def __init__(self):
        """Initialise le client Azure OpenAI"""
        try:
            self.client = AzureOpenAI(
                api_key=API_KEY,
                api_version="2024-02-15-preview",
                azure_endpoint=API_BASE
            )
            self.deployment_id = EMBEDDING_DEPLOYMENT_ID
            logger.info("Client Azure OpenAI initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client Azure OpenAI: {str(e)}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Génère les embeddings pour une liste de textes"""
        try:
            # Préparer les textes pour l'API
            texts = [text.replace("\n", " ") for text in texts]
            
            # Appeler l'API Azure OpenAI
            response = self.client.embeddings.create(
                model=self.deployment_id,
                input=texts
            )
            
            # Extraire les embeddings
            embeddings = [data.embedding for data in response.data]
            return embeddings
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des embeddings: {str(e)}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Génère l'embedding pour un seul texte"""
        try:
            # Nettoyer le texte
            text = text.replace("\n", " ")
            
            # Appeler l'API Azure OpenAI
            response = self.client.embeddings.create(
                model=self.deployment_id,
                input=text
            )
            
            # Retourner l'embedding
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'embedding: {str(e)}")
            raise