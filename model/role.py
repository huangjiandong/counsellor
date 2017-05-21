from django.db import models


class Role(models.Model):
    """
    角色拥有的菜单
    """
    # id
    id = models.IntegerField(primary_key=True, max_length=64)
    # menu列表
    menu = models.CharField(max_length=256)

    # 若不定义该内部类，表名默认为app_label + '_' + module_name,即app+'_'+user==>app_user
    class Meta:
        app_label = 'app'  # app--name
        db_table = 'ebf_role'  # 数据库表名
