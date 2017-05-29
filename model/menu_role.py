# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class MenuRole(models.Model):
    """
    角色表
    """
    # id
    id = models.IntegerField(primary_key=True, max_length=64)
    # 角色名
    name = models.CharField(max_length=64)

    # 若不定义该内部类，表名默认为app_label + '_' + module_name,即app+'_'+user==>app_user
    class Meta:
        app_label = 'app'  # app--name
        db_table = 'ebf_menu_role'  # 数据库表名
