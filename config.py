# config.py
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    MAX_RESULTS_PER_QUERY = 100
    NUM_SEARCH_QUERIES = 1
    MAX_VIDEOS_TO_ANALYZE = NUM_SEARCH_QUERIES * MAX_RESULTS_PER_QUERY
    MAX_SUBTITLE_LENGTH = 1000
    LOG_FILE = 'app.log'
    MAX_THREADS = 100
    MAX_WORKERS = 100
    BATCH_SIZE = 100
