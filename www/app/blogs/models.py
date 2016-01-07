from app import db
from app.blogs import constants as BLOG
import time

class Blog(db.Model):

  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  title = db.Column(db.String(120))
  content = db.Column(db.Text)
  status = db.Column(db.SmallInteger, default=BLOG.DRAFT)
  read_num = db.Column(db.Integer, default=0)
  created_at = db.Column(db.Integer)
  modified_at = db.Column(db.Integer)

  def __repr__(self):
    return '<Blog %r>' % (self.id)