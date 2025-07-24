#!/bin/bash

echo "🔄 Veritabanı kontrol ediliyor..."

# Eğer migrations klasörü yoksa init et
if [ ! -d "migrations" ]; then
    echo "📦 Migrations klasörü oluşturuluyor..."
    flask db init
fi

# Eğer migration dosyası yoksa oluştur
if [ ! "$(ls -A migrations/versions)" ]; then
    echo "📝 İlk migration oluşturuluyor..."
    flask db migrate -m "Initial migration: create scan and vulnerability tables"
fi

# Migration'ları uygula
echo "⬆️ Veritabanı migration'ları uygulanıyor..."
flask db upgrade

echo "🚀 Flask uygulaması başlatılıyor..."
python run.py 