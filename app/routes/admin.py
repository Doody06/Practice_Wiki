
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.decorators import admin_required
from app import db
from app.forms import NewPageForm
from app.models import Page

bp = Blueprint('admin', __name__)

@admin_required
@bp.route('/dashboard')
def dashboard():
    username = current_user.username
    return render_template('dashboard.html', username=username)

@admin_required
@bp.route('/new_page', methods=['GET', 'POST'])
def new_page():
    form = NewPageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if Page.query.filter_by(slug=Page.slugify(request.form.get('title'))).first():
                flash('A page with this title already exists.', 'error')
                return '', 400
            title = request.form.get('title')
            content = request.form.get('content')
            slug = Page.slugify(title)
            db.session.add(Page(title=title, content=content,slug = slug, author=current_user))
            db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('new_page.html', form=form)

@admin_required
@bp.route('/edit_page/<slug>', methods=['GET', 'POST'])
def edit_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    form = NewPageForm(obj=page)
    if request.method == 'POST':
        if form.validate_on_submit():
            page.title = request.form.get('title')
            page.content = request.form.get('content')
            page.slug = Page.slugify(page.title)
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
    return render_template('edit_page.html', form=form, page=page)

@admin_required
@bp.route('/delete_page/<slug>', methods=['GET', 'POST'])
def delete_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    db.session.delete(page)
    db.session.commit()
    return '', 204
