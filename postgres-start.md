# 🐘 PostgreSQL Özel Setup

Basit, temiz PostgreSQL kurulumu. Hiç env dosyası yok, dümdüz çalışıyor.

## 🚀 Kullanım

```bash
# PostgreSQL versiyonunu başlat
docker-compose -f docker-compose.postgres.yml up -d

# Durumu kontrol et
docker-compose -f docker-compose.postgres.yml ps

# Logları gör
docker-compose -f docker-compose.postgres.yml logs -f web

# Durdur
docker-compose -f docker-compose.postgres.yml down
```

## 📊 Servisler

| Servis | Port | Container | Açıklama |
|--------|------|-----------|----------|
| **Web API** | 5000 | tuna_security_app | Ana uygulama |
| **PostgreSQL** | 5432 | tuna_postgres | Veritabanı |
| **Redis** | 6379 | tuna_redis | Cache |
| **ZAP** | 8080 | tuna_zap | Tarayıcı |

## 🔐 Veritabanı Bilgileri

```
Host: localhost
Port: 5432
Database: security_scanner
User: tuna_user
Password: tuna123password
```

## 📝 Test

```bash
# Tarama başlat
curl -X POST -H "Content-Type: application/json" \
     -d '{"url": "http://testphp.vulnweb.com"}' \
     http://localhost:5000/scans

# Sonucu gör
curl http://localhost:5000/scans/1
```

## 🛠️ Veritabanı Yönetimi

```bash
# PostgreSQL'e bağlan
docker exec -it tuna_postgres psql -U tuna_user -d security_scanner

# Tabloları listele
\dt

# Çık
\q
```

**Hiç karışıklık yok, dümdüz çalışıyor! 🎯** 