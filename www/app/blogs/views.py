# -*- coding:utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, jsonify
from app import db
from app.blogs.models import Blog
from app.users.models import User
from app.comments.models import Comment
from app.blogs import constants as BLOG
from app.blogs.forms import EditBlogForm
from app.users.decorators import requires_login
from app import utility as Util

import time
import math
from markdown import markdown

mod = Blueprint('blogs', __name__, url_prefix='/blogs')

@mod.route('/')
def index():
  page = request.args.get('page', 1)
  page = int(page)

  blog_num = db.session.query(Blog.id).count()
  pages = blog_num / BLOG.PAGE_NUM + (1 if blog_num % BLOG.PAGE_NUM > 0 else 0)
  
  blogs = []

  for blog, user, comment_num in db.session.query(Blog, User, db.func.count(Comment.id)).\
    outerjoin(User, Blog.user_id==User.id).\
    outerjoin(Comment, Comment.blog_id==Blog.id).\
    group_by(Blog.id).\
    order_by(Blog.created_at.desc()).\
    offset((page - 1) * BLOG.PAGE_NUM).\
    limit(BLOG.PAGE_NUM).\
    all():
    blog.created_at = Util.format_time(blog.created_at)
    blog.content = Util.html2text(markdown(blog.content))[:500]
    blog.author = user
    blog.comment_num = comment_num
    blogs.append(blog)

  return render_template('blogs/index.html', 
    blogs=blogs, 
    current_page=page, 
    pages=pages,
    base=url_for('blogs.index'))


@mod.route('/<blogid>/')
def show_blog(blogid):

  # db.session.autoflush = False
  blog, author = db.session.query(Blog, User).\
    filter(Blog.id==blogid).\
    filter(User.id==Blog.user_id).\
    first()
    
  Blog.query.filter_by(id=blogid).update(dict(
    read_num=blog.read_num+1
  ))
  db.session.commit()

  next = db.session.query(Blog.id, Blog.title).\
    order_by(Blog.created_at).\
    filter(Blog.created_at > blog.created_at).\
    limit(1).\
    first()

  last = db.session.query(Blog.id, Blog.title).\
    order_by(Blog.created_at.desc()).\
    filter(Blog.created_at < blog.created_at).\
    limit(1).\
    first()

  comments = []
  for comment, user in db.session.query(Comment, User).\
    outerjoin(User).\
    filter(Comment.blog_id==blogid).\
    all():
    comment.created_at = Util.format_time_inverted(comment.created_at)
    comment.content = markdown(comment.content, ['codehilite'])
    comment.user_name = user.name
    comment.user_avatar = user.avatar
    comment.user_id = user.id
    comments.append(comment)

  blog.created_at = Util.format_time(blog.created_at)
  blog.modified_at = Util.format_time(blog.modified_at)
  blog.content = markdown(blog.content, ['codehilite'])
  blog.last = last
  blog.next = next
  blog.comment_num = len(comments)

  return render_template('blogs/detail.html',
    blog=blog,
    author=author,
    comments=comments
  )


@mod.route('/create/', methods=['GET', 'POST'])
@requires_login
def create_blog():
  form = EditBlogForm(request.form)

  if form.validate_on_submit():
    blog = Blog(
      user_id=g.user.id, 
      title=form.title.data,
      content=form.content.data,
      status=BLOG.PUBLISH
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
def delete_blog(blogid):
  blog = Blog.query.filter_by(id=blogid).first()

  if not blog or not blog.user_id == g.user.id:
    return jsonify(errcode=-1, msg=u'删除文章失败!')

  Blog.query.filter_by(id=blogid).delete()
  db.session.commit()
  return jsonify(errcode=0, msg=u"删除文章成功")
