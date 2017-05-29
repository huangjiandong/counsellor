# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

messages_patterns = patterns(
    'app.messages.views',
    url(r'messages$', 'messages', name='messages'),
    url(r'messages_edit$', 'messages_edit', name='messages_edit'),
    url(r'messages_delete$', 'messages_delete', name='messages_delete'),
    # \w 表示匹配大小写英文字母、数字以及下划线，等价于'[A-Za-z0-9_]'。\S 表示匹配非空白字符
    url(r'messages_detail/(?P<num_id>\w+)$', 'messages_detail', name='content_detail'),
)
