import os
import sys

from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

@app.route('/')
def index():
  return redirect(url_for('blogs.index'))

@app.route('/source/')
def source():
  return redirect('https://github.com/kevenwu/mars-webapp')

@app.route('/about/')
def about():
  return render_template('about.html')

from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

from app.blogs.views import mod as blogsModule
app.register_blueprint(blogsModule)