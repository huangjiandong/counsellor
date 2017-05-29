# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Url(models.Model):
    """
    菜单表
    """
    # id
    id = models.IntegerField(primary_key=True, max_length=64)
    # url地址
    url = models.CharField(max_length=256, null=True)
    # 菜单名
    name = models.CharField(max_length=64)
    # 菜单图标 允许为空
    icon = models.CharField(max_length=64, null=True)
    # 第几级菜单 0：一级
    pid = models.IntegerField(max_length=1)
    # 一级菜单是否有二级菜单 1：有 2：没有 0:二级菜单
    first = models.IntegerField(max_length=1, null=True)

    # 若不定义该内部类，表名默认为app_label + '_' + module_name,即app+'_'+user==>app_user
    class Meta:
        app_label = 'app'  # app--name
        db_table = 'ebf_url'  # 数据库表名
