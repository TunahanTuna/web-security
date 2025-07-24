# Python 3.11 base image
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Entrypoint script'ini kopyala ve çalıştırılabilir yap
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Port 5000'i dışa aç
EXPOSE 5000

# Entrypoint script'ini çalıştır
ENTRYPOINT ["/entrypoint.sh"] 