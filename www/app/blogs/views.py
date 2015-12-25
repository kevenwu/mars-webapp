from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.blogs.models import Blog
from app.blogs import constants as BLOG
from app.users.decorators import requires_login
from markdown import markdown

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
  if request.method == 'GET':
    return render_template('blogs/edit.html')
  else:
    blog = Blog(
      user_id=g.user.id, 
      title=request.form['title'],
      content=request.form['content'],
      status=BLOG.PUBLIC
    )
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for('blogs.index'))

@mod.route('/<blogid>/edit', methods=['GET', 'POST'])
@requires_login
def edit_blog(blogid):
  if request.methods == 'GET':
    blog = Blog.query.filter_by(blogid)
    if not blog:
      pass
    return render_template(url_for('blogs/edit.html'), blog=blog)
  else:
    blog = Blog.query.filter_by(blogid).update(**dict(
      title=request.form['title'],
      content=request.form['content'],
      modified_at=int(time.time())
    ))
    return render_template(url_for('blogs/edit.html'), blog=blog)

@mod.route('/<blogid>/delete/', methods=['POST'])
@requires_login
def delete_blog(blogid):
  Blog.query.filter_by(blogid).delete()
  return redirect(url_for('blogs.index'))

@mod.route('/<blogid>/comment/', methods=['POST'])
@requires_login
def create_comment():
  pass

@mod.route('/<commentid>/delete', methods=['POST'])
@requires_login
def delete_comment():
  pass
