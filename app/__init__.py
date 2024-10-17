# app/__init__.py
from flask import Flask
from .routes import main
from .utils.logger import setup_logging
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurer le logging
    setup_logging(app)

    # Enregistrer les blueprints
    app.register_blueprint(main)

    return app
