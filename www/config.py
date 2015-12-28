import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'This string will be replaced with a proper key in production.'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123@127.0.0.1:3306/mars'
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = False

GITHUB_CLIENT_ID = 'f7764bde15ab2962b374'
GITHUB_CLIENT_SECRET = 'a36cf604ab6fc6fa23a1f50eba24d8b0d5edf62b'

QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''
QINIU_BUKET_NAME = ''
QINIU_DOMIN = ''