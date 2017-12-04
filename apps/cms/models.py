#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        # self.password执行的是下面的setter方法
        self.email = email

    @property
    # 将方法变为属性(get), obj.password
    # 改变_password对外字段名
    def password(self):
        return self._password

    @password.setter
    # 跟property配对用, ex:user.password = 'abc'
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
        # Boolen

    @property
    def permissions(self):
        if not self.roles:
            return 0
            # 权限是由整数(二进制)来确定的,0代表没有角色,即没有权限
        all_permissions = 0
        for role in self.roles:
            all_permissions |= role.permissions
            # 每个用户可能有多个角色,遍历用户的每个角色,将每个角色的所有权限合并到一起
        return all_permissions

    def has_permission(self, permission):
        # 当用户访问某个接口时,需要先判断是否拥有权限
        all_permissions = self.permissions
        # result = all_permissions&permission == permission # ==操作符优先级大于=,result为bool类型
        # return result
        return all_permissions & permission == permission
        # 判断用户是否拥有某权限,只需要将用户所有的权限与某权限做与操作,若结果和某权限相等,则证明有该权限

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)


class CMSPermission():
    # 权限和角色一般改动不大
    ALL_PERMISSION = 0b11111111
    VISITOR = 0b00000001  # 访问者权限
    POSTER = 0b00000010  # 管理帖子权限
    COMMENTER = 0b00000100  # 管理评论权限
    BOARDER = 0b00001000  # 管理板块权限
    FRONTUSER = 0b00010000  # 管理前台用户的权限
    CMSUSER = 0b00100000  # 管理后台用户
    ADMIN = 0b01000000  # 管理后台管理员


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)
    # 用整形存储权限值
    users = db.relationship('CMSUser', secondary='cms_role_user', backref='roles')


cms_role_user = db.Table(
    # 用户与角色多对多中间表,用户并不能直接拿到权限,而是通过对其进行角色划分拿到权限
    'cms_role_user',
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True)
)
