# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import hashlib
import copy
import json
from django.contrib.auth.hashers import make_password, check_password
from common.mysql_helper import sql_username_password
from django.http.response import HttpResponseRedirect


def set_password(pwd):
    """

    :param pwd: 明文密码
    :return:
    """
    result = make_password(pwd, 'A', 'pbkdf2_sha256')  # 每次生成一样的密文
    # result = make_password(pwd, None, 'pbkdf2_sha256')  # 每次生成不一样的密文，用check_password(明文,密文)检查，返回结果是true , false
    return result


def get_password(username, text):
    pwd = sql_username_password(username)
    result = check_password(text, pwd)
    return result


def login_required(func):
    """
    登录装饰器，用于判断是否登录
    :return:
    """

    def wrap(request):
        if not request.session.get('username', False):
            return HttpResponseRedirect("login")
        else:
            return func(request)

    return wrap
