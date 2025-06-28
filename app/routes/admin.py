
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
bp = Blueprint('admin', __name__)

@login_required
@bp.route('/dashboard')
def dashboard():
    username = current_user.username
    return render_template('dashboard.html', username=username)