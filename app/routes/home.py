# home.py module

from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

# consolidate routes for app to register with bp
bp = Blueprint('home', __name__, url_prefix='/')


# decorator functions - appended to bp
@bp.route('/')
def index():
    # get all posts
    db = get_db()
    # query the db for posts in descending order
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    # respond with homepage and the posts as posts
    return render_template(
        'homepage.html',
        posts=posts,
        loggedIn=session.get('loggedIn')
    )


@bp.route('/login')
def login():
    # if not logged in yet
    if session.get('loggedIn') is None:
        return render_template('login.html')
    # when session.get('loggedIn') = True
    return redirect('/dashboard')


@bp.route('/post/<id>')
# get a single post by its id
def single(id):
    db = get_db()
    # Filter to use the WHERE clause to find one post with matching id
    post = db.query(Post).filter(Post.id == id).one()

    # render single post template with post as post
    return render_template('single-post.html', post=post, loggedIn=session.get('loggedIn'))



