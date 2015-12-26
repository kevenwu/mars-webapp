# -*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class EditBlogForm(Form):
  title = TextField(u'标题', [Required(message=u'标题不能为空')])
  content = TextAreaField(u'正文', [Required(message=u'正文不能为空')])