# -*- coding:utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from app import db
from app.blogs.models import Blog
from app.blogs import constants as BLOG
from app.blogs.forms import EditBlogForm
from app.users.models import User
from app.users.decorators import requires_login
from app.util import calendar
from markdown import markdown
import time
# from nltk.util import *

mod = Blueprint('blogs', __name__, url_prefix='/blogs')

@mod.route('/')
def index():
  blogs = []

  for blog, user in db.session.query(Blog, User).\
    outerjoin(User).\
    order_by(Blog.created_at).\
    limit(10).\
    all():
    blog.created_at = calendar.format_time(blog.created_at)
    blog.content = markdown(blog.content)
    # blog.content = get_text(blog.content)
    blog.author_name = user.name
    blog.comment_num = 5
    blogs.append(blog)

  return render_template('blogs/index.html', blogs=blogs)

@mod.route('/<blogid>/')
def show_blog(blogid):
  blog, author = db.session.query(Blog, User).\
    outerjoin(User).\
    filter(Blog.id==blogid).\
    first()
  blog.created_at = calendar.format_time(blog.created_at)
  blog.modified_at = calendar.format_time(blog.modified_at)
  blog.content = markdown(blog.content)

  return render_template('blogs/detail.html', **dict(
    blog=blog,
    author=author
  ))

@mod.route('/create/', methods=['GET', 'POST'])
@requires_login
def create_blog():
  form = EditBlogForm(request.form)
  if form.validate_on_submit():
    blog = Blog(
      user_id=g.user.id, 
      title=form.title.data,
      content=form.content.data,
      status=BLOG.PUBLIC
    )
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for('blogs.index'))

  return render_template('blogs/edit.html', form=form)

@mod.route('/<blogid>/edit', methods=['GET', 'POST'])
@requires_login
def edit_blog(blogid):
  if request.method == 'GET':
    blog = Blog.query.filter_by(id=blogid).first()
    if not blog:
      return redirect(url_for('blogs.create_blog'))

    form = EditBlogForm(obj=blog)
    return render_template('blogs/edit.html', form=form, isEdit=True)
  else:
    form = EditBlogForm(request.form)
    if form.validate_on_submit():
      Blog.query.filter_by(id=blogid).update(dict(
        title=form.title.data,
        content=form.content.data,
        modified_at=int(time.time())
      ))
      db.session.commit()
      return redirect(url_for('blogs.index'))

    return render_template('blogs/edit.html', form=form, isEdit=True)

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
