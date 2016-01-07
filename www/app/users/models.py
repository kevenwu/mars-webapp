from app import db
from app.users import constants as USER
import time

class User(db.Model):

  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)
  avatar = db.Column(db.String(256))
  role = db.Column(db.SmallInteger, default=USER.READER)
  created_at = db.Column(db.Integer)

  def getRole(self):
    return USER.ROLE[self.role]

  def __repr__(self):
    return '<User %r>' % (self.name)
