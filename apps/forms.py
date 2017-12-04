#!/usr/bin/env python
# coding=utf-8
#@author sunxiongfei
'''將所有form表單中共性部分抽取出來，創建一個新的基類(繼承自Form類)
如隨機取一條表單驗證失敗信息返回'''
from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        error_msg = self.errors.popitem()[1][0]
        # dict.popitem()返回字典中任意一个键值对,以元组的形式返回
        return error_msg
