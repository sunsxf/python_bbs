#!/usr/bin/env python
# coding=utf-8
#@author sunxiongfei
from flask import Blueprint

bp = Blueprint('front',__name__)

@bp.route('/')
def index():
    return 'front index'