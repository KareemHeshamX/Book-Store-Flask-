from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Book, User, Order, CartItem

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator that restricts access to admin users."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function


# ─── Dashboard ───────────────────────────────────────────────────────────────────

@admin.route('/')
@admin_required
def dashboard():
    orders = Order.query.order_by(Order.id.desc()).limit(10).all()
    total_sales = sum(o.total for o in Order.query.all())
    book_count = Book.query.count()
    user_count = User.query.count()
    return render_template(
        'admin.html', orders=orders, total_sales=total_sales,
        book_count=book_count, user_count=user_count
    )


# ─── Book Management ────────────────────────────────────────────────────────────

@admin.route('/books', methods=['GET', 'POST'])
@admin_required
def books():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            book = Book(
                title=request.form.get('title'),
                author=request.form.get('author'),
                price=float(request.form.get('price')),
                category=request.form.get('category'),
                book_format=request.form.get('book_format'),
                description=request.form.get('description', ''),
                image_url=request.form.get('image_url', '')
            )
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully.', 'success')

        elif action == 'edit':
            book = Book.query.get(request.form.get('book_id'))
            if book:
                book.title = request.form.get('title')
                book.author = request.form.get('author')
                book.price = float(request.form.get('price'))
                book.category = request.form.get('category')
                book.book_format = request.form.get('book_format')
                book.description = request.form.get('description', '')
                book.image_url = request.form.get('image_url', '')
                db.session.commit()
                flash('Book updated successfully.', 'success')

        elif action == 'delete':
            book = Book.query.get(request.form.get('book_id'))
            if book:
                CartItem.query.filter_by(book_id=book.id).delete()
                db.session.delete(book)
                db.session.commit()
                flash('Book deleted successfully.', 'success')

        return redirect(url_for('admin.books'))

    all_books = Book.query.order_by(Book.id.desc()).all()
    return render_template('admin_books.html', books=all_books)


# ─── User Management ────────────────────────────────────────────────────────────

@admin.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_admin':
            email = request.form.get('email')
            username = request.form.get('username')
            if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
                flash('User with that email or username already exists.', 'error')
            else:
                user = User(
                    full_name=request.form.get('full_name'),
                    username=username,
                    email=email,
                    is_admin=True
                )
                user.set_password(request.form.get('password'))
                db.session.add(user)
                db.session.commit()
                flash('Admin created successfully.', 'success')

        elif action == 'toggle_admin':
            user = User.query.get(request.form.get('user_id'))
            if user and user.id != current_user.id:
                user.is_admin = not user.is_admin
                db.session.commit()
                flash('User admin status updated.', 'success')

        elif action == 'delete':
            user = User.query.get(request.form.get('user_id'))
            if user and user.id != current_user.id:
                CartItem.query.filter_by(user_id=user.id).delete()
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully.', 'success')

        return redirect(url_for('admin.users'))

    all_users = User.query.order_by(User.id.desc()).all()
    return render_template('admin_users.html', users=all_users)
