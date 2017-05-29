# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 表格
import datetime
import json
import logging
from bson import ObjectId
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from common.helper import login_required
from common.mongo_helper import mmgrid_decorator, select_messages, get_db
from common.mysql_helper import sql_my_profile
from common.utils import UTC2LocalEncoder
from audioop import reverse


@login_required
@mmgrid_decorator(has_user=False, db_type='mongodb')
def messages(request, skip=0, limit=20, field='create_time', order=-1, **kwargs):
    """
    数据管理
    :param request:
    :param skip:
    :param limit:
    :param field:
    :param order:
    :param kwargs:
    :return:
    """
    if request.method == 'GET':
        # 当前用户
        username = request.session["username"]
        res = sql_my_profile(username)
        user_type = res['user_type']
        return render(request, 'messages/messages.html', locals())
    if request.method == 'POST':
        username = request.session["username"]
        res = sql_my_profile(username)
        user_type = res['user_type']
        # 查询条件
        message_title = kwargs.get('message_title')
        message_type = kwargs.get('message_type')
        message_name = kwargs.get('message_name')
        # 上传时间段
        min_date = kwargs.get('min_date')
        max_date = kwargs.get('max_date')
        if user_type == 3:
            message_name = username
        results = select_messages(message_title, message_type, message_name, min_date, max_date, field, order,
                                  skip, limit)
        return JsonResponse(results, encoder=UTC2LocalEncoder)


@login_required
@csrf_exempt
def messages_edit(request):
    """
    数据管理添加,编辑
    :param request:
    :return:
    """
    action = request.REQUEST.get('action', None)
    message_name = request.session["username"]
    res = sql_my_profile(message_name)
    user_type = res['user_type']
    if action is None:
        return HttpResponseRedirect(reverse("404"))
    if request.method == 'GET':
        if action == 'add':
            title = "添加"
            return render(request, 'messages/messages-edit.html', locals())
        if action == 'edit':
            title = "编辑"
            _id = ObjectId(request.GET.get('_id'))

            db = get_db()
            content = db.ebf_messages.find_one({'_id': _id})
            content = {key.strip('_'): str(value) for key, value in content.items()}
            return render(request, 'messages/messages-edit.html', locals())

    elif request.method == 'POST':
        try:
            if action == 'add':
                message_content = request.POST.get('message_content', None)
                message_type = request.POST.get('message_type', None)
                message_title = request.POST.get('message_title', None)
                content = {
                    'message_title': message_title,
                    'message_content': message_content,
                    'reply_content': "",
                    'message_type': message_type,
                    'message_name': message_name,
                    'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db = get_db()
                posts = db.ebf_messages
                posts.insert(content)
                return HttpResponse(json.dumps({"status": 0}))
            elif action == 'edit':
                _id = request.POST.get('_id', None)
                message_title = request.POST.get('message_title', None)
                message_content = request.POST.get('message_content', None)
                content = {
                    'message_title': message_title,
                    'message_content': message_content,
                }
                if user_type != 3:
                    reply_content = request.POST.get('reply_content', None)
                    content["reply_content"] = reply_content
                db = get_db()
                posts = db.ebf_messages
                _id = ObjectId(_id)
                old_content = posts.find_one({'_id': _id})
                old_content.update(content)
                posts.update({"_id": _id}, old_content)
                return HttpResponse(json.dumps({"status": 0}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"status": -1}))
    else:
        return HttpResponseRedirect(reverse("404"))


@login_required
@csrf_exempt
def messages_delete(request):
    """
    删除数据
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 数据id
        _id = ObjectId(request.POST.get('id'))
        if _id:
            try:
                db = get_db()
                pos = db.ebf_messages.find_one({'_id': _id})
                if pos is None:
                    return HttpResponse(json.dumps({"status": -1}))
                else:
                    db.ebf_messages.remove({"_id": pos["_id"]})
                return HttpResponse(json.dumps({"status": 0}))
            except Exception as e:
                print(e)
    return HttpResponse(json.dumps({"status": -1}))


# @login_required  # 不知道为什么加上这句会报错
@csrf_exempt
def messages_detail(request, num_id):
    """
    数据详情
    :param request:
    :param num_id:
    :return:
    """
    try:
        db = get_db()
        results = db.ebf_messages.find_one({'_id': ObjectId(num_id)})
        if results:
            message = None
        else:
            message = '没有数据'
    except Exception as e:
        logging.error(e)
    return render(request, 'messages/messages-detail.html', locals())
