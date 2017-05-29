#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
project name: counsellor
file name: init_table
author: Administrator
create time:  2017-05-21 16:03

┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
import datetime
import os

from common.utils import md5_16
from common.mysql_helper import MysqlHandler
from common.utils import format_time


def get_project_path():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.dirname(curr_path)
    return project_path


def init_table():
    project_path = get_project_path()
    base_python = "python %s/manage.py" % project_path
    cmd_list = [
        "%s validate" % base_python,
        "%s sqlall app" % base_python,
        "%s syncdb" % base_python,
    ]
    for cmd in cmd_list:
        print("cmd: %s" % cmd)
        os.system(cmd)


def init_message():
    password = md5_16("adminadmin")
    create_time = datetime.datetime.now()
    sql_list = [
        "INSERT INTO `ebf_account` VALUES ('admin', '%s', 'admin', '1', 'static/img/upload/刘亦菲.jpg', '1', '%s');" % (
        password, format_time(create_time)),
        "INSERT INTO `ebf_menu_role` VALUES ('2', '辅导员');",
        "INSERT INTO `ebf_menu_role` VALUES ('3', '其它师生');",
        "INSERT INTO `ebf_role` VALUES ('2', '1,2,3');",
        "INSERT INTO `ebf_role` VALUES ('3', '1,2');",
        "INSERT INTO `ebf_url` VALUES ('1', 'main', '首页', '', '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('2', 'messages', '留言管理', null, '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('3', 'ad_content', '后台管理', null, '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('4', 'users', '用户管理', null, '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('5', 'menu', '角色菜单', null, '0', '2');",
    ]
    conn = MysqlHandler().conn
    cur = conn.cursor()
    for sql in sql_list:
        print("sql: %s" % sql)
        cur.execute(sql)
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    print("初始化完成")


def main():
    init_table()
    init_message()


if __name__ == '__main__':
    main()
