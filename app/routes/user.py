
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

bp = Blueprint('user', __name__)

@bp.route('/')
def redirect_home():
    return redirect(url_for('user.home'))

@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/all_pages')
def all_pages():
    from app.models import Page
    pages = Page.query.all()
    return render_template('all_pages.html', pages=pages)