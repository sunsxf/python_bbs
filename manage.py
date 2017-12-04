#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from python_bbs import app
from apps.cms import models as cms_models

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
# flask_script提供的添加自定义参数装饰器
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('CMS用户添加成功')
    # python manage.py create_cms_user -u root -p 123456 -e 236764503@qq.com


@manager.command
# 在部署到生产环境时,通过命令行的形式创建所有的角色以及对应的权限
# 不然只有一张角色表,没有任何实际拥有权限的角色,开发者不应该再进入数据库去手动添加各种角色
# python manage.py create_role
def create_role():
    visitor = CMSRole(name='访问者', desc='只能浏览,不能修改')
    visitor.permissions = CMSPermission.VISITOR  # 可以修改个人信息
    operator = CMSRole(name='运营', desc='管理帖子,评论,前台用户')
    operator.permissions = CMSPermission.VISITOR | CMSPermission.FRONTUSER\
                           | CMSPermission.COMMENTER | CMSPermission.POSTER
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.FRONTUSER | CMSPermission.COMMENTER\
                        | CMSPermission.POSTER | CMSPermission.BOARDER | CMSPermission.CMSUSER
    developer = CMSRole(name='开发者', desc='开发人员专用权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-r', '--role', dest='role')
def add_role_to_user(email, role):
    # 给某个用户添加角色,以便测试某个角色具有的权限
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=role).first()
        if role:
            user.roles.append(role)
            # 由于CMSUser和CMSRole表是多对多关系,所以应该用user.roles.append方法将角色添加到用户的角色列表中
            # 若是一对多的关系模型,则为user.role = role
            db.session.commit()
        else:
            print('该系统没有这个角色')
    else:
        print('没有这个用户')


@manager.command
# 测试角色有没有某个权限
def test_permissions():
    user = CMSUser.query.get(2)
    # if user.has_permission(CMSPermission.ALL_PERMISSION):
    if user.is_developer:
        print('hello,developer')
    else:
        print('no permission')


if __name__ == '__main__':
    manager.run()
