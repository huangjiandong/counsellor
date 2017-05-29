# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.db import models

# Create your models here.
from common.utils import format_time


class User(models.Model):
    """
    用户表
    """
    # 帐号
    username = models.CharField(primary_key=True, max_length=64, null=False)
    # 密码
    password = models.CharField(max_length=256, null=False)  # 数据库中的列名db_column='密码'
    # 昵称
    nickname = models.CharField(max_length=64, null=False)
    # 帐号类型 1：管理员 2：辅导员 3:普通师生
    user_type = models.IntegerField(max_length=1, null=False)
    # 头像
    upload_head = models.FileField(upload_to='./static/img/upload/', max_length=64, null=False)
    # 是否被禁用 1:未禁用 2：禁用 3：待审核
    status = models.IntegerField(max_length=1, null=False)
    create_time = models.CharField(max_length=45, default=format_time(datetime.datetime.now()))

    # 若不定义该内部类，表名默认为app_label + '_' + module_name,即app+'_'+user==>app_user
    class Meta:
        app_label = 'app'  # app--name
        db_table = 'ebf_account'  # 数据库表名
