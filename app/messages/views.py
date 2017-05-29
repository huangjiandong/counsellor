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
from common.mongo_helper import mmgrid_decorator, select_ad_content, get_db
from common.utils import UTC2LocalEncoder
from audioop import reverse


@login_required
@mmgrid_decorator(has_user=False, db_type='mongodb')
def ad_content(request, skip=0, limit=20, field='system_time', order=-1, **kwargs):
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
        return render(request, 'table/ad-content.html', locals())
    if request.method == 'POST':
        # 查询条件
        new_title = kwargs.get('new_title')
        new_type = kwargs.get('new_type')
        # 上传时间段
        min_date = kwargs.get('min_date')
        max_date = kwargs.get('max_date')
        results = select_ad_content(new_title, new_type, min_date, max_date, field, order, skip, limit)
        return JsonResponse(results, encoder=UTC2LocalEncoder)


@login_required
@csrf_exempt
def ad_content_edit(request):
    """
    数据管理添加,编辑
    :param request:
    :return:
    """
    action = request.REQUEST.get('action', None)
    if action is None:
        return HttpResponseRedirect(reverse("404"))
    if request.method == 'GET':
        if action == 'add':
            title = "添加"
            return render(request, 'table/ad-content-edit.html', locals())
        if action == 'edit':
            title = "编辑"
            _id = ObjectId(request.GET.get('_id'))

            db = get_db()
            content = db.ebf_content.find_one({'_id': _id})
            content = {key.strip('_'): str(value) for key, value in content.items()}
            return render(request, 'table/ad-content-edit.html', locals())

    elif request.method == 'POST':
        try:
            if action == 'add':
                new_content = request.POST.get('new_content', None)
                new_type = request.POST.get('new_type', None)
                new_title = request.POST.get('new_title', None)
                content = {
                    'new_title': new_title,
                    'new_content': new_content,
                    'new_type': new_type,
                    'system_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db = get_db()
                posts = db.ebf_content
                posts.insert(content)
                return HttpResponse(json.dumps({"status": 0}))
            elif action == 'edit':
                _id = request.POST.get('_id', None)
                new_title = request.POST.get('new_title', None)
                new_content = request.POST.get('new_content', None)
                new_type = request.POST.get('new_type', None)
                system_time = request.POST.get('system_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                content = {
                    'new_title': new_title,
                    'new_content': new_content,
                    'new_type': new_type,
                    'system_time': system_time
                }
                db = get_db()
                posts = db.ebf_content
                _id = ObjectId(_id)
                posts.update({"_id": _id}, content)
                return HttpResponse(json.dumps({"status": 0}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"status": -1}))
    else:
        return HttpResponseRedirect(reverse("404"))


@login_required
@csrf_exempt
def ad_content_delete(request):
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
                pos = db.ebf_content.find_one({'_id': _id})
                if pos is None:
                    return HttpResponse(json.dumps({"status": -1}))
                else:
                    db.ebf_content.remove({"_id": pos["_id"]})
                return HttpResponse(json.dumps({"status": 0}))
            except Exception as e:
                print(e)
    return HttpResponse(json.dumps({"status": -1}))


# @login_required  # 不知道为什么加上这句会报错
@csrf_exempt
def content_detail(request, num_id):
    """
    数据详情
    :param request:
    :param num_id:
    :return:
    """
    try:
        db = get_db()
        results = db.ebf_content.find_one({'_id': ObjectId(num_id)})
        if results:
            message = None
        else:
            message = '没有数据'
    except Exception as e:
        logging.error(e)
    return render(request, 'table/ad-content-detail.html', locals())
