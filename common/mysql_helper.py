# coding=utf-8
# import MySQLdb
# conn = Mysqldb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset='UTF8')
# 查询结果是列表
import logging

import pymysql
from conf.dbconf import MYSQL_PWD_MAIN, MYSQL_USER_MAIN, MYSQL_DB_MAIN, MYSQL_PORT_MAIN, MYSQL_HOST_MAIN


class MysqlHandler(object):
    def __init__(self):
        # charset='utf8'不加这项中文会无法读取
        # 查询结果是字典
        self.conn = pymysql.connect(host=MYSQL_HOST_MAIN,
                                    port=MYSQL_PORT_MAIN,
                                    user=MYSQL_USER_MAIN,
                                    passwd=MYSQL_PWD_MAIN,
                                    db=MYSQL_DB_MAIN,
                                    charset='UTF8',
                                    cursorclass=pymysql.cursors.DictCursor)


def sql_my_profile(username):
    """
    查找用户所有资料
    :param username: 帐号
    :return:
    """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select * from ebf_account where username=%s"
    cur.execute(sql, username)
    rc = cur.fetchone()
    return rc


def sql_user_type_menu(user_type):
    """
   查找用户的菜单
   :param user_type: 帐号类型
   :return:
   """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select menu from ebf_role where id=%s"
    cur.execute(sql, user_type)
    rc = cur.fetchone()
    if rc and rc['menu']:
        res = rc['menu'].split(',')
        ret = []
        for i in res:
            ret.append(int(i))
        return ret
    else:
        return []


def sql_url_menu():
    """
   所有的菜单内容
   :return:
   """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select * from ebf_url"
    cur.execute(sql)
    rc = cur.fetchall()
    if rc:
        return rc
    else:
        return []


def sql_url_id():
    """
   所有的菜单的id
   :return:
   """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select id from ebf_url"
    cur.execute(sql)
    rc = cur.fetchall()
    res = []
    for i in rc:
        res.append(i['id'])
    return res


def sql_menu_role():
    """
   所有角色
   :return:
   """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select * from ebf_menu_role"
    cur.execute(sql)
    rc = cur.fetchall()
    return rc


def sql_update_menu_role(user_type, asd):
    """
   修改角色菜单
   :param user_type: 帐号类型
   :param asd: 值
   :return:
   """
    try:
        conn = MysqlHandler().conn
        cur = conn.cursor()
        sql = 'UPDATE ebf_role SET menu=%s WHERE id=%s'
        args = [asd, user_type]
        cur.execute(sql, args)
        conn.commit()
        return 'ok'
    except Exception as e:
        logging.log(e)
        return 'error'


def sql_update_password(new_pwd, username):
    """
   修改密码
   :param new_pwd: 新密码
   :param username: 用户名
   :return:
   """
    try:
        conn = MysqlHandler().conn
        cur = conn.cursor()
        sql = 'update ebf_account SET password=%s WHERE username=%s'
        cur.execute(sql, [new_pwd, username])
        conn.commit()
        return 'ok'
    except Exception as e:
        logging.log(e)
        return 'error'


def sql_username_password(username):
    """

    :param username: 用户名
    :return:
    """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select password from ebf_account where username=%s"
    cur.execute(sql, username)
    cur.execute(sql, username)
    res = cur.fetchone()
    password = res['password']
    return password
