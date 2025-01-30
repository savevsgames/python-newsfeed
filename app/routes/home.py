# home.py module

from flask import Blueprint, render_template

# consolidate routes for app to register with bp
bp = Blueprint('home', __name__, url_prefix='/')


# decorator functions - appended to bp
@bp.route('/')
def index():
    # respond with homepage
    return render_template('homepage.html')


@bp.route('/login')
def login():
    # respond with login
    return render_template('login.html')

@bp.route('/post/<id>')
def single(id):
    return render_template('single-post.html')
