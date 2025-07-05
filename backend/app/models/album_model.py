import datetime
from app import db

# Association table for the many-to-many relationship between Album and Photo
album_photos = db.Table('album_photos',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('photo_id', db.Integer, db.ForeignKey('photos.id'), primary_key=True),
    db.Column('added_at', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    creator = db.relationship('User', backref=db.backref('albums', lazy=True))
    photos = db.relationship('Photo', secondary=album_photos, lazy='subquery',
                             backref=db.backref('albums', lazy=True))

    def __repr__(self):
        return f'<Album {self.name}>' 