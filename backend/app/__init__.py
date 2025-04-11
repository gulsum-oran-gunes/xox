# /app/__init__.py

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  # Flask uygulamasını başlat
    app.config.from_object(Config)
    db.init_app(app)
    from app.routes import routes
    app.register_blueprint(routes)  # Blueprint kaydet
    
    migrate = Migrate(app, db)
    
    return app

