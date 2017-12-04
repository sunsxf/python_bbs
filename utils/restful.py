#!/usr/bin/env python
# coding=utf-8
# @author sunxiongfei
'''優化JSON數據返回'''
from flask import jsonify


class Code():
    ok = 200
    paramserror = 400
    unautherror = 401
    servererror = 500


def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message='', data=None):
    return restful_result(Code.ok, message=message, data=data)


def params_error(message=''):
    return restful_result(Code.paramserror, message=message, data=None)


def unauth_error(message=''):
    return restful_result(Code.unautherror, message=message, data=None)


def server_error(message=''):
    return restful_result(Code.servererror, message=message or '服務器內部錯誤', data=None)
