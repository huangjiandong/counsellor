# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from common.utils import login_required
from common.helper import error, set_password
from common.mysql_helper import sql_my_profile, sql_user_type_menu, sql_url_menu, sql_url_id
from common.mysql_helper import sql_menu_role, sql_update_menu_role, sql_update_password, sql_username_password
from model.user import User


def index_main(request):
    return render(request, 'index1.html', locals())


def bulletin_board(request):
    return render(request, 'bulletin_board.html', locals())


def message(request):
    return render(request, 'message.html', locals())


def counsellor(request):
    return render(request, 'counsellor.html', locals())


# 注册
def register(request):
    if request.method == 'POST':
        # 获得表单数据
        username = request.REQUEST.get('username', None)
        pwd = request.REQUEST.get('password', None)
        password2 = request.REQUEST.get('password2', None)
        nickname = request.REQUEST.get('nickname', None)
        upload_head = request.FILES['upload_head']
        if username and pwd and nickname and upload_head:
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
            password = set_password(pwd)
            User.objects.create(username=username, password=password, nickname=nickname, upload_head=upload_head)
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
            password = set_password(pwd)
            print("用户名： {}， 密码：{}, 加密后密码：{}".format(username, pwd, password))
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/index')
                res = sql_my_profile(username)
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
            else:
                # 比较失败
                return HttpResponse('<html><script type="text/javascript">alert("帐号密码不匹配"); '
                                    'window.location="/login"</script></html>')
        else:
            return HttpResponse('<html><script type="text/javascript">alert("帐号密码不能为空"); '
                                'window.location="/login"</script></html>')
    elif request.method == 'GET':
        return render(request, 'woqu.html')


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
                old_pwd = set_password(old_pwd)
                if password == old_pwd:
                    new_pwd += username
                    new_pwd = set_password(new_pwd)
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
