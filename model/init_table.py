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

import os
from common.mysql_helper import MysqlHandler


def init_table():
    cmd_list = [
        "python manage.py validate",
        "python manage.py sqlall app",
        "python manage.py syncdb",
    ]
    for cmd in cmd_list:
        os.system(cmd)


def init_message():
    sql_list = [
        "INSERT INTO `ebf_account` VALUES ('admin', 'pbkdf2_sha256$12000$A$tYnrI1fHx175ufLALASydwN3wUirAL2SvwwrDntxDyU=', 'admin', '1', 'static/img/upload/刘亦菲.jpg', '1');",
        "INSERT INTO `ebf_menu_role` VALUES ('2', '普通用户');",
        "INSERT INTO `ebf_menu_role` VALUES ('3', '会员');",
        "INSERT INTO `ebf_menu_role` VALUES ('4', '超级会员');"
        "INSERT INTO `ebf_role` VALUES ('2', '1');",
        "INSERT INTO `ebf_role` VALUES ('3', '1');",
        "INSERT INTO `ebf_role` VALUES ('4', '1,2');",
        "INSERT INTO `ebf_url` VALUES ('1', 'main', '首页', '', '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('2', 'ad_content', '表格显示', null, '0', '2');",
        "INSERT INTO `ebf_url` VALUES ('3', 'menu', '角色菜单', null, '0', '2');",
    ]
    conn = MysqlHandler().conn
    cur = conn.cursor()
    for sql in sql_list:
        cur.execute(sql)
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    print("初始化完成")


def main():
    # init_table()
    init_message()


if __name__ == '__main__':
    main()
