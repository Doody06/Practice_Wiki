from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.check_password(User, user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login')) #temporarily redirect to login after registration
    return render_template('auth/register.html', form=form)

@bp.route('/logout') 
@login_required  
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  
    