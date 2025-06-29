
from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        form = NewPageForm()
        if form.validate_on_submit():
            title = request.form.get('title')
            content = request.form.get('content')
            slug = Page.slugify(title)
            db.session.add(Page(title=title, content=content,slug = slug, author=current_user))
            db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('new_page.html')

