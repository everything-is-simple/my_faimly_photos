import datetime
from app import db

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    taken_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    uploader = db.relationship('User', backref=db.backref('photos', lazy=True))

    def __repr__(self):
        return f'<Photo {self.filename}>' 