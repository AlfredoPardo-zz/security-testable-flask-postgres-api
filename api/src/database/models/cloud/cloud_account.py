from database import db

class CloudAccount(db.Model):
    
    __tablename__ = 'cloud_account'
    uid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    customer_uid = db.Column(db.String(50), db.ForeignKey('customer.uid'))
    customer = db.relationship('Customer', backref=db.backref('cloud_account', lazy='dynamic'))
    cloud_provider_uid = db.Column(db.String(50), db.ForeignKey('cloud_provider.uid'))
    cloud_provider = db.relationship('CloudProvider', backref=db.backref('cloud_account', lazy='dynamic'))