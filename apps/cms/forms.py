#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm

class LoginForm(BaseForm):
    # BaseForm爲添加了隨機返回一條表單驗證失敗消息的Form類的子類
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='邮箱不能为空')])
    password = StringField(validators=[Length(6, 10, message='密码长度爲6-10位')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 10, message='原密码长度爲6-10位')])
    newpwd = StringField(validators=[Length(6, 10, message='新密码长度爲6-10位')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='兩次密碼不一致')])
    # EqualTo驗證器第一個參數爲字符串類型！