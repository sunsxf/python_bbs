#!/usr/bin/env python
# coding=utf-8
#@author sunxiongfei
from .views import bp
from flask import session, g
from .models import CMSUser

@bp.before_request
# 在所有請求前
def my_before_request():
    admin_id = session.get('admin_id')
    if admin_id:
        admin = CMSUser.query.get(admin_id)
        if admin:
            g.admin = admin