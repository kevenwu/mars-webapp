from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import app
from app import db
from app.users.models import User
from app.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')

from rauth import OAuth2Service
github = OAuth2Service(
  name='github',
  base_url='https://api.github.com/',
  access_token_url='https://github.com/login/oauth/access_token',
  authorize_url='https://github.com/login/oauth/authorize',
  client_id=app.config['GITHUB_CLIENT_ID'],
  client_secret=app.config['GITHUB_CLIENT_SECRET']
)

@app.before_request
def before_request():
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

@mod.route('/login/')
def login():
  redirect_uri = url_for('users.authorized', next=request.args.get('next') or 
    request.referrer or None, _external=True)
  params = {'redirect_uri': redirect_uri, 'scope': 'user:email'}
  return redirect(github.get_authorize_url(**params))

@mod.route('/github/callback')
def authorized():
  if not 'code' in request.args:
    return redirect(url_for('index'))

  redirect_uri = url_for('users.authorized', _external=True)

  data = dict(code=request.args['code'],
    redirect_uri=redirect_uri,
    scope='user:email,public_repo')
  auth = github.get_auth_session(data=data)

  me = auth.get('user').json()
  print me

  user = User.query.filter_by(id=me['id']).first()
  if not user:
    user = User(id=me['id'], name=me['name'] or me['login'], avatar=me['avatar_url'])
    db.session.add(user)
    db.session.commit()

  session['token'] = auth.access_token
  session['user_id'] = user.id

  # flash('Logged in as ' + me['name'])
  return redirect(url_for('index'))

@mod.route('/logout/')
def logout():
  session.pop('user_id', None)
  session.pop('token', None)
  return redirect(url_for('index'))

