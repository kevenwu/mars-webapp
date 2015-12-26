# -*- coding:utf-8 -*-
from datetime import datetime
import time

def datetime_filter(t):
  dt_cur = datetime.fromtimestamp(time.time())
  dt = datetime.fromtimestamp(t)
  delta = int(time.time() - t)
  if delta < 60:
    return u'刚刚'
  elif delta < 3600:
    return u'%s分钟前' % (delta // 60)
  elif delta < 86400:
    return u'%s小时前' % (delta // 3600)
  elif delta < 604800:
    return u'%s天前' % (delta // 86400)
  elif dt_cur.year == dt.year:
    return u'%s月%s日' % (dt.month, dt.day)
  else:
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)
