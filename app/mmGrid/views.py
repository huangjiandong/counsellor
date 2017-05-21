# 表格
import datetime
import json
import logging
from bson import ObjectId
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from common.utils import login_required
from common.mongo_helper import mmgrid_decorator, select_ad_content, get_db
from common.utils import UTC2LocalEncoder, utc2local
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
        _id = kwargs.get('_id')
        # 上传时间段
        min_date = kwargs.get('min_date')
        max_date = kwargs.get('max_date')
        results = select_ad_content(_id, min_date, max_date, field, order, skip, limit)
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
            content = db.ebf_qq.find_one({'_id': _id})
            system_time = utc2local(content['system_time']).strftime("%Y-%m-%d %H:%M:%S")
            content = {key.strip('_'): str(value) for key, value in content.items()}
            return render(request, 'table/ad-content-edit.html', locals())

    elif request.method == 'POST':
        try:
            if action == 'add':
                system_time = request.POST.get('system_time', None)
                online_number = request.POST.get('online_number', None)
                content = {
                    'online_number': online_number,
                    'system_time': system_time
                }
                db = get_db()
                posts = db.ebf_qq
                posts.insert(content)
                return HttpResponse(json.dumps({"status": 0}))
            elif action == 'edit':
                _id = request.POST.get('_id', None)
                online_number = request.POST.get('online_number', None)
                content = {
                    'online_number': online_number,
                    'system_time': datetime.datetime.utcnow()
                }
                db = get_db()
                posts = db.ebf_qq
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
                pos = db.ebf_qq.find_one({'_id': _id})
                if pos is None:
                    return HttpResponse(json.dumps({"status": -1}))
                else:
                    db.ebf_qq.remove({"_id": pos["_id"]})
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
        results = db.ebf_qq.find_one({'_id': ObjectId(num_id)})
        if results:
            results['system_time'] = utc2local(results['system_time']).strftime("%Y-%m-%d %H:%M:%S")
            message = None
        else:
            message = '没有数据'
    except Exception as e:
        logging.error(e)
    return render(request, 'table/ad-content-detail.html', locals())
