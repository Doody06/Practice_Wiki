
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')