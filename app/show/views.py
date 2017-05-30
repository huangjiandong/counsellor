# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from bson import ObjectId
from django.core.paginator import Paginator
from django.shortcuts import render
from common.mongo_helper import get_db
# @login_required  # 不知道为什么加上这句会报错
# @csrf_exempt
from common.mysql_helper import select_all_users


def show_info(request, type_type):
    """
    分页数据
    :param request:
    :param type_type:
    :return:
    """
    if type_type == "1":
        head_tile = "公告"
    elif type_type == "2":
        head_tile = "教学文件"
    elif type_type == "3":
        head_tile = "经验交流"
    elif type_type == "4":
        head_tile = "通知"
    elif type_type == "5":
        head_tile = "学术期刊"
    elif type_type == "6":
        head_tile = "留言板"
    db = get_db()
    page_type = request.REQUEST.get('page_type', "")
    now_page = int(request.REQUEST.get('now_page', 1))
    title = request.REQUEST.get("title", "")
    if page_type == 'page_up':
        now_page -= 1
    elif page_type == 'page_down':
        now_page += 1
    elif page_type == 'jump':
        pass
    else:
        now_page = 1
    param = {}
    if title:
        param["title_title"] = title
    if type_type == '6':
        param["type_type"] = "2"
        objects = db.ebf_messages.find(param)
    else:
        param["type_type"] = type_type
        objects = db.ebf_content.find(param)
    number = 10
    if objects:
        new_objects = []
        for x in objects:
            # 把'_id'改为'id'
            r = {key.strip('_'): value for key, value in x.items()}
            new_objects.append(r)
        p = Paginator(new_objects, number)  # 每页10条数据的一个分页器
        count = p.count
        if now_page != 1 and now_page > count:
            if count == 0:
                now_page = 1
            else:
                now_page = count
        page_info = p.page(now_page)  # 第?页
        results = page_info.object_list  # 第?页的数据
    else:
        page_info = None
        results = None
    return render(request, 'show/show.html', locals())


def show_counsellor(request):
    """
    辅导员信息
    :param request:
    :return:
    """
    now_page = 1
    page_type = request.REQUEST.get('page_type', None)
    username = request.REQUEST.get('username', None)
    now_page = int(request.REQUEST.get('now_page', 1))
    if page_type == 'page_up':
        now_page -= 1
    elif page_type == 'page_down':
        now_page += 1
    number = 10
    skip = (now_page - 1) * number
    users_info = select_all_users(username=username, user_type=2, status=1, min_date="", max_date="",
                                  field="create_time", order=1, skip=skip, limit=number)
    new_objects = [{"nickname": i["nickname"], "upload_head": i["upload_head"]} for i in users_info["items"]]
    if new_objects:
        p = Paginator(new_objects, number)  # 每页10条数据的一个分页器
        page_info = p.page(now_page)  # 第?页
        results = page_info.object_list  # 第?页的数据
    else:
        page_info = None
        results = None
    return render(request, 'show/counsellor.html', locals())
