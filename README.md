# eBus Chatbot - RAG Multilingue avec Support Multimodal

## Architecture du Projet

```
ebusChatbot/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── feedback.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── embeddings.py
│   │   │   ├── vector_store.py
│   │   │   └── context_processor.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   └── openrouter.py
│   │   └── image/
│   │       ├── __init__.py
│   │       └── processor.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py
│   │   └── feedback.py
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── dashboard.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── documents/
│   └── vector_store/
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── chat/
│   └── admin/
├── tests/
├── .env
├── .gitignore
├── app.py
└── requirements.txt
```

## Fonctionnalités Principales

### 1. Pipeline RAG Complet
- Preprocessing des requêtes avec détection de langue
- Embeddings multilingues avec SentenceTransformers
- Base vectorielle persistante avec ChromaDB
- Compression contextuelle intelligente
- Génération via meta-llama/llama-4-scout:free (OpenRouter)
- Score de confiance pour chaque réponse
- Post-traitement et formatage des réponses

### 2. Support Multilingue
- Détection automatique de la langue (FR/EN)
- Embeddings multilingues
- Traitement contextuel adapté à la langue
- Réponses dans la langue de la requête

### 3. Mémoire et Amélioration Continue
- Stockage PostgreSQL des conversations
- Système de feedback utilisateur
- Analyse des feedbacks pour amélioration continue
- Métriques de performance

### 4. Support Multimodal
- Analyse d'images avec OCR
- Intégration du contexte visuel dans le RAG
- Support des modèles multimodaux via OpenRouter

### 5. Interface Admin
- Dashboard Flask-Admin
- Visualisation des conversations
- Analyse des feedbacks
- Statistiques en temps réel
- Export des données

## Installation

1. Cloner le repository
2. Créer un environnement virtuel Python 3.9+
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```
4. Configurer les variables d'environnement dans `.env`
5. Initialiser la base de données :
```bash
flask db upgrade
```
6. Lancer l'application :
```bash
python app.py
```

## Configuration

Le fichier `.env` doit contenir :
```
OPENROUTER_API_KEY=your_key
POSTGRES_URI=postgresql://user:pass@localhost:5432/ebus_chatbot
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
```

## API Endpoints

### Chat
- `POST /api/chat` - Envoi d'un message (texte + image optionnelle)
- `GET /api/conversations` - Liste des conversations
- `GET /api/conversations/<id>` - Détails d'une conversation

### Feedback
- `POST /api/feedback` - Envoi d'un feedback
- `GET /api/feedback` - Liste des feedbacks

### Admin
- `GET /admin` - Dashboard admin
- `GET /admin/stats` - Statistiques
- `GET /admin/export` - Export des données

## Développement

### Tests
```bash
pytest tests/
```

### Linting
```bash
flake8 app/
```

## Licence

MIT