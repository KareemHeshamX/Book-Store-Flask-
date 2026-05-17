from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the-book-store-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ─── Models ───

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


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    book_format = db.Column(db.String(50), default='Hardcover')
    description = db.Column(db.Text, default='')
    image_url = db.Column(db.String(500), default='')


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    book = db.relationship('Book')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Delivered')
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── Context Processor & Decorators ───

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_cart_count():
    count = 0
    if current_user.is_authenticated:
        count = CartItem.query.filter_by(user_id=current_user.id).count()
    return dict(cart_count=count)


# ─── Routes ───

@app.route('/')
def home():
    books = Book.query.limit(5).all()
    featured = Book.query.first()
    categories = db.session.query(Book.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('home.html', books=books, featured=featured, categories=categories)


@app.route('/explore')
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
    categories = db.session.query(Book.category).distinct().all()
    categories = [c[0] for c in categories]
    formats = db.session.query(Book.book_format).distinct().all()
    formats = [f[0] for f in formats]
    return render_template('explore.html', books=books, categories=categories, formats=formats,
                           selected_categories=category, selected_formats=book_format, search=search)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    related = Book.query.filter(Book.category == book.category, Book.id != book.id).limit(3).all()
    return render_template('book.html', book=book, related=related)


@app.route('/api/books')
def api_books():
    """JSON endpoint for live search."""
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
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'price': b.price,
        'category': b.category,
        'book_format': b.book_format,
        'image_url': b.image_url
    } for b in books])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    tab = request.args.get('tab', 'signin')
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'signin':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Welcome back!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password.', 'error')
                return redirect(url_for('login', tab='signin'))
        elif action == 'register':
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return redirect(url_for('login', tab='register'))
            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'error')
                return redirect(url_for('login', tab='register'))
            user = User(full_name=full_name, username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', tab=tab)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    current_user.full_name = request.form.get('full_name', current_user.full_name)
    current_user.username = request.form.get('username', current_user.username)
    current_user.email = request.form.get('email', current_user.email)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/profile/password', methods=['POST'])
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
    return redirect(url_for('profile'))


@app.route('/profile/picture', methods=['POST'])
@login_required
def update_profile_picture():
    action = request.form.get('action')
    if action == 'remove':
        if current_user.profile_picture:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_picture))
            except OSError:
                pass
            current_user.profile_picture = ''
            db.session.commit()
            flash('Profile picture removed.', 'success')
    elif action == 'upload':
        if 'picture' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('profile'))
        file = request.files['picture']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('profile'))
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"user_{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            if current_user.profile_picture:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_picture))
                except OSError:
                    pass
            
            current_user.profile_picture = unique_filename
            db.session.commit()
            flash('Profile picture updated.', 'success')
    return redirect(url_for('profile'))


@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.book.price * item.quantity for item in items)
    return render_template('cart.html', items=items, subtotal=subtotal)


@app.route('/cart/add/<int:book_id>')
@login_required
def add_to_cart(book_id):
    existing = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing:
        existing.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('explore'))


@app.route('/cart/update/<int:item_id>/<action>')
@login_required
def update_cart(item_id, action):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return redirect(url_for('cart'))
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
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))

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
            order_item = OrderItem(
                order_id=order.id,
                book_title=item.book.title,
                quantity=item.quantity,
                price=item.book.price
            )
            db.session.add(order_item)
            db.session.delete(item)

        db.session.commit()
        flash('Payment successful! Order placed.', 'success')
        return redirect(url_for('orders'))
        
    return render_template('checkout.html', items=items, subtotal=subtotal)


@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template('orders.html', orders=user_orders)


# ─── Admin Routes ───

@app.route('/admin')
@admin_required
def admin_dashboard():
    orders = Order.query.order_by(Order.id.desc()).limit(10).all()
    total_sales = sum(o.total for o in Order.query.all())
    book_count = Book.query.count()
    user_count = User.query.count()
    return render_template('admin.html', orders=orders, total_sales=total_sales, book_count=book_count, user_count=user_count)


@app.route('/admin/books', methods=['GET', 'POST'])
@admin_required
def admin_books():
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
        return redirect(url_for('admin_books'))
    
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template('admin_books.html', books=books)


@app.route('/admin/users', methods=['GET', 'POST'])
@admin_required
def admin_users():
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
        return redirect(url_for('admin_users'))
        
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin_users.html', users=users)


# ─── Database Initialization ───

def seed_database():
    """Seed the database with sample data."""
    if Book.query.count() == 0:
        books_data = [
            {
                'title': 'The Architecture of Silence',
                'author': 'Julian Barnes',
                'price': 45.00,
                'category': 'Architecture',
                'book_format': 'Hardcover',
                'description': 'A masterful exploration of space, memory, and the unspoken language of structures.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuB7tRmXCArmaBZCdS-PkkVe3NXGbHTG9Tjat0WRiDSh4z0TrChwI7znP92NRRJ4KCjqt4k4Qrsy3JcZtLFnERfsGY2kulIKVRJ26nii1E5Y2zSJq1OX3tmN1hRgNhjsoH0c4fADn7mwaXOFKd11j3WjhP3cmOYtJN5m7ZnevX8KHNndSSED17K9D4ZVSHUKnX8u8cKngz0iGdOTLD6l4mbpa60Jw-yPZgaBVpn5AWx8_lflYomOXCxFai79ufkbL5Sx1nTska5kDtg'
            },
            {
                'title': 'Design as Art',
                'author': 'Bruno Munari',
                'price': 35.00,
                'category': 'Graphic Design',
                'book_format': 'Softcover',
                'description': 'A playful look at the visual arts, from advertising to industrial design.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCTCUntAQue90UvMMYfiBEP0uQ2E-lgerU0i7Sd830mLoYvhD5uKaKilB0Bn6k7fRfb1LwO4LrvHW2OdUca8SZX4iZ9oy0rV0I5midSbktfCG5VVOm7tcePCi00gWHvdLiN0NP4c6Ya9_t6Ibbvnfy6MlB3Hmmr9DfNynxjeV_yAGUYg9D8EMLluf1p1_N3tLIPyrprjwe5m_7axEFhzcZlsI_qM-wdCDz-9cl035A3IIqnpjuLrzMGzgR5C3ZanEpYqrhvGpu8m6Q'
            },
            {
                'title': 'The Poetics of Space',
                'author': 'Gaston Bachelard',
                'price': 28.00,
                'category': 'Architecture',
                'book_format': 'Softcover',
                'description': 'A philosophical examination of the spaces we inhabit and their intimate meanings.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuC7PlWXkCBzxQw1_P_Uonr48wXj8-cm0lDNDSi6Y-jtLkvbAQsih6cD7Soq-mx5I14j92s3VhbvGKJIXHgbf_zRS8ZVejCBrBTzGMjXGTkDpUWNp-LnVxHLNig2DhE3AatTSU1O4hfvcql1L5did8VxvRgQLdbgLV8sAl-0A_siAHxtIaXQSlFewGMdYlTTsokHIrbMK9RC6yO6lxyNrPWHuwLUCZyCt4ihXXoEmKyds-FYN-1dmOPg9XkgbcGFCi-cdIlwZuMUQsc'
            },
            {
                'title': 'On Typography',
                'author': 'Eric Gill',
                'price': 42.00,
                'category': 'Typography',
                'book_format': 'Hardcover',
                'description': 'A classic essay on the art and craft of letter design.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBTRzSLo8q7c5NlqxPDgGeEOWfF8W0RBDue_Dsepay_axyoVRMglTqddQNiLTdXLR9uirNUlC1WbIWB6sFRIEV7SlTcn4q6KMU7o2jUzoWb5f7_u2uUbnOriONJpk58bU3l1BCXjAt9jfx8EjwEyZOpEMCCVbYYvldkZdimPltj464O0xXXRfi09h9z7Ij-5YSVlIvkuOrrUTiBEpwhu8A_vHEvqR5CbOxYSp9aeCeVyYOeRYqEVo8yWxDJMn_ovpNrHTyPBOngk2I'
            },
            {
                'title': 'Brutalism Resurgent',
                'author': 'Alistair Vance',
                'price': 85.00,
                'category': 'Architecture',
                'book_format': 'Hardcover',
                'description': 'A definitive survey of the brutalist architectural movement in the 21st century.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAKm-iUpt2HEn2mBLsFEDma6sv6W-Mwkwzhw49tiN3BB6DTdzRdLCBL6YpOSkN_sK9yBOqvdzkl20tJhw9KDqaSWZIDbNCX-q7pNYoxjp46JI4wcOhf2utwzz6Y6msy8m-40jqFUdhhNhC9EeoaauFD-UQ4YwH3pLw_I1Dfd-TXpj0CFFM8tOzFziOYhVAXCqbC00QxTWeZlQCUfVPQrK7VHF2G20lA3rwV97r0yZx9QpKgcSZaoWpBToWDFNuT6puOS1hZvvmnO8A'
            },
            {
                'title': 'Grid Systems',
                'author': 'Josef Müller-Brockmann',
                'price': 45.00,
                'category': 'Graphic Design',
                'book_format': 'Hardcover',
                'description': 'The definitive guide to grid systems in graphic design.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA05Tee0cFV9xTEMHyc7YB8UvLg24GDqG8bCmL0Pjl2O0X7d5E74wGvtrFzO9j9a9ks1j9R_FJh1JNuDVtR_9j3jteavkcQRDl8yOygOeX-6fzWNFk2KfMKdjOVt5eTvsXgqWdgCGgaplgaO3WkIAgJ5dFLUnb3gLhRQyhy_Y__56dcUGbCR_msIoZK5SCMhyIGkokxOoDSGnOgxH9-t4WAipR9WR_Gbb0nN0B1gocez9KNjQSMrvj1WZBVwSbgxHwRlMpOqONXV_U'
            },
            {
                'title': 'Silent Spaces',
                'author': 'Elena Rostova',
                'price': 120.00,
                'category': 'Photography',
                'book_format': 'Limited Edition',
                'description': 'A photographic journey through abandoned sacred spaces around the world.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCyFW8boR_IPkPqASclGbYM5OavIbeRzvjvydjYQ7GFefdzw9K26x7HIW4L0NTXBacVJywFInbznJV7aRFYVVpR8WXC6kN6HedWoRXW5bzqC2b-zQFyyzJ5cLU8OEQYYM57cl7XNHbLjPahyTKh86zNIgsvKFAilCd5zHqU67ub3Rqm8BzltwUWasK_phuTpJZQbvZK1os8-xyeV6f9eiVFdku7e0jOUyr4qT_34ve_VUTJQm0VbgtCJaFNSk8tUJowJrDR_Ej4hGQ'
            },
            {
                'title': 'The Shape of Things',
                'author': 'Marcus Chen',
                'price': 65.00,
                'category': 'Typography',
                'book_format': 'Hardcover',
                'description': 'An exploration of form and meaning in typographic design.',
                'image_url': ''
            },
            {
                'title': 'Organic Forms',
                'author': 'Sarah Jenkins',
                'price': 90.00,
                'category': 'Contemporary Art',
                'book_format': 'Hardcover',
                'description': 'A survey of organic forms in contemporary art and sculpture.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA5OSBMfuMx7LRKJCip2tBzEAcS2nFgAhcWdLlFa_sUbtDdxcpKXlTCq0MzPsEMlS5VHeNphcklv1kcWr1U434A4paagPkjEVALvttJbkGyIAkFj9aosy2rnZuol-_49zIKvu9Dql7uPh_HBRV_w863KiG8HNf9dLiPmD39wdGJ6Atlt2vPBWuZTkN-yfFzip_64Uf7WJev7Kjfh-qBf1g-m7Ss9QWt_vnxyqfhVnDahTvQaprhKszg2LLyxc3qu1iHBnKNwQoYMxs'
            },
            {
                'title': 'The Architecture of Light',
                'author': 'James Crawford',
                'price': 65.00,
                'category': 'Architecture',
                'book_format': 'Hardcover',
                'description': 'How light shapes our experience of the built environment.',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBupme-CZY3uMxh4MXttspRVmBNNfU8rM9JwbsKof7tJsdQf2zNDNoDIqXyTeV2Y4bCF16JtMxIEfyVvYyvX6psd16R6PBhSQcWLnBPI5SUbOcNmar3rtT18upv4qPvntpY1mTSwBG1asSkUuelrX6x6t1yUopmqGe1eDQCkR00lhXTtkWzQg58qTZZzqV6k4CypkX4clN-2Xz7AeT-OR7c4887hN9Ms7Fes5H_W41WZAxr-SDQRg2DIfoBzN7d0UIEbPebd2C17fo'
            },
        ]
        for bdata in books_data:
            book = Book(**bdata)
            db.session.add(book)
        db.session.commit()

    # Create a demo user
    if User.query.count() == 0:
        demo_user = User(
            full_name='Kareem Hesham',
            username='kareem_hesham',
            email='kareem.hesham@example.com',
            member_since='2024',
            is_admin=True
        )
        demo_user.set_password('password123')
        db.session.add(demo_user)
        db.session.commit()

        # Create sample orders
        order1 = Order(
            user_id=demo_user.id,
            order_number='#TBS-8921',
            date='Oct 12, 2023',
            total=142.00,
            status='Delivered'
        )
        db.session.add(order1)
        db.session.flush()
        db.session.add(OrderItem(order_id=order1.id, book_title='The Architecture of Silence', quantity=1, price=45.00))
        db.session.add(OrderItem(order_id=order1.id, book_title='Design as Art', quantity=1, price=35.00))

        order2 = Order(
            user_id=demo_user.id,
            order_number='#TBS-8105',
            date='Sep 04, 2023',
            total=85.50,
            status='Delivered'
        )
        db.session.add(order2)

        order3 = Order(
            user_id=demo_user.id,
            order_number='#TBS-7422',
            date='Jul 22, 2023',
            total=120.00,
            status='Returned'
        )
        db.session.add(order3)
        db.session.commit()


# ─── App startup ───

with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
