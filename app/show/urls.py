# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

show_patterns = patterns(
    'app.show.views',
    url(r'show_info/(?P<type_type>\w+)$', 'show_info', name='show_info'),
    url(r'show_counsellor$', 'show_counsellor', name='show_counsellor'),
)
