# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify, g, url_for
from app import db
from app.comments.models import Comment
from app.users.decorators import requires_login
from markdown import markdown

mod = Blueprint('comments', __name__, url_prefix='/comments')

@mod.route('/create/', methods=['POST'])
def create_comment():
  if not g.user:
    return jsonify(errcode=-1, msg=u'请先登录!')

  comment = Comment(
    user_id=g.user.id, 
    blog_id=request.form['blogid'],
    content=request.form['content'],
  )
  print comment
  db.session.add(comment)
  db.session.commit()
  return jsonify(errcode=0, msg=u"评论成功")

@mod.route('/<commentid>/delete', methods=['POST'])
def delete_comment(commentid):
  comment = Comment.query.filter_by(commentid).first()

  if not comment or not comment.user_id == g.user.id:
    return jsonify(errcode=-1, msg=u'删除失败!')

  Comment.query.filter_by(commentid).delete()
  db.session.commit()
  return jsonify(errcode=0, msg=u"删除成功")
