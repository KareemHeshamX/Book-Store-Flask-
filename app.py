import os
from flask import Flask
from flask_login import current_user

from extensions import db, login_manager
from models import User, CartItem
from seed import seed_database


def create_app():
    app = Flask(__name__)

    # ─── Configuration ──────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = 'the-book-store-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ─── Initialize Extensions ──────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)

    # ─── User Loader ────────────────────────────────────────────────────────
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ─── Context Processors ─────────────────────────────────────────────────
    @app.context_processor
    def inject_cart_count():
        count = 0
        if current_user.is_authenticated:
            count = CartItem.query.filter_by(user_id=current_user.id).count()
        return dict(cart_count=count)

    # ─── Register Blueprints ────────────────────────────────────────────────
    from routes.main import main
    from routes.auth import auth
    from routes.admin import admin
    from routes.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    # ─── Database Setup ─────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_database()

    return app


# ─── Run ────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
