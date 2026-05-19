"""
Database models for The Book Store.

All SQLAlchemy models are defined here, separated from application logic.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


# ─── User ───────────────────────────────────────────────────────────────────────

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    member_since = db.Column(db.String(10), default='2024')
    profile_picture = db.Column(db.String(200), default='')
    is_admin = db.Column(db.Boolean, default=False)

    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ─── Book ───────────────────────────────────────────────────────────────────────

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    book_format = db.Column(db.String(50), default='Hardcover')
    description = db.Column(db.Text, default='')
    image_url = db.Column(db.String(500), default='')

    def __repr__(self):
        return f'<Book {self.title}>'


# ─── Cart ───────────────────────────────────────────────────────────────────────

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    book = db.relationship('Book')

    def __repr__(self):
        return f'<CartItem user={self.user_id} book={self.book_id} qty={self.quantity}>'


# ─── Orders ─────────────────────────────────────────────────────────────────────

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Delivered')

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.book_title}>'
