# **Proje: AI Destekli Web Güvenlik Tarama Platformu \- Backend**

Merhaba Cursor,

Bu projede, web uygulamalarındaki güvenlik zafiyetlerini tespit etmek için açık kaynaklı araçları kullanan bir platformun **backend** servisini oluşturacağız.

* **Framework:** Flask  
* **Veritabanı:** SQLAlchemy ile SQLite (Geliştirme için) / PostgreSQL (Production için)  
* **Asenkron Görevler:** Başlangıç için threading modülü, production için Celery/Redis ile değiştirilecek.  
* **Güvenlik Aracı:** OWASP ZAP (Docker üzerinden)

Lütfen aşağıdaki adımları takip ederek projeyi oluştur.

## **Adım 0: Proje Kurulumu ve Bağımlılıklar**

Önce proje dizinini ve sanal ortamı (virtual environment) oluşturalım. Ardından gerekli Python kütüphanelerini yükleyelim.

\# Proje klasörünü oluştur ve içine gir  
mkdir security-scanner-backend  
cd security-scanner-backend

\# Sanal ortamı oluştur ve aktif et  
python \-m venv venv  
source venv/bin/activate  \# Windows için: venv\\Scripts\\activate

\# Gerekli kütüphaneleri yükle  
pip install Flask Flask-SQLAlchemy Flask-Migrate python-dotenv

## **Adım 1: Proje Dosya Yapısı**

Aşağıdaki dosya ve klasör yapısını oluştur. Bu yapı, projenin modüler ve ölçeklenebilir olmasını sağlayacak.

/security-scanner-backend  
|  
|-- app/  
|   |-- \_\_init\_\_.py       \# Uygulama fabrikası (Application Factory)  
|   |-- models.py         \# Veritabanı modelleri (Scan, Vulnerability)  
|   |-- routes.py         \# API endpoint'leri  
|   |-- tasks.py          \# Asenkron tarama görevleri  
|  
|-- migrations/           \# Veritabanı göç (migration) dosyaları  
|  
|-- .flaskenv             \# Flask ortam değişkenleri  
|-- config.py             \# Konfigürasyon ayarları  
|-- run.py                \# Uygulamayı çalıştıran ana dosya  
|-- requirements.txt      \# Proje bağımlılıkları (son adımda oluşturulacak)

## **Adım 2: Dosyaların İçeriğini Oluşturma**

Şimdi her bir dosyanın içeriğini sırayla oluşturalım.

### **config.py**

Bu dosya, uygulamanın konfigürasyonlarını içerecek. Veritabanı yolu gibi hassas bilgileri buradan yöneteceğiz.

\# config.py  
import os

\# Projenin temel dizinini al  
basedir \= os.path.abspath(os.path.dirname(\_\_file\_\_))

class Config:  
    """Uygulamanın temel konfigürasyon ayarları."""  
    SECRET\_KEY \= os.environ.get('SECRET\_KEY') or 'cok-gizli-bir-anahtar'  
      
    \# Veritabanı konfigürasyonu  
    SQLALCHEMY\_DATABASE\_URI \= os.environ.get('DATABASE\_URL') or \\  
        'sqlite:///' \+ os.path.join(basedir, 'app.db')  
    SQLALCHEMY\_TRACK\_MODIFICATIONS \= False

### **app/\_\_init\_\_.py**

Bu dosya, Flask uygulamasını oluşturan "Application Factory" desenini kullanır. Eklentileri (database, migration) burada başlatırız.

\# app/\_\_init\_\_.py  
from flask import Flask  
from config import Config  
from flask\_sqlalchemy import SQLAlchemy  
from flask\_migrate import Migrate  
import os

\# Eklenti (extension) nesnelerini oluştur  
db \= SQLAlchemy()  
migrate \= Migrate()

def create\_app(config\_class=Config):  
    """Flask uygulama örneğini oluşturan fabrika fonksiyonu."""  
    app \= Flask(\_\_name\_\_)  
    app.config.from\_object(config\_class)

    \# Eklentileri uygulama ile ilişkilendir  
    db.init\_app(app)  
    migrate.init\_app(app, db)

    \# Blueprint'leri (route'ları) kaydet  
    from app.routes import bp as main\_bp  
    app.register\_blueprint(main\_bp)  
      
    \# Veritabanı dosyasının olduğu dizinin var olduğundan emin ol  
    with app.app\_context():  
        \# Veritabanı URI'sından dosya yolunu çıkar  
        db\_path \= app.config\['SQLALCHEMY\_DATABASE\_URI'\].replace('sqlite:///', '')  
        db\_dir \= os.path.dirname(db\_path)  
        \# Eğer dizin yoksa ve mutlak bir yol değilse oluştur  
        if db\_dir and not os.path.exists(db\_dir) and not os.path.isabs(db\_dir):  
            os.makedirs(db\_dir)

    return app

\# Modelleri import et (migrate'in modelleri tanıması için önemli)  
from app import models

### **app/models.py**

Veritabanı tablolarımızı temsil eden Python sınıflarını (modelleri) burada tanımlayacağız.

\# app/models.py  
from app import db  
from datetime import datetime, timezone

class Scan(db.Model):  
    """Taramaları temsil eden model."""  
    id \= db.Column(db.Integer, primary\_key=True)  
    url \= db.Column(db.String(256), nullable=False, index=True)  
    status \= db.Column(db.String(64), default='PENDING', nullable=False) \# PENDING, RUNNING, COMPLETED, FAILED  
    created\_at \= db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
      
    \# Bir taramanın birden çok zafiyeti olabilir  
    vulnerabilities \= db.relationship('Vulnerability', backref='scan', lazy='dynamic', cascade="all, delete-orphan")

    def \_\_repr\_\_(self):  
        return f'\<Scan {self.id}: {self.url} \[{self.status}\]\>'

class Vulnerability(db.Model):  
    """Bulunan zafiyetleri temsil eden model."""  
    id \= db.Column(db.Integer, primary\_key=True)  
    name \= db.Column(db.String(256), nullable=False)  
    description \= db.Column(db.Text, nullable=False)  
    severity \= db.Column(db.String(64), nullable=False)  
    confidence \= db.Column(db.String(64), nullable=False)  
    solution \= db.Column(db.Text, nullable=True)  
      
    \# Hangi taramaya ait olduğu  
    scan\_id \= db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)  
      
    def \_\_repr\_\_(self):  
        return f'\<Vulnerability {self.name} ({self.severity})\>'

### **app/tasks.py**

OWASP ZAP taramasını yürütecek olan ana mantık burada yer alacak.

\# app/tasks.py  
import subprocess  
import json  
import os  
from app import db, create\_app  
from app.models import Scan, Vulnerability

def run\_zap\_scan(scan\_id):  
    """  
    Verilen scan\_id için OWASP ZAP taramasını başlatır, sonuçları işler ve veritabanına kaydeder.  
    Bu fonksiyon bir arka plan thread'inde çalıştırılacak.  
    """  
    \# Flask uygulama bağlamı (app context) oluşturarak eklentilere erişim sağla  
    app \= create\_app()  
    with app.app\_context():  
        scan \= db.session.get(Scan, scan\_id)  
        if not scan:  
            print(f"Hata: {scan\_id} ID'li tarama bulunamadı.")  
            return

        \# Tarama durumunu 'RUNNING' olarak güncelle  
        scan.status \= 'RUNNING'  
        db.session.commit()

        target\_url \= scan.url  
        \# Rapor dosyasının tam yolunu oluştur  
        report\_path \= os.path.join(os.getcwd(), f"zap\_report\_{scan\_id}.json")

        print(f"Tarama başlatılıyor: {target\_url}")

        \# OWASP ZAP'i Docker üzerinden baseline taraması için çalıştır  
        \# Docker'ın mevcut çalışma dizinini bağlamasına izin veriyoruz.  
        command \= \[  
            "docker", "run", "--rm",   
            "-v", f"{os.getcwd()}:/zap/wrk/:rw",  
            "owasp/zap2docker-stable",   
            "zap-baseline.py",  
            "-t", target\_url,  
            "-J", os.path.basename(report\_path) \# Docker içinde sadece dosya adını kullan  
        \]

        try:  
            subprocess.run(command, check=True, capture\_output=True, text=True)  
              
            \# Rapor dosyasını oku ve işle  
            with open(report\_path, "r") as f:  
                report\_data \= json.load(f)

            for site in report\_data.get('site', \[\]):  
                for alert in site.get('alerts', \[\]):  
                    vuln \= Vulnerability(  
                        name=alert.get('name'),  
                        description=alert.get('description'),  
                        severity=alert.get('risk'),  
                        confidence=alert.get('confidence'),  
                        solution=alert.get('solution'),  
                        scan\_id=scan.id  
                    )  
                    db.session.add(vuln)

            scan.status \= 'COMPLETED'  
            print(f"Tarama tamamlandı: {target\_url}")

        except subprocess.CalledProcessError as e:  
            scan.status \= 'FAILED'  
            print(f"Hata: Tarama başarısız oldu. {e.stderr}")  
        except FileNotFoundError:  
            scan.status \= 'FAILED'  
            print(f"Hata: Rapor dosyası '{report\_path}' bulunamadı.")  
        finally:  
            \# Her durumda veritabanı oturumunu kaydet ve rapor dosyasını sil  
            db.session.commit()  
            if os.path.exists(report\_path):  
                os.remove(report\_path)

### **app/routes.py**

Kullanıcıların tarama başlatmak ve sonuçları görmek için etkileşime gireceği API endpoint'lerini tanımlar.

\# app/routes.py  
from flask import Blueprint, request, jsonify  
from app.models import Scan, Vulnerability  
from app import db  
from app.tasks import run\_zap\_scan  
import threading

bp \= Blueprint('main', \_\_name\_\_)

@bp.route('/scans', methods=\['POST'\])  
def start\_new\_scan():  
    """Yeni bir tarama başlatır."""  
    data \= request.get\_json()  
    if not data or 'url' not in data:  
        return jsonify({'error': 'URL bilgisi eksik.'}), 400

    url \= data\['url'\]  
      
    \# Yeni bir tarama nesnesi oluştur ve veritabanına ekle  
    new\_scan \= Scan(url=url, status='PENDING')  
    db.session.add(new\_scan)  
    db.session.commit()

    \# Tarama görevini arka planda bir thread'de başlat  
    \# Production'da bu Celery gibi bir görev kuyruğu ile yapılmalıdır.  
    thread \= threading.Thread(target=run\_zap\_scan, args=(new\_scan.id,))  
    thread.start()

    return jsonify({  
        'message': 'Tarama başarıyla başlatıldı.',  
        'scan\_id': new\_scan.id,  
        'status': new\_scan.status  
    }), 202 \# 202 Accepted: İstek kabul edildi, işlem sürüyor

@bp.route('/scans/\<int:scan\_id\>', methods=\['GET'\])  
def get\_scan\_status(scan\_id):  
    """Belirli bir taramanın durumunu ve sonuçlarını döndürür."""  
    scan \= db.session.get(Scan, scan\_id)  
    if scan is None:  
        return jsonify({'error': 'Tarama bulunamadı'}), 404  
      
    response \= {  
        'scan\_id': scan.id,  
        'url': scan.url,  
        'status': scan.status,  
        'created\_at': scan.created\_at.isoformat()  
    }

    if scan.status \== 'COMPLETED':  
        vulnerabilities \= \[\]  
        for vuln in scan.vulnerabilities:  
            vulnerabilities.append({  
                'id': vuln.id,  
                'name': vuln.name,  
                'severity': vuln.severity,  
                'confidence': vuln.confidence,  
                'description': vuln.description  
            })  
        response\['vulnerabilities'\] \= vulnerabilities  
      
    return jsonify(response)

### **.flaskenv**

Bu dosya, flask run komutu için ortam değişkenlerini ayarlar.

FLASK\_APP=run.py  
FLASK\_DEBUG=1

### **run.py**

Uygulamayı başlatan en üst düzey script.

\# run.py  
from app import create\_app

app \= create\_app()

if \_\_name\_\_ \== '\_\_main\_\_':  
    app.run()

## **Adım 3: Veritabanını Kurma**

Modellerimizi oluşturduk, şimdi bu modellere göre veritabanı şemasını oluşturmamız gerekiyor. Bu işlemi Flask-Migrate ile yapacağız.

\# Veritabanı migration deposunu oluştur (sadece bir kez çalıştırılır)  
flask db init

\# Modellerdeki değişikliklere göre yeni bir migration script'i oluştur  
flask db migrate \-m "Initial migration; create scan and vulnerability tables"

\# Migration'ı veritabanına uygula  
flask db upgrade

Bu komutlardan sonra projenizin ana dizininde app.db adında bir SQLite veritabanı dosyası oluşacaktır.

## **Adım 4: Uygulamayı Çalıştırma ve Test Etme**

Her şey hazır\! Docker'ın çalıştığından emin olduktan sonra uygulamayı başlatabiliriz.

1. **Uygulamayı Çalıştır:**  
   flask run

   Sunucu varsayılan olarak http://127.0.0.1:5000 adresinde çalışacaktır.  
2. **Test Etme (cURL ile):**  
   * **Yeni Bir Tarama Başlat:** (URL'i test edeceğiniz bir site ile değiştirin, örneğin http://testphp.vulnweb.com)  
     curl \-X POST \-H "Content-Type: application/json" \-d '{"url": "http://testphp.vulnweb.com"}' http://127.0.0.1:5000/scans

     Bu komut size şöyle bir yanıt vermelidir:  
     {  
       "message": "Tarama başarıyla başlatıldı.",  
       "scan\_id": 1,  
       "status": "PENDING"  
     }

   * **Tarama Durumunu Kontrol Et:** Birkaç dakika sonra, yukarıdaki yanıttan aldığınız scan\_id ile tarama durumunu kontrol edin.  
     curl http://127.0.0.1:5000/scans/1

     Tarama bittiğinde, zafiyetleri içeren tam bir JSON yanıtı alacaksınız.

Bu adımlarla, sağlam bir temele sahip, ölçeklenebilir bir backend servisi oluşturmuş olacaksın. Sonraki adımlar bu temelin üzerine Frontend'i inşa etmek ve görev kuyruğunu Celery/Redis ile değiştirmek olacaktır.