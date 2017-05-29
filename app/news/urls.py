# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

news_patterns = patterns(
    'app.news.views',
    url(r'ad_content$', 'ad_content', name='ad_content'),
    url(r'ad_content_edit$', 'ad_content_edit', name='ad_content_edit'),
    url(r'ad_content_delete$', 'ad_content_delete', name='ad_content_delete'),
    # \w 表示匹配大小写英文字母、数字以及下划线，等价于'[A-Za-z0-9_]'。\S 表示匹配非空白字符
    url(r'content_detail/(?P<num_id>\w+)$', 'content_detail', name='content_detail'),
)
