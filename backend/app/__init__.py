# /app/__init__.py

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_migrate import Migrate



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  # Flask uygulamasını başlat
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
    db.init_app(app)
    from app.routes import routes
    app.register_blueprint(routes)  # Blueprint kaydet
    
    migrate = Migrate(app, db)
    
    return app

