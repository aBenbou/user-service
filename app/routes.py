from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the index page or redirect to API docs"""
    return render_template('index.html')

@main_bp.route('/docs')
def docs_redirect():
    """Redirect to API documentation"""
    return redirect('/api/docs')