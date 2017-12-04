#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei
from flask import Blueprint, views, render_template, request
from flask import session, redirect, url_for, jsonify
from .models import CMSUser
from .decorators import login_required
from .forms import LoginForm, ResetPwdForm
from exts import db, mail
from flask_mail import Message
from utils import restful
import string, random

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/logout/')
def logout():
    del session['admin_id']
    return redirect(url_for('cms.login'))


@bp.route('/reset_email/')
@login_required
def reset_email():
    return render_template('cms/cms_resetemail.html')


@bp.route('/email_capture/')
@login_required
def email_capture():
    # localhost:5000/cms/email_capture/?email=xxx@qq.com
    email = request.args.get('email')
    print(email)
    if not email:
        return restful.server_error('請輸入郵箱')
    source = list(string.ascii_letters)
    source_num = map(lambda x: str(x), range(10))
    # 生成0-9的字符串形式的列表
    source.extend(source_num)
    # 合並兩個列表, 此方法爲原地方法，即直接作用於source對象上
    capture_li = random.sample(source, 6)  # 隨機取六位，返回的是一個列表
    capture = ''.join(capture_li)
    message = Message('python論壇修改郵箱驗證碼', recipients=[email], body='您的驗證碼爲%s' % capture)
    # recipients需要接受一個列表
    try:
        mail.send(message)
    except:
        return restful.server_error()
    return restful.success()


class LoginView(views.MethodView):
    def get(self, error_msg=None):
        return render_template('cms/cms_login.html', error_msg=error_msg)

    def post(self):
        form = LoginForm(request.form)
        # 將用戶提交的數據經wtforms進行表單驗證後的form對象
        if form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            # password = form.password.data 同上
            remember = request.form.get('remember')
            admin = CMSUser.query.filter_by(email=email).first()
            if admin and admin.check_password(password):
                session['admin_id'] = admin.id
                # 设置session,记录登录状态
                if remember:
                    session.permanent = True
                    # 可在配置文件中设置默认时间
                return redirect(url_for('cms.index'))
                # url_for反转时,endpoint前一定要加上蓝图名!
            else:
                return self.get(error_msg='用户名或密码错误')
        else:
            return self.get(error_msg=form.get_error())


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    # flask類方法添加裝飾器
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            admin_id = session.get('admin_id')
            admin = CMSUser.query.get(admin_id)
            if admin and admin.check_password(oldpwd):
                admin.password = newpwd
                # session.commit() 這是服務器會話
                db.session.commit()
                return restful.success()
                # AJAX技術需要返回一個JSON數據,當需要返回JSON格式時,應採用固定格式
                # 如{"code":200,"message":""}
            else:
                # return jsonify({'code':400,'message':'原密碼錯誤'})
                return restful.params_error('原密碼錯誤')
        else:
            # error_msg = form.errors.popitem()[1][0]
            # 經常用到，抽取到FORM表單的基類中去
            # return jsonify({'code':401,'message':form.get_error()})
            return restful.params_error(form.get_error())


bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
