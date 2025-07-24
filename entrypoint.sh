#!/bin/bash

echo "🔄 Sistem başlatılıyor..."

# PostgreSQL bağlantısı için DATABASE_URL kontrolü
if [[ $DATABASE_URL == postgresql://* ]]; then
    echo "🐘 PostgreSQL bağlantısı tespit edildi, bağlantı kontrol ediliyor..."
    
    # PostgreSQL'in hazır olmasını bekle (max 60 saniye)
    for i in {1..60}; do
        if python -c "
import psycopg2
import os
from urllib.parse import urlparse

url = os.environ.get('DATABASE_URL')
parsed = urlparse(url)
try:
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:]
    )
    conn.close()
except:
    exit(1)
" 2>/dev/null; then
            echo "✅ PostgreSQL hazır!"
            break
        else
            echo "⏳ PostgreSQL bekleniyor... ($i/60)"
            sleep 2
        fi
    done
    
    if [ $i -eq 60 ]; then
        echo "❌ PostgreSQL bağlantısı başarısız!"
        exit 1
    fi
else
    echo "📁 SQLite kullanılıyor, bağlantı kontrolü atlanıyor..."
fi

echo "🔄 Veritabanı migration'ları kontrol ediliyor..."

# Eğer migrations klasörü yoksa init et
if [ ! -d "migrations" ]; then
    echo "📦 Migrations klasörü oluşturuluyor..."
    flask db init
fi

# Versions klasörünün olduğundan emin ol
if [ ! -d "migrations/versions" ]; then
    echo "📁 Versions klasörü oluşturuluyor..."
    mkdir -p migrations/versions
fi

# Migration history'sini temizle ve yeniden oluştur (PostgreSQL geçişi için)
if [[ $DATABASE_URL == postgresql://* ]] && [ -d "migrations/versions" ]; then
    echo "🔄 PostgreSQL için migration'lar yeniden oluşturuluyor..."
    rm -rf migrations/versions/*
fi

# Eğer migration dosyası yoksa oluştur
if [ ! "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "📝 İlk migration oluşturuluyor..."
    flask db migrate -m "Initial migration: create scan and vulnerability tables"
fi

# Migration'ları uygula
echo "⬆️ Veritabanı migration'ları uygulanıyor..."
flask db upgrade

echo "🚀 Flask uygulaması başlatılıyor..."
python run.py 