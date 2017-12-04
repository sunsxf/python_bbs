#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei
from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
import config
from exts import db, mail

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)
db.init_app(app)
mail.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
