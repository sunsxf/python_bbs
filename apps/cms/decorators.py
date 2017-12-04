#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei
from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('admin_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper
