# coding=utf-8
import datetime
import logging

from bson import ObjectId
from pymongo import MongoClient
from django.db import models
from time import mktime
import time

"""
# mongodb备份整个数据库
# 无密码：mongodump -h 127.0.0.1:27017 -d test -o /home/lcx/Desktop/mongodb/
# 有密码：mongodump -h 127.0.0.1 --port 27017 -u abc -p abc -d test --authenticationDatabase admin -o /home/lcx/Desktop/mongodb/
# mongodb还原整个数据库
# 无密码：mongorestore -h 127.0.0.1:27017 -d test --directoryperdb /home/lcx/Desktop/mongodb/test
# 有密码：mongorestore -h 127.0.0.1 --port 27017 -u abc -p abc -d test --authenticationDatabase admin --directoryperdb /home/lcx/Desktop/mongodb/test
"""


# mongodb数据库连接
def get_db():
    connection = MongoClient('localhost', 27017)
    db = connection.test
    # 设置了密码
    # db.authenticate('root', 'root')
    return db


def convert_str_to_date(str_date):
    """
    将time.struct_time转为 datetime.datetimef
    :param str_date:
    :return:
    """
    rs = time.strptime(str_date, "%Y-%m-%d")
    dt = datetime.datetime.fromtimestamp(mktime(rs))
    return dt


def converts_str2int(value, default=0):
    """
    将str换成int
    :param value:
    :param default: 转换失败的默认值
    :return:
    """
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as e:
        print(e)
        return default


def wrap_model(results, keys=None):
    """
    包装model的结果成为一个list
    :param results:
    :param keys: 指定需要返回的字段，list
                外键需要指定取出外键对象中的哪个字段 a#b
                如果有外键，并且需要外键中其他字段值，必须指定
    :return:
    """
    if not results:
        return []
    items = []
    f_keys = []
    if keys:
        for key in keys:
            if '#' in key:
                a, b = key.split('#')
                f_keys.append((a, b))
            else:
                f_keys.append((key, None))
        keys = f_keys

    for result in results:
        item = dict()
        if isinstance(result, models.Model):
            # 如果指定了keys，需要获取外键对象的指定值
            if keys:
                for key in keys:
                    if key[1]:
                        res = getattr(getattr(result, key[0], ''), key[1], '')
                        # 如果取出的还是一个外键，那么直接取出外键值即可，不无限取下去
                        if isinstance(res, models.Model):
                            item[key[0]] = getattr(res, key[0] + "_id", '')
                        else:
                            item[key[0]] = res
                    else:
                        item[key[0]] = getattr(result, key[0], '')
            # 如果没有指定keys,则直接获取外键的id值即可
            else:
                rs = result.__dict__
                for r in rs:
                    if r.endswith('_id_id'):
                        item[r[:-3]] = getattr(result, r, '')
                    else:
                        item[r] = getattr(result, r, '')
        else:
            # 如果不是模型对象，那么直接取出键值对的值即可，也不会有外键的关系，所以只需要处理tuple的第一个值
            if keys:
                for key in keys:
                    if key[1] is None:
                        item[key[0]] = result.get(key[0], '')
            else:
                item = result
        items.append(item)
    return items


def select_ad_content(_id, min_date, max_date, field='system_time', order=-1, skip=0, limit=20):
    """

    查询数据
    :param _id:
    :param min_date:
    :param max_date:
    :param field:
    :param order:
    :param skip:
    :param limit:
    :return:
    """
    try:
        db = get_db()
        collection = db.ebf_qq
        params = dict()
        if min_date and max_date:
            date_range = {'$gte': min_date, '$lte': max_date}
            params['system_time'] = date_range
        if _id:
            params['_id'] = ObjectId(_id)
        results = collection.find(params)
        results.sort(field, order).skip(skip).limit(limit)
        count = results.count()
        items = wrap_model(results)
        return {"totalCount": count, "items": items}
    except Exception as e:
        print(e)
        return {"totalCount": 0, "items": []}


def mmgrid_decorator(has_user=False, db_type="model"):
    """
    mmgrid表格插件请求装饰器
    预先处理重复的数据
    :param has_user: 是否需要session中存储的用户
    :param db_type: 数据库类型
        model: django模型
        mysql: mysql数据库
        mongodb: mongodb 数据库
    :return:
    """

    def _wrap(func):
        def wrap(request, **kwargs):
            kwargs = dict(request.REQUEST, **kwargs)
            if '_' in kwargs:
                del kwargs['_']
            page = converts_str2int(kwargs.pop('page', 1), 1)
            limit = converts_str2int(kwargs.get('limit', 20), 20)
            kwargs['skip'] = (page - 1) * limit
            kwargs['limit'] = limit
            # 设置排序方式
            sort = kwargs.pop("sort", None)
            if sort:
                field, order = sort.split('.')
                if db_type == 'mysql':
                    kwargs['order'] = order.upper()
                    kwargs['field'] = 'ebf_' + field
                elif db_type == 'model':
                    if order.lower() == 'desc':
                        kwargs['field'] = '-' + field
                    else:
                        kwargs['field'] = field
                elif db_type == 'mongodb':
                    kwargs['field'] = field
                    if order.lower() == 'desc':
                        kwargs['order'] = -1
                    else:
                        kwargs['order'] = 1

            date_range = kwargs.pop("dateRange", None)
            if date_range:
                min_time, max_time = date_range.split('~')
                kwargs['min_date'] = convert_local_to_utc(min_time.strip(), False)
                kwargs['max_date'] = convert_local_to_utc(max_time.strip(), False) + datetime.timedelta(days=1)

            # 如果设置需要登录用户信息，则设置
            # if has_user:
            #     kwargs['user_type'] = request.session.get(SESSION_USER_TYPE, None)
            #     kwargs['user_id'] = request.session.get(SESSION_USER_ID, None)
            return func(request, **kwargs)

        return wrap

    return _wrap


def convert_local_to_utc(normal, trans=True, fm='%Y-%m-%d'):
    """
    将本地正常时间转换成UTC时间
    :param normal:
    :param trans:
    :param fm:
    :return:
    """
    if isinstance(normal, str):
        normal = convert_str_to_date(normal)
    if trans:
        return (normal - datetime.timedelta(hours=8)).strftime(fm)
    else:
        return normal - datetime.timedelta(hours=8)


def mongodb_username_card():
    """
    查询发表过的说说内容
    :return:
    """
    try:
        db = get_db()
        collection = db.ebf_news
        results = collection.find()
        results.sort('create_date', -1)
        items = wrap_model(results)
        return items
    except Exception as e:
        logging.exception(e)
        items = []
    return items
