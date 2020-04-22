from database import db

class CloudProvider(db.Model):
    
    __tablename__ = 'cloud_provider'
    uid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbreviation = db.Column(db.String(50), nullable=False)
