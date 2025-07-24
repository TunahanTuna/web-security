# config.py
import os

# Projenin temel dizinini al
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Uygulamanın temel konfigürasyon ayarları."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-bir-anahtar'
    
    # Veritabanı konfigürasyonu
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 