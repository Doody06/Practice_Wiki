from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    #temporary login my account for debugging
   user = User.query.filter_by(username='doody').first()
   login_user(user)
   return redirect(url_for('admin.dashboard'))
    #normal login logic
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user and User.check_password(user, form.password.data):
    #         login_user(user)
    #         flash('Login successful', 'success')
    #         if user.is_admin:
    #             return redirect(url_for('admin.dashboard'))
    #         else:
    #             return redirect(url_for('home'))
    #     else:
    #         flash('Invalid username or password', 'danger')
    # return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): #learn how this works
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print("User registered successfully")
        return redirect(url_for('auth.login')) #temporarily redirect to login after registration
    else:
        print("Registration failed")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    return render_template('register.html', form=form)

@bp.route('/logout') 
@login_required  
def logout():
    logout_user()
    return redirect(url_for('user.home'))  

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    print(user.username)
    form = EditProfileForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile', username=user.username))
    else:
        if form.errors: #change this block to make it readable >:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    return render_template('edit_profile.html', form=form, user=user)
       
    