# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from common.helper import login_required
from common.mysql_helper import select_all_users, sql_my_profile, sql_update_password, delete_user, sql_update_status
from common.utils import error, md5_16
from common.mongo_helper import mmgrid_decorator
from common.utils import UTC2LocalEncoder


@login_required
@mmgrid_decorator(has_user=True, db_type='mysql')
def get_users(request, skip=0, limit=20, field='create_time', order=-1, **kwargs):
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
        return render(request, 'users/users.html', locals())
    if request.method == 'POST':
        # 查询条件
        username = kwargs.get('username')
        user_type = kwargs.get('user_type')
        status = kwargs.get('status')
        # 注册时间段
        min_date = kwargs.get('min_date')
        max_date = kwargs.get('max_date')
        results = select_all_users(username, user_type, status, min_date, max_date, field, order, skip, limit)
        return JsonResponse(results, encoder=UTC2LocalEncoder)


@login_required
@csrf_exempt
def users_edit(request):
    """
    对用户重置密码,更改状态等
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 数据id
        username = request.POST.get("username")
        action = request.POST.get("action")
        user_info = sql_my_profile(username)
        if user_info and user_info["user_type"] != 1:
            ret = error(1, "操作失败了")
            # 初始化密码
            if action == "init":
                new_pwd = username + username[::-1]
                # 用户名和密码一起加密
                new_pwd += username
                new_pwd = md5_16(new_pwd)
                result = sql_update_password(new_pwd, username)
                if result == 'ok':
                    ret = error(0)
                else:
                    ret = error(1, "重置密码失败了")
            elif action == "delete":
                result = delete_user(username)
                if result == 'ok':
                    ret = error(0)
                else:
                    ret = error(1, "删除用户失败了")
            elif action == "update":
                status = request.POST.get("status")
                status = int(status)
                if status in [1, 2, 3]:
                    result = sql_update_status(status, username)
                    if result == 'ok':
                        ret = error(0)
                    else:
                        ret = error(1, "更改用户失败了")
            return HttpResponse(ret)
        else:
            return HttpResponse(json.dumps({"status": -1, "data": "用户信息为空"}))
    return HttpResponse(json.dumps({"status": -1}))
