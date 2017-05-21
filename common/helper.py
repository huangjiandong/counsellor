# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import re
import hashlib
import copy
import json
from django.contrib.auth.hashers import make_password, check_password
from common.mysql_helper import sql_username_password

status = {
    0: '请求成功',

    1: '两次密码不一致',
    2: '原密码错误',
    3: '数据不完整',
    4: '修改操作失败'
}
message = {
    'status': '',
    'data': '',
    'error': ''
}


def error(code=0, data=''):
    """
    错误信息
    :param code:
    :param data:
    :return: 返回一个封装好错误信息的json格式的数据
    """
    msg = copy.copy(message)
    msg['status'] = code
    msg['error'] = status[code]
    if data:
        msg['data'] = data
    return json.dumps(msg)


def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号
    """
    try:
        word = word.encode("utf-8")
    except:
        word = str(word)
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()


def md5_16(word):
    """
    MD5加密 16位
    :param word:
    :return: 生成16位加密数据
    """
    return md5hex(word)[8:-8]


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


def qq_face_path():
    """
    QQ表情路径
    :return:
    """
    path = r'./static/qqface/face'
    result = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                name = name[:-4]
                result.append(name)
    result = json.dumps(result)
    return result


def font_to_img(item):
    """
    显示表情
    :param item:
    :return:
    """
    ret = re.findall('\[([\w]+)\]', item)
    for j in ret:
        b = "[" + j + "]"
        c = '<img src="static/qqface/face/' + j + '.gif" border="0">'
        item = item.replace(b, c)
    return item
