from database import db

class User(db.Model):
    
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(50), nullable=False)
