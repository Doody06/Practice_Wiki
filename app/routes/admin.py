from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.decorators import admin_required
from app import db
from app.forms import NewPageForm
from app.models import Page
from .user import render_safe_markdown

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
    from app.models import PageVersion
    page = Page.query.filter_by(slug=slug).first_or_404()
    form = NewPageForm(obj=page)
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.add(PageVersion(title=page.title, content=page.content, page_id=page.id, author=current_user))
            page.title = request.form.get('title')
            page.content = request.form.get('content')
            page.author = current_user
            page.slug = Page.slugify(page.title)
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
    return render_template('edit_page.html', form=form, page=page)

@admin_required
@bp.route('/delete_page/<slug>', methods=['GET', 'POST'])
def delete_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    if request.method == 'POST':
        for i in page.suggestions:
            db.session.delete(i)
        for version in page.versions:
            db.session.delete(version)
        for comment in page.comments:
            db.session.delete(comment)
        db.session.delete(page)
        db.session.commit()
        return redirect(url_for('user.all_pages'))

@admin_required
@bp.route('/accept_suggestion/<suggestion_id>', methods=['POST', 'GET'])
def accept_suggestion(suggestion_id):
    from app.models import Suggestion, PageVersion
    suggestion = Suggestion.query.get_or_404(suggestion_id) 
    page = Page.query.get_or_404(suggestion.page_id)
    db.session.add(PageVersion(title=page.title, content=page.content, page_id=page.id, author=current_user))
    page = suggestion.page
    page.title = suggestion.title
    page.content = suggestion.content
    db.session.delete(suggestion)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_required
@bp.route('/reject_suggestion/<suggestion_id>', methods=['POST', 'GET'])
def reject_suggestion(suggestion_id):
    from app.models import Suggestion
    suggestion = Suggestion.query.get_or_404(suggestion_id)
    db.session.delete(suggestion)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_required
@bp.route('/view_page_suggestions')
def view_page_suggestions():
    from app.models import Suggestion
    suggestions = Suggestion.query.all()
    return render_template('view_page_suggestions.html', suggestions=suggestions)

@admin_required
@bp.route('/view_suggestion/<slug>/<suggestion_id>')
def view_suggestion(suggestion_id, slug):
    from app.models import Suggestion
    suggestion = Suggestion.query.filter_by().first_or_404()
    suggestion.content = render_safe_markdown(suggestion.content)
    return render_template('view_suggestion.html', suggestion=suggestion)

@admin_required
@bp.route('/delete_comment/<comment_id>', methods=['POST', 'GET'])
def delete_comment(comment_id):
    from app.models import Comment
    comment = Comment.query.get_or_404(comment_id)
    slug = comment.page.slug
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('user.view_page', slug=slug))