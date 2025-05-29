from datetime import datetime
from .extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(32), unique=True, nullable=False)
    email         = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pwd):
        self.password_hash = bcrypt.generate_password_hash(pwd).decode()

    def check_password(self, pwd) -> bool:
        return bcrypt.check_password_hash(self.password_hash, pwd)
