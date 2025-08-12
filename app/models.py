from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    tips = db.relationship('Tip', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    barcode = db.Column(db.String(128), index=True, unique=True)
    tips = db.relationship('Tip', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    is_approved = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=0) # 1 to 10 stars
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    attachments = db.relationship('Attachment', backref='tip', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Tip {self.title}>'

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    tip_id = db.Column(db.Integer, db.ForeignKey('tip.id'))

    def __repr__(self):
        return f'<Attachment {self.filename}>'
