from database import db

class Customer(db.Model):

    __tablename__ = 'customer'
    uid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)