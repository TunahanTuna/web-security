# config.py
import os
from urllib.parse import urlparse

# Projenin temel dizinini al
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Uygulamanın temel konfigürasyon ayarları."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-bir-anahtar'
    
    # Veritabanı konfigürasyonu
    # Production ve development için PostgreSQL kullan, fallback olarak SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Heroku tarzı postgres:// URL'leri postgresql:// olarak düzelt
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback SQLite (sadece test/geliştirme için)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Bağlantı sağlığını kontrol et
        'pool_recycle': 300,    # 5 dakikada bir bağlantıları yenile
    } 