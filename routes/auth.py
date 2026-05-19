"""
Authentication routes — login, register, logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

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
                return redirect(url_for('main.home'))
            else:
                flash('Invalid email or password.', 'error')
                return redirect(url_for('auth.login', tab='signin'))

        elif action == 'register':
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return redirect(url_for('auth.login', tab='register'))
            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'error')
                return redirect(url_for('auth.login', tab='register'))

            user = User(full_name=full_name, username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('main.home'))

    return render_template('login.html', tab=tab)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))
