#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei
import os

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'pythonbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD,
                                                          DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)

# PERMANENT_SESSION_LIFETIME = 60 * 24
TEMPLATES_AUTO_RELOAD = True


MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL : 默认为 False
MAIL_USERNAME = '236764503@qq.com'
MAIL_PASSWORD = 'njaoqpahditabhfb'
MAIL_DEFAULT_SENDER = '236764503@qq.com'
