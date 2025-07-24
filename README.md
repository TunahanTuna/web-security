# 🛡️ Tuna ZAP - AI Destekli Web Güvenlik Tarama Platformu

Flask tabanlı, OWASP ZAP ile entegre güvenlik tarama platformu.

## 🚀 Hızlı Başlangıç

### Option 1: Basit Kurulum (SQLite)
```bash
docker-compose -f docker-compose.simple.yml up -d
```

### Option 2: Production Kurulum (PostgreSQL + Redis)
```bash
docker-compose -f docker-compose.prod-no-env.yml up -d
```

### Option 3: Nginx ile Production
```bash
docker-compose -f docker-compose.prod-no-env.yml --profile with-nginx up -d
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
| **PostgreSQL** | localhost:5432 | 5432 | Veritabanı |

## 🐳 Docker Hub

**Image:** `mustafatunahantuna/tuna_zap:latest`

```bash
docker pull mustafatunahantuna/tuna_zap:latest
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
- ✅ PostgreSQL + Redis support
- ✅ Nginx reverse proxy ready

## 🛠️ Geliştirme

```bash
# Geliştirme ortamı
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

---

**Geliştirici:** Tuna  
**Docker Hub:** mustafatunahantuna/tuna_zap 