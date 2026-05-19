"""
Main storefront routes — home, explore, book detail, cart, checkout, orders, profile.
"""

import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models import Book, CartItem, Order, OrderItem

main = Blueprint('main', __name__)


# ─── Storefront ─────────────────────────────────────────────────────────────────

@main.route('/')
def home():
    books = Book.query.limit(5).all()
    featured = Book.query.first()
    categories = [c[0] for c in db.session.query(Book.category).distinct().all()]
    return render_template('home.html', books=books, featured=featured, categories=categories)


@main.route('/explore')
def explore():
    category = request.args.getlist('category')
    book_format = request.args.getlist('format')
    search = request.args.get('search', '')

    query = Book.query
    if category:
        query = query.filter(Book.category.in_(category))
    if book_format:
        query = query.filter(Book.book_format.in_(book_format))
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) | (Book.author.ilike(f'%{search}%'))
        )

    books = query.all()
    categories = [c[0] for c in db.session.query(Book.category).distinct().all()]
    formats = [f[0] for f in db.session.query(Book.book_format).distinct().all()]
    return render_template(
        'explore.html', books=books, categories=categories, formats=formats,
        selected_categories=category, selected_formats=book_format, search=search
    )


@main.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    related = Book.query.filter(Book.category == book.category, Book.id != book.id).limit(3).all()
    return render_template('book.html', book=book, related=related)


# ─── Cart ────────────────────────────────────────────────────────────────────────

@main.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.book.price * item.quantity for item in items)
    return render_template('cart.html', items=items, subtotal=subtotal)


@main.route('/cart/add/<int:book_id>')
@login_required
def add_to_cart(book_id):
    existing = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing:
        existing.quantity += 1
    else:
        db.session.add(CartItem(user_id=current_user.id, book_id=book_id, quantity=1))
    db.session.commit()
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('main.explore'))


@main.route('/cart/update/<int:item_id>/<action>')
@login_required
def update_cart(item_id, action):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return redirect(url_for('main.cart'))
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
    elif action == 'remove':
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.cart'))


# ─── Checkout & Orders ──────────────────────────────────────────────────────────

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('main.cart'))

    subtotal = sum(item.book.price * item.quantity for item in items)

    if request.method == 'POST':
        order_number = f'#TBS-{Order.query.count() + 1001}'
        order = Order(
            user_id=current_user.id,
            order_number=order_number,
            date=datetime.now().strftime('%b %d, %Y'),
            total=subtotal,
            status='Delivered'
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            db.session.add(OrderItem(
                order_id=order.id,
                book_title=item.book.title,
                quantity=item.quantity,
                price=item.book.price
            ))
            db.session.delete(item)

        db.session.commit()
        flash('Payment successful! Order placed.', 'success')
        return redirect(url_for('main.orders'))

    return render_template('checkout.html', items=items, subtotal=subtotal)


@main.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template('orders.html', orders=user_orders)


# ─── Profile ────────────────────────────────────────────────────────────────────

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    current_user.full_name = request.form.get('full_name', current_user.full_name)
    current_user.username = request.form.get('username', current_user.username)
    current_user.email = request.form.get('email', current_user.email)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))


@main.route('/profile/password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    if current_user.check_password(old_password):
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
    else:
        flash('Current password is incorrect.', 'error')
    return redirect(url_for('main.profile'))


@main.route('/profile/picture', methods=['POST'])
@login_required
def update_profile_picture():
    action = request.form.get('action')

    if action == 'remove':
        if current_user.profile_picture:
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture))
            except OSError:
                pass
            current_user.profile_picture = ''
            db.session.commit()
            flash('Profile picture removed.', 'success')

    elif action == 'upload':
        if 'picture' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('main.profile'))

        file = request.files['picture']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('main.profile'))

        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"user_{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))

            # Remove old picture
            if current_user.profile_picture:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture))
                except OSError:
                    pass

            current_user.profile_picture = unique_filename
            db.session.commit()
            flash('Profile picture updated.', 'success')

    return redirect(url_for('main.profile'))
