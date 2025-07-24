# 🛡️ Tuna ZAP - AI Destekli Web Güvenlik Tarama Platformu

Flask tabanlı, OWASP ZAP ile entegre güvenlik tarama platformu.

## 🚀 Hızlı Başlangıç

### Option 1: Development (PostgreSQL) ✅ FİXED
```bash
# PostgreSQL ile development ortamı - SORUNLAR ÇÖZÜLDİ!
docker-compose up --build -d
```

### Option 2: Basit Test (SQLite)
```bash
# SQLite ile basit test ortamı
docker-compose -f docker-compose.simple.yml up -d
```

### Option 3: Production (PostgreSQL + Redis + Nginx)
```bash
# Production ortamını başlat
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 PostgreSQL Sorunları Çözüldü! ✅

### ✅ Çözülen Problemler:
1. **Authentication Hatası** - PostgreSQL auth yapılandırması düzeltildi
2. **Container Dependency** - Health check'li dependency sistemi eklendi
3. **Migration Conflict** - Akıllı migration yönetimi eklendi
4. **Connection Timing** - PostgreSQL bağlantı kontrolü eklendi

### 🛠️ Yeni Özellikler:
- **Health Check**: PostgreSQL'in tam hazır olmasını bekler
- **Smart Migration**: SQLite'dan PostgreSQL'e geçiş otomatik
- **Connection Retry**: 60 saniye bağlantı denemesi
- **Error Handling**: Detaylı hata mesajları

## 🗄️ PostgreSQL Kurulumu

### Development için:
Varsayılan docker-compose.yml dosyası artık PostgreSQL kullanıyor:
```
Database: security_scanner_dev
User: dev_user
Password: dev_password
Port: 5432
Health Check: ✅ Aktif
```

### Production için:
Environment variable'ları ayarlayın:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
POSTGRES_DB=security_scanner
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_secure_password
```

### Otomatik Migration:
```bash
# Container başlatılınca otomatik olarak:
# 1. PostgreSQL hazır olana kadar bekler
# 2. Migration'ları kontrol eder
# 3. Gerekirse yeni migration oluşturur
# 4. Migration'ları uygular
# 5. Uygulamayı başlatır
```

## 📊 API Kullanımı

### Yeni Tarama Başlatma
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"url": "http://testphp.vulnweb.com"}' \
     http://localhost:5000/scans
```

### Tarama Sonuçlarını Görüntüleme
```bash
curl http://localhost:5000/scans/{scan_id}
```

## 🔧 Servis Erişim Bilgileri

| Servis | URL | Port | Açıklama |
|--------|-----|------|----------|
| **Web API** | http://localhost:5000 | 5000 | Ana güvenlik tarama API'si |
| **ZAP API** | http://localhost:8080 | 8080 | OWASP ZAP yönetim paneli |
| **Redis** | localhost:6379 | 6379 | Cache servisi |
| **PostgreSQL** | localhost:5432 | 5432 | Veritabanı ✅ STABLE |

## 🐳 Docker Hub

**Latest Image:** `mustafatunahantuna/tuna_zap:latest` ✅ PostgreSQL Fixed

**Available Tags:**
- `latest` - En güncel versiyon (PostgreSQL sorunları çözülmüş)
- `postgres-fixed` - PostgreSQL sorunları çözülmüş özel tag
- `postgres` - İlk PostgreSQL denemesi

```bash
# En güncel versiyonu çek
docker pull mustafatunahantuna/tuna_zap:latest

# PostgreSQL çözümlü versiyonu çek
docker pull mustafatunahantuna/tuna_zap:postgres-fixed
```

## 🔐 Güvenlik Ayarları

### Production için Değiştir:
1. **SECRET_KEY** - Flask secret key
2. **POSTGRES_PASSWORD** - PostgreSQL şifresi
3. **REDIS_PASSWORD** - Redis şifresi

## 📈 Özellikler

- ✅ OWASP ZAP entegrasyonu
- ✅ Asenkron tarama
- ✅ RESTful API
- ✅ Docker containerized
- ✅ PostgreSQL + Redis support (**SORUNLAR ÇÖZÜLDİ**)
- ✅ Nginx reverse proxy ready
- ✅ Health check sistemi
- ✅ Akıllı migration yönetimi

## 🛠️ Geliştirme

```bash
# Geliştirme ortamı (PostgreSQL ile)
docker-compose up --build

# Logları görüntüle
docker-compose logs -f web

# Container'ları durdur
docker-compose down
```

## 📝 API Endpoints

- `POST /scans` - Yeni tarama başlat
- `GET /scans/{id}` - Tarama durumu/sonuçları

## 🔍 Test URLs

- http://testphp.vulnweb.com (Vulnerable test site)
- https://httpbin.org (HTTP test service)

## 🎯 Son Güncellemeler

### v2.0 - PostgreSQL Sorunları Çözüldü (2025-01-24)
- ✅ Authentication problemi çözüldü
- ✅ Health check sistemi eklendi
- ✅ Migration conflict'i çözüldü
- ✅ Connection timeout yönetimi
- ✅ Production ready PostgreSQL setup

---

**Geliştirici:** Tuna  
**Docker Hub:** mustafatunahantuna/tuna_zap  
**Status:** ✅ STABLE - PostgreSQL Issues Fixed 