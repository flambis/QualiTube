# app/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import sys
from config import Config

def setup_logging(app):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    try:
        console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    except Exception as e:
        logger.error(f"Error configuring console handler: {e}")
    logger.addHandler(console_handler)

    # Handler fichier avec rotation
    file_handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Vérifier la présence de la clé API Gemini
    if not app.config['GEMINI_API_KEY']:
        logger.error("Gemini API key is not set in environment variables.")
        raise ValueError("Gemini API key is not set in environment variables.")
