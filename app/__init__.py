# app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Eklenti (extension) nesnelerini oluştur
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Flask uygulama örneğini oluşturan fabrika fonksiyonu."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Eklentileri uygulama ile ilişkilendir
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint'leri (route'ları) kaydet
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Veritabanı dosyasının olduğu dizinin var olduğundan emin ol
    with app.app_context():
        # Veritabanı URI'sından dosya yolunu çıkar
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        # Eğer dizin yoksa ve mutlak bir yol değilse oluştur
        if db_dir and not os.path.exists(db_dir) and not os.path.isabs(db_dir):
            os.makedirs(db_dir)

    return app

# Modelleri import et (migrate'in modelleri tanıması için önemli)
from app import models 