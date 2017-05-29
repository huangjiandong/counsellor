# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from common.helper import login_required
from common.mongo_helper import get_db
from common.utils import error, md5_16
from common.mysql_helper import sql_my_profile, sql_user_type_menu, sql_url_menu, sql_url_id, select_all_users
from common.mysql_helper import sql_menu_role, sql_update_menu_role, sql_update_password, sql_username_password
from model.user import User


def index_main(request):
    """
    首页
    :param request:
    :return:
    """
    db = get_db()
    objects = db.ebf_content.find()
    result = {}
    jinyan = []
    gonggao = []
    tongzhi = []
    wenjian = []
    xueshu = []
    for x in objects:
        # 把'_id'改为'id'
        r = {key.strip('_'): value for key, value in x.items()}
        type_type = r["type_type"]
        if type_type == "1":
            gonggao.append(r)
        elif type_type == "2":
            wenjian.append(r)
        elif type_type == "3":
            jinyan.append(r)
        elif type_type == "4":
            tongzhi.append(r)
        elif type_type == "5":
            xueshu.append(r)
    users_info = select_all_users(username="", user_type=2, status=1, min_date="", max_date="",
                                  field="create_time", order=1, skip=0, limit=5)
    fudaoyaun = [{"nickname": i["nickname"], "upload_head": i["upload_head"]} for i in users_info["items"]]
    return render(request, 'index1.html', locals())


# 注册
def register(request):
    if request.method == 'POST':
        # 获得表单数据
        username = request.REQUEST.get('username', None)
        pwd = request.REQUEST.get('password', None)
        password2 = request.REQUEST.get('password2', None)
        nickname = request.REQUEST.get('nickname', None)
        # 用户类型
        user_type = request.REQUEST.get('user_type', None)
        upload_head = request.FILES['upload_head']
        if username and pwd and nickname and upload_head and user_type:
            # 判断两次密码是否一致
            if pwd != password2:
                return HttpResponse('<html><script type="text/javascript">alert("两次密码不一致"); '
                                    'window.location="/register"</script></html>')
            # 判断用户名是否已经存在
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                return HttpResponse('<html><script type="text/javascript">alert("帐号已经存在"); '
                                    'window.location="/register"</script></html>')
            pwd += username
            # 添加到数据库
            password = md5_16(pwd)
            # 需要管理员审核
            if user_type == "2":
                status = "3"
            else:
                status = "1"
            User.objects.create(username=username, password=password, nickname=nickname, user_type=user_type,
                                upload_head=upload_head, status=status)
            return HttpResponse('<html><script type="text/javascript">alert("注册成功"); '
                                'window.location="/login"</script></html>')
        else:
            return HttpResponse('<html><script type="text/javascript">alert("数据格式不完整"); '
                                'window.location="/register"</script></html>')
    elif request.method == 'GET':
        return render(request, 'register.html')


# 登陆
def login(request):
    if request.method == 'POST':
        username = request.REQUEST.get('username', None)
        pwd = request.REQUEST.get('password', None)
        if username and pwd:
            pwd += username
            # 再次加密进行验证
            password = md5_16(pwd)
            print("用户名： {}， 密码：{}, 加密后密码：{}".format(username, pwd, password))
            # 获取的表单数据与数据库进行比较
            check_pwd = User.objects.filter(username__exact=username, password__exact=password)
            if check_pwd:
                res = sql_my_profile(username)
            else:
                # 比较失败
                return HttpResponse('<html><script type="text/javascript">alert("帐号密码不匹配"); '
                                    'window.location="/login"</script></html>')
            if res["status"] == 1:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/index')
                # 将username写入浏览器session
                request.session['username'] = username
                # 将用户类型写入session
                request.session['user_type'] = res['user_type']
                # 将upload_head写入浏览器session
                request.session['upload_head'] = res['upload_head']
                # 将upload_head写入浏览器cookie
                # 中文无法存入cookie中，可以存在session
                # response.set_cookie('upload_head', upload_head)
                # request.COOKIES['upload_head'] = upload_head
                return response
            elif res["status"] == 2:
                # 比较失败
                return HttpResponse('<html><script type="text/javascript">alert("您的帐号被禁用了，请联系管理员"); '
                                    'window.location="/login"</script></html>')
            elif res["status"] == 3:
                # 比较失败
                return HttpResponse('<html><script type="text/javascript">alert("您的帐号未通过审核，请联系管理员"); '
                                    'window.location="/login"</script></html>')
        else:
            return HttpResponse('<html><script type="text/javascript">alert("帐号密码不能为空"); '
                                'window.location="/login"</script></html>')
    elif request.method == 'GET':
        return render(request, 'login.html')


# 登陆成功
@login_required
def index(request):
    # upload_head = request.COOKIES['upload_head']
    # upload_head = request.COOKIES.get('upload_head', '')
    username = request.session["username"]
    res = sql_my_profile(username)
    user_type = res['user_type']
    if user_type == 1:
        # 用户拥有的菜单
        menu = sql_url_id()
        all_menu = sql_url_menu()
    else:
        # 用户拥有的菜单
        menu = sql_user_type_menu(user_type)
        # 总菜单
        all_menu = sql_url_menu()
    return render(request, 'index.html', locals())


# 退出
@login_required
def logout(request):
    response = HttpResponseRedirect('/login')
    # 清理session里保存的username,upload_head
    del request.session['username']
    del request.session['upload_head']
    # 清理cookie里保存的upload_head
    # del request.COOKIES['upload_head']
    # response.delete_cookie('upload_head')
    return response


# 登陆后主页
@login_required
def main(request):
    return render(request, 'main.html', locals())


# 修改密码
@login_required
def modify_pwd(request):
    if request.method == 'POST':
        old_pwd = request.REQUEST.get("old_pwd", None)
        new_pwd = request.REQUEST.get("new_pwd", None)
        new_again_pwd = request.REQUEST.get("new_again_pwd", None)
        if old_pwd and new_pwd and new_again_pwd:
            if new_pwd == new_again_pwd:
                # 从数据库获取密码
                username = request.session["username"]
                password = sql_username_password(username)
                old_pwd += username
                # 加密进行验证
                old_pwd = md5_16(old_pwd)
                if password == old_pwd:
                    new_pwd += username
                    new_pwd = md5_16(new_pwd)
                    result = sql_update_password(new_pwd, username)
                    if result == 'ok':
                        ret = error(0)
                else:
                    ret = error(2)
            else:
                ret = error(1)
        else:
            ret = error(3)
        return HttpResponse(ret)
    elif request.method == 'GET':
        return render(request, 'modify-pwd.html')


# 个人资料
@login_required
def my_profile(request):
    if request.method == 'GET':
        username = request.session["username"]
        result = sql_my_profile(username)
        return render(request, 'my-profile.html', locals())


# 菜单
@login_required
def menu(request):
    menu_role = sql_menu_role()
    user_type = menu_role[0]['id']
    # 用户拥有的菜单
    menu = sql_user_type_menu(user_type)
    # 总菜单
    all_menu = sql_url_menu()
    if request.method == 'POST':
        asd = request.POST.get('asd', None)
        action = request.POST.get('type', None)
        user_type = request.POST.get('user_type', None)
        if user_type:
            user_type = int(user_type)
        else:
            ret = error(4)
            return HttpResponse(ret)
        # 修改操作
        if action == 'ask':
            result = sql_update_menu_role(user_type, asd)
            if result == 'ok':
                ret = error(0)
            else:
                ret = error(4)
        else:
            # 用户拥有的菜单
            menu = sql_user_type_menu(user_type)
            ret = error(0, menu)
        return HttpResponse(ret)
    return render(request, 'menu.html', locals())
