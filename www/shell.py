#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'

'''
python shell.py 
>>> from app import db
>>> db.create_all()
>>> exit()
'''