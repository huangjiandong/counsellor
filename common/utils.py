# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#=============================================================================
#  ProjectName: counsellor
#     FileName: utils
#         Desc: 
#       Author: hjd
#        Email:
#     HomePage:
#      Version:
#   LastChange: 2017-05-21 09:45
#      History:
#=============================================================================

┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
import copy
import hashlib
import os
import re

import datetime
import json
import time
from decimal import Decimal
from bson import ObjectId

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


class UTC2LocalEncoder(json.JSONEncoder):
    """
    在json格式化的时候将时间转换成本地时间
    可以在这个时候对数据进行一些处理和转换
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return (obj + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return (obj + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def utc2local(utc_st):
    """
    UTC时间转本地时间（+8:00)
    :param utc_st:
    :return:
    """
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def local2utc(local_st):
    """
    本地时间转UTC时间（-8:00)
    :param local_st:
    :return:
    """
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    utc_st = local_st - offset
    return utc_st


def format_time(dt):
    """
    格式化日期时间
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


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
