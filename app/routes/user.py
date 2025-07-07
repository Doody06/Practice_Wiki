
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

bp = Blueprint('user', __name__)

@bp.route('/')
def redirect_home():
    return redirect(url_for('user.home'))

@bp.route('/home')
def home():
    user = current_user
    return render_template('home.html', user=user)

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

@login_required
@bp.route('/suggest_page_edit/<slug>', methods=['GET', 'POST'])
def suggest_page_edit(slug):
    from app.models import Page, Suggestion
    from app.forms import NewPageForm
    from app import db
    page = Page.query.filter_by(slug=slug).first_or_404()
    form = NewPageForm(obj=page)
    
    if not current_user.is_authenticated:
        flash('You must be logged in to suggest edits.', 'error')
        return redirect(url_for('user.view_page', slug=slug))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            title = request.form.get('title')
            content = request.form.get('content')
            suggestion = Suggestion(title=title, content=content, page=page, suggested_by=current_user)
            db.session.add(suggestion)
            db.session.commit()
            return redirect(url_for('user.view_page', slug=slug))
    
    return render_template('suggest_page_edit.html', form=form, page=page)