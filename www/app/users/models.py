from app import db
from app.users import constants as USER
import time

class User(db.Model):

  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(120), unique=True)
  avatar = db.Column(db.String(256))
  role = db.Column(db.SmallInteger, default=USER.READER)
  status = db.Column(db.SmallInteger, default=USER.INACTIVE)
  created_at = db.Column(db.Integer, default=int(time.time()))

  def getStatus(self):
    return USER.STATUS[self.status]

  def getRole(self):
    return USER.ROLE[self.role]

  def __repr__(self):
    return '<User %r>' % (self.name)
