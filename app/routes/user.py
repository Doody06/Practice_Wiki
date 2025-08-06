from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import User
import bleach
import markdown2

bp = Blueprint('user', __name__)

ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS).union({
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'blockquote', 'ul', 'ol', 'li',
    'strong', 'em', 'a', 'img', 'br', 'code', 'pre', 'hr',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
})
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id', 'style', 'href', 'title'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
def render_safe_markdown(content):
    from markupsafe import Markup
    html = markdown2.markdown(content)
    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, protocols=ALLOWED_PROTOCOLS)
    return Markup(clean_html)
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
    from app.models import Page, Comment, PageVersion
    import markdown2
    from markupsafe import Markup
    page = Page.query.filter_by(slug=slug).first_or_404()
    html_content = render_safe_markdown(page.content)
    from app.forms import CommentForm
    form = CommentForm()
    comments = Comment.query.filter_by(page_id=page.id).all()
    for comment in comments:
        comment.content = render_safe_markdown(comment.content)
    page_versions = PageVersion.query.filter_by(page_id=page.id).order_by(PageVersion.created_at.desc()).all()
    for version in page_versions:
        version.content = render_safe_markdown(version.content)
    if current_user.is_authenticated:
        is_admin = current_user.is_admin
    else:
        is_admin = False
    return render_template('page.html', page=page, form=form, comments=comments, page_versions=page_versions, is_admin=is_admin, content=html_content)

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

@login_required
@bp.route('/comment/<slug>/', methods=['POST'])
def comment_on_page(slug):
    from app.models import Page, Comment
    from app.forms import CommentForm
    from app import db
    page = Page.query.filter_by(slug=slug).first_or_404()
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            content = form.content.data
            comment = Comment(content=content, page=page, author=current_user)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
        else:
            flash('Error adding comment. Please try again.', 'error')
    return redirect(url_for('user.view_page', slug=slug, form=form))

@bp.route('/profile/<username>')
@login_required
def profile(username):
    from app.models import Suggestion, Comment
    user_id = User.query.filter_by(username=username).first_or_404().id
    user_suggestions = Suggestion.query.filter_by(suggested_by_id=user_id).all()
    user_comments = Comment.query.filter_by(author_id=user_id).all() 
    # if current_user.is_authenticated:
    #     do some stuff related to previous edits
    return render_template('profile.html', user=current_user, suggestions=user_suggestions, comments=user_comments)



