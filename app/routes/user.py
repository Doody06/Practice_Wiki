
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
    if current_user.is_authenticated:
        is_admin = current_user.is_admin
    else:
        is_admin = False
    return render_template('all_pages.html', pages=pages, is_admin=is_admin)

@bp.route('/page/<slug>')
def view_page(slug):
    from app.models import Page
    page = Page.query.filter_by(slug=slug).first_or_404()
    return render_template('page.html', page=page)