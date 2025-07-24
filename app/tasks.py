# app/tasks.py
import requests
import json
import time
from app import db, create_app
from app.models import Scan, Vulnerability

def run_zap_scan(scan_id):
    """
    Docker Compose'da çalışan ZAP ile tarama yapar
    ZAP API'sini kullanarak güvenlik taraması gerçekleştirir
    """
    app = create_app()
    with app.app_context():
        scan = db.session.get(Scan, scan_id)
        if not scan:
            print(f"Hata: {scan_id} ID'li tarama bulunamadı.")
            return

        scan.status = 'RUNNING'
        db.session.commit()

        target_url = scan.url
        print(f"🔍 ZAP Tarama başlatılıyor: {target_url}")

        try:
            # ZAP API'si ile tarama başlat
            zap_url = "http://zap:8080"  # Docker Compose service ismi
            
            # ZAP'ın hazır olup olmadığını kontrol et
            print("ZAP servisine bağlanıyor...")
            for attempt in range(30):  # 30 saniye bekle
                try:
                    response = requests.get(f"{zap_url}/JSON/core/view/version/", timeout=5)
                    if response.status_code == 200:
                        print(f"✅ ZAP hazır: {response.json()['version']}")
                        break
                except Exception:
                    print(f"ZAP bekleniyor... ({attempt + 1}/30)")
                    time.sleep(1)
            else:
                raise Exception("ZAP servisi başlatılamadı")
            
            # Mevcut siteleri temizle
            requests.get(f"{zap_url}/JSON/core/action/newSession/")
            
            # Spider taraması başlat
            print("🕷️ Spider taraması başlatılıyor...")
            spider_response = requests.get(f"{zap_url}/JSON/spider/action/scan/", 
                                         params={
                                             "url": target_url, 
                                             "maxChildren": "100",      # Kapsamlı tarama
                                             "recurse": "true",         # Alt sayfalara gir
                                             "subtreeOnly": "false"     # Tüm siteyi tara
                                         })
            
            if spider_response.status_code != 200:
                raise Exception(f"Spider başlatılamadı: {spider_response.text}")
            
            spider_scan_id = spider_response.json()['scan']
            print(f"Spider ID: {spider_scan_id}")
            
            # Spider tamamlanana kadar bekle
            while True:
                status_response = requests.get(f"{zap_url}/JSON/spider/view/status/", 
                                             params={"scanId": spider_scan_id})
                progress = int(status_response.json()['status'])
                print(f"🕷️ Spider Progress: {progress}%")
                
                if progress >= 100:
                    break
                time.sleep(3)
            
            print("✅ Spider taraması tamamlandı!")
            
            # Pasif tarama sonuçlarını al
            alerts_response = requests.get(f"{zap_url}/JSON/core/view/alerts/", 
                                         params={"baseurl": target_url})
            
            if alerts_response.status_code != 200:
                raise Exception(f"Alerts alınamadı: {alerts_response.text}")
            
            alerts = alerts_response.json()['alerts']
            print(f"📊 {len(alerts)} zafiyet bulundu")
            
            # Zafiyetleri veritabanına kaydet
            for alert in alerts:
                vuln = Vulnerability(
                    name=alert.get('alert', 'Unknown Vulnerability'),
                    description=alert.get('description', 'Açıklama bulunamadı'),
                    severity=alert.get('risk', 'Low'),
                    confidence=alert.get('confidence', 'Low'),
                    solution=alert.get('solution', 'Çözüm önerisi bulunamadı'),
                    scan_id=scan.id
                )
                db.session.add(vuln)

            scan.status = 'COMPLETED'
            print(f"✅ ZAP Tarama tamamlandı: {target_url} ({len(alerts)} zafiyet)")

        except Exception as e:
            scan.status = 'FAILED'
            print(f"❌ ZAP Tarama başarısız: {str(e)}")
        finally:
            db.session.commit() 