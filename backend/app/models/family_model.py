import datetime
from app import db

class Family(db.Model):
    __tablename__ = 'families'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    invite_code = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationship to users
    members = db.relationship('User', backref='family', lazy=True)

    def __repr__(self):
        return f'<Family {self.name}>' 