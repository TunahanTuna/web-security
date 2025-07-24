# app/models.py
from app import db
from datetime import datetime, timezone

class Scan(db.Model):
    """Taramaları temsil eden model."""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), nullable=False, index=True)
    status = db.Column(db.String(64), default='PENDING', nullable=False) # PENDING, RUNNING, COMPLETED, FAILED
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Bir taramanın birden çok zafiyeti olabilir
    vulnerabilities = db.relationship('Vulnerability', backref='scan', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Scan {self.id}: {self.url} [{self.status}]>'

class Vulnerability(db.Model):
    """Bulunan zafiyetleri temsil eden model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(64), nullable=False)
    confidence = db.Column(db.String(64), nullable=False)
    solution = db.Column(db.Text, nullable=True)
    
    # Hangi taramaya ait olduğu
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)

    def __repr__(self):
        return f'<Vulnerability {self.name} ({self.severity})>' 