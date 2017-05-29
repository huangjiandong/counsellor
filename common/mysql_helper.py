# !/usr/bin/env python
# -*- coding: utf-8 -*-


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


def get_main_connection():
    """
    连接主数据库
    :return:
    """
    conn = pymysql.connect(
        host=MYSQL_HOST_MAIN,
        port=MYSQL_PORT_MAIN,
        user=MYSQL_USER_MAIN,
        passwd=MYSQL_PWD_MAIN,
        db=MYSQL_DB_MAIN,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def close_connection(conn):
    """
    关闭数据库连接
    :param conn:
    :return:
    """
    conn.close()


def sql_my_profile(username, id=None):
    """
    查找用户所有资料
    :param id:
    :param username: 帐号
    :return:
    """
    args = []
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select * from ebf_account where username=%s"
    args.append(username)
    if id:
        sql += " and id=%s"
        args.append(id)
    cur.execute(sql, args)
    conn.close()
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
    conn.close()
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
    conn.close()
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
    conn.close()
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
    conn.close()
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
        conn.close()
        return 'ok'
    except Exception as e:
        logging.exception(e)
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
        conn.close()
        return 'ok'
    except Exception as e:
        logging.exception(e)
        return 'error'


def sql_update_status(status, username):
    """
   修改状态
   :param status: 状态
   :param username: 用户名
   :return:
   """
    try:
        conn = MysqlHandler().conn
        cur = conn.cursor()
        sql = 'update ebf_account SET status=%s WHERE username=%s'
        cur.execute(sql, [status, username])
        conn.commit()
        conn.close()
        return 'ok'
    except Exception as e:
        logging.exception(e)
        return 'error'


def execute_sql(sql, args=None, fetch_all=True):
    """
    执行sql查询语句
    :param sql:
    :param args:
    :param fetch_all:
    :return:
    """
    conn = get_main_connection()
    try:
        cursor = conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        items = cursor.fetchall() if fetch_all else cursor.fetchone()
    except Exception as e:
        print(e)
        items = [] if fetch_all else None
    finally:
        close_connection(conn)
    return items


def sql_username_password(username):
    """
    查询当前用户密码
    :param username: 用户名
    :return:
    """
    conn = MysqlHandler().conn
    cur = conn.cursor()
    sql = "select password from ebf_account where username=%s"
    cur.execute(sql, username)
    res = cur.fetchone()
    conn.close()
    password = res['password']
    return password


def delete_user(username):
    """
    根据用户名删除用户
    :param username: 用户名
    :return:
    """
    try:
        conn = MysqlHandler().conn
        cur = conn.cursor()
        sql = 'delete from ebf_account where username=%s'
        cur.execute(sql, username)
        conn.commit()
        conn.close()
        return 'ok'
    except Exception as e:
        logging.exception(e)
        return 'error'


def select_all_users(username, user_type, status, min_date, max_date, field, order, skip, limit):
    """

    :param username:
    :param user_type:
    :param status:
    :param min_date:
    :param max_date:
    :param field:
    :param order:
    :param skip:
    :param limit:
    :return:
    """

    sql = "select username,password,nickname,user_type,upload_head,status,create_time from ebf_account where 1=1"
    args = []
    if username:
        sql += " and username=%s"
        args.append(username)
    if user_type:
        sql += " and user_type=%s"
        args.append(user_type)
    if status:
        sql += " and status=%s"
        args.append(status)
    if min_date and max_date:
        sql += " and create_time <= % and create_time >= %"
        args.append(min_date)
        args.append(max_date)
    if order == -1:
        sql += " ORDER BY %s  DESC limit %s, %s"
    else:
        sql += " ORDER BY %s ASC limit %s, %s"
    args.append(field)
    args.append(skip)
    args.append(limit)
    items = execute_sql(sql, args)
    count = len(items)
    return {"totalCount": count, "items": items}
