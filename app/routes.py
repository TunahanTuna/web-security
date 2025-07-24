# app/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Scan, Vulnerability
from app.tasks import run_zap_scan
import threading

bp = Blueprint('main', __name__)

@bp.route('/scans', methods=['POST'])
def start_new_scan():
    """Yeni bir tarama başlatır."""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL bilgisi eksik.'}), 400

    url = data['url']
    
    # Yeni bir tarama nesnesi oluştur ve veritabanına ekle
    new_scan = Scan(url=url, status='PENDING')
    db.session.add(new_scan)
    db.session.commit()
    
    # Tarama görevini arka planda bir thread'de başlat
    # Production'da bu Celery gibi bir görev kuyruğu ile yapılmalıdır.
    thread = threading.Thread(target=run_zap_scan, args=(new_scan.id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message': 'Tarama başarıyla başlatıldı.',
        'scan_id': new_scan.id,
        'status': new_scan.status
    }), 202 # 202 Accepted: İstek kabul edildi, işlem sürüyor

@bp.route('/scans/<int:scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    """Belirli bir taramanın durumunu ve sonuçlarını döndürür."""
    scan = db.session.get(Scan, scan_id)
    if scan is None:
        return jsonify({'error': 'Tarama bulunamadı'}), 404
    
    response = {
        'scan_id': scan.id,
        'url': scan.url,
        'status': scan.status,
        'created_at': scan.created_at.isoformat()
    }

    if scan.status == 'COMPLETED':
        vulnerabilities = []
        for vuln in scan.vulnerabilities:
            vulnerabilities.append({
                'id': vuln.id,
                'name': vuln.name,
                'severity': vuln.severity,
                'confidence': vuln.confidence,
                'description': vuln.description
            })
        response['vulnerabilities'] = vulnerabilities
    
    return jsonify(response) 