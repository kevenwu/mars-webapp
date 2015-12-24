from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.blogs.models import Blog
from app.users.decorators import requires_login

mod = Blueprint('blogs', __name__, url_prefix='/blogs')

@mod.route('/')
def index():
  return render_template('blogs/index.html')

@mod.route('/<blogid>/')
def show_blog(blogid):
  return render_template('blogs/detail.html')

@mod.route('/create/', methods=['GET', 'POST'])
@requires_login
def create_blog():
  return render_template('blogs/create.html')

@mod.route('/<blogid>/delete/', methods=['POST'])
@requires_login
def delete_blog(blogid):
  return redirect(url_for('blogs.index'))

@mod.route('/<blogid>/comment/', methods=['POST'])
@requires_login
def create_comment():
  pass

@mod.route('/<commentid>/delete', methods=['POST'])
@requires_login
def delete_comment():
  pass

@mod.before_request
def before_request():
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])
