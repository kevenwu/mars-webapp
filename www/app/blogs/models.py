from app import db
from app.blogs import constants as BLOG
import time

class Blog(db.Model):

  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  title = db.Column(db.String(120))
  content = db.Column(db.Text)
  read_num = db.Column(db.Integer)
  created_at = db.Column(db.Integer, default=int(time.time()))
  modified_at = db.Column(db.Integer, default=int(time.time()))

class Comment(db.Model):

  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  content = db.Column(db.Text)
  created_at = db.Column(db.Integer, default=int(time.time()))