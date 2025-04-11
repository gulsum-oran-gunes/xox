import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Veritabanı URI'si (PostgreSQL bağlantısı için örnek)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/xoxdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Gereksiz sorguları önlemek için
    SECRET_KEY = os.getenv('SECRET_KEY', 'xoxgamesecretkey') 